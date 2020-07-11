import time
from datetime import datetime


from flask import Flask, request

app = Flask(__name__)
server_start_moment = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
messages = [
               # {'username': 'Arnold', 'text': 'Hello everyone', 'timestamp': time.time()}
]

users = {
    # 'Arnold': '123' login and password
}

@app.route("/")
def hello():
    return 'Здравствуй, пользователь! Это мой мессенджер. Его <a href="/status">статус</a>'


@app.route("/status")
def status():
    return {
        'status': 'OK',
        'name': 'Messenger in Python',
        'time': datetime.now().strftime('%H:%M:%S %d/%m/%Y'),
        'current_time_sec': time.time(), # количество секунд с начала эпохи UNIX; .asctime() - время в виде строки
        'server_start_time': server_start_moment,
        'users_count': len(users),
        'messages_count': len(messages)
    }

@app.route("/send_message")
def send_message():
    username = request.json['username']
    password = request.json['password']
    text = request.json['text']
    if username in users:
        if users[username] != password:
            return {'ok': False}
    else:
        users[username] = password

    messages.append({'username': username, 'text': text, 'timestamp': time.time()})
    return {'ok': True}

@app.route("/get_message")
def get_message():
    after = float(request.args['after'])
    result = []
    for message in messages:
        if message['timestamp'] > after:
            result.append(message)
    return {
        'messages': result
    }

app.run()
