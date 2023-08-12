"""Importing modules and create a Flask web application
Flask- Flask applications
request- access incoming request data
render_template - render HTML templates
redirect and url_for - redirecting users
"""
from flask import Flask, request, render_template, redirect, url_for
from data_models import db, Author, Book # imported from a module named data_models. separate module handling data models
from datetime import datetime #handling date and time
import requests #make HTTP requests.

app = Flask(__name__)

#Set the database URI for SQLAlchemy, providing file path
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite3'

#Initialize the SQLAlchemy database (db) with the Flask app (app)
db.init_app(app)


# Define the route for the home page
@app.route('/', methods=['GET'])
def home():
    sort_criteria = request.args.get('sort', 'title')
    search_query = request.args.get('search', '').strip()
    action = request.args.get('action', 'sort')  # Default to 'sort'

    # Query the Book table to get the list of books, their authors, and ISBNs
    books_with_authors_isbns = Book.query.join(Author).all()

    # Perform action based on user selection
    if action == 'search' and search_query:
        books_with_authors_isbns = [book for book in books_with_authors_isbns
                                    if
                                    search_query.lower() in book.title.lower() or
                                    search_query.lower() in book.author.name.lower()]

    # Sort the books based on the selected criteria
    if sort_criteria == 'title':
        books_with_authors_isbns.sort(key=lambda book: book.title)
    elif sort_criteria == 'author':
        books_with_authors_isbns.sort(key=lambda book: book.author.name)

    # Prepare the data for rendering the template
    book_data = []

    for book in books_with_authors_isbns:
        isbn = book.isbn
        cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
        book_data.append({
            'id': book.id,  # Include the book's ID in the data
            'title': book.title,
            'author': book.author.name,
            'cover_url': cover_url
        })

    if not book_data:
        message = "No books match the search criteria."
    else:
        message = None

    return render_template('home.html', books=book_data, message=message)
#defines a route for adding authors (/add_author) using both HTTP GET and POST methods
@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        birthdate = datetime.strptime(request.form.get('birthdate'), '%Y-%m-%d').date()
        date_of_death = datetime.strptime(request.form.get('date_of_death'), '%Y-%m-%d').date() if request.form.get('date_of_death') else None

        # Create a new Author instance
        new_author = Author(name=name, birth_date=birthdate, date_of_death=date_of_death)

        # Add and commit the new author to the database
        db.session.add(new_author)
        db.session.commit()

        # Display a success message
        success_message = "Author added successfully!"
        return render_template('add_author.html', success_message=success_message)

    # For GET requests, render the add_author.html template
    return render_template('add_author.html')



#defines a route for adding books (/add_book) using both HTTP GET and POST methods
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Get data from the form
        title = request.form.get('title')
        publication_year = int(request.form.get('publication_year'))
        author_id = int(request.form.get('author_id'))

        # Fetch ISBN from Open Library API based on the title
        isbn = fetch_isbn_from_api(title)

        # Create a new Book instance
        new_book = Book(isbn=isbn, title=title,
                        publication_year=publication_year, author_id=author_id)

        # Add and commit the new book to the database
        db.session.add(new_book)
        db.session.commit()

        # Display a success message
        success_message = "Book added successfully!"
        authors = Author.query.all()
        return render_template('add_book.html',
                               success_message=success_message,
                               authors=authors)

    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)




# makes an API request to the Open Library API to fetch ISBN based on a book title
def fetch_isbn_from_api(title):
    # Make a request to Open Library API
    response = requests.get(f'https://openlibrary.org/search.json?q={title}')
    data = response.json()

    # Extract ISBN from the API response
    isbn = None
    if 'docs' in data:
        docs = data['docs']
        if docs and 'isbn' in docs[0]:
            isbn = docs[0]['isbn'][0]

    return isbn
#route for deleting a book (/book/<int:book_id>/delete) using the HTTP POST method
@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    # Query the database for the book to be deleted
    book = Book.query.get_or_404(book_id)

    # Delete the book from the database
    db.session.delete(book)
    db.session.commit()

    # Display a success message
    success_message = "Book deleted successfully!"

    # Redirect the user to the homepage
    return redirect(url_for('home', message=success_message))



#runs the Flask app on the IP address "0.0.0.0" and port 5002 with enabled debug mode

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)


#create the database tables
# with app.app_context():
#     db.create_all()
