"""
Parse a Dota 2 replay file
"""
from cStringIO import StringIO
import struct
import snappy
import functools

from dota2py import messages
from dota2py.proto import demo_pb2, netmessages_pb2

import ctypes

KEY_DATA_TYPES = {
    1: "val_string",
    2: "val_float",
    3: "val_long",
    4: "val_short",
    5: "val_byte",
    6: "val_bool",
    7: "val_uint64"
}


class GameEvent(object):
    def __init__(self, name):
        self.name = name
        self.keys = {}

    def __str__(self):
        return "%s: %s" % (self.name, self.keys)


class PlayerInfo(ctypes.Structure):
    """
    The player_info_s struct that is used to store some player information.
    Easier to use ctypes because of the byte alignment that structs do

    For some reason the ctypes.sizeof() for this structure says 144, but the
    binary data is 140. It doesn't seem to cause any problems but there may
    be a mistake in here somewhere that I haven't been able to find
    """
    _fields_ = [
        ("xuid", ctypes.c_ulonglong),
        ("name", ctypes.c_char * 32),
        ("userID", ctypes.c_int32),
        ("guid", ctypes.c_char * 33),
        ("friendsID", ctypes.c_uint32),
        ("friendsName", ctypes.c_char * 32),
        ("fakeplayer", ctypes.c_bool),
        ("ishltv", ctypes.c_bool),
        ("customFiles", ctypes.c_uint32 * 4),
        ("filesDownloaded", ctypes.c_ubyte),
    ]

    def __str__(self):
        return ", ".join("%s=%s" % (x[0], getattr(self, x[0])) for x in
                        self._fields_)


class Reader(object):
    """
    Some utilities to make it a bit easier to read values out of the .dem file
    """

    def __init__(self, stream):
        self.stream = stream
        stream.seek(0, 2)
        self.size = stream.tell()
        self.remaining = self.size
        stream.seek(0)

    def more(self):
        return self.remaining > 0

    def nibble(self, length):
        self.remaining -= length
        if self.remaining < 0:
            raise ValueError("Not enough data")

    def read_byte(self):
        self.nibble(1)
        return ord(self.stream.read(1))

    def read(self, length=None):
        if length is None:
            length = self.remaining

        self.nibble(length)
        return self.stream.read(length)

    def read_int32(self):
        self.nibble(4)
        return struct.unpack("i", self.stream.read(4))[0]

    def read_uint32(self):
        self.nibble(4)
        return struct.unpack("I", self.stream.read(4))[0]

    def read_vint32(self):
        """
        This seems to be a variable length integer ala utf-8 style
        """
        result = 0
        count = 0
        while True:
            if count > 4:
                raise ValueError("Corrupt VarInt32")

            b = self.read_byte()
            result = result | (b & 0x7F) << (7 * count)
            count += 1

            if not b & 0x80:
                return result

    def read_message(self, message_type, compressed=False, read_size=True):
        """
        Read a protobuf message
        """
        if read_size:
            size = self.read_vint32()
            b = self.read(size)
        else:
            b = self.read()

        if compressed:
            b = snappy.decompress(b)

        m = message_type()
        m.ParseFromString(b)
        return m


