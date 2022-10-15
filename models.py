from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #SQLAlchemy를 사용해 데이터베이스 저장

class User(db.Model): #데이터 모델을 나타내는 객체 선언
    __tablename__ = 'user_table' #테이블 이름
    
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    point = db.Column(db.Integer(), nullable=True)
    # tot = db.Column(db.Integer(), nullable=True)
    # attend = db.Column(db.Integer(), nullable=True)
    # temp = db.Column(db.Integer(), nullable=True)


    def set_password(self, password):
        self.password = generate_password_hash(password)
 
    def check_password(self, password):
        return check_password_hash(self.password, password)

class NewPoint(db.Model): #데이터 모델을 나타내는 객체 선언
    __tablename__ = 'new_point_table' #테이블 이름
    
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(150), unique=True, nullable=False)
    point = db.Column(db.Integer(), nullable=True)

class Attend(db.Model):
    __tablename__ = 'attend_table'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    userid = db.Column(db.String(150), unique=True, nullable=False)
    attend = db.Column(db.Boolean, nullable=False)
    
class Content(db.Model): #데이터 모델을 나타내는 객체 선언
    __tablename__ = 'content_table' #테이블 이름
    
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(150), unique=True, nullable=False)
    title = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.String(2000), unique=True, nullable=False)
    like = db.Column(db.Integer(), nullable=True)
    unlike = db.Column(db.Integer(), nullable=True)
    view = db.Column(db.Integer(), nullable=True)


class Comment(db.Model): #데이터 모델을 나타내는 객체 선언
    __tablename__ = 'comment_table' #테이블 이름
    
    id = db.Column(db.Integer, primary_key=True)
    cont_id = db.Column(db.Integer(), nullable=False)
    cmnt_grp = db.Column(db.Integer(), nullable=False)
    userid = db.Column(db.String(150), unique=True, nullable=False)
    comment = db.Column(db.String(500), unique=True, nullable=False)
    like = db.Column(db.Integer(), nullable=True)
    unlike = db.Column(db.Integer(), nullable=True)