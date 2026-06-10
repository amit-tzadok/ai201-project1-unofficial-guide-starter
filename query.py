"""
Query module: retrieval + grounded generation.

Takes a user question, retrieves relevant chunks, and generates
a grounded answer using Groq's LLM with source citations.
"""

import os
from dotenv import load_dotenv
from groq import Groq
from retrieval import retrieve

load_dotenv()

_groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are "The Unofficial Guide" — a helpful big-sister figure who gives practical, honest advice to computer science students at the University at Buffalo.

STRICT RULES:
1. Answer ONLY using the information provided in the "Retrieved Documents" below. Do not use any outside knowledge.
2. If the retrieved documents do not contain enough information to answer the question, say: "I don't have enough information on that in my sources. Try asking about CS clubs, courses, internships, research, career prep, or grad school at UB."
3. For every claim in your answer, cite the source document in parentheses, like (source: 04_leetcode_interview_prep.txt).
4. Be warm, direct, and practical — like an older student giving real advice, not a university brochure.
5. Keep answers concise but thorough. Use bullet points when listing multiple tips."""


def generate_answer(query, k=5):
    """Retrieve relevant chunks and generate a grounded answer.

    Returns a dict with:
    - "answer": the LLM's response
    - "sources": list of unique source filenames used
    - "chunks": the retrieved chunks (for debugging/display)
    """
    # Retrieve relevant chunks
    chunks = retrieve(query, k=k)

    # Format chunks as context for the LLM
    context = "\n\n---\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in chunks
    )

    # Build the user message with retrieved context
    user_message = f"""Retrieved Documents:
{context}

---

Question: {query}"""

    # Call Groq LLM
    response = _groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,  # low temperature for more grounded responses
        max_tokens=1024,
    )

    answer = response.choices[0].message.content

    # Collect unique sources from retrieved chunks
    sources = list(dict.fromkeys(c["source"] for c in chunks))

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks,
    }


if __name__ == "__main__":
    # Quick test
    test_queries = [
        "When should I start leetcoding and what should I focus on first?",
        "What's the best pizza place near campus?",  # out-of-scope test
    ]

    for q in test_queries:
        print(f"Q: {q}")
        print("=" * 60)
        result = generate_answer(q)
        print(result["answer"])
        print(f"\nSources: {', '.join(result['sources'])}")
        print()
