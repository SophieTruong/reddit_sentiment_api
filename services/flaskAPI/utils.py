import uuid
from flask import Response


def get_uuid_id():
    return str(uuid.uuid4())
