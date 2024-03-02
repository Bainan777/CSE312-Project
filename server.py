from flask import Flask, render_template, make_response

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

@server.route('/nav.html')
@server.route('/public/nav.html')
def nav_html():
    response = make_response(render_template('nav.html'))
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
    

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080)