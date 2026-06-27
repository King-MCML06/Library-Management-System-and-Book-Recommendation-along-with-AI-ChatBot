
<div align="center">
  <h1>📚 Library Management & Book Recommendation System</h1>
  <p><strong>Empowering Libraries through Smart Automation and AI-ML</strong></p>
  <p><i>Developed as a course project for CS 1201 (IIT Patna)</i></p>
</div>

<br />

## 📖 Project Overview

Traditional library management systems often lack personalization and automation, making book discovery a struggle due to limited search features. Furthermore, manual borrowing and returning processes are time-consuming and prone to errors. 

**Our Solution:** We transformed the traditional library into an efficient, AI and ML-powered web platform. This system enhances accessibility and provides personalized recommendations while maintaining the warmth and interactivity of a physical library experience.

---

## ✨ Key Features

### 👤 User & Role Management
* **Secure Authentication:** Robust login and registration system.
* **Role-Based Access Control:** Distinct interfaces and permissions for Students and Admins.
* **User Profiles:** Clean interface displaying borrowed books, history, and personal details.

### 📚 Core Library Operations
* **Interactive Book Catalog:** Browse books with detailed metadata (title, author, publisher, publication year, ISBN, availability).
* **Automated Borrowing & Returning:** Dynamic stock and status updates upon transactions.
* **Real-time Tracking:** Accurate tracking of book availability across the system.
* **Admin Dashboard:** Comprehensive view of all book transactions, sorted chronologically for easy monitoring and reporting.

### 🤖 AI & Machine Learning Integration
* **Intelligent Book Recommendation System:** * Implements both **Popularity-Based** and **Collaborative Filtering** algorithms to suggest books tailored to user behavior.
* **Interactive AI Chatbot:**
  * Powered by GPT-4 / LangChain.
  * Assists users with library queries, understands reading preferences, and provides personalized book suggestions.
  * Features quick-replies for seamless interaction and strict privacy maintenance (clears conversation logs post-interaction).

### ✍️ Community Building
* **Blogs Page:** A dedicated space for readers to share thoughts, post reviews, and foster a thriving reading community.

---

## 🛠️ Tech Stack

| Layer | Technologies | Purpose |
| :--- | :--- | :--- |
| **Frontend** | HTML, CSS, Bootstrap, Jinja2, JavaScript | Responsive UI, Forms, Dynamic Book Listings |
| **Backend** | Flask, Flask-Login, Flask-WTF, FastAPI | Authentication, Business Logic, Routing |
| **Database** | PostgreSQL, SQLite, SQLAlchemy | Storing Books, Users, Transactions (`library.db`) |
| **Machine Learning** | Scikit-learn, Pandas, NumPy, TensorFlow | Data Ingestion, Preprocessing, Collaborative Filtering |
| **AI ChatBot** | Botpress, JavaScript, NLP, SDK & APIs | Conversational UI, User Interaction, Recommendations |

---

## 🏗️ Technical Architecture

### Data Structures & Algorithms
To ensure maximum efficiency, the system implements specific data structures for core operations:
* **Dictionary:** For Session User Authentication Data (Fast lookup).
* **SQLAlchemy ORM (Hash Tables, B-Trees):** For robust database indexing and retrieval of Books & Users.
* **Doubly Linked List / Queue (FIFO):** For processing borrowing transactions and tracking history.
* **2D Arrays:** For structured data rendering (HTML Tables).
* **Graphs (Adjacency List) & Heap Sort:** Core to the Recommendation System for analyzing user behavior and suggesting books efficiently.

### Database Schema Structure
The relational database utilizes four primary tables:
1. `reader`: Manages user credentials (id, username, roll_number, email_address, password_hash, role).
2. `book`: Stores inventory metadata (id, title, author, publisher, isbn, quantity, available, publication_year).
3. `circulation_desk`: Tracks transactions (reader_details, book_details, issue_date, return_date).
4. `post`: Manages blog entries (post_title, post_body, slug, date).

---

## 🧠 Machine Learning Pipeline

Our recommendation engine runs on a carefully designed pipeline:
1. **Data Ingestion:** Loading large datasets (Books, Users, Ratings) using NumPy and Pandas.
2. **Data Preprocessing:** Cleaning data, removing duplicates, and structuring formats.
3. **Popularity-Based Filtering:** Highlighting books with $\ge 250$ ratings and merging metadata with average rating statistics.
4. **Collaborative Filtering:** Filtering for active users ( $\ge 200$ ratings) and popular books ( $\ge 50$ ratings). We utilize a pivot table filled with user ratings and compute **Cosine Similarity** between books.
5. **Recommendation Generation:** Utilizing `difflib` for matching user input and returning precise, similar book recommendations based on the similarity scores.

---

## 🚀 Request Flow & Architecture

1. **User Action:** User submits a form (e.g., login, borrow).
2. **Backend Processing:** Flask processes the `POST` request, validating data through WTForms and querying the SQLAlchemy DB.
3. **Template Rendering:** Jinja2 integrates the backend data into the HTML structure.
4. **Delivery:** Fully rendered, responsive HTML is served to the client browser.

---

## 👨‍💻 Contributors

* **Kingshuk Haldar** (2401MC34) 
* **L. Sai Prem** (2401PH30) 

---
*Created for the CS 1201 coursework.*
