from flask import Flask, render_template, request, jsonify
from agent.coordinator import CoordinatorAgent
import os

app = Flask(__name__)
coordinator = CoordinatorAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    success, message = coordinator.submit_travel_details(data)
    if success:
        return jsonify({"status": "success", "message": message}), 200
    else:
        return jsonify({"status": "error", "message": message}), 500

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    data = request.json
    feedback = data.get('feedback')
    current_itinerary = data.get('current_itinerary')
    
    itinerary_text = coordinator.generate_itinerary_text(data, feedback, current_itinerary)
    
    if itinerary_text.startswith("Error"):
        return jsonify({"status": "error", "message": itinerary_text}), 500
    else:
        return jsonify({"status": "success", "itinerary_text": itinerary_text}), 200

@app.route('/finalize_itinerary', methods=['POST'])
def finalize_itinerary():
    data = request.json
    itinerary_text = data.get('itinerary_text')
    image_url = data.get('image_url')
    
    if not itinerary_text:
        return jsonify({'message': 'No itinerary text provided'}), 400
        
    try:
        pdf_url = coordinator.finalize_itinerary(data, itinerary_text, image_url)
        return jsonify({'message': 'Itinerary finalized', 'pdf_url': pdf_url})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
