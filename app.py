from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory
)

from werkzeug.utils import secure_filename
from config import Config

from rag.pdf_loader import extract_text
from rag.chunker import chunk_text
from rag.embeddings import create_embeddings
from rag.vector_store import store_embeddings
from rag.retriever import retrieve_chunks

from agents.legal_agent import ask_legal_agent

import os
import traceback


app = Flask(__name__)
app.config.from_object(Config)


# Create uploads folder
os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)


# =====================================================
# Home Page
# =====================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =====================================================
# PDF Viewer Route
# =====================================================

@app.route("/pdf/<filename>")
def view_pdf(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# =====================================================
# Upload PDF
# =====================================================

@app.route("/upload", methods=["POST"])
def upload():

    try:

        if "file" not in request.files:

            return jsonify({
                "error": "No file uploaded"
            }), 400


        file = request.files["file"]


        if file.filename == "":

            return jsonify({
                "error": "No file selected"
            }), 400



        filename = secure_filename(
            file.filename
        )


        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )


        file.save(filepath)



        print("\n===================================")
        print("PDF Uploaded Successfully")
        print("===================================")



        # =================================================
        # STEP 1 : Extract Text
        # =================================================

        print("\nStep 1 : Extracting Text...")


        document_text = extract_text(filepath)


        if not document_text or len(document_text.strip()) == 0:

            return jsonify({

                "error":
                "No text found in PDF. Please upload a text-based PDF."

            }), 400



        print("Done")

        print(
            f"Characters : {len(document_text)}"
        )



        # =================================================
        # STEP 2 : Chunking
        # =================================================

        print("\nStep 2 : Creating Chunks...")


        chunks = chunk_text(
            document_text
        )


        if not chunks or len(chunks) == 0:

            return jsonify({

                "error":
                "Unable to create chunks from document"

            }), 400



        print(
            f"Chunks : {len(chunks)}"
        )



        # =================================================
        # STEP 3 : Embeddings
        # =================================================

        print("\nStep 3 : Creating Embeddings...")


        embeddings = create_embeddings(
            chunks
        )


        if embeddings is None or len(embeddings) == 0:

            return jsonify({

                "error":
                "Embedding creation failed"

            }), 400



        print("Done")


        print(
            "Embedding Shape :",
            embeddings.shape
        )



        # =================================================
        # STEP 4 : Store Embeddings
        # =================================================

        print("\nStep 4 : Storing Embeddings...")


        store_embeddings(
            chunks,
            embeddings
        )


        print("Done")



        # =================================================
        # STEP 5 : Test Retrieval
        # =================================================

        print("\nStep 5 : Testing Retrieval")


        results = retrieve_chunks(
            "What is this document about?"
        )


        print("\nRetrieved Chunks:\n")


        if results and "documents" in results:

            for i, doc in enumerate(results["documents"]):

                print(
                    f"\nChunk {i+1}"
                )

                print(
                    doc[:250]
                )



        return jsonify({

            "message":
            "Document uploaded successfully!",


            "filename":
            filename,


            "pdf_url":
            f"/pdf/{filename}",


            "characters":
            len(document_text),


            "chunks":
            len(chunks),


            "embedding_dimension":
            embeddings.shape[1]

        })



    except Exception as e:


        traceback.print_exc()


        return jsonify({

            "error":
            str(e)

        }), 500




# =====================================================
# Ask Question
# =====================================================

@app.route("/ask", methods=["POST"])
def ask():


    try:


        data = request.get_json()


        question = data.get(
            "question"
        )


        if not question:


            return jsonify({

                "error":
                "Question is required"

            }), 400



        print("\n===================================")
        print("Question")
        print(question)
        print("===================================")



        results = retrieve_chunks(
            question
        )


        documents = results["documents"]


        source_ids = results["ids"]



        answer = ask_legal_agent(

            documents,

            question

        )



        print("\nAI Answer\n")

        print(answer)



        return jsonify({

            "question":
            question,


            "answer":
            answer,


            "sources":
            source_ids

        })



    except Exception as e:


        traceback.print_exc()


        return jsonify({

            "error":
            str(e)

        }), 500





# =====================================================
# Run Application
# =====================================================

if __name__ == "__main__":


    app.run(
        debug=True
    )