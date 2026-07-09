from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from agno.agent import Agent
from agno.models.groq import Groq



legal_agent = Agent(
    model=Groq(
        id="llama-3.3-70b-versatile"
    ),
    markdown=True,
    description="""
You are an expert Legal AI Assistant.

Your job is to answer questions ONLY using the provided legal document context.

Rules:
- Answer only from the document.
- If the answer is not present in the document, say:
  "I couldn't find this information in the uploaded document."
- Keep answers clear and professional.
- Use bullet points whenever appropriate.
"""
)


def ask_legal_agent(context, question):
    """
    Ask the Legal AI using the retrieved document context.
    """

    prompt = f"""
You are given a legal document.

Document Context:
{context}

Question:
{question}

Answer using ONLY the document context.
"""

    response = legal_agent.run(prompt)

    return response.content