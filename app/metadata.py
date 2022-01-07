"""
metadata.py
    -- basic service for metadata 
"""

import os
import pandas as pd
import geopandas as gpd

from flask import Blueprint, jsonify
from flask import current_app

metadata = Blueprint("metadata",__name__)

@metadata.route("/")
def metadata_home():
    metajson = current_app.config['METADATA']
    status = check_metajson(metajson)

    desc = {"metadata":metajson, "status":status}

    return jsonify(desc)

@metadata.route('/<uid>')
def dashboard(uid):
   return jsonify(uid=uid)

def check_metajson(metadata):
    """check metajson file"""

    if not os.path.exists(metadata):
        return "not found"
    
    status = load_metajson(metadata)

    return status

def load_metajson(metadata):
    """load metadata from .geojsonfile"""

    feather = metadata.replace(".geojson",".feather")
    try:
        data = gpd.read_feather(feather)
    except FileNotFoundError:
        # feature is not found
        # load geosjon file and generate feather
        data = gpd.read_file(metadata)
        data.set_index("UID",inplace=True)
        data.to_feather(feather)
        
    numofrecord=len(data.index)

    return numofrecord 
