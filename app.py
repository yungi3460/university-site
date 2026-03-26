import json
import os
from flask import Flask, render_template

app = Flask(__name__)

# =========================
# 📌 JSON 안전 로더
# =========================
BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "data.json")

def load_json_safe():
    if not os.path.exists(file_path):
        print("❌ data.json 파일 없음")
        return {}

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

        if not text:
            print("❌ data.json 비어 있음")
            return {}

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            print("❌ JSON 오류:", e)
            return {}

# =========================
# 📌 데이터 로드
# =========================
data = load_json_safe()

# =========================
# 📌 라우터 (예시)
# =========================
@app.route("/")
def home():
    return render_template("index.html", data=data)

# =========================
# 📌 실행
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)