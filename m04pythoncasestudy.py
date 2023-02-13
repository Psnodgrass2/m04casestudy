from flask import Flask, request
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable = False)
    description = db.Column(db.String(120))
    publisher = db.Column(db.String(80), unique=True, nullable = False)
    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def index():
    return "Hello!"

@app.route("/Books")
def get_Books():
    Books = Book.query.all()
    output = []
    for Book in Books:
        Book_data = {"name": Book.book_name, "description": Book.description, "publisher":Book.publisher}
        output.append(Book_data)
    return {"Books": output}
@app.route("/Books/<id>")
def get_Book(id):
    Book = Book.query.get_or_404(id)
    return {"name": Book.book_name, "description": Book.description, "publisher":Book.publisher}


@app.route("/Books", methods=["POST"])
def add_Book():
    Book = Book(name=request.json["name"], description=request.json["description"], publisher=request.json["publisher"])
    db.session.add(Book)
    db.session.commit()
    return {"id": Book.id}

@app.route("/Books/<id>", methods=["DELETE"])
def delete_Book():
    Book = Book.query.get(id)
    if Book is None:
        return{"error": "not found"}
    db.session.delete(Book)
    db.session.commit()
    return {"message": "I am in agony, this class is terrible."}