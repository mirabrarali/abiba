import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

# Initialize Environment
load_dotenv()

# Configure Logging
log_filename = "/tmp/abiba.log" if "VERCEL" in os.environ else "abiba.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Optional file logging (safe for Vercel)
try:
    if not os.environ.get('VERCEL'):
        file_handler = logging.FileHandler(log_filename)
        logging.getLogger().addHandler(file_handler)
except Exception:
    pass

logger = logging.getLogger("Abiba")

app = Flask(__name__)
CORS(app)

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
        # Simulation Mode
        response = get_simulated_response(user_message)
        logger.info(f"Abiba (Simulation): {response}")
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
        logger.info(f"Abiba (Live): {ai_response}")
        return jsonify({"response": ai_response, "mode": "live"})
    
    except Exception as e:
        logger.error(f"Error calling Groq API: {str(e)}")
        return jsonify({"error": "Internal synchronization error in Abiba Neuro-Core", "details": str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    try:
        if not os.path.exists(log_filename):
            return jsonify({"logs": ["Log file not found."]})
        
        with open(log_filename, 'r') as f:
            lines = f.readlines()
            # Return last 50 lines
            return jsonify({"logs": [line.strip() for line in lines[-50:]]})
    except Exception as e:
        logger.error(f"Error reading logs: {str(e)}")
        return jsonify({"error": "Sync error"}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    try:
        if os.environ.get('VERCEL'):
            return jsonify({"logs": ["System active on Vercel Node.", f"Time: {datetime.now()}", "AI Brain: Llama-3.1-8b-instant", "Status: Optimized for Serverless Execution"]})
        
        if not os.path.exists(log_filename):
            return jsonify({"logs": ["Log file not found."]})
        
        with open(log_filename, 'r') as f:
            lines = f.readlines()
            return jsonify({"logs": [line.strip() for line in lines[-50:]]})
    except Exception as e:
        logger.error(f"Error reading logs: {str(e)}")
        return jsonify({"error": "Sync error"}), 500

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        "status": "online",
        "neuro_core": "v3.2.0",
        "finacle_sync": "active",
        "uptime": str(datetime.now())
    })

def get_simulated_response(input_text):
    lower = input_text.toLowerCase() if hasattr(input_text, 'toLowerCase') else input_text.lower()
    if 'npa' in lower:
        return "Initiating NPA trend visualization. Accessing Finacle endpoint... Current non-performing assets are categorized. I recommend a tactical review of the Q3 asset distribution to mitigate risk."
    elif 'health' in lower:
        return "System vitals optimized. All 24 neuro-cores operating at 100% efficiency. Security perimeter is healthy. Connection to Infosys Finacle suite is stable."
    elif 'fraud' in lower:
        return "Executing fraud risk assessment. Screening real-time transaction packets... No anomalies detected. Probability of compromise is currently 0.001%."
    return "I've analyzed your query regarding our financial ecosystem. My neural-connectors are ready to bridge with your local banking database to execute this sequence. Please provide a Groq API key to activate full cognitive capabilities."

if __name__ == '__main__':
    logger.info("Abiba Backend Terminal Starting...")
    app.run(port=5000, debug=True)
