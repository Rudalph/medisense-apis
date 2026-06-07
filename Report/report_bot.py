# from flask import request, jsonify
# from Report.load_documents import retrieval_chain



# def report_bot():
#     data = request.json
#     question = data['question']
#     print(question)
#     response = retrieval_chain.invoke({"input": question})
#     answer = response["answer"]
#     print(answer)
#     return jsonify({"answer": answer})

from flask import request, jsonify
from Report.load_documents import ask_question


def report_bot():
    data = request.json

    if not data or "question" not in data:
        return jsonify({"error": "Question is required"}), 400

    question = data["question"]

    try:
        response = ask_question(question)
        answer = response["answer"]

        return jsonify({"answer": answer}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500