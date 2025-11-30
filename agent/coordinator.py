from agent.data_collector import DataCollectionAgent
from agent.itinerary_builder import ItineraryBuilderAgent
from agent.communicator import CommunicatorAgent
from datetime import datetime
import os

class CoordinatorAgent:
    def __init__(self):
        self.data_collector = DataCollectionAgent()
        self.itinerary_builder = ItineraryBuilderAgent()
        self.communicator = CommunicatorAgent()

    def submit_travel_details(self, data):
        """
        Orchestrates the data collection step.
        """
        print("[Coordinator] Receiving travel details...")
        return self.data_collector.save_preferences(data)

    def generate_itinerary_text(self, data, feedback=None, current_itinerary=None):
        """
        Generates the itinerary text (preview).
        """
        print("[Coordinator] Generating itinerary text...")
        return self.itinerary_builder.generate_itinerary(data, feedback, current_itinerary)

    def finalize_itinerary(self, data, itinerary_text, image_url=None):
        """
        Finalizes the itinerary by creating a PDF and sending it via email.
        """
        print("[Coordinator] Finalizing itinerary...")
        
        # Create PDF
        pdf_path = self.itinerary_builder.create_pdf(data, itinerary_text, image_url)
        
        # Send Email (Mock)
        # self.communicator.send_email(data.get('email'), "Your Travel Itinerary", "Here is your itinerary!", pdf_path)
        
        return f"/static/itineraries/{os.path.basename(pdf_path)}"

    def create_itinerary(self, data):
        """
        DEPRECATED: Use generate_itinerary_text and finalize_itinerary instead.
        Kept for backward compatibility if needed, but logic is split now.
        """
        print("[Coordinator] Requesting itinerary generation (Legacy)...")
        
        # 1. Generate Itinerary Text
        itinerary_text = self.generate_itinerary_text(data)
        
        if itinerary_text.startswith("Error"):
            return {"status": "error", "message": itinerary_text}
            
        # 2. Finalize
        return self.finalize_itinerary(data, itinerary_text)
