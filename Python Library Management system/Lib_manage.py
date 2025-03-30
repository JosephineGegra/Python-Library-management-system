import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt

# Assuming Database is implemented elsewhere and properly imported.
sys.path.append('D:\\Users\\gegra\\OneDrive\\Documents\\Library system\\PycharmProjects\\pythonProject2')
from Database import Database  # Ensure the path and module are correct.

class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()  # Ensure Database class is implemented correctly
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Library Management System')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Input fields
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText('Title')
        layout.addWidget(self.title_input)

        self.author_input = QLineEdit(self)
        self.author_input.setPlaceholderText('Author')
        layout.addWidget(self.author_input)

        self.genre_input = QLineEdit(self)
        self.genre_input.setPlaceholderText('Genre')
        layout.addWidget(self.genre_input)

        self.year_input = QLineEdit(self)
        self.year_input.setPlaceholderText('Publication Year')
        layout.addWidget(self.year_input)

        self.quantity_input = QLineEdit(self)
        self.quantity_input.setPlaceholderText('Quantity')
        layout.addWidget(self.quantity_input)

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

        self.load_button = QPushButton('Load Books', self)
        self.load_button.clicked.connect(self.load_books)
        layout.addWidget(self.load_button)

        # Table to display books
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Title', 'Author', 'Genre', 'Year', 'Quantity'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_books()

    def add_book(self):
        try:
            title = self.title_input.text()
            author = self.author_input.text()
            genre = self.genre_input.text()
            year = int(self.year_input.text())
            quantity = int(self.quantity_input.text())

            if not title or not author or not genre:
                raise ValueError("All fields must be filled.")

            self.db.add_book(title, author, genre, year, quantity)
            QMessageBox.information(self, 'Success', 'Book added successfully!')
            self.load_books()
        except ValueError as ve:
            QMessageBox.warning(self, 'Input Error', f"Invalid input: {ve}")
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {e}")

    def update_book(self):
        try:
            row = self.table.currentRow()
            if row == -1:
                raise ValueError("No book selected for update.")

            book_id = int(self.table.item(row, 0).text())
            title = self.title_input.text()
            author = self.author_input.text()
            genre = self.genre_input.text()
            year = int(self.year_input.text())
            quantity = int(self.quantity_input.text())

            if not title or not author or not genre:
                raise ValueError("All fields must be filled.")

            self.db.update_book(book_id, title, author, genre, year, quantity)
            QMessageBox.information(self, 'Success', 'Book updated successfully!')
            self.load_books()
        except ValueError as ve:
            QMessageBox.warning(self, 'Input Error', f"Invalid input: {ve}")
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {e}")

    def delete_book(self):
        try:
            row = self.table.currentRow()
            if row == -1:
                raise ValueError("No book selected for deletion.")

            book_id = int(self.table.item(row, 0).text())
            self.db.delete_book(book_id)
            QMessageBox.information(self, 'Success', 'Book deleted successfully!')
            self.load_books()
        except ValueError as ve:
            QMessageBox.warning(self, 'Input Error', f"Invalid input: {ve}")
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {e}")

    def load_books(self):
        try:
            books = self.db.get_books()
            self.table.setRowCount(0)

            for book in books:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                for col, data in enumerate(book):
                    self.table.setItem(row_position, col, QTableWidgetItem(str(data)))

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred while loading books: {e}")

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
