class CommunicatorAgent:
    def __init__(self):
        pass

    def send_itinerary(self, email, pdf_path):
        """
        Simulates sending the itinerary PDF to the user's email.
        """
        print(f"[Communicator] 📧 Sending itinerary to {email}...")
        print(f"[Communicator] 📎 Attaching file: {pdf_path}")
        
        # Simulate processing time
        import time
        time.sleep(1)
        
        print(f"[Communicator] ✅ Email sent successfully!")
        return True, "Email sent successfully."
