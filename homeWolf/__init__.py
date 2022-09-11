from operator import countOf
from flask import Flask, request, render_template
from flask_socketio import SocketIO,  emit

from homeWolf.game import Game

socketio = SocketIO(cors_allowed_origins="*")
game = None

def emit_player_dict(broadast=True):
    player_names = list(game.players.keys())
    player_names.remove(game.teller)
    
    socketio.emit(
            "broadcast_players_dict",
            [{'name': k, 'figure': game.players[k]['figure']} for k in player_names],
            broadcast=broadast
         )


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
        if not game.players:
            game.handle_player_connection(name,request.sid,role='teller')
            print(game.teller)
        else:
            game.handle_player_connection(name,request.sid)
        socketio.emit('get_role', game.players[name]['role'])
        emit_player_dict(broadast=True)

    @socketio.on('get_players_dict')
    def get_players_dict():
        emit_player_dict()

    @socketio.on('get_role')
    def get_role(name):
        socketio.emit('get_role', game.players[name]['role'])

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
        emit_player_dict()


    @socketio.on('start_game')
    def start_game():
        # check if number of players is reached, excluding the 
        if game.config['spieler'] == len(game.players.keys()) -1 :
            game.current_phase = 'start'
            game.start_game()
        socketio.emit('get_phase', game.current_phase, broadcast=True)
        


    @app.route('/')
    def index():
        return render_template('index.html')


    socketio.on('vote')
    def vote(vote):
        print(vote)

    socketio.init_app(app)
    return app
