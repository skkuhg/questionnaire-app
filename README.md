# Interactive Questionnaire App

A Python Streamlit application that simulates an interactive questionnaire with randomized questions, validation, and data export capabilities.

## Features

- **5+ Questions**: Mix of multiple-choice and open-ended questions
- **Question Randomization**: Questions are randomized for each session
- **Input Validation**: Ensures all questions are answered before submission
- **Response Display**: Shows all responses clearly after submission
- **CSV/Excel Export**: Saves responses to both CSV and Excel formats
- **100 Participant Simulation**: Generate simulated responses for testing
- **Unique Participant IDs**: Each session gets a unique participant identifier

## Installation

1. Install Python 3.7 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run questionnaire_app.py
   ```

2. The app will open in your default web browser at `http://localhost:8501`

## Application Features

### Main Interface
- Answer 5 randomized questions (3 multiple-choice, 2 open-ended)
- Submit button validates all responses before acceptance
- View all responses after submission
- Download responses as CSV or Excel files

### Sidebar Controls
- **Randomize Questions**: Get a new set of randomized questions
- **Simulate 100 Participants**: Generate and download simulated participant data

### Question Types
- **Multiple Choice**: Age group, education level, technology usage, transportation preference, job satisfaction
- **Open-ended**: Work motivation, weekend activities, daily challenges, skill learning, community improvements

### Data Export
- Responses are automatically saved to:
  - `questionnaire_responses.csv`
  - `questionnaire_responses.xlsx`
- Simulated data saved to:
  - `simulated_responses.csv`
  - `simulated_responses.xlsx`

## File Structure
```
├── questionnaire_app.py    # Main application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── questionnaire_responses.csv     # Generated responses
├── questionnaire_responses.xlsx    # Generated responses
├── simulated_responses.csv         # Simulated data
└── simulated_responses.xlsx        # Simulated data
```

## Data Format

Each response includes:
- Participant_ID: Unique identifier (format: P_XXXX or SIM_XXX)
- Timestamp: When the response was submitted
- Individual question responses with appropriate column names

## Validation

The application includes comprehensive validation:
- All questions must be answered
- Multiple-choice responses must match available options
- Error messages guide users to complete missing questions