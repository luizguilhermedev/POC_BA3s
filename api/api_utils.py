from pydantic import BaseModel

"""This module is intended to be used as a utility for the FatsAPI API. It contains te pydantic  models to be used as a
message payload for the API endpoints."""


class MessagePayload(BaseModel):
    input: str
