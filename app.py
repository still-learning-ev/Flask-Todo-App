from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
@app.route('/createnewdb')
def createdb():
    with app.app_context():
        db.create_all()
        return "DB created"
@app.route('/')
def hello_world():
    todo=Todo(title="first todo", desc="start investing in stocks")
    db.session.add(todo)
    db.session.commit()
    return "Hello world"


@app.route('/json')
def jsonFunction():
    return {"name": "hello", "game": "something"}


@app.route('/renderhtml', methods=['GET','POST'])
def renderhtml():
    if request.method== 'POST':
        title =request.form['title']
        desc = request.form['desc']
        todo =Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route("/showall")
def product():
    allTodo=Todo.query.all()
    print(allTodo)
    return "product"


@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/renderhtml")

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/renderhtml')
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
