"""
Build mappings between ENUMs and actual message types automatically
"""

from dota2py.proto import demo_pb2, netmessages_pb2, usermessages_pb2
from dota2py.proto import dota_usermessages_pb2


def build_mapping(module, enum_prefix, class_prefix, special_cases=None):
    special_cases = special_cases or {}
    mapping = dict(special_cases)

    for attr in dir(module):
        if attr.startswith(enum_prefix):
            t = "%s%s" % (class_prefix, attr[len(enum_prefix):], )
            try:
                mapping[getattr(module, attr)] = getattr(module, t)
            except AttributeError:
                pass

    return mapping

MESSAGE_TYPES = build_mapping(demo_pb2, "DEM_", "CDemo",
        {demo_pb2.DEM_SignonPacket: demo_pb2.CDemoPacket})

NET_MESSAGE_TYPES = build_mapping(netmessages_pb2, "net_", "CNETMsg_")
SVC_MESSAGE_TYPES = build_mapping(netmessages_pb2, "svc_", "CSVCMsg_")

DEMO_PACKET_MESSAGE_TYPES = dict(NET_MESSAGE_TYPES)
DEMO_PACKET_MESSAGE_TYPES.update(SVC_MESSAGE_TYPES)

USER_MESSAGE_TYPES = build_mapping(usermessages_pb2, "UM_", "CUserMsg_")
DOTA_USER_MESSAGE_TYPES = build_mapping(dota_usermessages_pb2, "DOTA_UM_",
                                        "CDOTAUserMsg_")

COMBINED_USER_MESSAGE_TYPES = dict(USER_MESSAGE_TYPES)
COMBINED_USER_MESSAGE_TYPES.update(DOTA_USER_MESSAGE_TYPES)
