import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. API Setup
load_dotenv()
genai.configure(api_key="AIzaSyCJxyEbRnrr8UTzoBtum2EwvugIpSvC6do") # Yahan apni key lagayein

# 2. Prompt Engineering (System Instruction)
# Is se bot ko pata chalega ke usne "Medical Assistant" ki tarah behave karna hai
system_prompt = """
Act as a professional, friendly, and helpful Medical Assistant. 
- Provide clear and concise information about general health queries.
- ALWAYS add a disclaimer: 'I am an AI, not a doctor. Please consult a medical professional for serious concerns.'
- If someone asks for dangerous advice or illegal substances, politely refuse.
- Use bullet points for easy reading.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompt
)

# 3. Streamlit UI UI (Design)
st.set_page_config(page_title="HealthCare AI", page_icon="🏥")

st.title("🏥 HealthCare Chatbot")
st.markdown("---")

# Chat history initialize
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani messages dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Logic
if prompt := st.chat_input("Apna sehat se mutalliq sawal poochein..."):
    # User message save karna
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response
    with st.chat_message("assistant"):
        # Hum user ki query ke saath safety context bhi bhej sakte hain
        full_response = model.generate_content(prompt)
        response_text = full_response.text
        
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})