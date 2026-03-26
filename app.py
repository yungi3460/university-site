from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open("data.json", encoding="utf-8") as f:
    universities = json.load(f)

def convert_grade(grade, system):
    if system == "5":
        return grade * 2
    return grade

@app.route("/", methods=["GET", "POST"])
def index():
    results = {"상향": [], "적정": [], "안정": []}

    if request.method == "POST":
        grade = float(request.form["grade"])
        system = request.form["system"]
        category = request.form["category"]
        selected_major = request.form["major"]

        grade = convert_grade(grade, system)

        for uni in universities["universities"]:
            for m in uni["majors"]:

                # 계열 체크
                if m["category"] != category:
                    continue

                # 전체 or 같은 그룹
                if selected_major == "전체" or m["group"] == selected_major:

                    if grade <= uni["grade_cut"]:

                        diff = uni["grade_cut"] - grade

                        if diff <= 0.2:
                            results["상향"].append(uni["name"])
                        elif diff <= 0.6:
                            results["적정"].append(uni["name"])
                        else:
                            results["안정"].append(uni["name"])

                    break

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run()