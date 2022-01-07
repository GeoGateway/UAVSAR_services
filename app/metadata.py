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

@metadata.route('/uid<int:uid>')
def checkuid(uid):
    metajson = current_app.config['METADATA']
    data = load_metajson(metajson)
    try:
        ob = data.loc[[uid]]
    except KeyError:
        return {"UID":uid,"Status":"not found"}
        
    ob = ob.to_json()
    response = current_app.response_class(response=ob,
                                  status=200,
                                  mimetype='application/json')
    return response

def check_metajson(metadata):
    """check metajson file"""

    if not os.path.exists(metadata):
        return "not found"
    
    status = load_metajson(metadata,checkstatus=True)

    return status

def load_metajson(metajson,checkstatus=False):
    """load metadata from .geojsonfile"""

    feather = metajson.replace(".geojson",".feather")
    try:
        data = gpd.read_feather(feather)
    except FileNotFoundError:
        # feature is not found
        # load geosjon file and generate feather
        data = gpd.read_file(metajson)
        data.set_index("UID",inplace=True,drop=False)
        data.to_feather(feather)
    if checkstatus:
        numofrecord=len(data.index)
        return numofrecord

    # normally it return the data
    return data

