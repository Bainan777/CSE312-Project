from flask import Flask, jsonify, render_template, make_response, request, redirect, flash
from werkzeug.utils import secure_filename
import bcrypt
import uuid
import hashlib
from markupsafe import escape
from pymongo import MongoClient
import random
import html
import os
from flask_socketio import SocketIO, emit, send

mongo_client = MongoClient("mongo")
db = mongo_client["cse-312-project"]
user_collection = db["user"]
token_collection = db["auth_token"]
post_collection = db["posts"]
chat_collection = db["chat"]

server = Flask(__name__, template_folder='public')
socketio = SocketIO(server, transport = ['websocket'])

jpeg_sig = bytes.fromhex('FF D8 FF E0 00 10 4A 46 49 46 00 01')
jpeg_sig2 = b"Exif\x00\x00"
jpeg_sig3 = b'\xff\xd8\xff\xe1'
png_sig = bytes.fromhex('89 50 4E 47 0D 0A 1A 0A')
    
gif_sig = bytes.fromhex("47 49 46 38 39 61")
gif_sig2 = bytes.fromhex("47 49 46 38 37 61")

@server.route('/')
@server.route('/public/index.html')
def homepage():
    posts = list(post_collection.find())
    token = request.cookies.get("auth_token")

    response = make_response(render_template('index.html', posts=posts, token=token))
    response.headers["X-Content-Type-Options"] = "nosniff"
    # emit('home_load', {'posts':posts})
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

@server.route('/public/chatroom.css')
def chat_css():
    response = make_response(render_template('chatroom.css'))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "text/css"
    return response

@server.route('/public/post.css')
def post_css():
    response = make_response(render_template('post.css'))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "text/css"
    return response

@server.route('/public/stars.css')
def stars_css():
    response = make_response(render_template('stars.css'))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "text/css"
    return response

@server.route('/public/profile-card.css')
def profile_css():
    response = make_response(render_template('profile-card.css'))
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
            name = "Hello, " + getToken[0]["username"] + "! "
            logout = "Logout"
            visibility = "hidden"
            href = "/logout"
            profile_href = "/profile.html"

            getPfp = user_collection.find({"username": getToken[0]["username"]})
            getPfp = list(getPfp)

            if len(getPfp) != 0:
                pfp = getPfp[0]["profile-pic"]
            else:
                pfp = "default.jpg"
        else:
            name = "Guest"
            logout = "Sign Up"
            visibility = "visible"
            href="/signup.html"
            profile_href = "/login.html"
            pfp = "temp-logo.png"
    else:
        name = "Guest"
        logout = "Sign Up"
        visibility = "visible"
        href="/signup.html"
        pfp = "temp-logo.png"
        profile_href = "/login.html"

    response = make_response(render_template('nav.html',  
        name=name, 
        pfp=pfp, 
        profile_href=profile_href, 
        logout=logout, 
        visibility=visibility, 
        href=href))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "text/html"
    return response

@server.route('/public/assets/favicon.ico')
def icon():
    with open("public/assets/favicon.ico", "rb") as file:
        byte_string = file.read()
        response = make_response(byte_string)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Content-Type"] = "image/x-icon"
    return response

@server.route('/public/assets/images/profile_pictures/<filename>')
def getPfps(filename):
    filename = filename.replace("/", "")

    try:
        with open("public/assets/images/profile_pictures/"+filename, "rb") as file:
            byte_string = file.read()
            response = make_response(byte_string)
            response.headers["X-Content-Type-Options"] = "nosniff"

            if jpeg_sig in byte_string or (jpeg_sig2 in byte_string and jpeg_sig3 in byte_string):
                response.headers["Content-Type"] = "image/jpeg"
            elif png_sig in byte_string:
                response.headers["Content-Type"] = "image/png"
            elif gif_sig in byte_string or gif_sig2 in byte_string:
                response.headers["Content-Type"] = "image/gif"
            else:
                return make_response("Not an image", 404)
    except IOError:
        return make_response("File not found", 404)

    return response

@server.route('/public/assets/images/<filename>')
def getImages(filename):
    filename = filename.replace("/", "")

    try:
        with open("public/assets/images/"+filename, "rb") as file:
            byte_string = file.read()
            response = make_response(byte_string)
            response.headers["X-Content-Type-Options"] = "nosniff"
            
            if jpeg_sig in byte_string or (jpeg_sig2 in byte_string and jpeg_sig3 in byte_string):
                response.headers["Content-Type"] = "image/jpeg"
            elif png_sig in byte_string:
                response.headers["Content-Type"] = "image/png"
            elif gif_sig in byte_string or gif_sig2 in byte_string:
                response.headers["Content-Type"] = "image/gif"
            else:
                return make_response("Not an image", 404)
    except IOError:
        return make_response("File not found", 404)
    
    return response
    
@server.route('/public/functions.js')
def homepage_js():
    response = make_response(render_template('functions.js'))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "text/javascript"
    return response

