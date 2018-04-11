from flask import render_template, flash, redirect, jsonify, json, url_for, request
from app.forms import LoginForm, QuestionForm, SurveyForm, TokenForm
from app.models import Question, Answer, User
from app import app
from app import db
from flask_login import login_user, logout_user
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin

# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)

@app.route('/')
@app.route('/index')
def index():
    '''This is the route for the Home Page.'''
    return render_template('index.html', 
                           title='Gesundheit/Ernährung/Freizeit')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """The Login route."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        token = User.query.filter_by(password = form.accessToken.data, used=False).first()
        print(form.accessToken.data)
        if token is None:
            flash('Kein gültiger Token oder Token bereits verbraucht.')
            return redirect(url_for('login'))
        login_user(token)
        return redirect('/umfrage')
    return render_template('login.html', title='Authentifizierung', form=form)

@app.route('/logout')
def logout():
    """The Logout route."""
    logout_user()
    return redirect(url_for('index'))

@app.route('/token/neu', methods=['GET', 'POST'])
@roles_required('Admin')
def newToken():
    """Route to generate new token."""
    form = TokenForm()
    if form.validate_on_submit():
        User.generate_token(form.quantity.data, form.role.data)
        quantity = User.get_num_unused_token()
        flash(f'Es gibt jetzt {quantity} unbenutzte Token in der Datenbank')
        return redirect('/token/neu')
    return render_template('newToken.html', title='Tokengenerierung', form=form)

@app.route('/frage/neu', methods=['GET', 'POST'])
@roles_required('Admin')
def newQuestion():
    """Route to generate new questions."""
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

@app.route('/umfrage', methods=['GET', 'POST'])
@login_required
def newSurvey():
    """Route to the survey."""
    form = SurveyForm()
    ans = Answer(usedToken=current_user.id)
    db.session.add(ans)
    db.session.commit()
    if form.is_submitted():
        ans = Answer.query.filter_by(usedToken=current_user.id).first()
        for element in form:
            if element.id.startswith('q'):
                if type(element.data) is list:
                    setattr(ans, element.id, str(element.data))
                else:
                    setattr(ans, element.id, element.data)
        db.session.commit()
        if not current_user.is_Admin:
            current_user.invalidate_token()
        logout_user()
        return redirect('/fertig')
    return render_template('newSurvey.html', title='Umfrage', form=form)

@app.route('/fertig')
def success():
    """The Route after a submitted survey."""
    return render_template('success.html')

@app.route('/save', methods=['POST'])
def save():
    """Route called by Ajax method when user switches a tab in the survey."""
    ans = Answer.query.filter_by(usedToken=current_user.id).first()
    for k, v in request.form.items():
        if k.startswith('q'):
            setattr(ans, k, v)
    db.session.commit()
    return jsonify({'status': 'ok'})
    