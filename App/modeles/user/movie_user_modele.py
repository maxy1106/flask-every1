
from werkzeug.security import generate_password_hash, check_password_hash

from App.ext import db
from App.modeles import BaseModel
from App.modeles.user.model_constant import PERMISSION_NONE

class User(BaseModel):
    __tablename__ = "user"
    userName = db.Column(db.String(128),unique=True)
    userPassword = db.Column(db.String(1024))
    addressCode = db.Column(db.String(256))
    addressDefaultName = db.Column(db.String(256))
    userPhoto = db.Column(db.String(128))
    userIntroduction = db.Column(db.String(1024))
    isBindingPhone = db.Column(db.Boolean,default=False)
    phone = db.Column(db.String(32),unique=True)
    isBindingWx = db.Column(db.Boolean,default=False)
    wxId = db.Column(db.String(128))
    isVip = db.Column(db.Boolean,default=False)
    memberFlag = db.Column(db.Boolean,default=False)
    memberLevel = db.Column(db.String(10))
    memberStatus = db.Column(db.String(16))
    money = db.Column(db.FLOAT)
    myBalanceIcon = db.Column(db.String(128))
    myBalanceTitle = db.Column(db.String(128))

    @property
    def userpassword(self):
        raise Exception("password not access")

    @userpassword.setter
    def userpassword(self,value):
        self.userPassword = generate_password_hash(value)

    def check_passwprd(self,password):
        print(check_password_hash(self.userPassword,password))
        return check_password_hash(self.userPassword,password)

