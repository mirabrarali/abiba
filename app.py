import os
import logging
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

# Initialize Environment
load_dotenv()

# Configure Logging (STDOUT only for Vercel/Serverless safety)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("Abiba")

app = Flask(__name__)
CORS(app)

# --- Static File Routing ---
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/chat.html')
def serve_chat():
    return send_from_directory('.', 'chat.html')

@app.route('/logs.html')
def serve_logs():
    return send_from_directory('.', 'logs.html')

@app.route('/security.js')
def serve_security():
    return send_from_directory('.', 'security.js')

# --- API Endpoints ---

# Initialize Groq Client
groq_api_key = os.getenv("GROQ_API_KEY")
client = None
if groq_api_key:
    client = Groq(api_key=groq_api_key)
    logger.info("Groq client initialized successfully.")
else:
    logger.warning("GROQ_API_KEY not found. AI features will run in simulation mode.")

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    logger.info(f"User Query: {user_message}")
    
    if not client:
        response = get_simulated_response(user_message)
        return jsonify({"response": response, "mode": "simulation"})

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are Abiba, the smartest financial AI ecosystem. You help banks with data visualizations, task automation, and secure banking operations. You are professional, precise, and authoritative. Never mention Llama or Groq; you are Abiba itself."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        ai_response = completion.choices[0].message.content
        return jsonify({"response": ai_response, "mode": "live"})
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": "Internal synchronization error"}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    # Return PREMIUM BRANDED DUMMY LOGS for Vercel stability
    now = datetime.now()
    dummy_logs = [
        f"{now - timedelta(seconds=120):%Y-%m-%d %H:%M:%S,%f} [INFO] Abiba Neuro-Core v3.2.0 initialized.",
        f"{now - timedelta(seconds=110):%Y-%m-%d %H:%M:%S,%f} [INFO] Establishing encrypted tunnel to Finacle API...",
        f"{now - timedelta(seconds=105):%Y-%m-%d %H:%M:%S,%f} [INFO] Security Perimeter: SASHA PROTOCOL ACTIVE.",
        f"{now - timedelta(seconds=100):%Y-%m-%d %H:%M:%S,%f} [INFO] Connection to decentralized ledger: STABLE.",
        f"{now - timedelta(seconds=90):%Y-%m-%d %H:%M:%S,%f} [INFO] Monitoring real-time liquidity pools...",
        f"{now - timedelta(seconds=80):%Y-%m-%d %H:%M:%S,%f} [WARNING] High cognitive load detected in Risk-Scanner module.",
        f"{now - timedelta(seconds=70):%Y-%m-%d %H:%M:%S,%f} [INFO] Auto-balancing neuro-cores... Optimization successful.",
        f"{now - timedelta(seconds=60):%Y-%m-%d %H:%M:%S,%f} [INFO] Fraud-Shield: No anomalies detected in past 10,000 packets.",
        f"{now - timedelta(seconds=45):%Y-%m-%d %H:%M:%S,%f} [INFO] AI Brain: Llama-3.1-8b-instant ready for sequences.",
        f"{now - timedelta(seconds=30):%Y-%m-%d %H:%M:%S,%f} [INFO] System Status: OPTIMAL.",
        f"{now - timedelta(seconds=15):%Y-%m-%d %H:%M:%S,%f} [INFO] Waiting for user command input...",
        f"{now:%Y-%m-%d %H:%M:%S,%f} [INFO] Heartbeat pulse: Synchronized with Vercel Global Edge."
    ]
    return jsonify({"logs": dummy_logs})

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        "status": "online",
        "neuro_core": "v3.2.0-serverless",
        "finacle_sync": "active",
        "uptime": str(datetime.now())
    })

def get_simulated_response(input_text):
    lower = input_text.lower()
    if 'npa' in lower:
        return "Initiating NPA trend visualization. Accessing Finacle endpoint... Current non-performing assets are categorized."
    elif 'health' in lower:
        return "System vitals optimized. All 24 neuro-cores operating at 100% efficiency."
    elif 'fraud' in lower:
        return "Executing fraud risk assessment. Screening real-time transaction packets... No anomalies detected."
    return "I've analyzed your query regarding our financial ecosystem. Please provide a Groq API key to activate full cognitive capabilities."

if __name__ == '__main__':
    app.run(port=5000)
