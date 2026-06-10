"""
The Unofficial Guide — Gradio Web Interface

A RAG-powered guide for CS students at the University at Buffalo.
Run with: python app.py
Then open http://localhost:7860
"""

import gradio as gr
from query import generate_answer


def handle_query(question):
    """Process a user question and return the answer + sources."""
    if not question.strip():
        return "Please enter a question!", ""

    result = generate_answer(question)

    # Format sources as a bulleted list
    sources = "\n".join(f"• {s}" for s in result["sources"])

    return result["answer"], sources


with gr.Blocks(title="The Unofficial Guide — UB CS") as demo:
    gr.Markdown(
        """
        # 🎓 The Unofficial Guide — UB Computer Science
        *A big-sister guide for CS students at the University at Buffalo.*

        Ask me about CS clubs, courses, internships, research, leetcode prep,
        career fairs, TA positions, grad school, or tools to learn.
        """
    )

    with gr.Row():
        with gr.Column():
            inp = gr.Textbox(
                label="Your question",
                placeholder="e.g. When should I start leetcoding?",
                lines=2,
            )
            btn = gr.Button("Ask", variant="primary")

    with gr.Row():
        with gr.Column():
            answer = gr.Textbox(label="Answer", lines=10, interactive=False)
        with gr.Column():
            sources = gr.Textbox(label="Sources", lines=10, interactive=False)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()
