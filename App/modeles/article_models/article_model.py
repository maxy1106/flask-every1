from datetime import datetime

from App.ext import db
from App.modeles import BaseModel


class Article(BaseModel):
    title = db.Column(db.String(128),nullable=False)
    context = db.Column(db.Text,nullable=False)
    nickname = db.Column(db.String(128),nullable=False)
    publishTime = db.Column(db.DateTime)
    lastModifyTime = db.Column(db.DateTime, default=datetime.now())
    isDelete = db.Column(db.Boolean,default=False)
    authorId = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    author = db.relationship('User', backref=db.backref('article'), lazy=True)
