# 📚 Book Management Console Application

## 📖 Overview

This project is a **console-based Book Management Application** written in Python. It allows users to manage a collection of books using natural language-like commands. The application can:

* Add new books
* Display all books
* Search for books by keyword
* Store and retrieve data from an SQLite database

The program automatically understands user intent, extracts parameters, and performs the correct database operation.

---

## ⚙️ Features

### 1. Add a Book

Allows the user to add a book with a title and author.

**Command format:**

```
add "Title" author "Author"
```

**Example:**

```
add "The Hobbit" author "J.R.R. Tolkien"
```

---

### 2. List All Books

Displays all books stored in the database.

**Command format:**

```
list
```

---

### 3. Search for a Book

Searches for books containing a specific keyword in the title or author.

**Command format:**

```
search "keyword"
```

**Example:**

```
search "Tolkien"
```

---

## 🧠 Intent Recognition System

The application analyzes user input and determines the intended action:

| Command                     | Intent |
| --------------------------- | ------ |
| add "Title" author "Author" | ADD    |
| list                        | LIST   |
| search "word"               | SEARCH |

The system extracts parameters such as:

* Book title
* Author name
* Search keyword

---

## 🗄️ Database

The project uses **SQLite**, a lightweight file-based database.

### Database File

```
books.db
```

### Table Structure

```
books
```

| Column | Type    | Description |
| ------ | ------- | ----------- |
| id     | INTEGER | Primary key |
| title  | TEXT    | Book title  |
| author | TEXT    | Book author |

---

## 🏗️ Project Architecture

The project follows Object-Oriented Programming (OOP) principles.

### Main Components

#### 1. Database Layer

Responsible for:

* Connecting to SQLite
* Creating tables
* Inserting books
* Retrieving books
* Searching books

#### 2. Command Parser

Responsible for:

* Reading user input
* Detecting intent (ADD, LIST, SEARCH)
* Extracting parameters

#### 3. Application Controller

Responsible for:

* Connecting parser and database
* Executing correct operations

#### 4. Main Program

Responsible for:

* Running the console loop
* Accepting user commands

---

## 📂 Project Structure

```
project/
│
├── main.py
├── database.py
├── parser.py
├── models.py
├── books.db
└── README.md
```

---

## ▶️ How to Run

### 1. Install Python

Make sure Python 3 is installed:

```
python --version
```

### 2. Run the program

```
python main.py
```

---

## 💻 Example Usage

```
> add "The Hobbit" author "J.R.R. Tolkien"
Book added successfully.

> list
1. The Hobbit - J.R.R. Tolkien

> search "Hobbit"
1. The Hobbit - J.R.R. Tolkien
```

---

## 🧩 OOP Principles Used

### Encapsulation

Database operations are encapsulated inside the database class.

### Separation of Concerns

* Parser handles input
* Database handles storage
* Main handles execution

### Modularity

Each component has a specific responsibility.

---

## 🚀 Future Improvements

Possible enhancements include:

* Delete books
* Update books
* GUI interface
* Web version
* User authentication

---

## 🧾 Requirements

* Python 3.x
* SQLite (included with Python)

---

## ✅ Summary

This project demonstrates:

* Console application development
* SQLite database integration
* Intent recognition
* Object-Oriented Programming
* Clean architecture

It is suitable for beginners learning Python, databases, and software design.

---

## 👨‍💻 Author

Created as a learning project.
