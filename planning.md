# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

Survival guide for computer science students at the University at Buffalo. This guide covers the practical knowledge that CS students need but struggle to find — things like how to find research opportunities, when to start preparing for internships and leetcoding, which clubs and communities can help you find your path, which courses matter most for your career goals, and how to build experience as a coder outside of schoolwork.

This information is hard to find because CS students at UB tend to keep to themselves. As a girl in a male-dominated program, I didn't fit into the study cliques that formed naturally, so I was mostly a one-woman team through my degree. Research opportunities weren't advertised in any obvious way, and I wish I had known as a freshman how important it was to start building experience early through research and internships. The upperclassmen I did talk to mostly just said "it's so hard" and "you're cooked" instead of offering real, actionable advice. An unofficial guide with honest, helpful tips from someone who's been through it would have made a huge difference.

---

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | UB CSE Dept — Student Organizations | CS clubs at UB: ACM, UB Hacking, MakeOpenSource, UBNetDef, DivTech, etc. | https://engineering.buffalo.edu/computer-science-engineering/people/professional-and-student-organizations.html |
| 2 | UB CSE Dept — Undergraduate Research | How to find research opportunities, REU program, research areas, faculty contacts | https://engineering.buffalo.edu/computer-science-engineering/undergraduate/experiential-learning/undergraduate-research.html |
| 3 | UB CSE Dept — Internships | Internship credit, finding opportunities, application process, international student requirements | https://engineering.buffalo.edu/computer-science-engineering/information-for-students/experiential-learning/internships.html |
| 4 | LeetCode Discuss — Intern Guide | LeetCode preparation timeline, study strategies, and technical interview advice | https://leetcode.com/discuss/post/229221/an-unofficial-guide-for-first-timers-interns-version/ |
| 5 | UB Career Design Center — STEAM Fair | Career fair preparation, employer list, resume tips, interview practice resources | https://www.buffalo.edu/career/events/stemup.html |
| 6 | UB CSE Dept — Course Catalog + BS CS | Full course listing, curriculum structure, required and elective courses with advice | https://engineering.buffalo.edu/computer-science-engineering/undergraduate/courses/course-catalog.html |
| 7 | UB CSE Dept — TA Resources + Handbook | How to become a TA/SA, responsibilities, grading guidelines, tips for working with TAs | https://engineering.buffalo.edu/computer-science-engineering/information-for-students/undergraduate-program/cse-teaching-assistant-ta-resources.html |
| 8 | UB CSE Dept — Graduate Programs (MS) | Grad school prep, MS specializations, BS/MS combined program, application requirements, funding | https://engineering.buffalo.edu/computer-science-engineering/graduate/degrees-and-programs/ms-in-computer-science-and-engineering.html |
| 9 | Compiled student advice | Programming languages and tools to learn outside class, portfolio building, career paths | Student advice compilation |
| 10 | CSE 331 Support Page — TA Advice | Study strategies, common mistakes, and survival tips for CSE 331 (Algorithms) | http://www-student.cse.buffalo.edu/~atri/cse331/support/advice/index.html |
| 11 | UB CSE Dept — Experiential Learning | Overview of hackathons, research, internships, workshops, and clubs | https://engineering.buffalo.edu/computer-science-engineering/undergraduate/experiential-learning.html |
| 12 | Niche.com — UB CS Reviews | Student reviews of UB's CS program: course quality, career outcomes, challenges, facilities | https://www.niche.com/colleges/university-at-buffalo-suny/academics/ |

---

## Chunking Strategy

**Chunk size:** 500 characters

**Overlap:** 100 characters

**Reasoning:** My documents are a mix of tip lists (short, discrete pieces of advice) and informational guides (longer paragraphs covering a single topic). Most individual tips or pieces of advice run 200–600 characters. A 500-character chunk is large enough to capture a complete tip or a full paragraph of advice, which means most chunks will be self-contained and retrievable on their own. The 100-character overlap ensures that if a key fact spans a chunk boundary — for example, a sentence that starts at the end of one chunk and finishes in the next — both chunks will contain enough of that sentence to be useful. I'm splitting by character count rather than by paragraph because paragraph lengths vary widely across my documents (some "paragraphs" are one-liners, others are 800+ characters), and a fixed character split gives more consistent chunk sizes for the embedding model.

---

