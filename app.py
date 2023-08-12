from flask import Flask, render_template, redirect, request, flash,session
from flask import abort
# Importing the required modules and classes
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize the empty responses list
responses = []

# Creating the root page, question pages, and the answer page
@app.route('/')
def show_survey_title():


#Show the survey title, instructions, and a button to start the survey.
    return render_template('survey_title.html', survey=satisfaction_survey)

@app.route ('/start')
def start_survey():
    session["responses"] =[]
    print(session["responses"])
    return redirect(f'/questions/0')

@app.route('/questions/<int:question_id>', methods=['GET', 'POST'])
def show_question(question_id):
# Show the current question and handle the form submission.
    print("Currently Proccesing Question" + str(question_id))
    if question_id < len(satisfaction_survey.questions):
        question = satisfaction_survey.questions[question_id]
        print("Question ID < Survey Question")
        if request.method == 'POST':
            response = request.form.get('choice')
            if not response:
                flash('Please select an answer before submitting.', 'error')
            else:
                responses = session["responses"]
                print(responses)
                responses.append(response)
                print(responses)
                session["responses"] = responses
                print(session["responses"])
                print("Checking question_id")
                #responses.append(response)
                return redirect(f'/questions/{question_id + 1}')

# Verify if the user is on the correct question based on responses these are just to prevent manipulation of the URL

        if question_id != len(session["responses"]):
            flash('Invalid question. Please answer the questions in order.', 'error')
            return redirect(f'/questions/{len(session["responses"])}')

        return render_template('question.html', question=question, question_id=question_id)
    elif question_id == len(satisfaction_survey.questions):
        return redirect('/thankyou')
    else:

# Flash an error message for accessing an invalid question
        flash('Invalid question ID.', 'error')
        return redirect(f'/questions/{len(session["responses"])}')

@app.route('/thankyou')

def show_thank_you():
#Show a Thank You page.
    return render_template('thank_you.html')

#Running the app
if __name__ == '__main__':
    app.run(debug=True)
