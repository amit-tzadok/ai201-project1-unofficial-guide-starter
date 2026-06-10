"""
Document ingestion and chunking pipeline.

Loads .txt files from documents/, splits them into chunks using
paragraph-based splitting (with character fallback for long paragraphs),
and returns chunks with source metadata.
"""

import os
import glob


def load_documents(docs_dir="documents"):
    """Load all .txt files from the documents directory.

    Returns a list of dicts: [{"filename": "...", "text": "..."}]
    """
    documents = []
    for filepath in sorted(glob.glob(os.path.join(docs_dir, "*.txt"))):
        filename = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        documents.append({"filename": filename, "text": text})
    return documents


def strip_metadata_header(text):
    """Remove the Source/URL/Type metadata lines from the top of a document."""
    lines = text.split("\n")
    content_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("Source:") or stripped.startswith("URL:") or stripped.startswith("URLs:") or stripped.startswith("Type:"):
            content_start = i + 1
        elif stripped == "":
            continue
        else:
            break
    return "\n".join(lines[content_start:]).strip()


def chunk_text(text, source_filename, max_chunk_size=500, overlap=100, min_chunk_size=100):
    """Split text into chunks using paragraph-based splitting.

    Strategy:
    1. Strip metadata header (Source/URL/Type lines)
    2. Split by double newlines (paragraphs)
    3. Merge short paragraphs (under min_chunk_size) with the next one
    4. Split long paragraphs (over max_chunk_size) by character with overlap,
       breaking at the last space to avoid cutting mid-word

    Returns a list of dicts: [{"text": "...", "source": "..."}]
    """
    # Strip metadata header
    text = strip_metadata_header(text)

    # Split into paragraphs by double newline
    raw_paragraphs = text.split("\n\n")

    # Clean up: strip whitespace, remove empty paragraphs
    paragraphs = [p.strip() for p in raw_paragraphs if p.strip()]

    # Merge short paragraphs with the next one
    merged = []
    buffer = ""
    for para in paragraphs:
        if buffer:
            buffer = buffer + "\n\n" + para
        else:
            buffer = para

        if len(buffer) >= min_chunk_size:
            merged.append(buffer)
            buffer = ""

    # Don't lose any remaining text in the buffer
    if buffer:
        if merged:
            merged[-1] = merged[-1] + "\n\n" + buffer
        else:
            merged.append(buffer)

    # Now split long paragraphs by character with overlap
    chunks = []
    for para in merged:
        if len(para) <= max_chunk_size:
            chunks.append({"text": para, "source": source_filename})
        else:
            # Character-based splitting for long paragraphs.
            # Break at last newline (list item boundary), sentence end, or space.
            sub_chunks = []
            start = 0
            while start < len(para):
                end = min(start + max_chunk_size, len(para))
                if end < len(para):
                    # Try to break at the last newline (list item boundary)
                    nl_idx = para.rfind("\n", start + min_chunk_size, end)
                    if nl_idx > start:
                        end = nl_idx
                    else:
                        # Try sentence boundary
                        sent_idx = para.rfind(". ", start + min_chunk_size, end)
                        if sent_idx > start:
                            end = sent_idx + 1
                        else:
                            # Fall back to last space
                            space_idx = para.rfind(" ", start, end)
                            if space_idx > start:
                                end = space_idx
                sub_chunks.append(para[start:end].strip())
                start = end

            # Merge any small trailing fragment into the previous sub-chunk
            if len(sub_chunks) > 1 and len(sub_chunks[-1]) < min_chunk_size:
                sub_chunks[-2] = sub_chunks[-2] + " " + sub_chunks[-1]
                sub_chunks.pop()

            for sc in sub_chunks:
                if sc:
                    chunks.append({"text": sc, "source": source_filename})

    return chunks


def ingest_all(docs_dir="documents"):
    """Load all documents and chunk them.

    Returns a list of all chunks across all documents.
    """
    documents = load_documents(docs_dir)
    all_chunks = []

    for doc in documents:
        doc_chunks = chunk_text(doc["text"], doc["filename"])
        all_chunks.extend(doc_chunks)

    return all_chunks


if __name__ == "__main__":
    # Run ingestion and print stats + sample chunks
    chunks = ingest_all()

    print(f"Total chunks: {len(chunks)}")
    print(f"Documents processed: {len(load_documents())}")
    print()

    # Print 5 sample chunks
    import random
    random.seed(42)
    samples = random.sample(chunks, min(5, len(chunks)))

    for i, chunk in enumerate(samples, 1):
        print(f"--- Sample Chunk {i} (from {chunk['source']}) ---")
        print(f"Length: {len(chunk['text'])} chars")
        print(chunk["text"])
        print()
