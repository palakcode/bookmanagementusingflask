from flask import request, Response, jsonify, render_template

import BookModel
from server import *
import json


@app.route('/')
def hello():
    return 'hello'


@app.route('/books')
def get_books():
    return jsonify({'books': BookModel.get_all_books()})


@app.route('/books_with_html')
def get_books_with_html():
    return render_template('books.html', books=BookModel.get_all_books())


@app.route('/books/<int:isbn>')
def get_books_by_isbn(isbn):
    return_value = BookModel.get_book(isbn)
    return jsonify(return_value)


def validbookobject(bookobject):
    if "name" in bookobject and 'author' in bookobject and 'isbn' in bookobject:
        return True
    else:
        return False


def validbookobjectwithnameorauthor(bookobject):
    if "name" in bookobject or 'author' in bookobject:
        return True
    else:
        return False


# Post/books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.json
    if validbookobject(request_data):
        BookModel.add_book(request_data['name'], request_data['author'], request_data['isbn'])
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request ",
            "helpString": "Data passed in similar to this { 'name': 'bookname','author':'authorname','isbn': 288383}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response


@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if not validbookobject(request_data):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request "
        }
    BookModel.replace_book(isbn, request_data['name'], request_data['author'])
    response = Response("", status=204)
    return response


@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if BookModel.delete_book(isbn):
        response = Response("", status=204)
        return response
    invalidBookObjectErrorMsg = {
        "error": "Book with isbn number that was provided not found,therefore unable to delete"
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404)
    return response


@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book_name(isbn):
    request_data = request.get_json()
    if not validbookobjectwithnameorauthor(request_data):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request ",
            "helpString": "Data passed in similar to this { 'name': 'bookname','author':'authorname','isbn': 288383}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
        return response
    if "name" in request_data:
        print("In Name")
        BookModel.update_book_name(isbn, request_data['name'])
    if "author" in request_data:
        print("In Author")
        BookModel.update_book_author(isbn, request_data['author'])
    response = Response("", status=204)
    response.headers['Location'] = '/books/' + str(isbn)
    return response


#
# def start():
#     with app.app_context():

app.run(port=5000)

# start()
