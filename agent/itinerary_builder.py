import os
import google.generativeai as genai
from fpdf import FPDF
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

class ItineraryBuilderAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("Warning: GEMINI_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_itinerary(self, preferences, feedback=None, current_itinerary=None):
        """
        Generates a travel itinerary using Gemini based on user preferences.
        If feedback is provided, it refines the current itinerary.
        """
        if not self.api_key:
            return "Error: Gemini API Key is missing. Please configure it in .env file."

        prompt = self._construct_prompt(preferences, feedback, current_itinerary)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating itinerary: {str(e)}"

    def _construct_prompt(self, data, feedback=None, current_itinerary=None):
        base_prompt = f"""
        Act as an expert travel agent. Create a detailed day-by-day itinerary for a trip for {data.get('name', 'Traveler')} with the following details:
        
        Destination: {data.get('destination')}
        Start Location: {data.get('start_location')}
        Travel Mode: {data.get('travel_mode')}
        Dates: {data.get('travel_date')}
        Duration: {data.get('duration')} days
        Travelers: {data.get('travelers_count')}
        Budget: {data.get('budget')}
        Travel Style: {data.get('travel_style')}
        Food Habits: {data.get('food_habits')}
        Interests: {data.get('interests')}
        
        Please format the output clearly in markdown format:
        - A catchy title for the trip.
        - A short description or some historical background of the destination.
        - Day 1, Day 2, etc. headers.
        - Use bullet points for activities.
        - Morning, Afternoon, Evening activities for each day.
        - For each major attraction, include a brief description. highlighting text in bold and italics. 
        - Recommended restaurants or food spots (based on food habits).
        - include expected weather condition for each day
        - Estimated daily costs in Indian rupees (optional but helpful).
        
        Keep the tone exciting and personalized to the travel style.
        """

        if feedback and current_itinerary:
            return f"""
            You previously generated this itinerary:
            {current_itinerary}

            The user has provided the following feedback to improve it:
            "{feedback}"

            Please rewrite the itinerary incorporating this feedback while keeping the rest of the details consistent with the original request where appropriate.
            Maintain the same markdown format.
            """
        
        return base_prompt

    def _clean_text_for_pdf(self, text):
        """
        Clean text to remove characters not supported by FPDF (Latin-1 encoding).
        Replace common Unicode characters with ASCII equivalents.
        """
        replacements = {
            '\u20b9': 'Rs.',  # Indian Rupee symbol
            '\u20ac': 'EUR',  # Euro symbol
            '\u00a3': 'GBP',  # Pound symbol
            '\u00a5': 'YEN',  # Yen symbol
            '\u2018': "'",    # Left single quote
            '\u2019': "'",    # Right single quote
            '\u201c': '"',    # Left double quote
            '\u201d': '"',    # Right double quote
            '\u2013': '-',    # En dash
            '\u2014': '--',   # Em dash
            '\u2022': '*',    # Bullet point
            '\u2026': '...',  # Ellipsis
        }
        
        for unicode_char, replacement in replacements.items():
            text = text.replace(unicode_char, replacement)
        
        # Remove any remaining non-Latin-1 characters
        try:
            text.encode('latin-1')
        except UnicodeEncodeError:
            # If there are still problematic characters, replace them
            text = text.encode('latin-1', errors='replace').decode('latin-1')
        
        return text

    def create_pdf(self, user_data, itinerary_text, image_url=None):
        pdf = FPDF()
        pdf.add_page()
        
        # Clean the itinerary text for PDF
        itinerary_text = self._clean_text_for_pdf(itinerary_text)
        
        # Add Collage Image
        if image_url:
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open("temp_collage.png", "wb") as f:
                        f.write(response.content)
                    pdf.image("temp_collage.png", x=10, y=10, w=190)
                    pdf.ln(100) # Move cursor down
                    os.remove("temp_collage.png")
                else:
                    # Fallback if download fails
                    if os.path.exists("collage.png"):
                        pdf.image("collage.png", x=10, y=10, w=190)
                        pdf.ln(120)
            except Exception as e:
                print(f"Error downloading image: {e}")
                # Fallback
                if os.path.exists("collage.png"):
                    pdf.image("collage.png", x=10, y=10, w=190)
                    pdf.ln(120)
        elif os.path.exists("collage.png"):
            pdf.image("collage.png", x=10, y=10, w=190)
            pdf.ln(120)
            
        pdf.set_font("Arial", size=12)
        
        # Title
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, txt=f"Travel Itinerary for {user_data.get('destination', 'Your Trip')}", ln=True, align='C')
        pdf.ln(10)
        
        # Content Parsing (Simple Markdown)
        pdf.set_font("Arial", size=12)
        
        for line in itinerary_text.split('\n'):
            line = line.strip()
            if not line:
                pdf.ln(5)
                continue
                
            if line.startswith('# '):
                pdf.set_font("Arial", style="B", size=16)
                pdf.set_text_color(99, 102, 241) # Primary Color
                pdf.cell(0, 10, txt=line[2:], ln=True)
                pdf.set_text_color(0, 0, 0)
            elif line.startswith('## '):
                pdf.set_font("Arial", style="B", size=14)
                pdf.set_text_color(168, 85, 247) # Secondary Color
                pdf.cell(0, 10, txt=line[3:], ln=True)
                pdf.set_text_color(0, 0, 0)
            elif line.startswith('### '):
                pdf.set_font("Arial", style="B", size=12)
                pdf.cell(0, 10, txt=line[4:], ln=True)
            elif line.startswith('- ') or line.startswith('* '):
                pdf.set_font("Arial", size=12)
                pdf.cell(10) # Indent
                pdf.multi_cell(0, 8, txt=f"\u2022 {line[2:]}")
            elif line.startswith('**') and line.endswith('**'):
                 pdf.set_font("Arial", style="B", size=12)
                 pdf.multi_cell(0, 8, txt=line.replace('**', ''))
            else:
                pdf.set_font("Arial", size=12)
                # Handle bolding within lines (simple approximation)
                clean_line = line.replace('**', '')
                pdf.multi_cell(0, 8, txt=clean_line)
                
        output_path = os.path.join("static", "itineraries", f"itinerary_{user_data.get('name', 'traveler')}.pdf")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        pdf.output(output_path)
        return output_path
