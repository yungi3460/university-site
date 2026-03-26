import json
import os
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "data.json")

def load_json_safe():
    if not os.path.exists(file_path):
        return {"universities": []}

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
        if not text:
            return {"universities": []}
        try:
            return json.loads(text)
        except:
            return {"universities": []}

data = load_json_safe()


@app.route("/", methods=["GET", "POST"])
def home():

    results = {"상향": [], "적정": [], "안정": []}

    if request.method == "POST":
        grade = float(request.form.get("grade", 99))

        for uni in data["universities"]:
            cut = uni["grade_cut"]

            if grade < cut - 0.3:
                results["상향"].append(uni["name"])
            elif grade <= cut + 0.3:
                results["적정"].append(uni["name"])
            else:
                results["안정"].append(uni["name"])

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)