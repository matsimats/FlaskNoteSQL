from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

# utwórz instancję aplikacji Flask
app = Flask(__name__)

# ustawienie konfiguracji dla bazy danych SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'notes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# utwórz instancję bazy danych SQLAlchemy
db = SQLAlchemy(app)


# utwórz klasę modelu dla notatek
class NoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))

    def __repr__(self):
        return '<Note %r>' % self.content


# utwórz tabelę notatek w bazie danych
with app.app_context():
    db.create_all()


# widok domyślny, wyświetla listę notatek
@app.route('/')
def index():
    notes = NoteModel.query.all()
    return render_template('index.html', notes=notes)


# widok dodawania nowej notatki
@app.route('/add', methods=['POST'])
def add():
    note_content = request.form['content']
    new_note = NoteModel(content=note_content)
    db.session.add(new_note)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
