# Preppy
An AI driven exam preparation tool for students in the age between 12-18.Teacher can upload their material. The AI creates flashcards, a mockup exam and gives help as a chatbot. The Tool is webbased. 

## Introduction 
### Motivation

#### Advantages for teachers

#### Advantages for students

### Comparision to other AI Tools 
There are several webtools, that help the students to learn with flashcards and further material.

#### Quizlet
Quizlet is an online tool for students to create flashcards to learn the course material. Here the students have to create the flashcards by themself. Our model creates the flashcards according to the uploaded material from the teacher automatically. 

#### Note
Note is an online tool where students can create pages containing informations about the course mterial, time schedules and grading systems. The students has to fill in the information by themself. 
## Functions

#### teachers perspective
The teacher can create a new class and upload course material which is being used by the AI to create flashcards and a mockup exam. The uploaded material is the basis of the learning asisstent. 

#### students perspective
The student can look into the exam preparation via class code that is given by the teacher. Then they have access to automatically designed flashcards, the raw course material, a automatically created mockup exam and a learning assitent, that helps the student with further questions.

## Design
The Design of the application was implemented in Figma by Veronika Smilga, Kimberly Sharp and me during the course LLM in education in the university of Tuebingen during the summer semester 2024. Yin-Ying Li was creating the Flowchart based on the Figma Design. 
### Design on Figma
The figma prototype can be found here: https://www.figma.com/proto/1VhbgqEpKvuvH2E6JLZWm0/GradeAI-Website?node-id=8-2&t=gnWKger8cISlvrYW-0&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=8%3A2
The prototype includes following pages: 
- main
- about
- teachers pages
    - login
    - signup
    - register
    - profile
    - landing page
    - course material
    - uploading page
    - evaluation page
- students pages
    - login
    - signup
    - register
    - profile
    - landing page
    - course material
    - mockup exam
    - mockup evaluation
    - learning assistent
    - flashcards
Markup : ![picture alt](board/static/images/Main_Page.png "Figma Main page")

### Implementation function on Flask
So far the focus of the first draft is to implement a web-chatbot, that can be accessed for the students, when they log in. Therefore the first implemented pages are the following: main, login, signup, students landingpage and chatbot page. Furthermore a about the application page is being installed. 
The login and signup works via sqlite. The main programming language is python. For the web application, flask is used, implementating both html and css. 
For the chatbot the first idea was to use llama 3 with ollama so the server is locally. This can increase the privacy of the application. Furthermore Llama can be used without payment. Unfurtunatelly the fuctionallity was to slow. Next idea was to use llama 2 with a huggingface finetuned model. Nonetheless the kernel crashed. Next idea will be to use a OpenAI API. 
- [x] main
- [x] about
- [x] teachers pages
    - [x] login
    - [x] signup
    - [ ] profile
    - [x] landing page
    - [ ] course material
    - [x] uploading page
    - [ ] evaluation page
- [x] students pages
    - [x] login
    - [x] signup
    - [x] profile
    - [x] landing page
    - [ ] course material
    - [ ] mockup exam
    - [ ] mockup evaluation
    - [x] learning assistent
    - [ ] flashcards

The folder are structured as showed:
- ┣ 📂board
- ┃ ┣ 📂static
- ┃ ┃ ┣ 📂css
- ┃ ┃ ┃ ┣ 📜preppy.css
- ┃ ┃ ┃ ┗ 📜styles.css
- ┃ ┃ ┣ 📂images
- ┃ ┃ ┃ ┣ 📜arrow-circle-left.png
- ┃ ┃ ┃ ┣ 📜arrow-circle-up.png
- ┃ ┃ ┃ ┣ 📜Background_header.png
- ┃ ┃ ┃ ┣ 📜Backimage.png
- ┃ ┃ ┃ ┣ 📜house-chimney.png
- ┃ ┃ ┃ ┣ 📜Login Student.png
- ┃ ┃ ┃ ┣ 📜Logo.png
- ┃ ┃ ┃ ┣ 📜Main Page.png
- ┃ ┃ ┃ ┣ 📜Students Flashcards.png
- ┃ ┃ ┃ ┗ 📜Students Landing Page.png
- ┃ ┃ ┗ 📂js
- ┃ ┃ ┃ ┣ 📜base.js
- ┃ ┃ ┃ ┗ 📜chatbot.js
- ┃ ┣ 📂templates
- ┃ ┃ ┣ 📂auth
- ┃ ┃ ┃ ┣ 📜index.html
- ┃ ┃ ┃ ┣ 📜login.html
- ┃ ┃ ┃ ┣ 📜login2.html
- ┃ ┃ ┃ ┗ 📜signup.html
- ┃ ┃ ┣ 📂errors
- ┃ ┃ ┃ ┗ 📜404.html
- ┃ ┃ ┣ 📂pages
- ┃ ┃ ┃ ┣ 📜about.html
- ┃ ┃ ┃ ┣ 📜home.html
- ┃ ┃ ┃ ┗ 📜profile.html
- ┃ ┃ ┣ 📂student
- ┃ ┃ ┃ ┣ 📜chatbot.html
- ┃ ┃ ┃ ┗ 📜landing.html
- ┃ ┃ ┣ 📜base.html
- ┃ ┃ ┗ 📜_navigation.html
- ┣ 📜.env
- ┣ 📜.gitignore
- ┣ 📜README.md
- ┣ 📜requirements.txt
- ┗ 📜run.py

## Limitations
## Future Work
## Bibliography
- https://medium.com/@AlexanderObregon/how-to-build-a-simple-chatbot-with-python-4ce0742546a1
- https://pythonspot.com/login-authentication-with-flask/
- https://realpython.com/flask-project/
- https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
- https://medium.com/@abed63/flask-application-with-openai-chatgpt-integration-tutorial-958588ac6bdf
- https://pythonbasics.org/flask-upload-file/
- ChatGPT for creating the HTML and CSS components from the Figma input as well as for the python part and the javascript file for the flashcards
