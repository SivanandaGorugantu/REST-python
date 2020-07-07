from flask import Flask, jsonify, request, Response
import json
from settings import *
from BookModel import *


#GET /store  
@app.route('/books')
def get_books():
	return jsonify({'books': Book.get_all_books()})


#GET /books/isbn
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
	print(isbn)
	return_val = Book.get_book(isbn)
	print(return_val)
	return jsonify(return_val)

#POST /books

def validBookObject(bookObject):
	if "name" in bookObject and "price" in bookObject and "isbn" in bookObject:
		return True
	else:
		return False

@app.route('/books', methods=['POST'])
def add_book():
	request_data = request.get_json()
	if validBookObject(request_data):
		Book.add_book(request_data['name'],request_data['price'],request_data['isbn'])
		response = Response("",201,mimetype="application/json")
		response.headers['Location'] = "/books/"+str(request_data['isbn'])
		return response
	else:
		invalidBookObjectErrorMsg = {
			"error": "invalid book object passed in request",
			"helpString": "Data passed in similar to this {'name': 'bookname','price': 9.33,'isbn':341341341}"
		}
		response = Response(json.dumps(invalidBookObjectErrorMsg),status=400,mimetype="application/json")
		return response

app.run(port=5000)