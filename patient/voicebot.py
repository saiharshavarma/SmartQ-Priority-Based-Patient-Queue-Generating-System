import openai
import pyttsx3
import speech_recognition as sr
import re

# set up OpenAI API instance
openai.api_key = "YOUR OPENAI API KEY"
model_engine = "text-davinci-002"

# function to convert text to speech
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# function to convert speech to text
# function to convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=5)  # set phrase_time_limit to 5 seconds
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        text_to_speech("Sorry, I didn't get that. Can you please repeat your answer?")
        return speech_to_text()


# function to generate summary from symptoms
def generate_summary(patient_name, age, gender, past_history, current_symptoms):
    # ask symptom-related questions to patient
    questions = [
        "When did the symptoms start?",
        "Are you taking any medications?",
        "Do you have any allergies?",
    ]

# "What other symptoms are you experiencing?"
# "Do you have any ongoing health issues?"
# "Are there any other relevant details that you would like to share?"

    answers = []
    for i, question in enumerate(questions):
        text_to_speech(question)
        answer = speech_to_text()
        answers.append(f"{i+1}. {question} {answer}")
    
    # generate summary
    answer_text = "\n".join(answers)
    summary_prompt = f"Generate a short summary for the following patient: {patient_name}, {age}, {gender}, past history of {past_history}. \nSymptoms: {current_symptoms} \nQuestions asked: {answer_text}"
    summary = openai.Completion.create(
        engine=model_engine,
        prompt=summary_prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text
    return summary

# main function to run the bot
def run_bot(patient_name):
    # greet the patient
    text_to_speech(f"Hello {patient_name}! I am a chatbot designed to help you with your symptoms.")
    text_to_speech("What is your age?")
    age = speech_to_text()
    text_to_speech("Are you male or female?")
    gender = speech_to_text()
    text_to_speech("Do you have any past history of the same problems?")
    past_history = speech_to_text()
    text_to_speech("Please describe your symptoms.")
    current_symptoms = speech_to_text()

    # generate summary
    summary = generate_summary(patient_name, age, gender, past_history, current_symptoms)

    # output summary to patient
    text_to_speech(f"Thank you {patient_name} for answering the questions. Here is a summary of your symptoms: {summary}")
    return summary