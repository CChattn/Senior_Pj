from flask import Blueprint,render_template, request,redirect, url_for, flash
from flask_login import current_user, login_required
from . import db
from .models import User_interaction,LDA_group
import random
from datetime import datetime
import pytz

onclick = Blueprint('onclick', __name__,static_folder='static')

#rendering the HTML page which has the button
@onclick.route('/')
def index():
   return render_template('index.html')

#background process happening without any refreshing
@onclick.route("/page")
@login_required
def page():
   if current_user.is_authenticated:
      select_id = request.args.get('id', 0, type=int)
      email = current_user.email
      get_article = LDA_group.query.filter_by(id=select_id).first()
      article_title = get_article.Title 
      bangkok = pytz.timezone("Asia/Bangkok") 
      timestamp = str(datetime.now(bangkok))

      user_interaction = User_interaction(email=email,
                                          article_id=select_id,
                                          article_title=article_title,                             
                                          interaction_type="read",
                                          timestamp=timestamp)

      db.session.add(user_interaction)
      db.session.commit()
   else:
      return redirect(url_for('auth.login')) 
   data = LDA_group.query.get(select_id)
   # แสดงข้อมูลกลุ่มที่ได้จัดไว้
   LDA_grouping = data.LDA_group_num #ได้เลขกลุ่มออกมา
   recommended_group = LDA_group.query.filter_by(LDA_group_num=LDA_grouping).all()
   random_rec = random.sample(recommended_group,5)
   return render_template("page.html",data=data, name=current_user.name,datas=random_rec)

@onclick.route("/link")
@login_required
def link():
   if current_user.is_authenticated:
      select_id = request.args.get('id', 0, type=int)
      email = current_user.email
      get_article = LDA_group.query.filter_by(id=select_id).first()
      article_title = get_article.Title 
      link = get_article.Link
      bangkok = pytz.timezone("Asia/Bangkok") 
      timestamp = str(datetime.now(bangkok))

      user_interaction = User_interaction(email=email,
                                          article_id=select_id,
                                          article_title=article_title,                             
                                          interaction_type="link",
                                          timestamp=timestamp)

      db.session.add(user_interaction)
      db.session.commit()
   else:
      return redirect(url_for('auth.login')) 
   return redirect((f"{link}"))

   
