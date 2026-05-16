from app.agent.orchestrator import SHLRecommendationAgent

agent = SHLRecommendationAgent()

messages = [
    {
        "role": "user",
        "content": (
            "Need a short frontend angular assessment "
            "for mid-level developers"
        )
    }
]

response = agent.handle_conversation(messages)

print("\nAGENT RESPONSE:\n")

print(response)