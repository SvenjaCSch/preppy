# preppy
AI driven exam preparation tool for students between 12-18.Teacher can upload their material. The AI creates flashcards, a mockup exam and gives help as a chatbot. The Tool is webbased. 

## Introduction 
### Motivation

#### Advantages for teachers

#### Advantages for students

### Comparision to other AI Tools 

#### Quizlet
#### Note

## Functions

#### teachers perspective

#### students perspective

## Design
The Design of the application was implemented in Figma by Veronika Smilga, Kimberly Sharp and me during the course LLM in education in the university of Tuebingen during the summer semester 2024. Yin-Ying Li was creating the Flowchart based on the Figma Design. 
### Design on Figma
The figma prototype can be found here: https://www.figma.com/proto/1VhbgqEpKvuvH2E6JLZWm0/GradeAI-Website?node-id=8-2&t=gnWKger8cISlvrYW-0&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=8%3A2
The prototype includes following pages: 
\begin{enumerate}
\item main
\item about
\item teachers pages
\begin{enumerate}
\item login
\item signup
\item register
\item profile
\item landing page
\item course material
\item uploading page
\item evaluation page
\end{enumerate}
\item students pages
\begin{enumerate}
\item login
\item signup
\item register
\item profile
\item landing page
\item course material
\item mockup exam
\item mockup evaluation
\item learning assistent
\item flashcards
\end{enumerate}
\end{enumerate}


### Implementation function on Flask
So far the focus of the first draft is to implement a web-chatbot, that can be accessed for the students, when they log in. Therefore the first implemented pages are the following: main, login, signup, students landingpage and chatbot page. Furthermore a about the application page is being installed. 
The login and signup works via sqlite. The main programming language is python. For the web application, flask is used, implementating both html and css. 
For the chatbot the first idea was to use llama 3 with ollama so the server is locally. This can increase the privacy of the application. Furthermore Llama can be used without payment. Unfurtunatelly the fuctionallity was to slow. Next idea was to use llama 2 with a huggingface finetuned model. Nonetheless the kernel crashed. Next idea will be to use a OpenAI API. 

## Limitations
## Future Work
## Bibliography
- https://medium.com/@AlexanderObregon/how-to-build-a-simple-chatbot-with-python-4ce0742546a1
- https://pythonspot.com/login-authentication-with-flask/
- https://realpython.com/flask-project/
- https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
