# SHL Assessment Recommendation System

An intelligent SHL assessment recommendation system built with FastAPI, semantic search, reranking, and conversational refinement.

## Features

- SHL assessment recommendations
- Semantic retrieval using embeddings
- Hybrid search and reranking
- Prompt injection defense
- Out-of-scope refusal
- Clarification for vague hiring requirements
- Multi-turn refinement
- Comparison between assessments
- Conversation finalization detection

---

## Project Structure

```text
shl_recommender/
│── app/
│   ├── agent/
│   ├── guardrails/
│   ├── parser/
│   ├── retrieval/
│   └── main.py
│
│── data/
│   ├── raw/
│   ├── enriched/
│   └── embeddings/
│
│── scripts/
│── tests/
│── requirements.txt
│── Dockerfile
│── README.md