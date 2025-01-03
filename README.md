# Ahmed-AI-Interviewer
# TalentScout Technical Interview Assistant

## Overview
An AI-powered technical interview assistant built with Streamlit and Groq API. Automates the technical interview process while maintaining a professional and engaging conversation flow.

## Features
- 🤖 AI-driven interview process
- 📝 Structured conversation flow
- ✅ Input validation for email and phone
- 💾 Interview data storage
- 📊 Technical assessment generation
- 🔄 Dynamic conversation state management

## Prerequisites
- Python 3.8+
- Groq API key
- Windows/Linux/MacOS

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/Ahmedfurkhan/Ahmed-AI-Interviewer.git
cd Ahmed-AI-Interviewer
```

2. **Set up virtual environment**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
5. **Configure environment variables Create a .env file in the project root:**
   ```bash
   GROQ_API_KEY=your_api_key_here
   ```

## Usage
1. **Start the application**
   ```bash
   streamlit run app.py
   ```
2. **Access the interface Open your browser and navigate to: http://localhost:8501**
   Project Structure
   ```bash
   talentscout-assistant/
    ├── app.py              # Main application file
    ├── .env               # Environment variables
    ├── requirements.txt   # Project dependencies
    └── README.md         # Documentation
   ```
# Interview Flow

## Initial Greeting
- Welcome the candidate and provide an overview of the interview process.

## Collect Personal Information
1. **Name**
2. **Email**
   - Validation: Standard email format.
3. **Phone**
   - Validation: International format support (9-15 digits).

## Professional Background
1. **Experience**
   - Discuss previous roles and responsibilities.
2. **Desired Position**
   - Understand the role the candidate is applying for.
3. **Technical Skills**
   - Evaluate proficiency in relevant tools, technologies, and methodologies.

## Technical Assessment
- Conduct a skills-based assessment based on the candidate's expertise and the position requirements.

## Conclusion
- Provide feedback (if applicable).
- Outline the next steps in the interview process.

---

# Configuration Options

## Model Settings
- **Model**: `llama-3.3-70b-versatile`
- **Temperature**: `0.7`
- **Max Tokens**: `1000`

## Validation Rules
- **Email**: Must conform to a standard email format.
- **Phone**: Must support international formats with 9-15 digits.

---

# Contributing

1. **Fork the Repository**
2. **Create a Feature Branch**
3. **Commit Changes**
4. **Push to the Branch**
5. **Create a Pull Request**

---

# License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

# Support
For support, please open an issue in the [GitHub repository](https://github.com/Ahmedfurkhan/Ahmed-AI-Interviewer.git).
