# The Unofficial Guide — UB Computer Science

A RAG (Retrieval-Augmented Generation) system that makes practical CS student knowledge at the University at Buffalo searchable and answerable. Ask a plain-language question and get a grounded, cited answer drawn from real documents.

**Run it:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your Groq API key
python retrieval.py    # build the vector store (first time only)
python app.py          # open http://localhost:7860
```

---

## Domain

Survival guide for computer science students at the University at Buffalo. This guide covers the practical knowledge that CS students need but struggle to find — things like how to find research opportunities, when to start preparing for internships and leetcoding, which clubs and communities can help you find your path, which courses matter most for your career goals, and how to build experience as a coder outside of schoolwork.

This information is hard to find because CS students at UB tend to keep to themselves. As a girl in a male-dominated program, I didn't fit into the study cliques that formed naturally, so I was mostly a one-woman team through my degree. Research opportunities weren't advertised in any obvious way, and I wish I had known as a freshman how important it was to start building experience early through research and internships. The upperclassmen I did talk to mostly just said "it's so hard" and "you're cooked" instead of offering real, actionable advice. An unofficial guide with honest, helpful tips from someone who's been through it would have made a huge difference.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | UB CSE Dept — Student Organizations | Official dept page | https://engineering.buffalo.edu/computer-science-engineering/people/professional-and-student-organizations.html |
| 2 | UB CSE Dept — Undergraduate Research | Official dept page | https://engineering.buffalo.edu/computer-science-engineering/undergraduate/experiential-learning/undergraduate-research.html |
| 3 | UB CSE Dept — Internships | Official dept page | https://engineering.buffalo.edu/computer-science-engineering/information-for-students/experiential-learning/internships.html |
| 4 | LeetCode Discuss — Intern Guide + personal advice | Forum + student advice | https://leetcode.com/discuss/post/229221/an-unofficial-guide-for-first-timers-interns-version/ |
| 5 | UB Career Design Center — STEAM Fair | Official university page | https://www.buffalo.edu/career/events/stemup.html |
| 6 | UB CSE Dept — Course Catalog + BS CS | Official dept page | https://engineering.buffalo.edu/computer-science-engineering/undergraduate/courses/course-catalog.html |
| 7 | UB CSE Dept — TA Resources + Handbook | Official dept resource | https://engineering.buffalo.edu/computer-science-engineering/information-for-students/undergraduate-program/cse-teaching-assistant-ta-resources.html |
| 8 | UB CSE Dept — Graduate Programs (MS) | Official dept page | https://engineering.buffalo.edu/computer-science-engineering/graduate/degrees-and-programs/ms-in-computer-science-and-engineering.html |
| 9 | Compiled student advice | Student advice compilation | documents/09_tools_languages_learn.txt |
| 10 | CSE 331 Support Page — TA Advice | Student/TA advice | http://www-student.cse.buffalo.edu/~atri/cse331/support/advice/index.html |
| 11 | UB CSE Dept — Experiential Learning | Official dept page | https://engineering.buffalo.edu/computer-science-engineering/undergraduate/experiential-learning.html |
| 12 | Niche.com — UB CS Reviews | Student review platform | https://www.niche.com/colleges/university-at-buffalo-suny/academics/ |

---

## Chunking Strategy

**Chunk size:** 500 characters (max per chunk)

**Overlap:** 100 characters (used only when character-splitting long paragraphs)

**Why these choices fit your documents:** My documents are structured like a big-sister guide — each paragraph usually covers one distinct piece of advice. I split by paragraph first (double newlines), which preserves natural boundaries so each chunk is a complete, self-contained tip. Purely character-based splitting would cut tips in half and make chunks harder to retrieve meaningfully. For paragraphs longer than 500 characters, I fall back to character splitting, breaking at sentence boundaries or spaces to avoid cutting mid-word. Very short paragraphs (under 100 characters) get merged with the next one to avoid tiny, useless chunks. I also strip metadata headers (Source/URL/Type lines) from the top of each document before chunking so they don't become their own chunks.

**Final chunk count:** 109 chunks across 12 documents (smallest: 100 chars, largest: 556 chars, average: 342 chars)

### Sample Chunks

**Sample 1** (from `06_cs_curriculum_courses.txt`, 481 chars):
> Popular Electives (400-level, choose based on your interests):
> - CSE 312: Introduction to Web Applications — Full-stack web development. Very practical and job-relevant.
> - CSE 365: Introduction to Computer Security — Covers vulnerabilities, cryptography, network security. Pairs well with UBNetDef club.
> - CSE 368: Introduction to Artificial Intelligence — AI fundamentals, search, logic, planning.
> - CSE 370: Applied HCI and Interface Design — User experience design, prototyping.

**Sample 2** (from `06_cs_curriculum_courses.txt`, 477 chars):
> - CSE 191: Introduction to Discrete Structures — Math for CS: logic, proofs, sets, combinatorics. Many students find this challenging if they're not comfortable with abstract math.
> - CSE 220: Systems Programming — C programming, memory management, pointers. A tough transition from Python/Java. Start early on assignments.
> - CSE 250: Data Structures — Arrays, linked lists, trees, hash tables, graphs. One of the most important courses for interview prep. Master this material.

**Sample 3** (from `03_internship_guide.txt`, 144 chars):
> Completion Requirements: Submit the CSE Internship Evaluation Form by the last day of classes. Failure to submit results in an Incomplete grade.

**Sample 4** (from `09_tools_languages_learn.txt`, 272 chars):
> - Go or Rust: Increasingly popular for systems programming and cloud infrastructure. Knowing one of these sets you apart from other candidates.
> - Swift or Kotlin: If you're interested in mobile development. iOS (Swift) and Android (Kotlin) are both lucrative career paths.

**Sample 5** (from `03_internship_guide.txt`, 306 chars):
> Application Process: Force registration deadline is the second Friday of the semester. Required documents: completed application form and official company offer letter on company letterhead with job duties, dates, time commitment, and reporting structure. Submit through the SEAS Force Registration Portal.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via sentence-transformers. It runs locally with no API key, produces 384-dimensional embeddings, and works well for short English text — which matches my paragraph-sized chunks.

**Production tradeoff reflection:** If I were deploying this for real UB students, I'd consider multilingual support since UB has a large international student population. A model like `paraphrase-multilingual-MiniLM-L12-v2` would let students search in their native language, making the guide more accessible. I'd also consider a model with a longer context window — `all-MiniLM-L6-v2` only handles 256 tokens per chunk, so longer paragraphs could get truncated during embedding, meaning the search might miss relevant content buried at the end of a chunk.

### Retrieval Test Results

**Query 1:** "When should I start leetcoding and what should I focus on first?"
- **Top chunks:** Recommended timeline from leetcode doc (dist: 0.49), internship prep advice (dist: 0.49), when-to-start section (dist: 0.54)
- **Why relevant:** All three directly address the timing and focus of leetcode prep, pulling from both the dedicated leetcode doc and the internship guide for complementary advice.

**Query 2:** "Which CS clubs should I join as a freshman?"
- **Top chunks:** General club advice (dist: 0.27), club listing with ACM/UBNetDef/DivTech (dist: 0.41), student reviews (dist: 0.46)
- **Why relevant:** The top result (0.27 — strong match) directly advises joining clubs in first semester. The second chunk names specific clubs.

**Query 3:** "How do I prepare for the STEAM career fair?"
- **Top chunks:** Fair overview (dist: 0.32), preparation checklist (dist: 0.40), career center tips (dist: 0.44)
- **Why relevant:** Top 4 results all come from career fair and internship docs with directly actionable prep steps.

---

## Grounded Generation

**System prompt grounding instruction:**

The system prompt instructs the LLM to act as "The Unofficial Guide — a helpful big-sister figure" and enforces three strict rules:
1. "Answer ONLY using the information provided in the Retrieved Documents below. Do not use any outside knowledge."
2. "If the retrieved documents do not contain enough information to answer the question, say: 'I don't have enough information on that in my sources.'"
3. "For every claim in your answer, cite the source document in parentheses, like (source: 04_leetcode_interview_prep.txt)."

The temperature is set to 0.3 (low) to reduce creative generation and keep answers grounded.

**How source attribution is surfaced in the response:**

Source attribution happens at two levels:
1. **In the LLM response:** The system prompt requires inline citations for every claim, e.g., "(source: 04_leetcode_interview_prep.txt)".
2. **In the UI:** The retrieved chunk sources are collected programmatically and displayed in a separate "Sources" panel next to the answer, so even if the LLM misses a citation, the user can see which documents were consulted.

### Example Responses

**Example 1 — Grounded response with citations:**
> Q: "How do I become a TA in the CS department?"
>
> A: "To become a TA in the CS department, you should start by expressing interest directly to a professor whose course you did well in (source: 07_ta_experience_grading.txt). If you're an undergraduate, you can serve as a Student Assistant (SA) for lower-level courses like CSE 115 and CSE 116, as long as you've done well in the course yourself (typically an A or A-) (source: 07_ta_experience_grading.txt)..."
>
> Sources: 07_ta_experience_grading.txt, 12_niche_cs_reviews.txt

**Example 2 — Grounded response with multiple sources:**
> Q: "How do I prepare for the STEAM career fair?"
>
> A: "To prepare for the STEAM career fair, follow these steps (source: 05_career_fair_tips.txt): Register through Bullseye, research employers before the fair, bookmark target employers... Additionally, get your resume reviewed at the Career Design Center (source: 03_internship_guide.txt)..."
>
> Sources: 05_career_fair_tips.txt, 03_internship_guide.txt, 12_niche_cs_reviews.txt

**Example 3 — Out-of-scope refusal:**
> Q: "What's the best pizza place near campus?"
>
> A: "I don't have enough information on that in my sources. Try asking about CS clubs, courses, internships, research, career prep, or grad school at UB."

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | When should I start leetcoding and what should I focus on first? | Start after CSE 115, go slow, focus on Easy problems with topics you know (arrays, strings, loops). | Said to start as a freshman with Easy problems, focus on arrays/strings/loops, aim for 2-3 problems/week after CSE 250. Cited leetcode and internship docs. | Relevant | Partially accurate — correct advice but didn't mention CTCI book or study groups, which were in a lower-ranked chunk. |
| 2 | Which CS clubs should I join as a freshman? | UB ACM, UB DivTech, and Society of Women Engineers (SWE). | Recommended ACM, UBNetDef, MakeOpenSource, and DivTech. Did not mention SWE. | Partially relevant | Partially accurate — good club recommendations but missed SWE because it's not in the documents. |
| 3 | How do I prepare for the STEAM career fair? | Research companies, make a list, prepare questions, practice pitch, print resume, buy professional outfit. | Covered all key points: register on Bullseye, research employers, plan booth visits, practice pitch, dress professionally, bring resumes, update LinkedIn. | Relevant | Accurate |
| 4 | How do I become a TA in the CS department? | Go to office hours, build relationships with professors, get strong grades (A or A-), express interest directly. | Said to express interest to professors, need A or A-, watch for application announcements. Mentioned responsibilities. | Relevant | Partially accurate — covered grades and applying, but didn't emphasize building relationships through office hours as strongly as expected. |
| 5 | What programming languages should I learn outside of class? | Depends on career path, Python is a must. JS/TS for web, Go/Rust for systems, Swift/Kotlin for mobile, SQL for all. | Recommended JavaScript/TypeScript and SQL specifically. Mentioned web dev frameworks. | Relevant | Partially accurate — good specific recommendations but didn't explicitly say "Python is a must" or cover the career-path breakdown. |

---

## Failure Case Analysis

**Question that failed:** "Which CS clubs should I join as a freshman?"

**What the system returned:** The system recommended UB ACM, UBNetDef, MakeOpenSource, and UB DivTech — all real CS clubs at UB. However, it did not mention the Society of Women Engineers (SWE), which was part of my expected answer.

**Root cause (tied to a specific pipeline stage):** This is a **document coverage failure**, not a retrieval or generation failure. SWE (Society of Women Engineers) is not mentioned anywhere in the 12 collected documents. The documents focus on CSE-department-affiliated clubs, and SWE is an engineering-wide organization listed separately. Since RAG can only answer from what's in the documents, the system had no way to recommend SWE. The retrieval correctly found the most relevant club-related chunks, and the LLM correctly limited its answer to what those chunks contained — the system worked as designed, but the documents didn't cover everything I wanted.

**What you would change to fix it:** Add a document specifically about engineering-wide organizations that benefit CS students (SWE, oSTEM, NSBE, etc.) and women-in-tech resources at UB. This would give the retrieval system access to those recommendations. This failure is a good example of why document selection is the foundation of a RAG system — no amount of model tuning can compensate for missing source material.

---

## Spec Reflection

**One way the spec helped you during implementation:** Writing the domain description in planning.md kept me focused on what the guide was actually about. When collecting documents, I was tempted to include general campus life content (housing, dining, winter survival), but the spec clearly defined my scope as CS student advice. This prevented scope creep and kept the document collection targeted, which ultimately made retrieval more precise — every chunk is relevant to the kinds of questions a CS student would ask.

**One way your implementation diverged from the spec, and why:** I originally planned to build a general campus survival guide for UB students, but pivoted entirely to a CS-focused guide after writing the first version of planning.md. The general domain didn't feel authentic — I was collecting documents about topics I didn't have strong opinions on. The CS domain let me draw on my own experience as a UB CS student to define what questions actually matter, which made the evaluation plan and document collection much more intentional. I rewrote planning.md from scratch after the pivot.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* I gave Claude Code my chunking strategy from planning.md (paragraph-based splitting, 500-char max, 100-char overlap, merge short paragraphs) and asked it to implement the `chunk_text()` function in `ingest.py`.
- *What it produced:* A working function that split by double newlines, merged short paragraphs, and used character splitting as a fallback for long paragraphs.
- *What I changed or overrode:* The first version produced small orphan fragments from the overlap logic (e.g., 69-character pieces like leftover sentence endings). I had Claude fix the character splitting to break at sentence boundaries and newlines first, and merge any trailing fragments under 100 characters back into the previous chunk. I also had it strip the Source/URL/Type metadata headers from documents before chunking, because those were becoming their own chunks.

**Instance 2**

- *What I gave the AI:* I gave Claude Code the grounding requirement (answers only from retrieved documents, with source citations, and a refusal response for out-of-scope questions) and asked it to implement the generation module and Gradio UI.
- *What it produced:* A `query.py` module with a system prompt and a `generate_answer()` function calling Groq, and an `app.py` with a Gradio interface showing the answer and sources side by side.
- *What I changed or overrode:* I added my personal interview prep tips (recommending CTCI, CodePath, and study groups) directly to the leetcode document rather than hardcoding them in the system prompt, because the RAG system should ground all answers in documents. Claude suggested this approach by explaining that hardcoding tips in the prompt would bypass the RAG pipeline and break grounding.

### Query Interface

**Input:** A single text box where the user types a plain-language question about CS life at UB.

**Output:** Two panels — an "Answer" panel with the LLM's grounded response (including inline source citations), and a "Sources" panel listing which document files were consulted.

**Sample interaction:**
> **Input:** "What resources should I use to prepare for coding interviews?"
>
> **Answer:** "To prepare for coding interviews, I'd recommend the following resources: Cracking the Coding Interview (CTCI) by Gayle Laakmann McDowell - read it cover to cover for insights on interviews and answer structuring (source: 04_leetcode_interview_prep.txt). CodePath Technical Interview Course - a free, structured course to guide your prep (source: 04_leetcode_interview_prep.txt). LeetCode, focusing on Medium problems and practicing out loud (source: 04_leetcode_interview_prep.txt). UB ACM's mock interview sessions and coding workshops (source: 04_leetcode_interview_prep.txt)..."
>
> **Sources:** 04_leetcode_interview_prep.txt, 05_career_fair_tips.txt
