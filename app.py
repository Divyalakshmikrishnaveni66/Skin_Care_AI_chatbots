from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔥 Advanced backend logic (100+ problems scalable)
def get_skin_tips(concern):
    concern = concern.lower()

    skin_data = {
        "acne": "1. Use salicylic acid face wash\n2. Avoid oily food\n3. Keep face clean",
        "pimple": "1. Use benzoyl peroxide cream\n2. Do not touch face\n3. Wash twice daily",
        "acne marks": "1. Use Vitamin C serum\n2. Apply sunscreen\n3. Use niacinamide",
        "dark spots": "1. Use Vitamin C serum\n2. Avoid sun exposure\n3. Use SPF 50 sunscreen",
        "pigmentation": "1. Use kojic acid cream\n2. Apply sunscreen\n3. Consult dermatologist",
        "dry skin": "1. Use moisturizer\n2. Drink water\n3. Avoid hot showers",
        "oily skin": "1. Use oil-free face wash\n2. Avoid junk food\n3. Wash twice daily",
        "tan": "1. Apply aloe vera gel\n2. Use sunscreen\n3. Use de-tan packs",
        "sunburn": "1. Apply aloe vera\n2. Use cooling gel\n3. Avoid sun exposure",
        "blackheads": "1. Use salicylic acid\n2. Exfoliate weekly\n3. Steam face",
        "whiteheads": "1. Use gentle cleanser\n2. Avoid heavy creams\n3. Exfoliate",
        "wrinkles": "1. Use retinol cream\n2. Apply sunscreen\n3. Stay hydrated",
        "fine lines": "1. Use anti-aging serum\n2. Moisturize daily\n3. Sleep well",
        "dark circles": "1. Sleep properly\n2. Use eye cream\n3. Reduce screen time",
        "dull skin": "1. Use Vitamin C\n2. Exfoliate\n3. Stay hydrated",
        "glowing skin": "1. Drink water\n2. Eat fruits\n3. Follow skincare routine",
        "sensitive skin": "1. Use mild products\n2. Avoid chemicals\n3. Patch test",
        "itching": "1. Use soothing cream\n2. Avoid allergens\n3. Consult doctor",
        "redness": "1. Use calming gel\n2. Avoid heat\n3. Use aloe vera",
        "large pores": "1. Use toner\n2. Ice massage\n3. Clay mask",
        "uneven skin tone": "1. Use Vitamin C\n2. Sunscreen\n3. Chemical peel",
        "skin allergy": "1. Avoid triggers\n2. Use antihistamine\n3. Consult doctor",
        "face wash": "Use a gentle cleanser based on your skin type",
        "moisturizer": "Use according to skin type: oily/light, dry/heavy",
        "sunscreen": "Use SPF 30+ daily",
        "hello": "Hello! Tell me your skin concern 😊",
        "hi": "Hi! How can I help your skin today? 😊",
        "hey": "Hey! what's your skin concern today? 😊",
        "Thank you": "You're welcome! Take care of your skin! 😊",
        
    }

    for key in skin_data:
        if key in concern:
            return skin_data[key]

    return "Sorry, I didn't understand. Please describe your skin problem clearly."

# 🔥 Frontend (Advanced UI)
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>SkinCare AI Chatbot</title>
    <style>
        body {
            font-family: Arial;
            background: #f0f4f8;
            display: flex;
            justify-content: center;
            margin-top: 50px;
        }
        #chatContainer {
            width: 400px;
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        #chatBox {
            height: 350px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 10px;
            background: #fafafa;
        }
        .user {
            background: #007bff;
            color: white;
            padding: 8px;
            border-radius: 10px;
            margin: 5px;
            text-align: right;
        }
        .bot {
            background: #e4e6eb;
            color: black;
            padding: 8px;
            border-radius: 10px;
            margin: 5px;
        }
        input {
            width: 70%;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        button {
            padding: 10px;
            background: green;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
    </style>
</head>
<body>

<div id="chatContainer">
    <h2>🤖 SkinCare AI Chatbot</h2>
    <div id="chatBox"></div>
    <input type="text" id="userInput" placeholder="Enter your skin concern...">
    <button onclick="sendMessage()">Send</button>
</div>

<script>
function sendMessage() {
    const input = document.getElementById('userInput').value;
    if (!input) return alert("Enter your skin concern!");

    const chatBox = document.getElementById('chatBox');

    // User message
    chatBox.innerHTML += `<div class="user"><b>You:</b> ${input}</div>`;

    // Typing message
    const id = "msg-" + Date.now();
    chatBox.innerHTML += `<div class="bot" id="${id}"><b>Bot:</b> Typing...</div>`;

    // API call
    fetch('/get_advice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ concern: input })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById(id).innerHTML = `<b>Bot:</b> ${data.advice.replace(/\\n/g, "<br>")}`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(() => {
        document.getElementById(id).innerHTML = `<b>Bot:</b> Error occurred`;
    });

    document.getElementById('userInput').value = '';
}
</script>

</body>
</html>
"""

# 🔹 Routes
@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/get_advice", methods=["POST"])
def advice():
    data = request.json
    concern = data.get("concern", "")
    result = get_skin_tips(concern)
    return jsonify({"advice": result})

# 🔹 Run
if __name__ == "__main__":
    app.run(debug=True)