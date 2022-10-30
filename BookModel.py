from sqlalchemy import true

from server import db, app


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.Integer)


def json(self):
    return {'name': self.name, 'author': self.author, 'isbn': self.isbn}


def add_book(_name, _author, _isbn):
    new_book = Book(name=_name, author=_author, isbn=_isbn)
    db.session.add(new_book)
    db.session.commit()


def get_all_books():
    return [json(book) for book in Book.query.all()]


def get_book(_isbn):
    return json(Book.query.filter_by(isbn=_isbn).first())


def delete_book(_isbn):
    Book.query.filter_by(isbn=_isbn).delete()
    db.session.commit()
    return true


def update_book_author(_isbn, _author):
    book_to_update = Book.query.filter_by(isbn=_isbn).first()
    book_to_update.author = _author
    db.session.commit()


def update_book_name(_isbn, _name):
    book_to_update = Book.query.filter_by(isbn=_isbn).first()
    book_to_update.name = _name
    db.session.commit()


def replace_book(_isbn, _name, _author):
    book_to_replace = Book.query.filter_by(isbn=_isbn).first()
    book_to_replace.author = _author
    book_to_replace.name = _name
    db.session.commit()


def __repr__(self):
    book_object = {
        'name': self.name,
        'author': self.author,
        'isbn': self.isbn
    }
    return json.dumps(book_object)
#
#
# def create_table():
#     with app.app_context():
#         db.create_all()
