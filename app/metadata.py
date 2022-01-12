"""
metadata.py
    -- basic service for metadata 
"""

import os
import pandas as pd
import geopandas as gpd

from flask import Blueprint
from flask import current_app
from flask import request

metadata = Blueprint("metadata",__name__)

@metadata.route("/")
def metadata_home():
    metajson = current_app.config['METADATA']
    status = check_metajson(metajson)

    desc = {"metadata":metajson, "status":status}

    return desc

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

@metadata.route('/search')
def search_metadata():
    """ search metadata"""
    geometry_str = request.args.get('geometry',default="")
    name_str = request.args.get('flightname',default="")
    date_str = request.args.get('eventdate',default="")

    search_dict ={"geometry":geometry_str,"flightname":name_str,"eventdate":date_str}

    if search_dict['geometry'] == "" and  search_dict['flightname'] == "":
         search_dict["result"] = 0
         return search_dict

    search_result = search_uavsar(search_dict) 
    search_dict["result"] = len(search_result)

    if search_dict["result"] >0:
        response = current_app.response_class(response=search_result.to_json(),
                                  status=200,
                                  mimetype='application/json')
        return response

    return search_dict


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

def search_uavsar_flightname(sdata,flightname):
    """search flight name"""
    
    # Dataname field

    data = sdata.loc[sdata['Dataname'].str.contains(flightname,case=False)]
    
    return data

def search_uavsar(searchdict):
    """search UAVSAR """
    metajson = current_app.config['METADATA']
    # read all the search_data
    searchdata = load_metajson(metajson)
    # searchdict: geometry, flightname, eventname
    if len(searchdict['flightname']) >=1:
        searchdata = search_uavsar_flightname(searchdata,searchdict['flightname'])
    
    return searchdata
