"""
DaVinci Design Server Flask API

H6 TEC Ballerup
"""
from flask import Flask
from flask import request
from random import Random

app = Flask(__name__)
sessions = []


class Slot:
    connected = False
    isHost = False
    ipAddress = None
    extra = None

    def __init__(self):
        pass

    def as_dict(self):
        return {
            'connected': self.connected,
            'isHost': self.isHost,
            'ipAddress': self.ipAddress,
            'extra': self.extra
        }


class Session:
    """
    :type token int
    :type slots Slot[]
    """
    token = None
    slots = []

    def __init__(self, token):
        self.token = token
        self.slots = []

    def join(self, kwargs):
        slot = Slot()
        for k, v in dict(kwargs).items():
            setattr(slot, k, v)
        self.slots.append(slot)

    def asHTML(self):
        ret = f"<h1>{self.token}</h1>"

        for slot in self.slots:
            ret += \
                f"<h2>Slot</h2>" \
                f"<b>connected: </b> {slot.connected}</br>" \
                f"<b>Is Host: </b> {slot.isHost}</br>" \
                f"<b>IP Address: </b> {slot.ipAddress}</br>" \
                f"<b>Extra: </b> {slot.extra}</br>"
        return ret


@app.route('/session/new')
def new_session():
    id = Random().randint(1000, 9999)

    for item in sessions:
        if item.token == id:
            return new_session()

    session = Session(id)
    sessions.append(session)
    return str(id)


@app.route("/sessions")
def infoAll():
    ret = ""
    for item in sessions:
        ret += item.asHTML()
    return ret


@app.route("/session/delete/<int:token>")
def delete(token):
    for item in sessions:
        if item.token == token:
            sessions.remove(item)
            return "OK"
    return "ERROR"


@app.route('/session/info/<int:token>')
def info(token):
    for item in sessions:
        if item.token == token:
            return item.asHTML()


@app.route("/session/join/<int:token>")
def join(token):
    data = request.args.items()
    for item in sessions:
        if item.token == token:
            item.join(dict(data))
            return "OK"
    return "NOT FOUND"


if __name__ == '__main__':
    app.run("0.0.0.0", 5000)
