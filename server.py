from flask import Flask, render_template, make_response, request, redirect
import bcrypt
import uuid
import hashlib
from markupsafe import escape
from pymongo import MongoClient

mongo_client = MongoClient("mongo")
db = mongo_client["cse-312-project"]
user_collection = db["user"]
token_collection = db["auth_token"]
post_collection = db["posts"]

server = Flask(__name__, template_folder='public')

@server.route('/')
@server.route('/public/index.html')
def homepage():
    response = make_response(render_template('index.html'))
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@server.route('/public/style.css')
def homepage_css():
    response = make_response(render_template('style.css'))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "text/css"
    return response

@server.route('/public/nav.css')
def nav_css():
    response = make_response(render_template('nav.css'))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "text/css"
    return response

@server.route('/public/post.css')
def post_css():
    response = make_response(render_template('post.css'))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "text/css"
    return response

@server.route('/nav.html')
@server.route('/public/nav.html')
def nav_html():
    token = request.cookies.get("auth_token")

    if token:
        sha256 = hashlib.sha256()
        sha256.update(token.encode())
        hash_token = sha256.hexdigest()
        getToken = token_collection.find({"hash-token": str(hash_token)})
        getToken = list(getToken)

        if len(getToken) != 0:
            name = "Hello, " + getToken[0]["username"] + "!"
            logout = "Logout"
            visibility = "hidden"
            href = "/logout"
        else:
            name = "Guest"
            logout = "Sign Up"
            visibility = "visible"
            href="/public/signup.html"
    else:
        name = "Guest"
        logout = "Sign Up"
        visibility = "visible"
        href="/public/signup.html"

    response = make_response(render_template('nav.html',  name=name, logout=logout, visibility=visibility, href=href))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "text/html"
    return response

@server.route('/public/assets/temp-logo.png')
def logo():
    with open("public/assets/temp-logo.png", "rb") as file:
        byte_string = file.read()
        response = make_response(byte_string)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Content-Type"] = "image/png"
    return response

@server.route('/public/assets/favicon.ico')
def icon():
    with open("public/assets/temp-logo.png", "rb") as file:
        byte_string = file.read()
        response = make_response(byte_string)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Content-Type"] = "image/x-icon"
    return response
    
@server.route('/public/functions.js')
def homepage_js():
    response = make_response(render_template('functions.js'))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "text/javascript"
    return response

@server.route('/signup.html')
@server.route('/public/signup.html')
def signup_html():
    response = make_response(render_template('signup.html'))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "text/html"
    return response

@server.route('/login.html')
@server.route('/public/login.html')
def login_html():
    response = make_response(render_template('login.html'))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "text/html"
    return response

@server.route('/create_account', methods = ['POST'])
def registration_check():
    msg = ""
    email = request.form["signup_email"]
    username = request.form["signup_username"]
    password = request.form["signup_password"]
    re_password = request.form["signup_re_password"]
    found_username =  user_collection.find({"username": str(username)})
    found_username = list(found_username)

    if password != re_password:
        msg = "passwords are not the same"
    elif len(found_username) != 0:
        msg = "Username already existed"
    else:
        password_bytes = password.encode()
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password_bytes, salt)
        user_information_dict = {"username": str(username), "password": hash_password, "email": str(email)}
        user_collection.insert_one(user_information_dict)
        response = make_response(redirect("/"))
        return response

    response = make_response(render_template('signup.html', msg = msg))
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@server.route('/login', methods = ['POST'])
def login_check():
    msg = ""
    username = request.form["login_username"]
    password = request.form["login_password"]
    password_bytes = password.encode()
    user =  user_collection.find({"username": str(username)})
    user = list(user)
    if len(user) == 0:
        msg = "Incorrect username or password! Please try again"
    else:
        hashed_password = user[0]["password"]
        check_password = bcrypt.checkpw(password_bytes, hashed_password)
        if check_password:  
            token = uuid.uuid4()
            token_bytes = str(token).encode()
            sha256 = hashlib.sha256()
            sha256.update(token_bytes)
            hash_token = sha256.hexdigest()
            token_dict = {"username": str(username), "hash-token": str(hash_token)}
            token_collection.insert_one(token_dict)
            response = make_response(redirect("/"))
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.set_cookie(key = "auth_token", value = str(token), max_age = 3600, httponly = True)
            return response
        else:
            msg = "Incorrect username or password! Please try again"

    response = make_response(render_template('login.html', msg = msg))
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@server.route('/logout')
def logout_check():
    token = request.cookies.get("auth_token")

    sha256 = hashlib.sha256()
    sha256.update(token.encode())
    hash_token = sha256.hexdigest()
    token_collection.delete_many({"hash-token": hash_token})

    response = make_response(redirect("/"))
    response.set_cookie(key = "auth_token", value = str(token), max_age = 0, httponly = True)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@server.route('/create-post')
def post_render():
    response = make_response(render_template('post.html'))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "text/html"
    return response


@server.route('/create_post', methods = ['POST'])
def post_check():

    msg = ""
    token = request.cookies.get("auth_token")

    if token != None:

        sha256 = hashlib.sha256()
        sha256.update(token.encode())
        hash_token = sha256.hexdigest()
        record = token_collection.find_one({"hash-token": hash_token})

    if token != None and record != None:

        # add some code for storing infomation to databases, feel free to change it and do whatever you want.
        post_title = request.form["post-title"]
        post_content = request.form["post-content"]


    else:
        msg = "Only logged in user can make a post. Please log in"
        response = make_response(render_template('post.html', msg = msg))
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Content-Type"] = "text/html"
        

    return response

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080)