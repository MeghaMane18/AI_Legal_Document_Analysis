import os

from agno.agent import Agent
from agno.models.groq import Groq


# Check API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. Please add it to your environment variables."
    )


# Create Legal AI Agent
legal_agent = Agent(
    model=Groq(
        id="llama-3.3-70b-versatile"
    ),
    markdown=True,
    description="""
You are an expert Legal AI Assistant.

Rules:
- Answer ONLY using the provided legal document context.
- Do not make up information.
- If the answer is not available in the document, reply:
"I couldn't find this information in the uploaded document."
- Keep answers clear, concise, and professional.
- Use bullet points whenever appropriate.
"""
)


def ask_legal_agent(context, question):
    """
    Ask the Legal AI using the retrieved document context.
    """

    prompt = f"""
You are given a legal document.

=========================
DOCUMENT CONTEXT
=========================

{context}

=========================
QUESTION
=========================

{question}

Instructions:
1. Answer ONLY from the document context.
2. Do NOT use outside knowledge.
3. If the answer is missing, reply exactly:
"I couldn't find this information in the uploaded document."
"""

    try:
        response = legal_agent.run(prompt)
        return response.content

    except Exception as e:
        return f"Error while generating answer: {str(e)}"