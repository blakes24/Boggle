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
    """Home page with game instructions"""
    return render_template("start.html")


@app.route("/play")
def start_game():
    """generates boggle game board and adds it to session"""
    board = boggle_game.make_board()
    session["board"] = board
    if session.get("plays") is None:
        session["plays"] = 0
        session["high_score"] = 0

    plays = session["plays"]
    high_score = session["high_score"]
    return render_template("play.html", board=board, plays=plays, high_score=high_score)


@app.route("/check")
def check_word():
    """Checks if a word is valid and on the board. Sends the results to front end """
    word = request.args["guess"]
    board = session["board"]
    res = boggle_game.check_valid_word(board, word)
    return jsonify({"result": res})


@app.route("/score", methods=["POST"])
def set_score():
    """Checks if current score is greater than the high score in session. Adds 1 to games played and returns message with high score to front end"""
    plays = session["plays"]
    high_score = session["high_score"]
    score = request.json["score"]
    session["plays"] = plays + 1
    if score > high_score:
        session["high_score"] = score
        return jsonify({"msg": "New High Score!", "high": session["high_score"]})
    return jsonify({"msg": "Final Score:", "high": session["high_score"]})
