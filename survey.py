from app import app, db
from app.models import User, Question, Answer

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Question': Question, 'Answer': Answer}

if __name__ == '__main__':
    app.run()