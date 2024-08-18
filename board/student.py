from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from flask_login import login_required, current_user
from openai import OpenAI
import openai
import os
import json

bp = Blueprint("student", __name__)

client = OpenAI(
    api_key=os.getenv("OPENAI"),
)

history = []

#####################################################
# Flashcards
#####################################################
def read_file_with_multiple_encodings(filepath:str, encodings:list[str]=['utf-8', 'ISO-8859-1', 'cp1252'])->str:
    """
    tests different ecodings to decode the text correctly
    Arguments:
        str: filepath
        list[str]: encodings
    """
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        # Return empty values if the file doesn't exist
        return "", ""  

    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as file:
                text = file.read()

                # Remove headers and footers if they are in the first and last 1000 characters
                text_lines = text.split('\n')
                text_lines = text_lines[10:-10]
                text = '\n'.join(text_lines)

                # Remove references section assuming it starts with 'References' or 'REFERENCES'
                ref_index = text.lower().find('references')
                if ref_index != -1:
                    text = text[:ref_index]

                return text.replace('\n', ' '), encoding
        except (UnicodeDecodeError, FileNotFoundError) as e:
            print(f"Failed to read file {filepath} with encoding {encoding}: {e}")
            # Try the next encoding
            continue  
    # "utf-8",  encoding
    # b"",  object (empty because we don't have the byte sequence)
    # 0,  start position
    # 0,  end position
    raise UnicodeDecodeError(
        "utf-8",  
        b"",
        0,  
        0,  
        f"Failed to decode file {filepath} with available encodings."
    )

def get_flashcards(text:str)->list[str]:
    """
    returns text into flashcards
    """
    chunks = text.split('\n\n')

    # Limit to the first 10 chunks
    flashcard_limit = 10
    flashcards = []
    for chunk in chunks[:flashcard_limit]:
        prompt = f"Create a flashcard from the following text:\n\n{chunk}\n\nFlashcard:"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        flashcards.append(response.choices[0].message.content.strip())

    return flashcards

@bp.route("/flashcards", methods=['GET', 'POST'])
def flashcards()->str:
    """
    handles flashcards
    work in progress
    """
    flashcards_folder = os.path.join(current_app.instance_path, 'flashcards')
    os.makedirs(flashcards_folder, exist_ok=True)
    # Adjust the path to your TXT file
    file_path = os.path.join(current_app.instance_path, 'texts', 'text.txt')  
    
    if request.method == 'POST':
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        flashcards = get_flashcards(text) or []
        
        upload_path = os.path.join(flashcards_folder, 'flashcards.json')
        with open(upload_path, 'w', encoding='utf-8') as f:
            json.dump(flashcards, f)
        
        return render_template("student/flashcards.html", flashcards=flashcards)
    
    # Handle GET request
    upload_path = os.path.join(flashcards_folder, 'flashcards.json')
    
    # Load existing flashcards if needed
    if os.path.exists(upload_path):
        with open(upload_path, 'r', encoding='utf-8') as f:
            flashcards = json.load(f)
    else:
        flashcards = []
    
    return render_template("student/flashcards.html", flashcards=flashcards)

#####################################################
# Login
#####################################################

@bp.route('/student_landing')
@login_required
def landing()->str:
    """
    redirects to landing page if student. Otherwse login page
    """
    if current_user.role != 'student':
        return redirect(url_for('auth.login'))
    return render_template("student/landing.html", name=current_user.name)

#####################################################
# Chatbot
#####################################################

@bp.route("/chatbot", methods=['GET', 'POST'])
@login_required
def chatbot()->str:
    """
    handles chatbot response system
    """
    answer = ""
    if request.method == 'POST':
        submitted_text = request.form['textbox']
        answer = get_response(submitted_text)
        history.append((submitted_text, answer))
    
    return render_template("student/chatbot.html", message=history)

def get_response(question:str)->str:
    """
    get the response via LLM depending on the users input
    """
    try:
        # Read the prompt_extension when needed
        file_path = os.path.join(current_app.instance_path, 'texts', 'text.txt')
        prompt_extension, used_encoding = read_file_with_multiple_encodings(file_path)

        # Summarize the course material to fit within a smaller token limit
        summary_prompt = f"Summarize the following course material in a way that fits within 300 tokens:\n\n{prompt_extension}"
        summary_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": summary_prompt}
            ],
            max_tokens=300
        )
        
        summarized_material = summary_response.choices[0].message.content.strip()

        # Define the initial messages for the conversation, ensuring they are concise
        initial_messages = [
            {
                "role": "system",
                "content": f"You are a STEM teacher. Answer the question accuarately. Explain concepts behind in a simple way with easy examples. Your students are in the age between 12 and 15. This is the course material: {summarized_material}"
            },
            {
                "role": "user",
                "content": "How do we calculate a modulo? and what is the modulo?"
            },
            {
                "role": "assistant",
                "content": "Think of modulo as finding the remainder after division. For example, 10 mod 3 is 1 because 10 divided by 3 is 3 with a remainder of 1."
            },
            {
                "role": "user",
                "content": question
            }
        ]

        initial_token_count = sum(len(message['content'].split()) for message in initial_messages)

        # Trim the history to fit within the token limit
        max_total_tokens = 16385
        max_history_tokens = max_total_tokens - initial_token_count - 256  # 256 tokens reserved for response
        trimmed_history = []

        current_token_count = 0
        for q, a in reversed(history):
            q_tokens = len(q.split())
            a_tokens = len(a.split())
            if current_token_count + q_tokens + a_tokens <= max_history_tokens:
                trimmed_history.insert(0, {"role": "user", "content": q})
                trimmed_history.insert(0, {"role": "assistant", "content": a})
                current_token_count += q_tokens + a_tokens
            else:
                break

        # Combine the messages for the conversation
        messages = initial_messages + trimmed_history

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        processed = response.choices[0].message.content.strip()
        return processed
    
    except openai.RateLimitError as e:
        # Handle rate limit error gracefully
        print("Rate limit exceeded. Please wait and try again.")
        return "Rate limit exceeded. Please wait and try again."
    
    except openai.OpenAIError as e:
        # Handle other OpenAI API errors
        print(f"OpenAI API error: {e}")
        return f"OpenAI API error: {e}"

