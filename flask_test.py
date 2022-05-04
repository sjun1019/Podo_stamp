import os #디렉토리 절대 경로
from flask import Flask
from flask import render_template #template폴더 안에 파일을 쓰겠다
from flask import request #회원정보를 제출할 때 쓰는 request, post요청 처리
from flask import redirect #리다이렉트
from flask import flash
import math
#from flask_sqlalchemy import SQLAlchemy
from models import db
from models import User
from flask import session #세션
from flask_wtf.csrf import CSRFProtect #csrf
from form import RegisterForm, LoginForm, DetailForm, EditForm, FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

@app.route('/')
def mainpage():
    userid = session.get('userid')
    if userid == "admin":
        return redirect('/admin')
    if userid == None:
        return redirect('/login')
    point = 0
    star = 0
    stamp = 0
    user = User.query.filter_by(userid=userid).first()
    if user:
        point = user.point
        if point < 21:
            stamp = "stamp"+str(point)
        else:
            star = "star"+str(math.floor(point/20))
            stamp = "stamp"+str(point-20*math.floor(point/20))
    return render_template('podo.html', name=user.name, userid=userid, star=star, stamp=stamp)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    userid = session.get('userid')
    if userid != "admin":
        return redirect('/')
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    user_list = User.query.order_by(User.point.desc())
    if kw:
        search = '{}'.format(kw)
        user_list = User.query.filter((User.name==search) | (User.phone==search))
    user_list = user_list.paginate(page, per_page=10)
    return render_template('admin_page.html', userid=userid, user_list=user_list, page=page, kw=kw)


@app.route('/detail/<userid>', methods=['GET','POST'])
def detail(userid):
    form = DetailForm()
    if session['userid'] != "admin":
        return redirect('/')
    user = User.query.filter_by(userid=userid).first()
    if request.method == 'POST':
        user.point = form.data.get('point')
        db.session.commit()
        return redirect('/admin')
    return render_template('user_detail.html', user=user, form=form)
    
@app.route('/edit/<userid>', methods=['GET','POST'])
def edit(userid):
    userid = session.get('userid')
    if userid == None:
        return redirect('/login')
    form = EditForm()
    user = User.query.filter_by(userid=userid).first()
    if request.method == 'POST':
        user.phone = form.data.get('phone')
        user.name = form.data.get('name')
        db.session.commit()
        return redirect('/')
    return render_template('user_edit.html', user=user, userid=userid, form=form)


@app.route('/delete/<userid>', methods=['GET','POST'])
def delete(userid):
    userid = session.get('userid')
    if userid == None:
        return redirect('/login')
    form = FlaskForm()
    if session.get('userid') == "admin":
        user = User.query.filter_by(userid=userid).first()
        if request.method == 'POST':
            db.session.delete(user)
            db.session.commit()
            return redirect('/admin')
    elif userid != session.get('userid'):
        return redirect('/')
    user = User.query.filter_by(userid=userid).first()
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return redirect('/logout')
    return render_template('warning.html', userid=userid, form=form)


@app.route('/register', methods=['GET', 'POST']) #GET(정보보기), POST(정보수정) 메서드 허용
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit(): #유효성 검사. 내용 채우지 않은 항목이 있는지까지 체크
        user = User.query.filter_by(userid=form.userid.data).first()
        if not user:
            user = User()
            user.userid = form.data.get('userid')
            user.name = form.data.get('name')
            user.phone = form.data.get('phone')
            user.password = generate_password_hash(form.data.get('password'))
            user.point = 0
            user.tot = 0
            user.attend = 0
        else:
            flash('이미 존재하는 id 입니다')
        db.session.add(user) #DB저장
        db.session.commit() #변동사항 반영
        return redirect('/login')
    return render_template('register.html', form=form) #form이 어떤 form인지 명시한다


@app.route('/kstime', methods=['GET', 'POST'])
def kstime():
    userid = session.get('userid')
    if userid == None:
        return redirect('/login')
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    content_list = Content.query.order_by(User.point.desc())
    if kw:
        search = '{}'.format(kw)
        user_list = User.query.filter((User.name==search) | (User.phone==search))
    user_list = user_list.paginate(page, per_page=10)
    return render_template('kstime.html', userid=userid, user_list=user_list, rank_list2=enumerate(user_list.items), rank_list1=enumerate(user_list.items), page=page, kw=kw)


@app.route('/ranking', methods=['GET', 'POST'])
def ranking():
    userid = session.get('userid')
    if userid == None:
        return redirect('/login')
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    user_list = User.query.order_by(User.point.desc())
    if kw:
        search = '{}'.format(kw)
        user_list = User.query.filter((User.name==search) | (User.phone==search))
    user_list = user_list.paginate(page, per_page=10)
    return render_template('ranking.html', userid=userid, user_list=user_list, rank_list2=enumerate(user_list.items), rank_list1=enumerate(user_list.items), page=page, kw=kw)


@app.route('/login', methods=['GET','POST'])  
def login():
    form = LoginForm() #로그인폼
    if request.method == 'POST' and form.validate_on_submit(): #유효성 검사
        error = None
        user = User.query.filter_by(userid=form.userid.data).first()
        if not user:
            error = "회원 가입 후 이용하세요"
        elif not check_password_hash(user.password, form.password.data):
            error = "아이디 또는 비밀번호 틀림"
        if error is None:
            session.clear()
            session['userid'] = user.userid
            print('{}가 로그인 했습니다'.format(user.userid))
            return redirect('/') #성공하면 main.html로
        flash(error)
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')

if __name__ == "__main__":
    #데이터베이스---------
    basedir = os.path.abspath(os.path.dirname(__file__)) #현재 파일이 있는 디렉토리 절대 경로
    dbfile = os.path.join(basedir, 'db.sqlite') #데이터베이스 파일을 만든다

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #사용자에게 정보 전달완료하면 teadown. 그 때마다 커밋=DB반영
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #추가 메모리를 사용하므로 꺼둔다
    app.config['SECRET_KEY']='asdfasdfasdfqwerty' #해시값은 임의로 적음

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app) #app설정값 초기화
    db.app = app #Models.py에서 db를 가져와서 db.app에 app을 명시적으로 넣는다
    db.create_all() #DB생성

    app.run(host="0.0.0.0", port=8080, debug=True)