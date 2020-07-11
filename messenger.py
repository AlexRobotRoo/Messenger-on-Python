from PyQt5 import QtWidgets
from PyQt5 import QtCore
from datetime import datetime

import clientui
import requests


class ExampleApp(QtWidgets.QMainWindow, clientui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.last_timestamp = 0

        self.pushButton.pressed.connect(self.send_message)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

    def update_messages(self):
        response = requests.get(
            'http://127.0.0.1:5000/get_message',
            params={'after': self.last_timestamp}
        )
        messages = response.json()['messages']
        for message in messages:
            dt = datetime.fromtimestamp(message['timestamp'])
            dt = dt.strftime('%H:%M:%S %d/%m/%Y')
            self.textBrowser.append(dt + ' ' + message['username'])
            self.textBrowser.append(message['text'])
            self.textBrowser.append('')
            self.last_timestamp = message['timestamp']

    def send_message(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        text = self.lineEdit_3.text()
        requests.get(
            'http://127.0.0.1:5000/send_message',
            json={'username': username, 'password': password, 'text': text})
        self.lineEdit_3.clear()
        self.lineEdit_3.repaint()




app = QtWidgets.QApplication([])
window = ExampleApp()
window.show()
app.exec_()
