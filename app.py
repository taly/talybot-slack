from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return "Hello from Talybot! You are user {} in channel {} and you just said '{}'.".format(request.form.get('user_name'), request.form.get('channel_name'), request.form.get('text'))
