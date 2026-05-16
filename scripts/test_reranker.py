from app.retrieval.hybrid_search import HybridSearchEngine
from app.retrieval.reranker import AssessmentReranker

search_engine = HybridSearchEngine()

reranker = AssessmentReranker()

query = "short remote frontend angular assessment for mid level developer"

results = search_engine.hybrid_search(query)

reranked = reranker.rerank(query, results)

print("\nRERANKED RESULTS:\n")

for i, result in enumerate(reranked, start=1):

    print(f"{i}. {result['name']}")
    print(f"   Final Score: {result['final_score']}")
    print(f"   Business Score: {result['business_score']}")
    print(f"   Skills: {result['skills']}")
    print(f"   URL: {result['url']}")
    print()