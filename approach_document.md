# Approach Document: Conversational SHL Assessment Recommender

## 1. Problem Understanding

The goal is to build a conversational AI agent that recommends SHL assessments using only the SHL Product Catalog. The system must clarify vague hiring needs, support refinement, compare assessments, refuse unrelated requests, and return schema-compliant API responses.

## 2. Architecture

The system follows this pipeline:

User message → Safety Guard → State Manager → Intent Classifier → Query Parser → Hybrid Retrieval → Reranker → Validator → Response Builder

## 3. Data Processing

The SHL catalog is cleaned, enriched, embedded, and stored for retrieval. Each assessment record includes name, URL, description, test type, skills, job levels, remote availability, adaptive support, and duration.

## 4. Retrieval Strategy

The system uses hybrid retrieval:

- Semantic search with sentence-transformers
- FAISS vector search
- Keyword/BM25-style retrieval
- Metadata-aware reranking

This improves Recall@10 and handles both exact skills and broader recruiter intent.

## 5. Conversation Handling

The API is stateless. Every `/chat` request receives the full message history. The state manager reconstructs context from previous user turns, allowing multi-turn refinement such as “Add AWS and Docker.”

## 6. Clarification Logic

The agent asks clarifying questions when the user query lacks role, seniority, or skill information. This prevents premature or irrelevant recommendations.

## 7. Safety and Hallucination Prevention

The system prevents hallucinations by:

- using only catalog-derived recommendations
- validating SHL URLs
- removing duplicates
- refusing prompt injection
- refusing out-of-scope queries

## 8. Reranking Strategy

The reranker boosts assessments based on:

- skill match
- seniority match
- remote preference
- adaptive preference
- duration constraints

## 9. Supported Behaviors

The agent supports:

- recommendations
- clarification
- multi-turn refinement
- comparison
- refusal
- finalization

## 10. API Design

### GET /health

Returns service health.

### POST /chat

Request:
{
  "messages": [
    {
      "role": "user",
      "content": "Need Java assessment for senior developers"
    }
  ]
}

Response:
{
  "reply": "string",
  "recommendations": [
    {
      "name": "assessment name",
      "url": "official SHL URL",
      "test_type": "assessment category"
    }
  ],
  "end_of_conversation": false
}