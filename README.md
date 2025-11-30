# Travel Buddy - AI-Powered Travel Itinerary Generator

Travel Buddy is an intelligent web application that generates personalized travel itineraries using Google's Gemini AI. The application features a beautiful, modern UI with multi-step forms, dynamic image generation, and PDF export capabilities.

## Features

### 🎯 Core Features
- **AI-Powered Itinerary Generation**: Uses Google Gemini 2.0 Flash to create detailed, personalized travel plans
- **Multi-Step Form**: Intuitive 4-step form for collecting travel preferences
- **Dynamic Image Collages**: Automatically generates destination-specific image collages
- **Iterative Refinement**: Update and refine itineraries based on user feedback
- **PDF Export**: Download beautifully formatted PDF itineraries with embedded images
- **Responsive Design**: Modern glassmorphism UI with smooth animations

### 📋 Itinerary Customization
The application collects and considers:
- Starting location and destination
- Travel mode (Flight, Train, Car, Bus, Cruise, Taxi)
- Travel dates and duration
- Number of travelers
- Budget level (Budget, Standard, Luxury)
- Travel style (Solo, Couple, Family, Group)
- Food preferences (Vegetarian, Non-Vegetarian, Vegan)
- Personal interests

## Technology Stack

### Backend
- **Framework**: Flask (Python web framework)
- **AI Model**: Google Gemini 2.0 Flash
- **PDF Generation**: FPDF
- **HTTP Client**: Requests (for image downloading)
- **Environment Management**: python-dotenv

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Custom styling with CSS variables, animations, and glassmorphism effects
- **JavaScript**: Vanilla JS with async/await for API calls
- **Markdown Rendering**: marked.js for rich text display
- **Image Generation**: Pollinations.ai API

## Project Structure

```
TravelBuddy/
├── agent/
│   ├── __init__.py
│   ├── coordinator.py          # Orchestrates the application flow
│   ├── data_collector.py       # Handles user data collection
│   ├── itinerary_builder.py    # AI itinerary generation and PDF creation
│   └── communicator.py         # Email communication (mock)
├── static/
│   ├── css/
│   │   └── style.css          # Application styling
│   ├── js/
│   │   └── script.js          # Frontend logic
│   └── itineraries/           # Generated PDF storage
├── templates/
│   └── index.html             # Main application page
├── app.py                     # Flask application entry point
├── .env                       # Environment variables (not in repo)
└── README.md                  # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TravelBuddy
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask google-generativeai fpdf python-dotenv requests
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   
   Open your browser and navigate to: `http://127.0.0.1:5000`

## Usage Guide

### Generating an Itinerary

1. **Fill out the multi-step form**:
   - **Step 1**: Enter starting location, destination, and travel mode
   - **Step 2**: Select travel date, duration, and number of travelers
   - **Step 3**: Choose budget, travel style, and food preferences
   - **Step 4**: Add interests, name, and email

2. **Submit and Generate**:
   - Click "Start Planning" to submit your preferences
   - Click "Generate Itinerary with AI" to create your personalized plan

3. **Review and Refine**:
   - Review the generated itinerary with dynamic images
   - Provide feedback in the text area if changes are needed
   - Click "Update Itinerary" to refine based on your feedback

4. **Download PDF**:
   - Click "Finalize & Download PDF" to generate a downloadable PDF
   - The PDF includes the destination collage and formatted itinerary

### API Endpoints

#### `POST /submit`
Submits travel details for processing.

**Request Body**:
```json
{
  "destination": "Paris",
  "start_location": "New York",
  "travel_mode": "Flight",
  "travel_date": "2024-06-01",
  "duration": "7",
  "travelers_count": "2",
  "budget": "Standard",
  "travel_style": "Couple",
  "food_habits": "Non-Vegetarian",
  "interests": "Food, History, Art",
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Travel details saved successfully!"
}
```

#### `POST /generate_itinerary`
Generates or updates an itinerary using AI.

**Request Body**:
```json
{
  "destination": "Paris",
  // ... other travel details
  "feedback": "Add more food recommendations",  // Optional
  "current_itinerary": "..."  // Optional, for updates
}
```

