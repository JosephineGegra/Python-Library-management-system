import sqlite3


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT NOT NULL,
            genre TEXT NOT NULL,
            year TEXT NOT NULL
        )
        '''
        self.connection.execute(query)
        self.connection.commit()

    def add_book(self, title, author, isbn, genre, year):
        query = 'INSERT INTO books (title, author, isbn, genre, year) VALUES (?, ?, ?, ?, ?)'
        self.connection.execute(query, (title, author, isbn, genre, year))
        self.connection.commit()

    def update_book(self, book_id, title, author, isbn, genre, year):
        query = """
        UPDATE books
        SET title = ?, author = ?, isbn = ?, genre = ?, year = ?
        WHERE id = ?
        """
        self.connection.execute(query, (title, author, isbn, genre, year, book_id))
        self.connection.commit()

        def delete_book(self, book_id):
            query = 'DELETE FROM books WHERE id = ?'
            self.connection.execute(query, (book_id,))
            self.connection.commit()
        self.connection.execute(query, (book_id,))
        self.connection.commit()

    def get_books(self):
        query = 'SELECT * FROM books'
        cursor = self.connection.execute(query)
        return cursor.fetchall()

    def get_book_by_id(self, book_id):
        query = "SELECT * FROM books WHERE id = ?"
        cursor = self.connection.execute(query, (book_id,))
        return cursor.fetchone()  # Returns a single record as a tuple

    def search_books(self, keyword):
        query = '''
        SELECT * FROM books
        WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? OR genre LIKE ?
        '''
        wildcard_keyword = f"%{keyword}%"
        cursor = self.connection.execute(query,
                                         (wildcard_keyword, wildcard_keyword, wildcard_keyword, wildcard_keyword))
        return cursor.fetchall()

    def close(self):
        self.connection.close()

    def delete_book(self, book_id):
        pass
