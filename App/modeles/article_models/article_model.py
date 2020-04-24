from datetime import datetime

from App.ext import db
from App.modeles import BaseModel


class Article(BaseModel):
    title = db.Column(db.String(128),nullable=False)
    context = db.Column(db.Text,nullable=False)
    cateId = db.Column(db.Integer,db.ForeignKey("category.id"),nullable=False)
    publishTime = db.Column(db.DateTime)
    lastModifyTime = db.Column(db.DateTime, default=datetime.now())
    isDelete = db.Column(db.Boolean,default=False)
    fontReadNo = db.Column(db.Integer,default=0)
    detailsUrl = db.Column(db.String(200),default="http://127.0.0.1:5000/articles/articles/?articleid=")
    shareNo = db.Column(db.Integer,default=0)
    titlePic = db.Column(db.String(128))
    authorId = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    authorPhoto = db.Column(db.String(128))
    author = db.relationship('User', backref=db.backref('article'), lazy=True)
    cate = db.relationship('Category', backref=db.backref('article'), lazy=True)


class Category(BaseModel):
    """
    目录结构
    """
    __tablename__ = "category"
    name = db.Column(db.String(30),unique=True)
    desc = db.Column(db.Text)
    # category_type = db.Column(choices = CATEGORY_TYPE)
    category_type = db.Column(db.String(30),default=1)
    # parent_category = db.Column(db.ForeignKey("self"))
    parent_cateory = db.Column(db.String(30),default=1)
    is_tab = db.Column(db.Boolean,default=False)
    add_time = db.Column(db.DateTime,default=datetime.now())
    models = db.Column(db.Text)