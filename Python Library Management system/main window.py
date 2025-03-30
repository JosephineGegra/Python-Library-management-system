import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QPushButton, QLineEdit, QMessageBox, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from Database import Database


class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database("Database.db")  # Initialize database with file
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('LUCT Library Management System')
        self.setGeometry(300, 300, 1200, 700)

        # Set background color to blue
        self.setStyleSheet("background-color: lightblue;")

        layout = QVBoxLayout()

        # Input fields
        form_layout = QHBoxLayout()

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText('Title')
        form_layout.addWidget(QLabel('Title:'))
        form_layout.addWidget(self.title_input)

        self.author_input = QLineEdit(self)
        self.author_input.setPlaceholderText('Author')
        form_layout.addWidget(QLabel('Author:'))
        form_layout.addWidget(self.author_input)

        self.isbn_input = QLineEdit(self)
        self.isbn_input.setPlaceholderText('ISBN')
        form_layout.addWidget(QLabel('ISBN:'))
        form_layout.addWidget(self.isbn_input)

        self.genre_input = QLineEdit(self)
        self.genre_input.setPlaceholderText('Genre')
        form_layout.addWidget(QLabel('Genre:'))
        form_layout.addWidget(self.genre_input)

        self.year_input = QLineEdit(self)
        self.year_input.setPlaceholderText('Publication Year')
        form_layout.addWidget(QLabel('Year:'))
        form_layout.addWidget(self.year_input)

        layout.addLayout(form_layout)

        # CRUD Buttons
        self.add_button = QPushButton('Add Book', self)
        self.add_button.clicked.connect(self.add_book)
        layout.addWidget(self.add_button)

        self.update_button = QPushButton('Update Book', self)
        self.update_button.clicked.connect(self.update_book)
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton('Delete Book', self)
        self.delete_button.clicked.connect(self.delete_book)
        layout.addWidget(self.delete_button)

        self.View_button = QPushButton('View Books', self)
        self.View_button.clicked.connect(self.View_books)
        layout.addWidget(self.View_button)

        # Search and Filter
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('Search by Title, Author, ISBN, or Genre')
        search_layout.addWidget(QLabel('Search:'))
        search_layout.addWidget(self.search_input)
        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.search_books)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Table to display books
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Title', 'Author', 'ISBN', 'Genre', 'Year'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.View_books()

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        isbn = self.isbn_input.text()
        genre = self.genre_input.text()
        year = self.year_input.text()

        # Check if fields are filled
        if title and author and isbn and genre and year:
            try:
                self.db.add_book(title, author, isbn, genre, year)
                QMessageBox.information(self, 'Success', 'Book added successfully!')
                self.View_books()  # Refresh the table with updated data
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to add book: {str(e)}')
        else:
            QMessageBox.warning(self, 'Error', 'All fields are required!')

    def update_book(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            book_id = int(self.table.item(selected_row, 0).text())
            title = self.title_input.text()
            author = self.author_input.text()
            isbn = self.isbn_input.text()
            genre = self.genre_input.text()
            year = self.year_input.text()

            # Use current table data if fields are empty
            title = title if title else self.table.item(selected_row, 1).text()
            author = author if author else self.table.item(selected_row, 2).text()
            isbn = isbn if isbn else self.table.item(selected_row, 3).text()
            genre = genre if genre else self.table.item(selected_row, 4).text()
            year = year if year else self.table.item(selected_row, 5).text()

            try:
                self.db.update_book(book_id, title, author, isbn, genre, year)
                QMessageBox.information(self, 'Success', 'Book updated successfully!')
                self.View_books()  # Refresh the table with updated data
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to update book: {str(e)}')
        else:
            QMessageBox.warning(self, 'Error', 'No book selected for update!')

    def delete_book(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            book_id = int(self.table.item(selected_row, 0).text())
            confirmation = QMessageBox.question(self, 'Confirm Deletion',
                                                f'Are you sure you want to delete book ID {book_id}?',
                                                QMessageBox.Yes | QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                self.db.delete_book(book_id)
                QMessageBox.information(self, 'Success', 'Book deleted successfully!')
                self.table.removeRow(selected_row)  # Remove the row from table view
        else:
            QMessageBox.warning(self, 'Error', 'No book selected for deletion!')

    def View_books(self):
        self.table.setRowCount(0)
        books = self.db.get_books()
        for book in books:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, data in enumerate(book):
                self.table.setItem(row_position, column, QTableWidgetItem(str(data)))

    def search_books(self):
        keyword = self.search_input.text()
        books = self.db.search_books(keyword)
        self.table.setRowCount(0)
        for book in books:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, data in enumerate(book):
                self.table.setItem(row_position, column, QTableWidgetItem(str(data)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
