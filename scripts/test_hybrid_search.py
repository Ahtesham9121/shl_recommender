from app.retrieval.hybrid_search import HybridSearchEngine

engine = HybridSearchEngine()

query = "frontend angular developer"

results = engine.hybrid_search(query)

print("\nHYBRID SEARCH RESULTS:\n")

for i, result in enumerate(results, start=1):

    print(f"{i}. {result['name']}")
    print(f"   Score: {result['score']}")
    print(f"   Skills: {result['skills']}")
    print(f"   URL: {result['url']}")
    print()