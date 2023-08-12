#Importing the SQLAlchemy class
from flask_sqlalchemy import SQLAlchemy
#SQLAlchemy instance named db, for interacting the database
db = SQLAlchemy()




class Author(db.Model):
    """ Define the Author class as a subclass of db.Model
Defines columns for the author table: id, name, birth_date, and date_of_death."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #primary key, autoincrement
    name = db.Column(db.String(100), nullable=False) #stores the author's name
    birth_date = db.Column(db.Date, nullable=True) #store birth dates
    date_of_death = db.Column(db.Date, nullable=True) #store death dates

    # Define the __repr__ method for representing Author instances
    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"

    # Define the __str__ method for displaying author names
    def __str__(self):
        return self.name


class Book(db.Model):
    """ Defines the Book class representing the book table.
Define columns: id, isbn, title, publication_year, and author_id.   """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), nullable=False, unique=True)  #stores the International Standard Book Number
    title = db.Column(db.String(255), nullable=False) #stores the book title
    publication_year = db.Column(db.Integer, nullable=True) #stores the year of publication
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), #foreign key that links to the id column of the author table
                          nullable=False)
    # Define a relationship with the Author class
    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    # Define the __repr__ method for representing Book instances
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author_id={self.author_id})>"

    # Define the __str__ method for displaying book titles
    def __str__(self):
        return self.title
