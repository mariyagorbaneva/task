from app import app
@app.route('/')
def login():
    return ('Привет')