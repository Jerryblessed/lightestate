import threading
from flask import Blueprint, Flask, jsonify, render_template, request, send_file
import os

app = Flask(__name__)

dapp = Blueprint('chat', __name__)


@dapp.route('/chat')
def index():
    return render_template('chat.html')
