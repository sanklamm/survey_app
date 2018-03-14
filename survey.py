from app import app, db
from app.models import Token, Question, Answer

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Token': Token, 'Question': Question, 'Answer': Answer}
