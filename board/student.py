from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from flask_login import login_required, current_user
from openai import OpenAI
import openai
import os

bp = Blueprint("student", __name__)

client = OpenAI(
    api_key=os.getenv("OPENAI"),
)

history = []

def read_file_with_multiple_encodings(filepath, encodings=['utf-8', 'ISO-8859-1', 'cp1252']):
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return "", ""  # Return empty values if the file doesn't exist

    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as file:
                text = file.read()

                # Remove headers and footers if they are in the first and last 1000 characters
                text_lines = text.split('\n')
                text_lines = text_lines[10:-10]

                # Combine back to text
                text = '\n'.join(text_lines)

                # Remove references section assuming it starts with 'References' or 'REFERENCES'
                ref_index = text.lower().find('references')
                if ref_index != -1:
                    text = text[:ref_index]

                return text.replace('\n', ' '), encoding
        except (UnicodeDecodeError, FileNotFoundError) as e:
            print(f"Failed to read file {filepath} with encoding {encoding}: {e}")
            continue  # Try the next encoding
    raise UnicodeDecodeError(
        "utf-8",  # encoding
        b"",  # object (empty because we don't have the byte sequence)
        0,  # start position
        0,  # end position
        f"Failed to decode file {filepath} with available encodings."
    )

# Function to extract text from a PDF (placeholder)
def extract_text_from_pdf(pdf_path):
    # Implement your PDF extraction logic here
    extracted_text = "Sample text extracted from PDF."  # Replace with actual extracted text
    return extracted_text

@bp.route('/upload_pdf', methods=['POST'])
@login_required
def upload_pdf():
    if 'pdf_file' not in request.files:
        return redirect(url_for('student.landing'))

    pdf_file = request.files['pdf_file']

    if pdf_file.filename == '':
        return redirect(url_for('student.landing'))

    # Save the uploaded PDF to a specific location (e.g., instance/pdfs)
    pdf_path = os.path.join(current_app.instance_path, 'pdfs', pdf_file.filename)
    pdf_file.save(pdf_path)

    # Extract text from the PDF
    extracted_text = extract_text_from_pdf(pdf_path)

    # Specify the path to the text file
    file_path = os.path.join(current_app.instance_path, 'texts', 'text.txt')

    # After extracting text from the PDF, make sure it's valid text
    if extracted_text:  # Assuming extracted_text is the result from your PDF processing
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        print("Extracted text written to:", file_path)
    else:
        print("No text was extracted from the PDF.")

    return redirect(url_for('student.landing'))

def generate_flashcards(text):
    chunks = text.split('\n\n')
    
    flashcards = []
    for chunk in chunks:
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
                "content": f"You are a STEM teacher. Explain concepts simply. This is the course material: {summarized_material}"
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

@bp.route("/flashcards", methods=['GET', 'POST'])
def flashcards():
    file_path = os.path.join(current_app.instance_path, 'texts', 'text.txt')  # Adjust the path to your TXT file
    text = read_file_with_multiple_encodings(file_path)[0]

    # Generate flashcards from the text
    flashcards = generate_flashcards(text) or []  # Ensure flashcards is always a list

    # Print the value of flashcards for debugging
    print("Flashcards:", flashcards)  # Debugging line to see the contents of flashcards

    # Render the template with the flashcards data
    return render_template("student/flashcards.html", flashcards=flashcards)

@bp.route("/flashcards", methods=['GET'])
def flashcards_get():
    file_path = os.path.join(current_app.instance_path, 'texts', 'text.txt')
    text = read_file_with_multiple_encodings(file_path)[0]

    # Generate flashcards from the text
    flashcards = generate_flashcards(text) or []

    # Render the template with the flashcards data
    return render_template("student/flashcards.html", flashcards=flashcards)
