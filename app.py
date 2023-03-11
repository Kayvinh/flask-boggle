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
    """ Checks if the submitted word is valid for a board given a game_id
        TODO: Clarify in first line that will return JSON and not Python objects

        Input: {
            "game_id": <str: GAME_ID>,
            "word" : <str: WORD>
        }

        Outputs:
            If not in word list:
                { result: 'not-word' }

            If not on game board:
                { result: 'not-on-board' }

            If valid word:
                { result: 'ok'}

    """

    word = request.json["word"]
    game_id = request.json["game_id"]
    game = games[game_id]

    if not game.is_word_in_word_list(word):
        return jsonify(result='not-word')
    elif not game.check_word_on_board(word):
        return jsonify(result='not-on-board')
    else:
        return jsonify(result='ok')
