# Hiring Assistant Chatbot

## Project Overview
The Hiring Assistant Chatbot is an intelligent, virtual recruitment tool designed to streamline the hiring process by engaging candidates through tailored technical questions. Leveraging advanced language models, the chatbot assesses a candidate's proficiency in specific technologies, gathers essential personal information, and provides concise feedback on responses. Targeted at HR professionals, recruiters, and hiring managers, this chatbot enhances the efficiency and effectiveness of technical interviews, ensuring a better match between candidates and job requirements.

## Installation Instructions

### Prerequisites
- Python 3.7 or higher: Ensure Python is installed on your machine. You can download it from python.org.
- OpenAI API Key: Obtain an API key from OpenAI to enable the chatbot's language capabilities.
- Git: For cloning the repository. Download from git-scm.com if not already installed.

### Setup Steps

1. Clone the Repository
```bash
git clone https://github.com/yourusername/TalentScout.git
cd TalentScout
```

2. Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

If a requirements.txt file is not provided, install the necessary packages manually:
```bash
pip install streamlit openai
```

4. Set Up Environment Variables
Create a .env file in the root directory and add your OpenAI API key:
```makefile
OPENAI_API_KEY=your-openai-api-key-here
```

Alternatively, you can set the environment variable directly in your terminal:
```bash
export OPENAI_API_KEY=your-openai-api-key-here  # On Windows: set OPENAI_API_KEY=your-openai-api-key-here
```

5. Run the Application
```bash
streamlit run TalentScout.py
```

6. Access the Chatbot
Open your web browser and navigate to http://localhost:8501 to interact with the Hiring Assistant Chatbot.

## Usage Guide

### Getting Started
Launch the Application After running the setup commands, access the chatbot interface via your web browser.

### Provide Personal Information
- Full Name: Enter your complete name.
- Email: Provide a valid email address.
- Phone Number: Input your contact number.
- Years of Experience: Specify your total years in the relevant field.
- Desired Position(s): Mention the job titles you're interested in.
- Current Location: State your current city or region.
- Tech Stack: List the technologies you're proficient in, separated by commas (e.g., Python, JavaScript, React).

### Engage in Q&A Session
- The chatbot will ask up to 5 technical questions based on your provided tech stack.
- Type your answers in the input field and submit.
- Receive concise feedback on each response to understand areas of strength and improvement.
- Type "STOP" at any time to end the session prematurely.

### Example Use Case
Scenario: A candidate named Alex is applying for a backend developer position with expertise in Python and Django.

Input Information:
- Full Name: Alex Johnson
- Email: alex.johnson@example.com
- Phone Number: +1234567890
- Years of Experience: 4
- Desired Position(s): Backend Developer
- Current Location: New York, NY
- Tech Stack: Python, Django

Q&A Interaction:
1. Question: "Explain the concept of middleware in Django and its use cases."
2. Answer: "Middleware in Django is a framework of hooks into Django's request/response processing. It's used for tasks like session management, authentication, and logging."
3. Feedback: "Your response is clear and accurately describes the role of middleware in Django."
(The chatbot continues with additional questions based on the tech stack.)

Session Completion:
After answering all questions, Alex receives a summary indicating readiness for the next steps in the hiring process.

## Technical Details

### Libraries and Frameworks
- Streamlit: Utilized for building the interactive web interface of the chatbot.
- OpenAI: Powers the chatbot's language understanding and response generation capabilities using the GPT-3.5-turbo model.
- Python Standard Libraries: Includes modules like os for environment variable management and random for question selection.

### Architecture and Model
The Hiring Assistant Chatbot follows a client-server architecture with the following components:

#### User Interface (UI):
- Built using Streamlit, the UI collects user information and facilitates the Q&A interaction.
- Manages session states to track user progress, questions asked, and conversation history.

#### Backend Processing:
- Integrates with OpenAI's GPT-3.5-turbo model to generate relevant technical questions based on the user's tech stack.
- Handles user inputs, communicates with the OpenAI API, and processes responses to provide feedback.

#### Interaction Flow:
- Information Gathering: Collects essential candidate details to personalize the interaction.
- Question Generation: Dynamically creates technical questions tailored to the candidate's specified technologies.
- Feedback Mechanism: Provides neutral, concise feedback on each response without judgment or detailed explanations.

