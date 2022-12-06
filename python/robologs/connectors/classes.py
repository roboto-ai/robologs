from pydantic import BaseModel
from typing import List, Union


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Sources(BaseModel):
    type:           str = ''
    args:           dict = dict()


class Destinations(BaseModel):
    type:           str = ''
    args:           dict = dict()


class Connectors(BaseModel):
    name:           str = ''
    sources:        Sources
    destinations:   Destinations


# class Connector:
#     def __init__(self,
#                  sources: list(Sources),
#                  destinations: Destinations):
#         self.name = ''
#         self.sources = sources
#         self.destination = destinations
#
#     def run(self):
#         print()

