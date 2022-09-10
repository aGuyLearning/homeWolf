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

class Game:
    def __init__(self) -> None:
        self.config = {
            'spieler': 7,
            'werwoelfe': 2,
            'anonymeAbstimmung': False,
            'maedchen': True,
            'mystiker': False,
            'amor': True,
            'hexe': True,
            'jaeger': False,
            'dieb': False,
            'dorfdepp': False,
            'seherin': True
        }
        self.current_phase = 'lobby'
        self.teller = "";
        self.players = {}


    def start_game(self):
        
        pass
    def print_config(self):
        print(self.config)
    

    def player_is_in_game(self,name):
        return name in self.players.keys()


    def handle_player_connection(self, name, sid, role='player'):
        print(self.player_is_in_game(name))
        if not self.player_is_in_game(name) and self.current_phase == 'lobby':
            self.players[name] = {
                    'role': role,
                    'sid': sid
                }
            if role == 'teller':
                self.teller = name
        elif self.player_is_in_game(name): 
            self.players[name]['sid'] = sid
    
    def remove_player(self,name):
        if self.player_is_in_game(name):
            del self.players[name]