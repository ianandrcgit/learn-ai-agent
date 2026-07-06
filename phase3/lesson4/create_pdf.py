from fpdf import FPDF

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

pages = [
    ("Introduction to Artificial Intelligence",
     "Artificial intelligence is the simulation of human intelligence by machines. "
     "It was founded as an academic discipline in 1956 by John McCarthy. "
     "AI systems are used in many applications including speech recognition and image processing."),

    ("Machine Learning Basics",
     "Machine learning is a subset of artificial intelligence. "
     "It allows computers to learn from data without being explicitly programmed. "
     "Common algorithms include linear regression, decision trees, and neural networks."),

    ("Deep Learning and Neural Networks",
     "Deep learning uses neural networks with many layers to learn complex patterns. "
     "It has revolutionized computer vision and natural language processing. "
     "GPT and Claude are examples of large language models built with deep learning."),

    ("RAG Systems",
     "Retrieval Augmented Generation combines document search with AI generation. "
     "RAG reduces hallucination by grounding answers in real documents. "
     "It is widely used in enterprise document Q&A systems."),
]

for title, content in pages:
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, title, ln=True)
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, content)

pdf.output("sample.pdf")
print("sample.pdf created successfully!")