**Response**:
```json
{
  "status": "success",
  "itinerary_text": "# Your Amazing Paris Adventure\n\n## Day 1..."
}
```

#### `POST /finalize_itinerary`
Creates a PDF from the itinerary.

**Request Body**:
```json
{
  "itinerary_text": "# Your Amazing Paris Adventure...",
  "image_url": "https://image.pollinations.ai/...",
  // ... other user data
}
```

**Response**:
```json
{
  "message": "Itinerary finalized",
  "pdf_url": "/static/itineraries/itinerary_JohnDoe.pdf"
}
```

## Architecture

### Agent-Based Design

The application uses an agent-based architecture with specialized components:

1. **CoordinatorAgent** (`coordinator.py`)
   - Orchestrates the entire workflow
   - Manages communication between agents
   - Handles the main application logic flow

2. **DataCollectionAgent** (`data_collector.py`)
   - Validates and stores user preferences
   - Manages travel detail collection

3. **ItineraryBuilderAgent** (`itinerary_builder.py`)
   - Interfaces with Google Gemini AI
   - Generates personalized itineraries
   - Creates PDF documents with proper formatting
   - Handles Unicode character encoding for PDF compatibility

4. **CommunicatorAgent** (`communicator.py`)
   - Manages email notifications (currently mock implementation)
   - Can be extended for actual email delivery

### Data Flow

```
User Input → DataCollectionAgent → CoordinatorAgent
                                         ↓
                              ItineraryBuilderAgent (Gemini AI)
                                         ↓
                              Markdown Itinerary Text
                                         ↓
                              Frontend (marked.js rendering)
                                         ↓
                              User Feedback (Optional)
                                         ↓
                              ItineraryBuilderAgent (Refinement)
                                         ↓
                              PDF Generation → Download
```

## Styling and UI

### Design System

The application uses a modern design system with:

- **Color Palette**:
  - Primary: `#6366f1` (Indigo)
  - Secondary: `#a855f7` (Purple)
  - Accent: `#ec4899` (Pink)
  - Background: `#0f172a` (Dark Blue)

- **Typography**: 'Outfit' font from Google Fonts

- **Effects**:
  - Glassmorphism with backdrop blur
  - Smooth transitions and animations
  - Gradient backgrounds
  - Hover effects with transforms

### Itinerary Formatting

The generated itinerary features:
- **Color-coded headers**: Different colors for H1, H2, H3, H4
- **Visual separators**: Borders and spacing between day sections
- **Highlighted text**: Golden bold text, purple italics
- **Responsive layout**: Adapts to different screen sizes

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

### Customization

#### Modify AI Prompt
Edit `agent/itinerary_builder.py`, method `_construct_prompt()` to customize the AI's behavior.

#### Change Styling
Edit `static/css/style.css` to modify colors, fonts, and layout.

#### Adjust Form Fields
Edit `templates/index.html` to add/remove form fields.

## Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY not found"**
   - Ensure `.env` file exists in the project root
   - Verify the API key is correctly set

2. **"'latin-1' codec can't encode character"**
   - This is handled automatically by the `_clean_text_for_pdf()` function
   - Unicode characters like ₹ are replaced with ASCII equivalents (Rs.)

3. **PDF not generating**
   - Check that the `static/itineraries/` directory exists
   - Verify write permissions

4. **Images not loading**
   - Check internet connection (images are fetched from Pollinations.ai)
   - Fallback to default `collage.png` if available

## Future Enhancements

- [ ] Actual email integration for sending itineraries
- [ ] User authentication and saved itineraries
- [ ] Multiple language support
- [ ] Integration with booking APIs
- [ ] Weather API integration for real-time forecasts
- [ ] Cost estimation with real-time pricing
- [ ] Social sharing features
- [ ] Mobile app version

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Google Gemini AI for powering the itinerary generation
- Pollinations.ai for dynamic image generation
- marked.js for markdown rendering
- FPDF for PDF generation

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**Built with ❤️ using Flask and Google Gemini AI**
