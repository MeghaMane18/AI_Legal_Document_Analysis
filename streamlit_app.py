import streamlit as st
import tempfile
import os

from rag.pdf_loader import extract_text
from agents.legal_agent import ask_legal_agent

st.set_page_config(
    page_title="AI Legal Document Analysis",
    layout="wide"
)

st.title("📄 AI Legal Document Analysis")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp_file:

        tmp_file.write(uploaded_file.read())
        pdf_path = tmp_file.name

    st.success("✅ PDF Uploaded Successfully")

    with st.spinner("Extracting text..."):

        document_text = extract_text(pdf_path)

    os.remove(pdf_path)

    if document_text:

        st.session_state["document_text"] = document_text

        st.success("✅ Text Extracted Successfully")

        st.write("### Preview")

        st.text_area(
            "Extracted Text",
            document_text[:3000],
            height=300
        )

    else:

        st.error("No text found in the PDF.")

from agents.legal_agent import ask_legal_agent

question = st.text_input("Ask a question about the document")

if st.button("Ask AI"):

    if "document_text" not in st.session_state:

        st.warning("Please upload a PDF first.")

    elif question.strip() == "":

        st.warning("Please enter a question.")

    else:

        with st.spinner("🤖 AI is analyzing the document..."):

            answer = ask_legal_agent(
                st.session_state["document_text"],
                question
            )

        st.subheader("Answer")

        st.markdown(answer)