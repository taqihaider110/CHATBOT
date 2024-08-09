# Chatbot Interface Project

This project is a simple chatbot interface built with Flask, HTML, CSS, and JavaScript. The chatbot is designed to interact with users, respond to their queries, and maintain a conversation in both English and Roman Urdu. The backend is powered by a basic rule-based chatbot using the `nltk` library.

## Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Customization](#customization)
- [Technologies Used](#technologies-used)
- [Screenshots](#screenshots)
- [License](#license)

## Project Structure

```
chatbot-interface/
│
├── static/
│   ├── style.css
│   ├── chatbot.jpg
│   └── chat.js
│
├── templates/
│   └── index.html
│
├── app.py
├── README.md
└── requirements.txt
```

- `static/`: Contains static files such as CSS, images, and JavaScript.
- `templates/`: Contains the HTML template for rendering the web page.
- `app.py`: The main Flask application file.
- `README.md`: The README file with project information.
- `requirements.txt`: Lists the Python dependencies for the project.

## Features

- **Interactive Chat Interface**: Users can type messages and receive responses from the chatbot.
- **Roman Urdu Support**: The chatbot can understand and respond in Roman Urdu.
- **Responsive Design**: The chat interface is styled for both desktop and mobile views.
- **Initial Greeting**: The chatbot automatically sends a greeting message when the page is loaded.
- **User-Friendly Interface**: The design is clean and minimalistic with a modern look.

## Usage

- Type a message into the input field and click "Send" or press "Enter" to communicate with the chatbot.
- The chatbot will respond based on predefined patterns and responses.
- The chatbot can answer in both English and Roman Urdu.

## Customization

- **Adding/Modifying Responses**:
  - You can customize the chatbot's responses by editing the `patterns_and_responses` list in `app.py`.
  - Each pattern-response pair allows the chatbot to match specific user inputs and respond accordingly.

- **Styling**:
  - Modify the `style.css` file in the `static/` folder to customize the appearance of the chat interface.

- **JavaScript**:
  - The chatbot interaction logic is handled in `chat.js`, located in the `static/` folder. You can extend or modify the functionality as needed.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework for Python.
- **HTML/CSS**: Markup and styling for the frontend interface.
- **JavaScript**: Handles user interaction and communication with the Flask backend.
- **nltk**: Python's Natural Language Toolkit, used for basic chatbot functionality.
- **Jinja2**: Templating engine for rendering dynamic content in HTML.

## Screenshots

# START OF CONVERSATION:

![WhatsApp Image 2024-08-09 at 22 02 43_978ceceb](https://github.com/user-attachments/assets/904d8b96-3376-47a1-bd4b-d95e04db76d3)

# FURTHERMORE:

![image](https://github.com/user-attachments/assets/ab054ea9-a4ec-4106-89e4-ccc4722c9e1c)


![image](https://github.com/user-attachments/assets/fbe32f4a-31c9-4310-8d98-000b45a0876b)



