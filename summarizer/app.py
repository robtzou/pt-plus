from flask import Flask, request, jsonify
from flask_cors import CORS
from summarize import process_text, get_summary_from_chunks
from tokenizer import tokenize_text, chunk_tokens


app = Flask(__name__)
CORS(app)

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    raw_text = data.get("text", "")
    command = data.get("command", "Summarize the content.")

    if not raw_text.strip():
        return jsonify({"error": "Empty input."}), 400

    chunks = process_text(raw_text)
    summary = get_summary_from_chunks(chunks, command)
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)
