from library import db
from library import bcrypt
from library import login_manager
from flask_login import UserMixin
import re
import time

@login_manager.user_loader
def load_user(user_id):
    return Reader.query.get(int(user_id))

class Reader(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    roll_number = db.Column(db.String(length=8), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=75), nullable=False)
    role = db.Column(db.String(length=15), nullable=False, default="Student")
    borrowings = db.relationship('Circulation_Desk', backref='reader', lazy=True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_password):
        self.password_hash = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __repr__(self):
       return f"User('{self.username}', '{self.roll_number}', '{self.email_address}', '{self.role}')"

class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=50), nullable=False, unique=True)
    author = db.Column(db.String(length=50), nullable=False)
    publisher = db.Column(db.String(length=30), nullable=False)
    isbn = db.Column(db.String(length=15), nullable=False, unique=True)
    quantity = db.Column(db.Integer(), nullable=False)
    available = db.Column(db.Boolean, default=True)
    publication_year = db.Column(db.Integer(), nullable=False)
    image_url = db.Column(db.String(length=400), nullable=True)
    issued_by = db.relationship('Circulation_Desk', backref='book', lazy=True)

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.publisher}', {self.available}, {self.quantity}, '{self.publication_year}', '{self.image_url}')"
    
class Circulation_Desk(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    reader_details = db.Column(db.Integer(), db.ForeignKey('reader.id'))
    book_details = db.Column(db.Integer(), db.ForeignKey('book.id'))
    issue_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    return_date = db.Column(db.DateTime, nullable = True)

    def __repr__(self):
        return f"Book('{self.issue_date}', '{self.return_date})"

def slugify(str):
    pattern = r'[^\w]+'
    return re.sub(pattern, '-', str).strip('-').lower()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    post_title = db.Column(db.String(length= 75), nullable=False, unique=False)
    post_body = db.Column(db.String(length= 300), nullable=True, unique=False)
    slug = db.Column(db.String(length= 100), unique=True)
    post_details = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.post_title:
            self.slug = slugify(self.post_title)
        else:
            self.slug = slugify(str(int(time.time())))
    
    def __repr__(self):
        return f"Post('{self.id}', '{self.post_title}')"