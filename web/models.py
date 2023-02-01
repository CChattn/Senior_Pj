from flask_login import UserMixin
from . import db
class User(UserMixin, db.Model):
    __tablename__ = 'user_new'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    
class User_interaction(db.Model):
    __tablename__ = 'User_interaction_new'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100))
    article_id = db.Column(db.Integer)
    article_title = db.Column(db.Text)
    interaction_type = db.Column(db.Text)
    timestamp = db.Column(db.Text)
    
class LDA_group(UserMixin, db.Model):
    __tablename__ = 'LDA_group'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    Authors = db.Column(db.Text)
    Title = db.Column(db.Text)
    Year = db.Column(db.Integer)
    Sourcetitle = db.Column(db.Text)
    DOI = db.Column(db.Text)
    Link = db.Column(db.Text)
    Affiliations = db.Column(db.Text)
    Authorswithaffiliations = db.Column(db.Text)
    Abstract = db.Column(db.Text)
    AuthorKeywords = db.Column(db.Text)
    IndexKeywords = db.Column(db.Text)
    Publisher = db.Column(db.Text)
    AbbreviatedSourceTitle = db.Column(db.Text)
    DocumentType = db.Column(db.Text)
    institution = db.Column(db.Text)
    Citedby = db.Column(db.Integer)
    LDA_group_num = db.Column(db.Integer)
    