from flask import Flask, request, jsonify, render_template
from transformers import pipeline

qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # This serves the HTML file

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question")
    if not user_input:
        return jsonify({"error": "No question provided"}), 400
    
    result = qa_pipeline(f"Q: {user_input} A:")
    answer = result[0]['generated_text']
    return jsonify({"answer": answer})
@app.route("/doctors", methods=["POST"])
def get_doctors():
    data = request.json
    department = data.get("department")
    lat = data.get("latitude")
    lon = data.get("longitude")

    if not department or lat is None or lon is None:
        return jsonify({"error": "Missing location or department"}), 400

    # For now: simulate doctor lookup (later: use real API)
    fake_doctors = {
        "Cardiology": ["Dr. Heartwell - City Hospital", "Dr. Arya - Cardio Clinic"],
        "Pediatrics": ["Dr. Kidsworth - Child Care Center", "Dr. Tiny - Baby Hospital"],
        "Dermatology": ["Dr. Skinner - Glow Clinic", "Dr. Fair - SkinPro"],
        "Neurology": ["Dr. Brain - Neuro Care", "Dr. Nerve - Mind Clinic"],
        "Orthopedics": ["Dr. Bones - Ortho Plus", "Dr. Joint - Flex Hospital"]
    }

    doctors = fake_doctors.get(department, [])
    return jsonify({"doctors": doctors})


if __name__ == "__main__":
    app.run(debug=True)
