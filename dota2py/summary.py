"""
Try and extract useful information from a Dota 2 replay
"""

from dota2py import parser
from dota2py.proto import demo_pb2, usermessages_pb2, netmessages_pb2
from collections import defaultdict

index = 0


def debug_dump(message, file_prefix="dump"):
    """
    Utility while developing to dump message data to play with in the
    interpreter
    """

    global index
    index += 1

    with open("%s_%s.dump" % (file_prefix, index), 'w') as f:
        f.write(message.SerializeToString())
        f.close()


class DemoSummary(object):
    """
    A collection of useful information from the demo
    """

    def __init__(self, filename):
        self.filename = filename
        self.info = defaultdict(dict)

    def parse(self):
        dp = parser.DemoParser(self.filename, verbosity=1, hooks={
            demo_pb2.CDemoFileInfo: self.parse_file_info,
            parser.GameEvent: self.parse_game_event,
            parser.PlayerInfo: self.parse_player_info,
            usermessages_pb2.CUserMsg_TextMsg: self.parse_user_message,
        })
        dp.parse()

    def parse_user_message(self, user_message):
        """
        The combat summaries come through as CUserMsg_TextMsg objects
        """
        #print user_message
        #debug_dump(user_message, 'user_message')

    def parse_player_info(self, player):
        """
        Parse a PlayerInfo struct
        """
        if not player.ishltv:
            self.info["players"][player.userID] = {
                "name": player.name,
                "user_id": player.userID,
                "guid": player.guid,
                "bot": player.fakeplayer,
            }

            self.info["player_names"][player.name] = player.userID

    def parse_file_info(self, file_info):
        """
        The CDemoFileInfo contains our winners as well as the length of the
        demo
        """

        self.info["playback_time"] = file_info.playback_time
        self.info["match_id"] = file_info.game_info.dota.match_id
        self.info["game_mode"] = file_info.game_info.dota.game_mode
        self.info["game_winner"] = file_info.game_info.dota.game_winner

        for player in file_info.game_info.dota.player_info:
            user_id = self.info["player_names"][player.player_name]
            self.info["players"][user_id]["hero"] = player.hero_name

    def parse_game_event(self, ge):
        """
        Game events contain the combat log as well as 'chase_hero' events which
        could be interesting
        """

        if ge.name is "dota_combatlog":
            pass
        elif ge.name is "dota_chase_hero":
            pass

    def print_info(self, d=None, indentation=0):
        for k, v in (d or self.info).items():
            if isinstance(v, dict):
                print "%s%s:" % ('  ' * indentation, k)
                self.print_info(v, indentation + 1)
            else:
                print "%s%s: %s" % ('  ' * indentation, k, v)


def main():
    import argparse
    p = argparse.ArgumentParser(description="Dota 2 demo parser")
    p.add_argument('demo', help="The .dem file to parse")

    args = p.parse_args()

    d = DemoSummary(args.demo)
    d.parse()
    d.print_info()

if __name__ == "__main__":
    main()
