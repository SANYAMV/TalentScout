import streamlit as st
import openai
import os
import random
from dotenv import load_dotenv 

# Load environment variables from .env file
load_dotenv()  # Call load_dotenv to load variables

Set up OpenAI and Streamlit

# Replace with your own or environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    st.error("OpenAI API key not found. Please set the 'OPENAI_API_KEY' environment variable.")
    st.stop()

st.set_page_config(page_title="TalentScout Hiring Chatbot", page_icon="🤖")

def get_gpt_response(messages):
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.6,
            max_tokens=300
        )
        content = response["choices"][0]["message"]["content"].strip()
 
        return content
    except Exception as e:
        return f"[Error calling OpenAI API: {e}]"

def generate_single_tech_question(tech):
    """
    Generate a single technical question about the given technology using GPT.
    """
    tech_lang = random.choice(tech)
    st.session_state.current_tech = tech_lang
    prompt = (
        f"You are a virtual hiring assistant specializing in technology recruitment. Generate a single, precise question to evaluate a candidate's fundamental to intermediate skills in {tech}. Ensure the question is specific, relevant to practical applications, and concise (one sentence)."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Act as a technical hiring assistant. Your sole task is to generate concise and relevant technical questions that assess candidates' skills in their specified technologies. Maintain focus and do not deviate from the objective of technical evaluation."
},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=100
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[Error generating question for {tech_lang}: {e}]"

def main():
    st.title("🤖 TalentScout Hiring Chatbot")
    st.write("""
    Hello! I'm TalentScout, your virtual hiring assistant. 
    I'll ask you up to 5 total questions based on your tech stack.
    You can type "STOP" at any time to end.
    """)
    if "user_info_submitted" not in st.session_state:
        st.session_state.user_info_submitted = False
    
    if "candidate_data" not in st.session_state:
        st.session_state.candidate_data = {
            "full_name": "",
            "email": "",
            "phone": "",
            "years_exp": "",
            "desired_position": "",
            "location": "",
            "tech_stack": []
        }

    # We'll track total number of questions asked
    if "current_tech" not in st.session_state:
        st.session_state.current_tech = 0

    # We'll track total number of questions asked
    if "questions_asked" not in st.session_state:
        st.session_state.questions_asked = 0

    # A queue of technologies to ask about
    if "tech_queue" not in st.session_state:
        st.session_state.tech_queue = []

    # The current question text
    if "current_question" not in st.session_state:
        st.session_state.current_question = ""

    # We track if we are currently on a "follow-up" question
    if "isfollowup" not in st.session_state:
        st.session_state.isfollowup = 0

    # We track if the conversation is ended
    if "chat_ended" not in st.session_state:
        st.session_state.chat_ended = False

    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = [
            {
                "role": "system",
                "content": (
                    "You are TalentScout, a professional virtual hiring assistant for technical recruitment. Your tasks include gathering candidate information, generating tech-stack-specific questions, and assessing responses concisely. Maintain professionalism, stay strictly within the hiring context, and gracefully handle conversation-ending commands like 'STOP.' Limit follow-ups to one per question and provide no external hints or guidance."
                )
            }
        ]

    # Step 1: Collect User Info
   
    if not st.session_state.user_info_submitted and not st.session_state.chat_ended:

        st.subheader("Step 1: Provide Your Information")
        with st.form("user_info_form"):
            st.session_state.candidate_data["full_name"] = st.text_input("Full Name:")
            st.session_state.candidate_data["email"] = st.text_input("Email:")
            st.session_state.candidate_data["phone"] = st.text_input("Phone Number:")
            st.session_state.candidate_data["years_exp"] = st.text_input("Years of Experience:")
            st.session_state.candidate_data["desired_position"] = st.text_input("Desired Position(s):")
            st.session_state.candidate_data["location"] = st.text_input("Current Location:")
            raw_tech = st.text_input("Tech Stack (comma-separated):")

            submitted = st.form_submit_button("Submit Info")
            if submitted:
                # Validate
                required = [
                    st.session_state.candidate_data["full_name"],
                    st.session_state.candidate_data["email"],
                    st.session_state.candidate_data["phone"],
                    st.session_state.candidate_data["years_exp"],
                    st.session_state.candidate_data["desired_position"],
                    st.session_state.candidate_data["location"],
                ]
                if all(field.strip() for field in required):
                    tech_list = [t.strip() for t in raw_tech.split(",") if t.strip()]
                    st.session_state.candidate_data["tech_stack"] = tech_list
                    st.session_state.user_info_submitted = True
                    # Shuffle the tech queue
                    st.session_state.tech_queue = tech_list[:]
                    random.shuffle(st.session_state.tech_queue)
                    st.success("Your information is recorded. Let's begin the Q&A!")
                else:
                    st.warning("Please fill out all required fields.")
        return
    if st.session_state.chat_ended:
        #Chat ended
        st.write("The conversation has ended. Thank you!")
        return

    # Step 2: Q&A

    st.subheader("Q&A Session")
    st.write("When you click the submit button, a new question will appear on your screen and you will recieve a feedback for you previous response below")
    num_ques = random.choice([3,4,5])
    if st.session_state.questions_asked >= num_ques:
        st.write("We've completed our session. Our team will get back to you soon. Thank you for your time!")
        st.session_state.chat_ended = True
        return
    if not st.session_state.current_question:
        #Generating the first question
        if st.session_state.tech_queue:
            random.shuffle(st.session_state.tech_queue)
            st.session_state.current_question = generate_single_tech_question(st.session_state.tech_queue)
    if st.session_state.isfollowup == 0: 
        #A question from new topic
        st.session_state.current_question = generate_single_tech_question(st.session_state.tech_queue)    
        st.markdown(f"**TalentScout**: {st.session_state.current_question}")
    else :
        # If the chatbot is to ask a followup question
        st.session_state.current_question = generate_single_tech_question(list(st.session_state.current_tech))
        st.markdown(f"**TalentScout**: Now I will ask a question based on our previous conversation, {st.session_state.current_question}")
    user_answer = st.text_input("Your answer:", key="user_answer_widget", value="")
    if user_answer.lower() == "stop":
        #User requested to stop the session
        st.session_state.chat_ended = True
        st.rerun()
    if st.button("Send"):
        if not user_answer.strip():
            st.warning("Please provide an answer or type STOP to end.")
            return
        #Maintaning conversation history for contextually aware conversations 
        st.session_state.conversation_history.append({"role": "system", "content": st.session_state.current_question})
        st.session_state.conversation_history.append({"role": "user", "content": user_answer.strip()})
        
        system_prompt = (
            f"Provide a brief and neutral feedback on the candidate's response: '{user_answer}'. Avoid judging correctness or offering explanations. Keep the feedback concise and focused on tone and content appropriateness."
        )
        st.session_state.conversation_history.append({"role": "user", "content": system_prompt})
        
        gpt_reply = get_gpt_response(st.session_state.conversation_history)
        st.markdown(f"**TalentScout**: {gpt_reply}")
        st.session_state.conversation_history.append({"role": "assistant", "content": gpt_reply})

        st.session_state.isfollowup = random.choice([0,1]) #1 means we're to follow-up on the previous question and 0 means new topic
        st.session_state.questions_asked += 1            
        st.session_state.current_question = ""

if __name__ == "__main__":
    main()