@server.route('/public/websocket.js')
def websocket_js():
    response = make_response(render_template('websocket.js'))
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

@server.route('/profile.html')
@server.route('/public/profile.html')
def profile_html():
    token = request.cookies.get("auth_token")

    if token:
        sha256 = hashlib.sha256()
        sha256.update(token.encode())
        hash_token = sha256.hexdigest()
        getToken = token_collection.find({"hash-token": str(hash_token)})
        getToken = list(getToken)

        if len(getToken) != 0:
            name = "@"+getToken[0]["username"]

            getProfile = user_collection.find({"username": getToken[0]["username"]})
            getProfile = list(getProfile)

            if len(getProfile) != 0:
                pfp = getProfile[0]["profile-pic"]
                caption = getProfile[0]["caption"]
                numPosts = getProfile[0]["numPosts"]
                favorite = getProfile[0]["favorite-anime"]
                aboutme = getProfile[0]["about-me"]
            else:
                pfp = "default.jpg"
                caption = "What are you?"
                numPosts = "0"
                favorite = "Keep track of your favorite anime!"
                aboutme = "Share about yourself!"
        else:
            name = "Guest"
            pfp = "temp-logo.png"
            caption = "Log in!"
            numPosts = "0"
            favorite = "Log in to share your favorite anime!"
            aboutme = "Log in to share about yourself!"   
    else:
        name = "Guest"
        pfp = "temp-logo.png"
        caption = "Log in!"
        numPosts = "0"
        favorite = "Log in to share your favorite anime!"
        aboutme = "Log in to share about yourself!"

    response = make_response(render_template('profile.html', 
        name=name, 
        pfp=pfp, 
        favorite=favorite, 
        aboutme=aboutme, 
        caption=caption, 
        numPosts=numPosts))
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
        user_information_dict = {"username": str(username), "password": hash_password, "email": str(email), 
            "profile-pic": "default.jpg", "numPosts": "0","caption": "What are you?", "about-me": "Share about yourself!", "favorite-anime": "Keep track of your favorite anime!"}
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

@server.route('/chat-room')
def direct_message_render():
    response = make_response(render_template('chatroom.html'))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "text/html"
    return response

def get_user(token):
    if token != None:
        sha256 = hashlib.sha256()
        sha256.update(token.encode())
        hash_token = sha256.hexdigest()
        record = token_collection.find_one({'hash-token': hash_token})

    if token != None and record != None: 
        return record['username']
    else:
        return None

@server.template_filter('get_pfp')
def get_pfp(username):
    if username != None:
        record = user_collection.find_one({"username": username})

    if username != None and record != None:
        return record['profile-pic']
    else:
        return None

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
        post_rating = request.form["post-rating"]

        #post_title = html.escape(post_title)
        #post_content = html.escape(post_content)
        #post_rating = html.escape(post_rating)

        if post_rating == "1/5":
            post_rating = "1"
        elif post_rating == "2/5":
            post_rating = "2"
        elif post_rating == "3/5":
            post_rating = "3"
        elif post_rating == "4/5":
            post_rating = "4"
        elif post_rating == "5/5":
            post_rating = "5"
        else:
            post_rating = "0"

        print(post_title)
        print(post_content)

        # Database content should be pulled for HTML use
        post_id = random.randint(1, 9999999999)
        post_contents = {"username": record["username"], "post_title": post_title, "post_content": post_content, "id": str(post_id), "post_rating": post_rating, "upvotes": [], "downvotes": []}

        post_collection.insert_one(post_contents)

        getPosts = user_collection.find({"username": record["username"]})
        getPosts = list(getPosts)
        postNum = int(getPosts[0]["numPosts"])
        postNum+=1
        user_collection.update_one({'username': record["username"]}, {'$set': {'numPosts':str(postNum)}})

        response = make_response(redirect("/public/index.html"))

    else:
        msg = "Only logged in users can make a post. Please log in"
        response = make_response(render_template('post.html', msg = msg))
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Content-Type"] = "text/html"

    return response

@socketio.on('upvote')
def upvote_post(post_id):
    upvoters = post_collection.find_one({'id': post_id})
    downvoters = []
    
    if upvoters:
        downvoters = upvoters['downvotes']
        upvoters = upvoters['upvotes']
    else:
        upvoters = []
    
    token = request.cookies.get("auth_token")
    username = get_user(token)
    
    if username not in upvoters:
        upvoters.append(username)
    else:
        upvoters.remove(username)

    post_collection.update_one({'id': post_id}, {'$set':{'upvotes':upvoters}})

    if username in downvoters: 
        downvoters.remove(username)
        post_collection.update_one({'id': post_id}, {'$set': {'downvotes':downvoters}})

    emit('vote_update', {'post_id': post_id, 'votes': len(upvoters) - len(downvoters), 'upvoted':True, 'downvoted':False})

