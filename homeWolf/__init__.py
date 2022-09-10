from queue import Empty
from socket import socket
from flask import Flask, request, render_template
from flask_socketio import SocketIO,  emit
from flask_cors import CORS

from homeWolf.game import Game

socketio = SocketIO(cors_allowed_origins="*")
game = None

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True,template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY='dev',  # change for deployment
    )
    @socketio.on('connect')
    def handle_connect():
       global game
       if not game:
        game = Game()
    

    @socketio.on('join_game')
    def join_game(name):
        if game.players is Empty:
            game.handle_player_connection(name,request.sid,role='teller')
        else:
            game.handle_player_connection(name,request.sid)
        print(game.players[name])


    @socketio.on('get_config')
    def config():
        print(request.method)
        emit('get_config', game.config)
    

    @socketio.on('set_config')
    def set_config(config):
        game.config = config
        game.print_config()


    @socketio.on('remove_player')
    def remove_player(name):
        game.remove_player(name)


    @socketio.on('start_game')
    def start_game():
        # check if number of players is reached, excluding the 
        if game.config['spieler'] != len(game.players.keys()) -1:
            game.current_phase = 'start'
            game.start_game()


    @app.route('/')
    def index():
        return render_template('index.html')


    socketio.on('vote')
    def vote(vote):
        print(vote)

    socketio.init_app(app)
    return app
