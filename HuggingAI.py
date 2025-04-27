from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

# Hugging Face API setup
HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"
HF_API_KEY = "your_huggingface_api_key_here"  # <-- Replace this!

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def query_huggingface(payload):
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    return response.json()

@app.route("/")
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Chat with AI</title>
        <style>
            body {
                background-color: #f9fafb;
                font-family: 'Inter', sans-serif;
                margin: 0;
                padding: 0;
                height: 100vh;
                display: flex;
                flex-direction: column;
            }
            .chat-container {
                flex: 1;
                display: flex;
                flex-direction: column;
                padding: 20px;
                overflow-y: auto;
                max-height: calc(100vh - 80px);
            }
            .message {
                max-width: 70%;
                padding: 12px 18px;
                margin: 10px 0;
                border-radius: 18px;
                font-size: 16px;
                line-height: 1.4;
                word-wrap: break-word;
                animation: fadeIn 0.3s ease-in-out;
            }
            .user {
                background-color: #007bff;
                color: white;
                align-self: flex-end;
            }
            .ai {
                background-color: #e5e7eb;
                color: #111827;
                align-self: flex-start;
            }
            .input-container {
                display: flex;
                padding: 10px;
                border-top: 1px solid #ddd;
                background: white;
            }
            input {
                flex: 1;
                padding: 12px;
                font-size: 16px;
                border-radius: 10px;
                border: 1px solid #ccc;
                outline: none;
            }
            button {
                background-color: #10b981;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 20px;
                margin-left: 10px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #059669;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
        </style>
    </head>
    <body>
        <div class="chat-container" id="chat"></div>
        <div class="input-container">
            <input type="text" id="userInput" placeholder="Type a message..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Send</button>
        </div>

        <script>
            function addMessage(content, sender) {
                const chat = document.getElementById('chat');
                const message = document.createElement('div');
                message.className = 'message ' + sender;
                message.innerText = content;
                chat.appendChild(message);
                chat.scrollTop = chat.scrollHeight;
            }

            async function sendMessage() {
                const inputField = document.getElementById('userInput');
                const userInput = inputField.value.trim();
                if (!userInput) return;
                addMessage(userInput, 'user');
                inputField.value = '';
                
                // Show a typing animation (simple)
                const thinking = document.createElement('div');
                thinking.className = 'message ai';
                thinking.innerText = '...';
                document.getElementById('chat').appendChild(thinking);
                document.getElementById('chat').scrollTop = document.getElementById('chat').scrollHeight;

                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ input: userInput })
                });
                const data = await response.json();

                // Remove thinking animation
                thinking.remove();

                addMessage(data.response, 'ai');
            }

            function handleKeyPress(event) {
                if (event.key === "Enter") {
                    sendMessage();
                }
            }
        </script>
    </body>
    </html>
    """
    return Response(html_content, mimetype='text/html')

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("input")
    payload = {"inputs": user_input}
    output = query_huggingface(payload)
    generated_text = output[0]['generated_text'] if isinstance(output, list) else output
    return jsonify({"response": generated_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
