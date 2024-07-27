from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from openai import OpenAI
import openai
import os

bp = Blueprint("student", __name__)

client = OpenAI(
    api_key=os.getenv("OPENAI"),
)

history = []

# Function to try different encodings
def read_file_with_multiple_encodings(filepath, encodings=['utf-8', 'ISO-8859-1', 'cp1252']):
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as file:
                return file.read().replace('\n', ''), encoding
        except (UnicodeDecodeError, FileNotFoundError):
            continue
    raise UnicodeDecodeError(f"Failed to decode file {filepath} with available encodings.")

file_path = 'instance/texts/text.txt'
try:
    prompt_extension, used_encoding = read_file_with_multiple_encodings(file_path)
    print(f"File {file_path} successfully read with encoding {used_encoding}")
except UnicodeDecodeError as e:
    print(e)
    prompt_extension = ""

def generate_flashcards(text):
    chunks = text.split('\n\n')
    flashcards = []

    for chunk in chunks:
        prompt = f"Create a flashcard from the following text:\n\n{chunk}\n\nFlashcard:"
        try:
            response = client.completions.create(
                model="text-davinci-003",  
                prompt=prompt,  
                max_tokens=150
            )
            flashcards.append(response.choices[0].text.strip())
        except Exception as e:
            print(f"Error generating flashcard: {e}")  
            flashcards.append("Error generating flashcard")

    return flashcards

@bp.route('/student_landing')
@login_required
def landing():
    if current_user.role != 'student':
        return redirect(url_for('auth.login'))
    return render_template("student/landing.html", name=current_user.name)

@bp.route("/chatbot", methods=['GET', 'POST'])
@login_required
def chatbot():
    answer = ""
    if request.method == 'POST':
        submitted_text = request.form['textbox']
        answer = get_response(submitted_text)
        history.append((submitted_text, answer))
    
    return render_template("student/chatbot.html", message=history)

@bp.route("/app_response", methods=['GET', 'POST'])
def app_response():
    answer = ""
    submitted_text = request.args.get('text')
    
    if request.method == 'POST' or request.method == 'GET':
        answer = get_response(submitted_text)
        history.append((submitted_text, answer))
    
    return jsonify({"history": history})

def get_response(question):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a STEM teacher for students between the age of 13 and 18. You should explain in a way to make the students understand your answer. This is the course material, the students have to learn: {prompt_extension}"
                },
                {
                    "role": "user",
                    "content": "How do we calculate a modulo? and what is the modulo?"
                },
                {
                    "role": "assistant",
                    "content": "Ah, I see you're curious about modulos! Well, think of a modulo as a way to find the remainder after dividing two numbers. Let me explain it in a fun way.\n\nImagine you have a box of 12 chocolates and you want to share them equally among you and your two best friends. You start dividing the chocolates, giving each friend 4 chocolates. But what about the remaining chocolates? That's where the modulo comes in!\n\nTo calculate the modulo, you count how many chocolates are left after everyone gets their fair share. In this case, when you divide 12 chocolates among 3 people, each person gets 4 chocolates and there are no leftover chocolates. So, the modulo is 0.\n\nNow, let's try a different example. Suppose you have 10 candies and you want to share them equally among 4 friends. You start dividing, giving each friend 2 candies. But there will be some leftovers this time, right?\n\nTo find the modulo, we count how many candies are left after dividing equally. In this case, after giving each friend 2 candies, you'll have 2 candies left over. So, the modulo is 2.\n\nYou can find the modulo for any division calculation by finding the remainder, or what's"
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        processed = response["choices"][0]["message"]["content"]
        return processed
    
    except openai.RateLimitError as e:
        # Handle rate limit error gracefully
        print("Rate limit exceeded. Please wait and try again.")
        return "Rate limit exceeded. Please wait and try again."
    
    except openai.OpenAIError as e:
        # Handle other OpenAI API errors
        print(f"OpenAI API error: {e}")
        return f"OpenAI API error: {e}"

@bp.route('/flashcards')
def flashcards():
    return render_template("student/flashcards.html")

@bp.route("/flashcards", methods=['GET'])
def flashcards_get():
    file_path = 'instance/texts/text.txt'  # Adjust the path to your TXT file
    text = read_file_with_multiple_encodings(file_path)[0]
    flashcards = generate_flashcards(text)
    return jsonify(flashcards)

@bp.route("/flashcards", methods=['POST'])
def flashcards_post():
    file_path = 'instance/texts/text.txt'  # Adjust the path to your TXT file
    text = read_file_with_multiple_encodings(file_path)[0]
    flashcards = generate_flashcards(text)
    return render_template("student/flashcards.html", flashcards=flashcards)