## Retrieval Approach

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers`. This model runs locally, requires no API key, and produces 384-dimensional embeddings. It's well-suited for short English text, which matches my document style.

**Top-k:** 5 chunks per query. This should provide enough context to answer most questions (2-3 highly relevant chunks plus some supporting material) without diluting the context with too many loosely related results.

**Production tradeoff reflection:** If I were deploying this for real users, I'd consider several tradeoffs. First, `all-MiniLM-L6-v2` has a 256-token context window for encoding — longer chunks may get truncated, which could hurt retrieval quality for dense paragraphs. A model like `all-mpnet-base-v2` handles longer inputs (384 tokens) and scores higher on benchmarks, but is slower. Second, UB has a large international student population, so a multilingual model like `paraphrase-multilingual-MiniLM-L12-v2` could help students who search in their native language. Third, for a production system with real-time users, I'd weigh API-hosted embeddings (like OpenAI's `text-embedding-3-small`) against local inference — API models are faster to deploy and update but add latency and cost per query.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Where should freshmen live at UB and why? | North Campus, because most freshman classes are there and commuting by bus from South Campus is inconvenient. Submit your housing application early for priority room selection. |
| 2 | What should I do if UB classes aren't canceled but the weather is dangerous? | Use your best judgment and prioritize safety. Email your professor — students won't be penalized for missing class due to hazardous travel conditions, but must make up work promptly. |
| 3 | How do I get mental health counseling at UB? | Call Counseling Services at 716-645-2720. Services are free for registered students and include individual counseling, group therapy, wellness coaching, and embedded counselors in each academic unit. Crisis line: press option 2 after hours, or call/text 988. |
| 4 | What are the parking rules for first-year students living on campus? | First-year residents can have a car but must park in their residence hall lot or Park and Ride lots Monday–Friday, 7 AM–3 PM. Governors residents use Governors E Lot. Register for a free virtual permit through the E-Business Center. |
| 5 | What should I check before signing an off-campus lease near UB? | Verify the property passed a NYS safety inspection within 3 years, visit in person, research the landlord, check for smoke/CO detectors, understand roommate liability (each tenant is responsible for full rent), and document existing damage with photos before moving in. |

---

## Anticipated Challenges

1. **Winter-related content overlap across multiple documents.** Three of my 12 documents focus on winter survival and weather policies. Chunks from these documents may compete with each other during retrieval, returning redundant information instead of pulling from different relevant sources. This could result in answers that are repetitive rather than comprehensive, and could crowd out chunks from other documents that might add useful context.

2. **Chunk boundary splitting key advice.** Some of my documents contain numbered tips where the context (e.g., "Tip 3: Meet with your advisor often") is followed by an explanation. If the chunk boundary falls between the tip header and its explanation, retrieval might return the explanation without the context of what it's about, or the header without the details. The 100-character overlap should mitigate this, but it won't catch all cases, especially for longer explanations.

---

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────────────┐
│  Document        │     │  Chunking         │     │  Embedding + Storage     │
│  Ingestion       │────▶│                   │────▶│                          │
│                  │     │  Split by 500     │     │  all-MiniLM-L6-v2        │
│  Load .txt files │     │  chars, 100       │     │  (sentence-transformers) │
│  from documents/ │     │  overlap          │     │  → ChromaDB collection   │
│  (Python I/O)    │     │  (Python)         │     │  with source metadata    │
└─────────────────┘     └──────────────────┘     └──────────┬───────────────┘
                                                             │
                                                             ▼
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────────────┐
│  Response        │     │  Generation       │     │  Retrieval               │
│  (Gradio UI)     │◀────│                   │◀────│                          │
│                  │     │  Groq LLM         │     │  Query → embed →         │
│  Answer +        │     │  (llama-3.3-70b)  │     │  ChromaDB similarity     │
│  source citations│     │  Grounded prompt  │     │  search, top-5 chunks    │
└─────────────────┘     └──────────────────┘     └──────────────────────────┘
```

---

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:**
I'll give Claude Code my Chunking Strategy section (500-char chunks, 100-char overlap) and the list of document files in `documents/`. I'll ask it to implement: (1) a `load_documents()` function that reads all `.txt` files from the documents directory and returns a list of `{filename, text}` dicts, and (2) a `chunk_text()` function that splits each document's cleaned text into chunks of 500 characters with 100-character overlap, attaching the source filename as metadata to each chunk. I'll verify by printing 5 random chunks and checking they're self-contained and correctly attributed.

**Milestone 4 — Embedding and retrieval:**
I'll give Claude Code my Retrieval Approach section and Architecture diagram. I'll ask it to implement: (1) embedding all chunks using `SentenceTransformer("all-MiniLM-L6-v2")`, (2) storing them in a ChromaDB collection with source filename metadata, and (3) a `retrieve(query, k=5)` function that returns the top-k chunks with distances and source info. I'll verify by running 3 of my evaluation plan queries and checking that the top results are relevant with distance scores below 0.5.

**Milestone 5 — Generation and interface:**
I'll give Claude Code my Architecture diagram and the grounding requirement (answers from retrieved context only, with source attribution). I'll ask it to implement: (1) a `generate_answer(query, chunks)` function that calls Groq's `llama-3.3-70b-versatile` with a system prompt enforcing grounded responses and source citations, and (2) a Gradio web UI with a text input, submit button, answer display, and sources display. I'll verify by asking 2-3 queries end-to-end, checking that responses cite sources and that an out-of-scope question gets a refusal.
