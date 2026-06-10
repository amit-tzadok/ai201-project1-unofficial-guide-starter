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

**Chunk size:** 500 characters (max per chunk)

**Overlap:** 100 characters

**Reasoning:** My documents are structured like a big-sister guide — each paragraph usually covers one distinct piece of advice (e.g., "start leetcoding after CSE 250" or "join UB ACM in your first semester"). Splitting by paragraph preserves these natural boundaries so each chunk is a complete, self-contained tip. If I split purely by character count, it would cut tips in half and make chunks harder to retrieve meaningfully. For paragraphs longer than 500 characters, I fall back to character splitting with 100-character overlap to catch sentences that land on the boundary. Very short paragraphs (under 100 characters) get merged with the next one to avoid tiny, useless chunks.

---

## Retrieval Approach

**Embedding model:** `all-MiniLM-L6-v2` via sentence-transformers. Runs locally, no API key needed, produces 384-dimensional embeddings. Good for short English text, which matches my document style.

**Top-k:** 5. My documents cover overlapping topics (e.g., internship advice appears in both the internship guide and the career fair doc), so retrieving 5 chunks gives enough breadth to pull relevant info from multiple sources without diluting the context.

**Production tradeoff reflection:** If I were deploying this for real UB students, I'd consider multilingual support since UB has a large international student population. A model like `paraphrase-multilingual-MiniLM-L12-v2` would let students search in their native language, which could make the guide more accessible. I'd also consider a model with a longer context window — `all-MiniLM-L6-v2` only handles 256 tokens per chunk, so longer paragraphs could get truncated during embedding, which means the search might miss relevant content buried at the end of a chunk.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | When should I start leetcoding and what should I focus on first? | Start as soon as you finish CSE 115. Begin early and go slow — focus on Easy problems with topics you already know (arrays, strings, basic loops) so you master the fundamentals over time rather than cramming before interview season. |
| 2 | Which CS clubs should I join as a freshman? | UB ACM (the main CS community with tech talks and hackathons), UB DivTech (support for underrepresented CS students), and Society of Women Engineers (SWE) for networking and mentorship. |
| 3 | How do I prepare for the STEAM career fair? | Research companies in advance and make a list of the most important ones to visit. Prepare a list of questions for each company. Write and practice an elevator pitch. Print copies of your resume on good paper. Purchase a business professional outfit. |
| 4 | How do I become a TA in the CS department? | Go to office hours regularly and build relationships with your professors. Put real effort into your classwork and show that you care about the material. You need a strong grade in the course (typically an A or A-), and expressing interest directly to the professor is often the best approach. |
| 5 | What programming languages should I learn outside of class? | Depends on your chosen career path, but Python is a must regardless. For web development, learn JavaScript/TypeScript. For systems work, consider Go or Rust. For mobile, Swift or Kotlin. SQL is valuable across all paths. |

---

## Anticipated Challenges

1. **My personal experience vs. what's actually in the documents.** Some of my expected answers come from my own experience as a CS student — like recommending SWE (Society of Women Engineers) for clubs, or advising students to go to office hours to build relationships with professors before applying to be a TA. If those specific tips aren't in the collected documents, the system can't ground its answer in them. It will either give an incomplete answer that's missing the most useful advice, or worse, hallucinate an answer that sounds right but isn't backed by any source. This is a real limitation of RAG — the system can only be as good as the documents it has.

2. **Slang and informal queries vs. formal document language.** Real CS students don't type "What study strategies should I use for CSE 331?" — they ask things like "am I cooked for 331?" or "how do I not fail algorithms?" The embedding model might not match these informal queries to the relevant chunks because the documents use more formal language. This could lead to poor retrieval even when the answer exists in the documents.

---

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────────────┐
│  Document        │     │  Chunking         │     │  Embedding + Storage     │
│  Ingestion       │────▶│                   │────▶│                          │
│                  │     │  Split by          │     │  all-MiniLM-L6-v2        │
│  Load .txt files │     │  paragraph, then   │     │  (sentence-transformers) │
│  from documents/ │     │  by 500 chars if   │     │  → ChromaDB collection   │
│  (Python I/O)    │     │  too long          │     │  with source metadata    │
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
I'll give Claude Code my Chunking Strategy section (paragraph-based splitting, 500-char max, 100-char overlap) and the list of document files in `documents/`. I'll ask it to implement: (1) a `load_documents()` function that reads all `.txt` files from the documents directory, and (2) a `chunk_text()` function that splits by paragraph first, then falls back to character splitting for long paragraphs, merging short ones. I'll verify by printing 5 random chunks and checking they're complete tips, not cut-off fragments.

**Milestone 4 — Embedding and retrieval:**
I'll give Claude Code my Retrieval Approach section and Architecture diagram. I'll ask it to implement: (1) embedding all chunks using `SentenceTransformer("all-MiniLM-L6-v2")`, (2) storing them in a ChromaDB collection with source filename metadata, and (3) a `retrieve(query, k=5)` function that returns the top-k chunks with distances and source info. I'll verify by running 3 of my evaluation plan queries and checking that the top results are actually relevant to the question.

**Milestone 5 — Generation and interface:**
I'll give Claude Code the grounding requirement (answers from retrieved context only, with source citations). I'll ask it to implement: (1) a `generate_answer(query, chunks)` function that calls Groq's `llama-3.3-70b-versatile` with a system prompt enforcing grounded responses, and (2) a Gradio web UI with a text input, answer display, and sources display. I'll verify by asking questions end-to-end, checking that responses cite real sources, and asking an off-topic question to make sure the system says "I don't have enough information" instead of making something up.
