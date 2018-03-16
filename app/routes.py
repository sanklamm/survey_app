from flask import render_template, flash, redirect, jsonify, json
from app.forms import LoginForm, QuestionForm, SurveyForm
from app.models import Question, Answer
from app import app
from app import db

@app.route('/')
@app.route('/index')
def index():
    '''This is the route for the Home Page.'''
    user = {'username': 'Sebastian'}
    return render_template('index.html', 
                           title='Gesundheit/Ernährung/Freizeit', 
                           user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Authentifizierung für Token {}'.format(
            form.accessToken.data))
        return redirect('/index')
    return render_template('login.html', title='Authentifizierung', form=form)

@app.route('/frage/neu', methods=['GET', 'POST'])
def newQuestion():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(category=form.category.data,
                            question=form.question.data,
                            frontend=form.frontend.data,
                            ans01=form.ans01.data,
                            ans02=form.ans02.data,
                            ans03=form.ans03.data,
                            ans04=form.ans04.data,
                            ans05=form.ans05.data,
                            ans06=form.ans06.data,
                            ans07=form.ans07.data,
                            ans08=form.ans08.data,
                            ans09=form.ans09.data,
                            ans10=form.ans10.data,
                            ans11=form.ans11.data,
                            ans12=form.ans12.data,
                            ans13=form.ans13.data,
                            ans14=form.ans14.data,
                            ans15=form.ans15.data,
                            ans16=form.ans16.data,
                            ans17=form.ans17.data,
                            ans18=form.ans18.data,
                            ans19=form.ans19.data,
                            ans20=form.ans20.data,
                            sort=form.sort.data,
                            )
        db.session.add(question)
        db.session.commit()
        return redirect('/frage/neu')
    return render_template('newQuestion.html', title='Neue Frage erfassen', form=form)

# TODO: Redirect to success page
@app.route('/umfrage', methods=['GET', 'POST'])
def newSurvey():
    form = SurveyForm()
    print(form.__dict__)
    for field in form:
        print()
        print(field.type)
    # for element in form:
    #     print(element.id)
    if form.validate_on_submit():
        answerString = generateAnswer(form)
        exec(answerString)
        # answer = Answer(usedToken='12345',
        #                 q01=form.q01.data,
        #                 q02=form.q02.data,
        #                 q03=form.q03.data,
        #                 q04=form.q04.data,
        #                 )
        # json.dumps()
        # db.session.add(answer)
        exec('db.session.add(answer)')
        db.session.commit()
        return redirect('/')
    return render_template('newSurvey.html', title='Umfrage', form=form)

# TODO: Add Token
def generateAnswer(form):
    # foo = f'answer = Answer(usedToken="12345", '
    foo = f'answer = Answer('
    for element in form:
        # print(element.data)
        if element.id.startswith('q'):
            foo= foo + f'q{int(element.id[1:])+1:02} = form.{element.id}.data, '
    foo = foo + ')'
    # print(foo)
    return foo
