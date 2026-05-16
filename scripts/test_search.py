from app.retrieval.semantic_search import SemanticSearchEngine

engine = SemanticSearchEngine()

query = "frontend developer with angular skills"

results = engine.search(query, top_k=5)

print("\nSEARCH RESULTS:\n")

for i, result in enumerate(results, start=1):

    print(f"{i}. {result['name']}")
    print(f"   Score: {result['score']}")
    print(f"   Skills: {result['skills']}")
    print(f"   URL: {result['url']}")
    print()