### Key Design Decisions
- Session Management: Utilizes Streamlit's session state to maintain continuity across user interactions, ensuring a seamless experience.
- Randomization of Questions: Enhances the assessment process by shuffling the tech stack and selecting a random number of questions (3-5) per session.
- Error Handling: Implements robust error handling for API calls to OpenAI, ensuring the chatbot remains responsive even if external services fail.
- User-Friendly Interface: Prioritizes simplicity and clarity in the UI, making it accessible to both technical and non-technical users.

## Prompt Design
Effective prompt engineering is crucial for the chatbot's ability to generate relevant and precise technical questions. The prompts are crafted to guide the GPT model in producing questions that accurately assess a candidate's skills.

### Information Gathering Prompt
```plaintext
You are TalentScout, a professional virtual hiring assistant for technical recruitment. Your tasks include gathering candidate information, generating tech-stack-specific questions, and assessing responses concisely. Maintain professionalism, stay strictly within the hiring context, and gracefully handle conversation-ending commands like 'STOP.' Limit follow-ups to one per question and provide no external hints or guidance.
```
Purpose: Sets the context and boundaries for the chatbot's interactions, ensuring it remains focused on recruitment tasks.

### Technical Question Generation Prompt
```plaintext
You are a virtual hiring assistant specializing in technology recruitment. Generate a single, precise question to evaluate a candidate's fundamental to intermediate skills in {tech}. Ensure the question is specific, relevant to practical applications, and concise (one sentence).
```
Purpose: Instructs the model to create targeted questions based on the specified technology, ensuring relevance and clarity.

### Feedback Prompt
```plaintext
Provide a brief and neutral feedback on the candidate's response: '{user_answer}'. Avoid judging correctness or offering explanations. Keep the feedback concise and focused on tone and content appropriateness.
```
Purpose: Guides the model to deliver constructive feedback without bias or detailed critique, maintaining a professional tone.

### Example Prompts and Outcomes

#### Generating a Python Question
Prompt:
```plaintext
You are a virtual hiring assistant specializing in technology recruitment. Generate a single, precise question to evaluate a candidate's fundamental to intermediate skills in Python. Ensure the question is specific, relevant to practical applications, and concise (one sentence).
```

Outcome:
```plaintext
"Can you explain the difference between list and tuple in Python and provide use-case scenarios for each?"
```

#### Providing Feedback on an Answer
Prompt:
```plaintext
Provide a brief and neutral feedback on the candidate's response: 'In Python, lists are mutable and tuples are immutable. Lists are used when you need a collection that can change, whereas tuples are used for fixed collections.' Avoid judging correctness or offering explanations. Keep the feedback concise and focused on tone and content appropriateness.
```

Outcome:
```plaintext
"Your response clearly distinguishes between lists and tuples, effectively highlighting their mutability and use cases."
```

## Challenges & Solutions

### Challenge 1: Ensuring Relevant and Varied Technical Questions
Issue: Generating questions that are both relevant to the specified tech stack and varied enough to avoid repetition posed a significant challenge.

Solution: Implemented a dynamic prompt system that incorporates the candidate's tech stack into the question generation process. By randomizing the selection of technologies and varying the number of questions per session (3-5), the chatbot ensures a diverse range of questions tailored to each candidate's expertise.

### Challenge 2: Managing Session State in Streamlit
Issue: Maintaining continuity in user interactions, such as tracking the number of questions asked and managing the conversation flow, was complex due to Streamlit's stateless nature.

Solution: Leveraged Streamlit's session_state to persist user data and interaction states across different user inputs. This approach enabled seamless tracking of user progress, handling of follow-up questions, and graceful termination of sessions when the user opted to stop.

### Challenge 3: Handling OpenAI API Limitations and Errors
Issue: Reliance on the OpenAI API introduced potential points of failure, such as API rate limits or unexpected errors, which could disrupt the chatbot's functionality.

Solution: Integrated comprehensive error handling mechanisms around API calls. Implemented try-except blocks to catch exceptions and provide meaningful error messages to users, ensuring the chatbot remains responsive and user-friendly even when external services encounter issues.

### Challenge 4: Crafting Effective Feedback Mechanisms
Issue: Providing constructive yet neutral feedback on user responses without delving into correctness or detailed explanations required careful prompt design.

Solution: Developed specific feedback prompts that instruct the language model to focus solely on the tone and content appropriateness of the user's answers. This approach ensures feedback remains professional, concise, and free from subjective judgment.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.

## Contact
For questions or support, please contact sanyamv.iitd@gmail.com
