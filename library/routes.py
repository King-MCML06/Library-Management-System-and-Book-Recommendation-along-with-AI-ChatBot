from flask import (
    Flask, current_app, flash, redirect, render_template, request, session, url_for
)
from flask_login import login_user, logout_user, login_required, current_user

import pickle
import pandas as pd
import numpy as np
import difflib

from library import app
from library.forms import RegisterForm, LoginForm, PostForm, BookForm
from library.models import Reader, Book, Circulation_Desk, Post
from library import db

popular_df = pickle.load(open('popular.pkl','rb'))
collab_df = pickle.load(open('collab_df.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
sim_scores = pickle.load(open('sim_scores.pkl','rb'))
unique_list = pickle.load(open('unique_books.pkl','rb'))

@app.route('/')
def home_page():
    book_count = Book.query.count()
    available_count = Book.query.filter_by(available = True).count()
    borrowed_count = Circulation_Desk.query.filter_by(return_date = None).count()
    users_count = Reader.query.filter_by(role = "Student").count()
    return render_template('home.html', book_count = book_count, available_count = available_count, 
                           borrowed_count = borrowed_count, users_count = users_count)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        attempted_user = Reader.query.filter_by(username = login_form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=login_form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! Logged in successfully as : {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password do not match! Please try again!', category='danger')

    return render_template('login.html', form=login_form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You are now logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/view_profile')
def view_profile():
    user_borrowings = db.session.query(Book).join(Circulation_Desk).filter(
        Circulation_Desk.reader_details == current_user.id,
        Circulation_Desk.return_date == None).all()
    return render_template('user_profile.html', user_borrowings = user_borrowings)

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = Reader(username = form.username.data,
                          role = form.role.data,
                          roll_number = form.roll_number.data,
                          email_address = form.email_address.data,
                          password = form.password1.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home_page'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating the account: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/library')
@login_required 
def view_library():
    page = request.args.get('page',1, type=int)
    search_book = request.args.get('search', '')
    if search_book:
        pagination = Book.query.filter(Book.title.ilike(f"%{search_book}%")).paginate(page=page, per_page=50, error_out=False)
    else:
        pagination = Book.query.paginate(page=page, per_page=50, error_out=False)
    borrowed_books = {borrow.book_details for borrow in Circulation_Desk.query.filter_by(reader_details= current_user.id, return_date = None).all()}
    return render_template('booksdb.html', all_books = pagination, borrowed_books=borrowed_books)

@app.route('/borrow/<int:book_id>', methods =['post'])
@login_required
def borrow_book(book_id):
    book = Book.query.get(book_id)

    if(book.available == 'false'):
        flash(f'Book is currently unavailable !', category='danger')
        return redirect(url_for('view_library'))
    
    already_borrowed = Circulation_Desk.query.filter_by(reader_details = current_user.id,
                                                      book_details = book.id,
                                                      return_date = None).first()
    if already_borrowed :
         flash(f'You have already borrowed this book !', category='warning')
         return redirect(url_for('view_library'))
    
    new_borrow = Circulation_Desk(reader_details = current_user.id, book_details = book.id)
    book.quantity = book.quantity-1;
    if book.quantity == 0:
        book.available = False

    db.session.add(new_borrow)
    db.session.commit()
    flash(f"You have successfully borrowed '{book.title}'", category='success')
    return redirect(url_for('view_library'))

@app.route('/return/<int:book_id>', methods=['POST'])
@login_required
def return_book(book_id):
    borrowed_entry = Circulation_Desk.query.filter_by(reader_details = current_user.id,
                                                      book_details = book_id,
                                                      return_date = None).first()
    borrowed_entry.return_date = db.func.current_timestamp()

    book = Book.query.get(book_id)
    book.quantity +=1
    if book.quantity > 0:
        book.available = True
    else:
        book.available = False
    db.session.commit()

    flash(f'Book returned successfully !', category='success')
    return redirect(url_for('view_library'))

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(title = form.title.data,
                        author = form.author.data,
                        publisher = form.publisher.data,
                        publication_year = form.publication_year.data,
                        isbn = form.isbn.data,
                        quantity = form.quantity.data,
                        image_url = form.image_url.data)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('view_library'))
    
    if form.errors != {}:
            flash(f'Book could npot be added to database !', category='danger')
    return render_template('add_book.html', form = form)

@app.route('/history')
def circulation_history():
    history = Circulation_Desk.query.filter(Circulation_Desk.return_date == None).order_by(Circulation_Desk.issue_date).all()
    return render_template('history.html', history = history)
    
@app.route('/explore')
def explore_books():
    return render_template('trending.html',
                           book_name = list(popular_df['Book-Title'].values),
                           rating = list(popular_df['Avg_Rating'].values),
                           author = list(popular_df['Book-Author'].values),
                           publisher = list(popular_df['Publisher'].values),
                           image = list(popular_df['Image-URL-M'].values)
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommendations.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    book_name = request.form.get('book_name')
    book_titles = books['Book-Title'].tolist()
    find_close_match = difflib.get_close_matches(book_name,book_titles)
    close_match = find_close_match[0]
    index = np.where(collab_df.index == close_match)[0][0]
    similar_choices = sorted(list(enumerate(sim_scores[index])),key = lambda x:x[1],reverse = True)[1:13]
    data = []
    for i in similar_choices:
        item = []
        temp_df = books[books['Book-Title'] == collab_df.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Publisher'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return render_template('recommendations.html', data = data)

@app.route('/blogs')
def blog_page():
    blogs = Post.query.all()
    return render_template('blogs.html', blogs = blogs)

@app.route('/blogs/<slug>')
def blog_details(slug):
    blog = Post.query.filter(Post.slug == slug).first()
    return render_template('blogdetails.html', post = blog)

@app.route('/create_post',  methods=['GET','POST'])
def create_post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        new_post = Post(post_title = post_form.post_title.data,
                    post_body = post_form.post_body.data)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog_details', slug = new_post.slug))
    return render_template('create_post.html', form=post_form)  
