from app.agent.comparison import ComparisonHandler
from app.parser.query_parser import QueryParser
from app.guardrails.safety import SafetyGuard
from app.guardrails.validator import RecommendationValidator

from app.agent.intent_classifier import IntentClassifier
from app.agent.state_manager import ConversationStateManager
from app.agent.clarification import ClarificationHandler

from app.retrieval.hybrid_search import HybridSearchEngine
from app.retrieval.reranker import AssessmentReranker


class SHLRecommendationAgent:

    def __init__(self):

        self.comparison_handler = ComparisonHandler()

        self.safety_guard = SafetyGuard()

        self.validator = RecommendationValidator()

        self.intent_classifier = IntentClassifier()

        self.state_manager = ConversationStateManager()

        self.clarification_handler = ClarificationHandler()

        self.search_engine = HybridSearchEngine()

        self.reranker = AssessmentReranker()

        self.query_parser = QueryParser()


    def handle_conversation(
        self,
        messages
    ):

        latest_query = (
            self.state_manager.extract_latest_user_message(
                messages
            )
        )


        search_query = self.state_manager.build_search_query(messages)

    
        
        parsed_query = self.query_parser.parse(
          search_query
         )

        

        # -------------------------
        # Prompt Injection Defense
        # -------------------------

       

        if self.safety_guard.detect_prompt_injection(
            latest_query
        ):

            

            return self.safety_guard.injection_response()

        # -------------------------
        # Out-of-Scope Defense
        # -------------------------

        if self.safety_guard.detect_out_of_scope(
            latest_query
        ):

            

            return self.safety_guard.refusal_response()

        # -------------------------
        # Intent Classification
        # -------------------------

        intent = self.intent_classifier.classify(
            latest_query
        )

        if intent == "finalize":
         
          return {
               "reply": "Confirmed. I will treat this as the final SHL assessment shortlist.",
               "recommendations": [],
               "end_of_conversation": True
            }

        # -------------------------
        # Refusal Intent
        # -------------------------

        if intent == "refuse":

            return {
                "reply": (
                    "I can only provide recommendations "
                    "related to SHL assessments."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }
    
        # -------------------------
        # Clarification Handling
        # -------------------------

        if self.clarification_handler.needs_clarification(
            parsed_query
        ):

            return {
                "reply": (
                    self.clarification_handler
                    .clarification_question()
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # -------------------------
        # Retrieval
        # -------------------------

        results = self.search_engine.hybrid_search(
            search_query,
            top_k=30
        )

        reranked = self.reranker.rerank(
            parsed_query,
            results
        )

        recommendations = []

        for result in reranked[:10]:

            recommendations.append({

                "name": result["name"],

                "url": result["url"],

                "test_type": ", ".join(
                    result.get("test_types", [])
                )
            })

        recommendations = (self.validator.validate_recommendations(recommendations))

        if intent == "compare":

           return self.comparison_handler.build_comparison_response(
             latest_query,
              recommendations
             )

        # -------------------------
        # Final Response
        # -------------------------

        return {

            "reply": (
                f"I found {len(recommendations)} "
                f"relevant SHL assessments "
                f"for your hiring needs."
            ),

            "recommendations": recommendations,

            "end_of_conversation": False
        }

