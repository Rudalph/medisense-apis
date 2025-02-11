from flask import request, jsonify
from Report.load_documents import retrieval_chain



def report_bot():
    data = request.json
    question = data['question']
    print(question)
    response = retrieval_chain.invoke({"input": question})
    answer = response["answer"]
    print(answer)
    return jsonify({"answer": answer})