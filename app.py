from pydoc import describe
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Criando classes do Banco de Dados
#class Todo(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    title = db.Column(db.String(100))
#    completed = db.Column(db.Boolean)

class Todo2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(100))
    completed = db.Column(db.Boolean)


@app.route("/")
def index():
    todo_list = Todo2.query.all()
    todo_completed = Todo2.query.filter_by(completed = True).all()
    todo_incompleted = Todo2.query.filter_by(completed = False).all()
    return render_template("index.html", todo_list=todo_list, todo_completed = len(todo_completed), todo_incompleted = len(todo_incompleted))

@app.route("/add", methods=["POST"])
def add():
    # Resgatando resposta do form
    title = request.form["ftitle"]
    description = request.form["fdescription"]

    # Criando novo item da classe Todo
    new_todo = Todo2(title=title, completed=False, description=description)
    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/update/<int:id>")
def update(id):
    todo = Todo2.query.filter_by(id = id).first()
    todo.completed = not(todo.completed)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo2.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

    

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    