from flask import Flask, request, jsonify, render_template


app = Flask(__name__)


keywords = {
    "apple": "red",
    "banana": "yellow",
    "orange": "orange",
    "grape": "purple",
    "kiwi": "green",
    "lemon": "yellow",
    "mango": "yellow",
}

default_response = "Sorry, I don't know that fruit."


@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").lower().strip()
    if not user_input:
        return jsonify({"error": "Please enter a valid message."})
    
    reply = default_response
    for keyword in keywords:
        if keyword in user_input:
            reply = f"The color of {keyword} is {keywords[keyword]}."
            break

    return jsonify({"reply": reply})




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

