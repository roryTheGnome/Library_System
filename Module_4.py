from flask import Flask, request, jsonify
import pandas as pd

try:
    books = pd.read_excel("books_with_extended_data.xlsx")
except FileNotFoundError:
    books = pd.DataFrame()  #i wanted program to work with empty canvas if there is an error(it feels a bit like the dumpster fire)

app = Flask(__name__)

@app.route('/')
def home():
    return '+Hello There! -General Kenobi?!? ^o^'


@app.route('/books')
def get_all_books():

    return jsonify(books.to_dict(orient='records'))



@app.route('/books/author')
def get_books_by_author():

    author = request.args.get('author', '').lower()

    if 'Surname' not in books.columns: #in the documantation it says name so i guessed if i use surname it would be more efficient, hope that okay
        return jsonify(error="no such colum check line 26 n update here"), 500 #heere for debugging

    filtered = books[books['Surname'].str.lower().str.contains(author, na=False)]
    return jsonify(filtered.to_dict(orient='records'))



@app.route('/books/title')
def search_by_title():
    word = request.args.get('word', '').lower()

    if 'Title' not in books.columns:
        return jsonify(error="no such colum check line 39 n update here"), 500 #here for debugiing

    print(f"Searching for title containing: '{word}'")   #here for debugiing and also feels like spying users so im most def gonna keep this

    filtered = books[books['Title'].str.lower().str.contains(word, na=False)]

    if filtered.empty:
        return jsonify(message="Woopsy daisy. No such book with that in the name exists")

    return jsonify(filtered.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)

""""
Example URL's: 

http://127.0.0.1:5000/books

http://127.0.0.1:5000/books/author?author=Owens
http://127.0.0.1:5000/books/author?author=King

http://127.0.0.1:5000/books/title?word=Where
http://127.0.0.1:5000/books/title?word=the
http://127.0.0.1:5000/books/title?word=and
"""
"""
Additional installs i had for this Module:
pip install flask
"""