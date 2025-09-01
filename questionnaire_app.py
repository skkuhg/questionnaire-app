import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="Interactive Questionnaire",
    page_icon="📋",
    layout="wide"
)

# Define the questions pool
QUESTIONS_POOL = {
    "multiple_choice": [
        {
            "question": "What is your age group?",
            "options": ["18-25", "26-35", "36-45", "46-55", "56+"],
            "key": "age_group"
        },
        {
            "question": "What is your highest level of education?",
            "options": ["High School", "Bachelor's Degree", "Master's Degree", "PhD", "Other"],
            "key": "education"
        },
        {
            "question": "How often do you use technology in your daily life?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"],
            "key": "tech_usage"
        },
        {
            "question": "What is your preferred mode of transportation?",
            "options": ["Car", "Public Transport", "Bicycle", "Walking", "Other"],
            "key": "transportation"
        },
        {
            "question": "How would you rate your overall job satisfaction?",
            "options": ["Very Dissatisfied", "Dissatisfied", "Neutral", "Satisfied", "Very Satisfied"],
            "key": "job_satisfaction"
        }
    ],
    "open_ended": [
        {
            "question": "What motivates you most in your work or studies?",
            "key": "motivation"
        },
        {
            "question": "Describe your ideal weekend activity.",
            "key": "weekend_activity"
        },
        {
            "question": "What is the biggest challenge you face in your daily life?",
            "key": "daily_challenge"
        },
        {
            "question": "If you could learn any new skill, what would it be and why?",
            "key": "new_skill"
        },
        {
            "question": "What change would you like to see in your community?",
            "key": "community_change"
        }
    ]
}

def initialize_session_state():
    """Initialize session state variables"""
    if 'questionnaire_submitted' not in st.session_state:
        st.session_state.questionnaire_submitted = False
    if 'current_questions' not in st.session_state:
        st.session_state.current_questions = None
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    if 'participant_id' not in st.session_state:
        st.session_state.participant_id = None

def randomize_questions(num_mc=3, num_oe=2):
    """Randomize and select questions from the pool"""
    mc_questions = random.sample(QUESTIONS_POOL["multiple_choice"], min(num_mc, len(QUESTIONS_POOL["multiple_choice"])))
    oe_questions = random.sample(QUESTIONS_POOL["open_ended"], min(num_oe, len(QUESTIONS_POOL["open_ended"])))
    
    all_questions = mc_questions + oe_questions
    random.shuffle(all_questions)
    
    return all_questions

def validate_responses(questions, responses):
    """Validate that all required questions are answered"""
    errors = []
    
    for q in questions:
        key = q['key']
        if key not in responses or not responses[key]:
            errors.append(f"Please answer: {q['question']}")
        elif 'options' in q and responses[key] not in q['options']:
            errors.append(f"Invalid selection for: {q['question']}")
    
    return errors

