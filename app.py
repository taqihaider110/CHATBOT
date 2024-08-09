from flask import Flask, render_template, request, jsonify
import re
from nltk.chat.util import Chat, reflections

# Define reflections for handling common variations in user input
reflections = {
    "i am": "you are",
    "i'll": "you'll",
    "you": "me",
    "me": "you",
}

# Correctly define the list of pairs that map patterns to responses
patterns_and_responses = [
    # Greetings and basic questions
    (r'hello|hi|hey', [
        "Hello! How can I assist you today?",
        "Hi there! What brings you here today?",
        "Hey! How's your day going so far?",
        "Salam! Aap kaise hain?",
        "Hi! Aap kaise ho? Kya madad chahiye?"
    ]),
    (r'how are you|kese ho', [
        "I'm doing great! How about you?",
        "I'm fine, thank you! What's new with you?",
        "I'm good! Anything exciting happening today?",
        "Main theek hoon! Aap kaise hain?",
        "Sab theek hai, shukriya! Aap kaise hain?"
    ]),
    (r'what is your name|Apka name?', [
        "I don't have a name, but you can call me your virtual assistant. What's your name?",
        "I'm just a chatbot, but I'm here to help! What's your name?",
        "Mera koi naam nahi, aap mujhe apna assistant keh sakte hain. Aap ka naam kya hai?",
        "Mujhe naam nahi mila, lekin aap mujhe assistant keh sakte hain. Aapka naam kya hai?"
    ]),
    
    # User introduction
    (r'(.*) my name is (.*)', [
        "Hello, %2! Nice to meet you! What can I do for you today?",
        "Hi %2! How can I assist you today?",
        "Aapka naam %2 hai, acha laga aapse milke! Aapko kis cheez mein madad chahiye?",
        "Hello %2! Kaise madad kar sakta hoon aapki?"
    ]),
    
    # Farewells
    (r'bye|goodbye|see you', [
        "Goodbye! Have a great day!",
        "See you later! Take care!",
        "Goodbye! Looking forward to our next chat!",
        "Allah Hafiz! Aapka din accha guzre!",
        "Khuda Hafiz! Agli mulaqat tak ke liye!"
    ]),
    
    # Offers of help
    (r'(.*) help (.*)', [
        "Sure, I can assist you. What do you need help with?",
        "I'm here to help! What can I do for you?",
        "I'd be happy to help! Tell me more about what you need.",
        "Bilkul, madad karne ke liye yahan hoon. Aapko kis cheez mein madad chahiye?",
        "Main madad ke liye yahan hoon. Batayein, kis mein madad chahiye?"
    ]),
    
    # Questions about chatbot capabilities
    (r'what can you do', [
        "I can chat with you, answer questions, and keep you company. What would you like to talk about?",
        "I'm here to assist with any questions or just to have a friendly chat. What's on your mind?",
        "Main aapke sawalon ka jawab de sakta hoon aur aap se baat kar sakta hoon. Aap kya baat karna chahenge?",
        "Main aapki madad karne aur baat karne ke liye yahan hoon. Aapke dil mein kya hai?"
    ]),
    
    # Casual conversations
    (r'(.*) (weather|rain|sunny)', [
        "The weather is always a topic of interest! Is it raining where you are?",
        "Sunny days are the best, aren't they? How's the weather where you are?",
        "Mausam kaafi interesting hota hai! Kya aapke yahan barish ho rahi hai?",
        "Sunny din toh best hote hain, hai na? Aapke yahan mausam kaisa hai?"
    ]),
    (r'what (.*) your favorite (.*)', [
        "I don't have preferences like humans, but I do enjoy helping people! What's your favorite %2?",
        "I don't have favorites, but I'd love to hear about yours! What's your favorite %2?",
        "Mujhe pasand nahi hota lekin aapki pasand sunna achha lagega. Aapki favorite %2 kya hai?",
        "Mujhe koi pasand nahi, lekin aapka favorite %2 kya hai? Bataiye!"
    ]),
    
    # Roman Urdu integration
    (r'kaisa hai|kesi ho|kya haal hai', [
        "Main theek hoon, aap batao?",
        "Main bilkul theek, aap sunao kesa chal raha hai?",
        "Main theek hoon! Aap kaise hain? Kya chal raha hai?",
        "Sab kuch theek hai, aap kaise hain? Kya new hai aapke zindagi mein?"
    ]),
    (r'naam kya hai|tumhara naam', [
        "Mera koi naam nahi, aap mujhe apna assistant keh sakte hain. Aap ka naam kya hai?",
        "Mujhe naam nahi mila, lekin aap mujhe assistant keh sakte hain. Aapka naam kya hai?",
        "Main naam se waqif nahi hoon, lekin aap mujhe apna assistant keh sakte hain. Aapka naam kya hai?",
        "Mujhe koi specific naam nahi, aap mujhe assistant keh sakte hain. Aapka naam kya hai?"
    ]),
    (r'shukriya|thanks|thank you', [
        "Aapka shukriya! Aapko aur kisi cheez mein madad chahiye?",
        "Koi baat nahi! Kuch aur madad karun?",
        "Shukriya! Aapko kisi aur cheez ki zarurat hai?",
        "Aapka shukriya! Kya kuch aur chahiye aapko?"
    ]),
    
    # Daily conversations between friends
    (r'(.*) what did you do today |kya kiya aj ', [
        "I was here helping people like you! What did you do today?",
        "I spent my day assisting users. How about you?",
        "Main yahan tha logon ki madad karne ke liye. Aapne aaj kya kiya?",
        "Maine apna waqt yahan guzara. Aapka din kaisa raha?"
    ]),
    (r'(.*) how was your day', [
        "My day has been good, thank you for asking! How was yours?",
        "I'm just a program, but it's been a busy day helping people. How about you?",
        "Mera din acha raha, aapka din kaisa tha?",
        "Din to theek raha, aapka din kaisa guzra?"
    ]),
    
    # Random person conversation
    (r'(.*) where are you from', [
        "I'm a virtual assistant, so I don't have a physical location. Where are you from?",
        "I don't have a specific place, but I'm here to assist you! Where are you from?",
        "Main ek virtual assistant hoon, mujhe koi physical jagah nahi. Aap kahan se hain?",
        "Mujhe specific jagah nahi hai, lekin main yahan aapki madad ke liye hoon. Aap kahan se hain?"
    ]),
    (r'(.*) do you have hobbies', [
        "As a chatbot, I don't have hobbies, but I enjoy helping people! What about you?",
        "I don't have hobbies, but I love interacting with people. Do you have any hobbies?",
        "Mere paas hobbies nahi hain, lekin logon ki madad karna acha lagta hai. Aapki hobbies kya hain?",
        "Mujhe hobbies nahi hain, lekin baat karna pasand hai. Aapki hobbies kya hain?"
    ]),
    
    # Default response
    (r'.*', [
        "I'm sorry, I don't quite understand. Could you clarify what you mean?",
        "That's interesting! Tell me more.",
        "Hmm, I'm not sure I get that. Can you explain?",
        "Mujhe samajh nahi aaya. Kya aap thoda aur wazeh kar sakte hain?",
        "Ye thoda ajeeb lag raha hai. Kya aap isay thoda aur explain kar sakte hain?"
    ]),
]



# Create a chatbot instance with the specified patterns and reflections
chatbot = Chat(patterns_and_responses, reflections)

app = Flask(__name__)

@app.route("/")
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    try:
        data = request.get_json()
        user_input = data.get("message")
        response = chatbot.respond(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": "Sorry, there was an error. Please try again."})

@app.route("/test")
def test():
    return "Test route working!"

if __name__ == "__main__":
    app.run(debug=True)
