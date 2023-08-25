from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"game_id": game_id, "board": game.board})

@app.post("/api/score-word")
def score_word():
    """check if word is legal and on board"""

    request_data = request.get_json()

    game_id = request_data["game_id"]
    game = games[game_id]

    word = request_data["word"]

    response = {"result": "ok"}

    if not (game.is_word_in_word_list(word)):
        response = {"result": "not-word"}
    elif not (game.check_word_on_board(word)):
        response = {"result": "not-on-board"}

    return jsonify(response)


