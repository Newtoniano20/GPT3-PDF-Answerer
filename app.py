from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
import os
import openai
from src import *
from werkzeug.utils import secure_filename

load_dotenv()

openai.api_key = str(os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'
app.config['UPLOAD_FOLDER'] = '.\\uploads'

@app.route("/", methods=('GET', 'POST'))
def home():
    if request.method == 'POST':

        question = request.form['content']
        file = request.files['file']

        if not question:
            flash('Question is required!')
        elif file.filename == '':
            flash('No selected file')
        else:
            if file and allowed_file(file.filename):
                path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                file.save(path_to_file)
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=generate_prompt(context=get_pdf_text(path_to_file), question=question),
                    temperature=0.5,
                    max_tokens=400
                )
            print(response)
            return redirect(url_for('home', result=response.choices[0].text))
        
    return render_template("home.html", result=request.args.get("result"))

def generate_prompt(context, question):
    return """
    Answer the following question given the provided context

    Context: {}
    
    Question: {}
    """.format(
        context, question
    )

if __name__ == "__main__":
    app.run(debug=True)