from flask import render_template,Blueprint
from flask_login import login_required, current_user
from flask import request
from . import db
from .models import LDA_group

main = Blueprint('main', __name__,static_folder='static')


#template เราจะใช้ jinja
@main.route('/') #กำหนดว่าถ้า path นี้จะเป็นอะไร(กำหนดเส้นทาง)
def index(): 
    # ระบบ search 
    
    search = request.args.get('search[value]')

    if search:
        query = query.filter(db.or_(LDA_group.Title.like(f'%{search}%')))
        total_filtered = query
    else:
        total_filtered = LDA_group

    ROWS_PER_PAGE = 16
    page = request.args.get('page', 1, type=int)
    # ดึงข้อมูลจาก database (ต้องไปเพิ่มข้อมูล csv ใส่ database ก่อนนะ)
    scopus = total_filtered.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    if current_user.is_authenticated:
        return render_template("index.html",datas=scopus, name=current_user.name)
    else:
        return render_template("index.html",datas=scopus)

@main.route('/profile') #กำหนดว่าถ้า path นี้จะเป็นอะไร(กำหนดเส้นทาง)
@login_required #ต้อง login ก่อน ถึงจะให้เข้า
def profile():
    return render_template("profile.html", name=current_user.name)


# dynamic route คือ url จะเปลี่ยนไปตามค่าที่เราส่งไป
@main.route('/user/<name>/<age>') #ต้องกรอก path ให้ครบไม่งั้น error
def member(name,age):
    return "<h1>สวัสดีสมาชิก : {} อายุ {}</h1>".format(name,age)