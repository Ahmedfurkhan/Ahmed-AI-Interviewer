from dotenv import load_dotenv
import os
import streamlit as st
from groq import Groq
from datetime import datetime
from typing import List, Dict
import re
import json

load_dotenv()  # Load environment variables from .env file

class TalentScoutAssistant:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        self.conversation_states = [
            "initial_greeting",
            "collect_name",
            "collect_email",
            "collect_phone",
            "collect_experience",
            "collect_position",
            "collect_tech_stack",
            "technical_assessment",
            "conclusion"
        ]
        self.current_state_index = 0
        self.candidate_data = {}
        self.conversation_history = []

    def get_system_prompt(self) -> str:
        return """You are TalentScout's AI hiring assistant, designed to professionally evaluate technical candidates. 
        Your communication style is clear, friendly, and professional. Focus on one question at a time and maintain 
        conversation context. Evaluate responses thoughtfully and generate relevant technical questions based on 
        candidates' expertise. If you detect conversation-ending phrases like 'goodbye', 'exit', or 'quit', 
        conclude the conversation professionally."""

    def validate_email(self, email: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

    def validate_phone(self, phone: str) -> bool:
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone))

    def generate_response(self, user_input: str = None) -> str:
        messages = [{"role": "system", "content": self.get_system_prompt()}]
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        if user_input:
            messages.append({"role": "user", "content": user_input})

        # Generate appropriate prompt based on current state
        if self.current_state_index < len(self.conversation_states):
            current_state = self.conversation_states[self.current_state_index]
            
            if current_state == "initial_greeting":
                prompt = "Greet the candidate and ask for their name."
            elif current_state == "collect_name":
                self.candidate_data["name"] = user_input
                prompt = "Ask for the candidate's email address."
            elif current_state == "collect_email":
                if not self.validate_email(user_input):
                    return "I apologize, but that doesn't appear to be a valid email address. Could you please provide a valid email?"
                self.candidate_data["email"] = user_input
                prompt = "Ask for the candidate's phone number."
            elif current_state == "collect_phone":
                if not self.validate_phone(user_input):
                    return "I apologize, but that doesn't appear to be a valid phone number. Please provide a valid phone number."
                self.candidate_data["phone"] = user_input
                prompt = "Ask about the candidate's years of experience in technology."
            elif current_state == "collect_experience":
                self.candidate_data["experience"] = user_input
                prompt = "Ask about the candidate's desired position."
            elif current_state == "collect_position":
                self.candidate_data["position"] = user_input
                prompt = "Ask the candidate to list their technical skills, frameworks, and tools they're proficient in."
            elif current_state == "collect_tech_stack":
                self.candidate_data["tech_stack"] = user_input
                prompt = f"""Generate 3-5 technical questions based on the candidate's tech stack: {user_input}. 
                Focus on practical scenarios and problem-solving abilities. Make the questions challenging but fair."""
            elif current_state == "technical_assessment":
                prompt = "Analyze the candidate's response and provide relevant follow-up questions or conclude the interview."
            else:
                prompt = "Thank the candidate and explain the next steps in the hiring process."

            messages.append({"role": "user", "content": prompt})

            try:
                chat_completion = self.client.chat.completions.create(
                    messages=messages,
                    model=self.model,
                    temperature=0.7,
                    max_tokens=1000
                )
                
                response = chat_completion.choices[0].message.content
                
                # Update conversation history
                if user_input:
                    self.conversation_history.append({"role": "user", "content": user_input})
                self.conversation_history.append({"role": "assistant", "content": response})
                
                # Move to next state if current response is valid
                if current_state != "technical_assessment" or "thank you" in response.lower():
                    self.current_state_index += 1
                
                return response
                
            except Exception as e:
                return f"I apologize, but I encountered an error. Please try again. Error: {str(e)}"
        
        return "Thank you for completing the interview process. We will be in touch soon!"

def create_streamlit_interface():
    st.set_page_config(page_title="Ahmed TalentScout Technical Interview", page_icon="💼")
    st.title("TalentScout Technical Interview Assistant")
    
    # Initialize session state
    if 'assistant' not in st.session_state:
        st.session_state.assistant = TalentScoutAssistant()
        st.session_state.messages = []
        
        # Generate initial greeting
        initial_response = st.session_state.assistant.generate_response()
        st.session_state.messages.append({"role": "assistant", "content": initial_response})

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Handle user input
    if user_input := st.chat_input("Your response"):
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate and display assistant response
        assistant_response = st.session_state.assistant.generate_response(user_input)
        with st.chat_message("assistant"):
            st.write(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
        # Save interview data if complete
        if st.session_state.assistant.current_state_index >= len(st.session_state.assistant.conversation_states):
            interview_data = {
                "timestamp": datetime.now().isoformat(),
                "candidate_data": st.session_state.assistant.candidate_data,
                "conversation": st.session_state.messages
            }
            st.sidebar.json(interview_data)

if __name__ == "__main__":
    create_streamlit_interface()