class DemoParser(object):
    """
    A parser for Dota 2 .dem files based on deminfo2
    https://developer.valvesoftware.com/wiki/Dota_2_Demo_Format
    """

    def __init__(self, filename, verbosity=3, frames=None, hooks=None):
        self.filename = filename
        self.verbosity = verbosity
        self.frames = frames

        self.eventlist = None
        self.event_lookup = {}

        self.combat_log_names = []

        self.internal_hooks = {
            demo_pb2.CDemoPacket: self.parse_demo_packet,
            demo_pb2.CDemoFullPacket: self.parse_demo_packet,
            demo_pb2.CDemoStringTables: self.parse_string_table,
            netmessages_pb2.CSVCMsg_UserMessage: self.parse_user_message,
            netmessages_pb2.CSVCMsg_GameEvent: self.parse_game_event,
            netmessages_pb2.CSVCMsg_GameEventList: self.parse_game_event_list,
            netmessages_pb2.CSVCMsg_CreateStringTable:
                self.create_string_table,
            netmessages_pb2.CSVCMsg_UpdateStringTable:
                self.update_string_table,
        }

        self.hooks = hooks or {}

        self.error = functools.partial(self.log, 1)
        self.important = functools.partial(self.log, 2)
        self.info = functools.partial(self.log, 3)
        self.debug = functools.partial(self.log, 4)
        self.worthless = functools.partial(self.log, 5)

    def log(self, level, message):
        """
        Log a message if our verbosity permits it
        """
        if level <= self.verbosity:
            print(message)

    def run_hooks(self, packet):
        """
        Run any additional functions that want to process this type of packet.
        These can be internal parser hooks, or external hooks that process
        information
        """

        if packet.__class__ in self.internal_hooks:
            self.internal_hooks[packet.__class__](packet)

        if packet.__class__ in self.hooks:
            self.hooks[packet.__class__](packet)

    def create_string_table(self, message):
        pass

    def update_string_table(self, message):
        pass

    def parse_string_table(self, tables):
        """
        Need to pull out player information from string table
        """
        self.info("String table: %s" % (tables.tables, ))

        for table in tables.tables:
            if table.table_name == "userinfo":
                for item in table.items:
                    if len(item.data) > 0:
                        if len(item.data) == 140:
                            p = PlayerInfo()
                            ctypes.memmove(ctypes.addressof(p), item.data, 140)
                            p.str = item.str
                            self.run_hooks(p)
            if table.table_name == "CombatLogNames":
                self.combat_log_names = dict(enumerate(
                    (item.str for item in table.items)))

    def parse_demo_packet(self, packet):
        if isinstance(packet, demo_pb2.CDemoFullPacket):
            data = packet.packet.data
        else:
            data = packet.data

        if isinstance(packet, demo_pb2.CDemoFullPacket):
            self.run_hooks(packet.string_table)

        reader = Reader(StringIO(data))

        while reader.more():
            cmd = reader.read_vint32()

            if cmd not in messages.DEMO_PACKET_MESSAGE_TYPES:
                raise IndexError("Unknown demo packet cmd")

            message_type = messages.DEMO_PACKET_MESSAGE_TYPES[cmd]
            message = reader.read_message(message_type)

            self.info("|>>> %s" % (message_type, ))
            self.worthless(message)

            self.run_hooks(message)

    def parse_user_message(self, message):
        cmd = message.msg_type
        if cmd not in messages.COMBINED_USER_MESSAGE_TYPES:
            raise IndexError("Unknown user message cmd: %s" % (cmd, ))

        reader = Reader(StringIO(message.msg_data))
        message_type = messages.COMBINED_USER_MESSAGE_TYPES[cmd]
        user_message = reader.read_message(message_type, read_size=False)

        self.run_hooks(user_message)

        self.info("|-----> %s" % (message_type, ))
        self.debug(user_message)

    def parse_game_event_list(self, eventlist):
        self.eventlist = eventlist

        for descriptor in eventlist.descriptors:
            self.event_lookup[descriptor.eventid] = descriptor

    def parse_game_event(self, event):
        """
        So CSVCMsg_GameEventList is a list of all events that can happen.
        A game event has an eventid which maps to a type of event that happened
        """

        if event.eventid in self.event_lookup:
            #Bash this into a nicer data format to work with
            event_type = self.event_lookup[event.eventid]
            ge = GameEvent(event_type.name)

            for i, key in enumerate(event.keys):
                key_type = event_type.keys[i]
                ge.keys[key_type.name] = getattr(key,
                                                    KEY_DATA_TYPES[key.type])

            self.debug("|==========> %s" % (ge, ))

            self.run_hooks(ge)

    def parse(self):
        """
        Parse a replay
        """

        self.important("Parsing demo file '%s'" % (self.filename, ))

        with open(self.filename, 'rb') as f:
            reader = Reader(StringIO(f.read()))

            filestamp = reader.read(8)
            offset = reader.read_int32()

            if filestamp != "PBUFDEM\x00":
                raise ValueError("Invalid replay - incorrect filestamp")

            buff = StringIO(f.read())

            frame = 0
            more = True
            while more and reader.remaining > 0:
                cmd = reader.read_vint32()
                tick = reader.read_vint32()
                compressed = False

                if cmd & demo_pb2.DEM_IsCompressed:
                    compressed = True
                    cmd = cmd & ~demo_pb2.DEM_IsCompressed

                if cmd not in messages.MESSAGE_TYPES:
                    raise KeyError("Unknown message type found")

                message_type = messages.MESSAGE_TYPES[cmd]
                message = reader.read_message(message_type, compressed)

                self.info('%s: %s' % (frame, message_type))
                self.worthless(message)

                self.run_hooks(message)

                self.info('|%s' % ('-' * 79, ))

                frame += 1

                if self.frames and frame > self.frames:
                    break


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Dota 2 demo parser")
    parser.add_argument('demo', help="The .dem file to parse")
    parser.add_argument("--verbosity", dest="verbosity", default=3, type=int,
                        help="how verbose [1-5] (optional)")
    parser.add_argument("--frames", dest="frames", default=None, type=int,
                        help="maximum number of frames to parse (optional)")

    args = parser.parse_args()

    r = DemoParser(args.demo, verbosity=args.verbosity, frames=args.frames)
    r.parse()

if __name__ == "__main__":
    main()
