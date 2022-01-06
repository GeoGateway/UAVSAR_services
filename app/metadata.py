"""
metadata.py
    -- basic service for metadata 
"""

from flask import Blueprint
from flask import current_app

metadata = Blueprint("metadata",__name__)

@metadata.route("/")
def metadata_home():
    metajson = current_app.config['METADATA']
    return "current meta: {}".format(metajson)
