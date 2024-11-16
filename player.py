
class Player:
    def __init__(self, player_id, player_name):
        self.player_id = player_id
        self.player_name = player_name

class PlayerCollection:
    def __init__(self):
        self.players = {}

    def add_player(self, player):
        if player.player_id in self.players:
            raise ValueError(f"Player with ID {player.player_id} already exists.")
        self.players[player.player_id] = player

    def delete_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]
        else:
            raise KeyError(f"Player with ID {player_id} not found.")

    def get_player(self, player_id):
        player = self.players.get(player_id)
        if player is None:
            return None
        return Player(player.player_id, player.player_name)

    def get_players(self):
        player_list = []
        for player_id, player in self.players.items():
            player_ = Player(player.player_id, player.player_name)
            player_list.append((player_id, player_))
        return player_list