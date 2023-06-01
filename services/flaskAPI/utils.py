import uuid6
from flask import Response


def get_uuid_id():
    return str(uuid6.uuid6()
)
