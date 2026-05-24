# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news_aggregator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)

# Models
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    votes = db.Column(db.Integer, default=0)
    tags = db.relationship('Tag', secondary='article_tag', backref=db.backref('articles', lazy=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

article_tag = db.Table('article_tag',
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    article = db.relationship('Article', backref=db.backref('comments', lazy=True))

# Routes
@app.route('/')
def index():
    articles = Article.query.order_by(Article.votes.desc()).all()
    return render_template('index.html', articles=articles)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        description = request.form['description']
        tag_names = request.form['tags'].split(',')
        
        article = Article(title=title, url=url, description=description)
        db.session.add(article)
        
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name.strip()).first()
            if not tag:
                tag = Tag(name=tag_name.strip())
                db.session.add(tag)
            article.tags.append(tag)
        
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('submit.html')

@app.route('/vote/<int:article_id>', methods=['POST'])
def vote(article_id):
    article = Article.query.get_or_404(article_id)
    article.votes += 1
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/article/<int:article_id>', methods=['GET', 'POST'])
def article(article_id):
    article = Article.query.get_or_404(article_id)
    if request.method == 'POST':
        content = request.form['content']
        comment = Comment(content=content, article=article)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('article', article_id=article_id))
    return render_template('article.html', article=article)

# Initialize DB
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)