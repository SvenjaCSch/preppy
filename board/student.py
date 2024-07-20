from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import openai

bp = Blueprint("student", __name__)
openai.api_key  = "<place your openai_api_key>"

@bp.route("/landing")
@login_required
def landing():
    return render_template("student/landing.html", name=current_user.name)

@bp.route("/chatbot")
@login_required
def chatbot():
    return render_template("student/chatbot.html", name=current_user.name)

@bp.route("/chatbot")
@login_required
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

@bp.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')  
    response = get_completion(userText)  
    #return str(bot.get_response(userText)) 
    return response