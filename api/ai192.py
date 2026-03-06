from flask import Flask, request, jsonify, render_template
from googlesearch import search
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def search_google(query):

    results_text = []

    for url in search(query, num_results=5):

        try:
            r = requests.get(url, timeout=5)

            soup = BeautifulSoup(r.text, "html.parser")

            paragraphs = soup.find_all("p")

            text = " ".join([p.get_text() for p in paragraphs])

            results_text.append(text[:1500])

        except:
            pass

    return " ".join(results_text)


def ai_answer(question):

    text = search_google(question)

    if len(text) < 50:
        return "لم أجد جواباً واضحاً."

    # نرجع جزء من النص كإجابة
    return text[:500]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():

    question = request.json["question"]

    answer = ai_answer(question)

    return jsonify({"answer": answer})


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)