@socketio.on('downvote')
def downvote_post(post_id):
    downvoters = post_collection.find_one({'id': post_id})
    upvoters = []

    if downvoters: 
        upvoters = downvoters['upvotes']
        downvoters = downvoters['downvotes']
    else:
        downvoters = []
    
    token = request.cookies.get("auth_token")
    username = get_user(token)

    if username not in downvoters:
        downvoters.append(username)
    else:
        downvoters.remove(username)
    
    post_collection.update_one({'id': post_id}, {'$set':{'downvotes':downvoters}})
    
    if username in upvoters: # do the same for upvote_post
        upvoters.remove(username)
        post_collection.update_one({'id': post_id}, {'$set':{'upvotes':upvoters}})

    emit('vote_update', {'post_id': post_id, 'votes': len(upvoters) - len(downvoters), 'upvoted':False, 'downvoted':True})

PFP_FOLDER = './public/assets/images/profile_pictures'
PFP_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

server.config['PFP_FOLDER'] = PFP_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in PFP_EXTENSIONS

@server.route('/change-pfp', methods=['POST'])
def upload_file():
    token = request.cookies.get("auth_token")

    if token:
        sha256 = hashlib.sha256()
        sha256.update(token.encode())
        hash_token = sha256.hexdigest()
        getToken = token_collection.find({"hash-token": str(hash_token)})
        getToken = list(getToken)

        if len(getToken) != 0:
            name = "@"+getToken[0]["username"]

            getProfile = user_collection.find({"username": getToken[0]["username"]})
            getProfile = list(getProfile)

            if len(getProfile) != 0:
                pfp = getProfile[0]["profile-pic"]
                caption = getProfile[0]["caption"]
                numPosts = getProfile[0]["numPosts"]
                favorite = getProfile[0]["favorite-anime"]
                aboutme = getProfile[0]["about-me"]
            else:
                pfp = "default.jpg"
                caption = "What are you?"
                numPosts = "0"
                favorite = "Keep track of your favorite anime!"
                aboutme = "Share about yourself!"
        else:
            name = "Guest"
            pfp = "temp-logo.png"
            caption = "Log in!"
            numPosts = "0"
            favorite = "Log in to share your favorite anime!"
            aboutme = "Log in to share about yourself!"   
    else:
        return make_response(render_template("/profile.html", 
            msg="Only registered users can change their profile pictures!", 
            name="Guest", 
            pfp="default.jpg", 
            color="red", 
            caption = "Log in!",
            favorite = "Log in to share your favorite anime!",
            aboutme = "Log in to share about yourself!",
            numPosts = "0"))

    if 'file' not in request.files:
        return make_response(render_template("/profile.html", 
            msg="There is no file part!", 
            name=name, 
            pfp=pfp, 
            caption=caption, 
            numPosts=numPosts, 
            favorite=favorite, 
            aboutme=aboutme, 
            color="red"))
    file = request.files['file']

    if file.filename == '':
        return make_response(render_template("/profile.html", 
            msg="You haven't uploaded any file!", 
            name=name, 
            pfp=pfp, 
            caption=caption, 
            numPosts=numPosts, 
            favorite=favorite, 
            aboutme=aboutme, 
            color="red"))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(server.config['PFP_FOLDER'], filename))

        username = getToken[0]["username"]
        user_collection.update_one({"username": str(username)}, {'$set': {'profile-pic': filename}})


    return make_response(render_template("/profile.html", 
        msg="Profile picture updated!", 
        name=name, 
        caption=caption, 
        numPosts=numPosts, 
        favorite=favorite, 
        aboutme=aboutme,
        color="blueviolet", 
        pfp=filename))

@server.route("/chat-history")
def chat_history():

    token = request.cookies.get("auth_token")

    if token:
        sha256 = hashlib.sha256()
        sha256.update(token.encode())
        hash_token = sha256.hexdigest()
        getToken = token_collection.find({"hash-token": str(hash_token)})
        getToken = list(getToken)

        if len(getToken) != 0:
            username = getToken[0]["username"]
            username_tag = f'<input id="username" value="{username}" hidden>'

    else:
        return make_response(redirect("/login.html"))
    
    chatHistory = chat_collection.find({})
    messages_dict = []
    for message in chatHistory:
        message_dict = {"username" :message["username"], "message": message["message"]}
        messages_dict.append(message_dict)
    
    return jsonify({"button_tag": username_tag, "chat_history": messages_dict})


@socketio.on('chat-message') 
def connect_handler(data_json):

    message_dict = {"username" :data_json["sender"], "message": html.escape(data_json["message"])}
    chat_collection.insert_one({"username" :data_json["sender"], "message": html.escape(data_json["message"])})

    emit("receive_message", message_dict, broadcast= True)

if __name__ == '__main__':
    socketio.run(server, host='0.0.0.0', port=8080, allow_unsafe_werkzeug=True)