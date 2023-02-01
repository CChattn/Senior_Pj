from flask import Blueprint,render_template, redirect, url_for, request, flash ,Flask, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db
import os
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/login', methods=['POST']) #ถ้ามีการ login ให้ redirect ไปที่ไหน

def login_post():
    email = request.form.get('email')
    
    remember = True if request.form.get('remember') else False
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        new_user = User(email=email) #กำหนดว่าให้สิ่งที่กรอกในฟอร์ม = อะไรใน database   
        #เพิ่มลงใน database
        db.session.add(new_user)
        db.session.commit()
        
        check_email = User.query.filter_by(email=email).first()
        login_user(check_email)
        return redirect(url_for('main.index'))
    
    login_user(user, remember=remember)
    return redirect(url_for('main.index')) #ไปไหนดี


#ggauth part
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" 
GOOGLE_CLIENT_ID = "75707457009-625guvkl4h53sj553fsrme3lvm2icq6f.apps.googleusercontent.com"  #enter your client id you got from Google console
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")  #set the path to where the .json file you got Google console is

flow = Flow.from_client_secrets_file(  #Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  #here we are specifing what do we get after the authorization
    redirect_uri="http://127.0.0.1:5000/callback"  #and the redirect URI is the point where the user will end up after the authorization
)

def login_is_required(function):  #a function to check if the user is authorized or not
    def wrapper(*args, **kwargs):
        if "google_id" not in session:  #authorization required
            return abort(401)
        else:
            return function()

    return wrapper

@auth.route("/ggauth")
def ggauth():
    authorization_url, state = flow.authorization_url()  #asking the flow class for the authorization (login) url
    session["state"] = state
    return redirect(authorization_url)


@auth.route("/callback")  #this is the page that will handle the callback process meaning process after the authorization
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  #state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")  #defing the results to show on the page
    session["email"] = id_info.get("email")
    
    #check for login
    ggemail = session["email"]
    ggpassword = "-"
    ggcheck_email = User.query.filter_by(email=ggemail).first()
    
    if ggcheck_email:
        login_user(ggcheck_email)
        redirect(url_for('main.index'))    
    else:
        ggnew_user = User(email=ggemail, password=ggpassword) #กำหนดว่าให้สิ่งที่กรอกในฟอร์ม = อะไรใน database

        #เพิ่มลงใน database
        db.session.add(ggnew_user)
        db.session.commit()
        
        ggcheck_email = User.query.filter_by(email=ggemail).first()
        login_user(ggcheck_email)
        return redirect(url_for('main.index'))
        
    
    return redirect(url_for('main.index'))  #the final page where the authorized users will end up


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))