def save_responses_to_csv(responses, participant_id):
    """Save responses to CSV file"""
    filename = "questionnaire_responses.csv"
    
    # Prepare data for CSV
    data = {
        'Participant_ID': participant_id,
        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **responses
    }
    
    # Convert to DataFrame
    df = pd.DataFrame([data])
    
    # Check if file exists and append or create
    if os.path.exists(filename):
        existing_df = pd.read_csv(filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_csv(filename, index=False)
    return filename

def save_responses_to_excel(responses, participant_id):
    """Save responses to Excel file"""
    filename = "questionnaire_responses.xlsx"
    
    # Prepare data for Excel
    data = {
        'Participant_ID': participant_id,
        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **responses
    }
    
    # Convert to DataFrame
    df = pd.DataFrame([data])
    
    # Check if file exists and append or create
    if os.path.exists(filename):
        existing_df = pd.read_excel(filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_excel(filename, index=False)
    return filename

def simulate_participants(num_participants=100):
    """Simulate responses from multiple participants"""
    simulated_data = []
    
    for i in range(1, num_participants + 1):
        participant_responses = {}
        
        # Generate random responses for multiple choice questions
        for q in QUESTIONS_POOL["multiple_choice"]:
            participant_responses[q['key']] = random.choice(q['options'])
        
        # Generate random responses for open-ended questions
        sample_open_responses = {
            "motivation": ["Career growth", "Learning new things", "Helping others", "Financial stability", "Creative expression"],
            "weekend_activity": ["Reading books", "Hiking outdoors", "Spending time with family", "Watching movies", "Playing sports"],
            "daily_challenge": ["Time management", "Work-life balance", "Financial concerns", "Health issues", "Communication"],
            "new_skill": ["Programming", "Public speaking", "Foreign language", "Musical instrument", "Cooking"],
            "community_change": ["Better public transport", "More green spaces", "Improved education", "Reduced crime", "Environmental awareness"]
        }
        
        for q in QUESTIONS_POOL["open_ended"]:
            key = q['key']
            if key in sample_open_responses:
                participant_responses[key] = random.choice(sample_open_responses[key])
        
        data = {
            'Participant_ID': f"SIM_{i:03d}",
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **participant_responses
        }
        
        simulated_data.append(data)
    
    # Save simulated data
    df = pd.DataFrame(simulated_data)
    
    # Save to CSV
    csv_filename = "simulated_responses.csv"
    df.to_csv(csv_filename, index=False)
    
    # Save to Excel
    excel_filename = "simulated_responses.xlsx"
    df.to_excel(excel_filename, index=False)
    
    return df, csv_filename, excel_filename

def main():
    initialize_session_state()
    
    st.title("📋 Interactive Questionnaire")
    st.markdown("---")
    
    # Sidebar for controls
    st.sidebar.title("Questionnaire Controls")
    
    # Randomize questions button
    if st.sidebar.button("🎲 Randomize Questions"):
        st.session_state.current_questions = randomize_questions()
        st.session_state.questionnaire_submitted = False
        st.session_state.responses = {}
        st.session_state.participant_id = f"P_{random.randint(1000, 9999)}"
        st.rerun()
    
    # Simulate participants button
    if st.sidebar.button("👥 Simulate 100 Participants"):
        with st.spinner("Simulating participant responses..."):
            sim_df, csv_file, excel_file = simulate_participants()
        
        st.sidebar.success(f"✅ Simulated {len(sim_df)} participants!")
        st.sidebar.download_button(
            label="📁 Download Simulated CSV",
            data=open(csv_file, 'rb').read(),
            file_name=csv_file,
            mime='text/csv'
        )
        st.sidebar.download_button(
            label="📊 Download Simulated Excel",
            data=open(excel_file, 'rb').read(),
            file_name=excel_file,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    # Initialize questions if not done
    if st.session_state.current_questions is None:
        st.session_state.current_questions = randomize_questions()
        st.session_state.participant_id = f"P_{random.randint(1000, 9999)}"
    
    if not st.session_state.questionnaire_submitted:
        # Display questionnaire
        st.header("Please answer the following questions:")
        st.info(f"Participant ID: {st.session_state.participant_id}")
        
        responses = {}
        
        # Display questions
        for i, question_data in enumerate(st.session_state.current_questions, 1):
            st.subheader(f"Question {i}")
            
            if 'options' in question_data:  # Multiple choice
                response = st.radio(
                    question_data['question'],
                    question_data['options'],
                    key=f"q_{question_data['key']}",
                    index=None
                )
                if response:
                    responses[question_data['key']] = response
            else:  # Open-ended
                response = st.text_area(
                    question_data['question'],
                    key=f"q_{question_data['key']}",
                    height=100
                )
                if response.strip():
                    responses[question_data['key']] = response.strip()
        
        # Submit button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📤 Submit Questionnaire", type="primary", use_container_width=True):
                # Validate responses
                errors = validate_responses(st.session_state.current_questions, responses)
                
                if errors:
                    st.error("Please complete all questions:")
                    for error in errors:
                        st.error(f"• {error}")
                else:
                    # Save responses
                    st.session_state.responses = responses
                    
                    # Save to files
                    csv_file = save_responses_to_csv(responses, st.session_state.participant_id)
                    excel_file = save_responses_to_excel(responses, st.session_state.participant_id)
                    
                    st.session_state.questionnaire_submitted = True
                    st.rerun()
    
    else:
        # Display results
        st.success("🎉 Thank you for completing the questionnaire!")
        st.header("Your Responses:")
        
        # Display responses in a nice format
        for question_data in st.session_state.current_questions:
            key = question_data['key']
            if key in st.session_state.responses:
                st.subheader(question_data['question'])
                st.write(f"**Your answer:** {st.session_state.responses[key]}")
                st.markdown("---")
        
        # Download options
        st.header("📁 Download Your Responses")
        col1, col2 = st.columns(2)
        
        with col1:
            if os.path.exists("questionnaire_responses.csv"):
                with open("questionnaire_responses.csv", 'rb') as file:
                    st.download_button(
                        label="📄 Download CSV",
                        data=file.read(),
                        file_name="questionnaire_responses.csv",
                        mime='text/csv',
                        use_container_width=True
                    )
        
        with col2:
            if os.path.exists("questionnaire_responses.xlsx"):
                with open("questionnaire_responses.xlsx", 'rb') as file:
                    st.download_button(
                        label="📊 Download Excel",
                        data=file.read(),
                        file_name="questionnaire_responses.xlsx",
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        use_container_width=True
                    )
        
        # Start new questionnaire button
        if st.button("🔄 Start New Questionnaire", type="secondary", use_container_width=True):
            st.session_state.questionnaire_submitted = False
            st.session_state.responses = {}
            st.session_state.current_questions = randomize_questions()
            st.session_state.participant_id = f"P_{random.randint(1000, 9999)}"
            st.rerun()

if __name__ == "__main__":
    main()