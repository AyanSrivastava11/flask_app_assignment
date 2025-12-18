import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file for local testing
load_dotenv()

app = Flask(__name__)

# --- MONGODB CONFIGURATION ---
# Part 2 Requirement: MongoDB Authentication and DNS Resolution
# These variables will be injected by Kubernetes Secrets/ConfigMaps
MONGO_USER = os.environ.get("MONGO_USER", "admin")
MONGO_PASS = os.environ.get("MONGO_PASS", "password")
# DNS Resolution: 'mongodb-service' is the name of your Kubernetes Service
MONGO_HOST = os.environ.get("MONGO_HOST", "mongodb-service") 

# Check if a full URI is provided (like for Atlas), otherwise build one from components
MONGODB_URI = os.environ.get("MONGODB_URI")

if not MONGODB_URI:
    # Building the URI with authentication for Kubernetes
    # authSource=admin is standard for MongoDB authenticated setups
    MONGODB_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:27017/flask_db?authSource=admin"

# Initialize MongoDB Client
client = MongoClient(MONGODB_URI)
db = client.flask_db
collection = db.data

# --- ROUTES ---

@app.route('/')
def index():
    """Returns a welcome message with the current date and time."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Welcome to the Flask app! The current time is: {current_time}"

@app.route('/data', methods=['GET', 'POST'])
def data_handler():
    """Handles POST to insert data and GET to retrieve data from MongoDB."""
    if request.method == 'POST':
        try:
            # Get JSON data from the request
            json_data = request.get_json()
            if not json_data:
                return jsonify({"error": "Invalid JSON"}), 400
                
            # Insert into MongoDB
            collection.insert_one(json_data)
            return jsonify({"status": "Data inserted"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'GET':
        try:
            # Retrieve all documents, excluding the MongoDB internal '_id'
            data_list = list(collection.find({}, {"_id": 0}))
            return jsonify(data_list), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# --- RUN APP ---
if __name__ == '__main__':
    # Listen on 0.0.0.0 is required for Docker/Kubernetes access
    app.run(host='0.0.0.0', port=5000)
