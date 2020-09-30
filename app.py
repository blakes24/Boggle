from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config["SECRET_KEY"] = "shhhItsAsecret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route("/")
def home():
    return render_template("start.html")


@app.route("/play")
def start_game():
    board = boggle_game.make_board()
    session["board"] = board
    return render_template("index.html", board=board)


@app.route("/check")
def check_word():
    word = request.args["guess"]
    board = session["board"]
    res = boggle_game.check_valid_word(board, word)
    return jsonify({"result": res})
