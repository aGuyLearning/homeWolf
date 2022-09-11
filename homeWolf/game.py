'''
Config hat folgende Keys:
    {
        spieler: int
        werwoelfe: int
        anonymeAbstimmung: boolean
        maedchen: boolean
        mystiker: boolean
        amor: boolean
        hexe: boolean
        jaeger: boolean
        dieb: boolean
        dorfdepp: boolean
        seherin: boolean
    }
'''

'''
Phases:
1. lobby
2. setup
3. vote_leader
4. prepare_night
    ... (depends on figures in play)
wake_up (declare dead)
vote_death
'''

class Game:
    def __init__(self) -> None:
        self.config = {
            'spieler': 7,
            'werwoelfe': 2,
            'anonymeAbstimmung': False,
            'maedchen': False,
            'mystiker': False,
            'amor': False,
            'hexe': False,
            'jaeger': False,
            'dieb': False,
            'dorfdepp': False,
            'seherin': False
        }
        self.current_phase = 'lobby'
        self.teller = "";
        self.players = {}


    def start_game(self):
        self.current_phase = 'setup'
        self._setup()

        
    def _setup(self):
        print(f"setting up game with: \n{self.players}")

    def print_config(self):
        print(self.config)
    

    def player_is_in_game(self,name):
        return name in self.players.keys()


    def handle_player_connection(self, name, sid, role='player'):
        print(self.player_is_in_game(name))
        if not self.player_is_in_game(name) and self.current_phase == 'lobby':
            self.players[name] = {
                    'role': role,
                    'sid': sid,
                    'figure': ""
                }
            if role == 'teller':
                self.teller = name
        elif self.player_is_in_game(name): 
            self.players[name]['sid'] = sid
    
    def remove_player(self,name):
        if self.player_is_in_game(name) and self.current_phase == 'lobby':
            del self.players[name]