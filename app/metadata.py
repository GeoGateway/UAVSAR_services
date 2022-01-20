"""
metadata.py
    -- basic service for metadata 
"""

from dataclasses import dataclass
import os
import numpy as np
import pandas as pd
import geopandas as gpd

from flask import Blueprint
from flask import current_app
from flask import request
from shapely.geometry import * 

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

    if search_dict['geometry'] == "" and search_dict['flightname'] == "" and search_dict['eventdate'] == "":
         search_dict["result"] = 0
         return search_dict

    search_result = search_uavsar(search_dict) 
    search_dict["count"] = len(search_result)

    if search_dict["count"] >0:
        df1 = pd.DataFrame(search_result.drop(columns='geometry'))
        search_dict["data"]=df1.to_dict(orient="records")
    else:
        search_dict["data"]=""

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

def search_uavsar_geometry(sdata,gstr):
    """search by geometry"""

    # sample gemetry input
    # Point: (33.94697109585554, -118.07714843749999)
    # Rectangle: ((33.343343561567, -118.69238281249999), (34.34703015733175, -117.04443359374999))
    # Line: (34.72713264415401, -119.37353515624999),(33.67311969894201, -117.76953124999999),(33.983418330994276, -116.20947265624999),(32.4021911686893, -116.91259765624999)
    # Polygon: (34.05626592724434, -117.59374999999999),(33.572488142047554, -118.38476562499999),(32.837100401791204, -117.25317382812499),(33.4809029903106, -116.73681640624999)
    gtype,gcoord = gstr.split(":")
    gtype = gtype.strip()
    gcoord = eval(gcoord)
    if gtype == "Point":
        lat,lon = gcoord
        geom = Point(lon,lat)
    elif gtype == "Line":
        lonlat = [(x[1],x[0]) for x in gcoord]
        geom = LineString(lonlat)
    elif gtype == "Polygon":
        lonlat = [(x[1],x[0]) for x in gcoord]
        geom = Polygon(lonlat)
    elif gtype == "Rectangle":
        lat0,lon0 = gcoord[0]
        lat1,lon1 = gcoord[1]
        lonlat = [(lon0,lat1), (lon0,lat0), (lon1,lat0), (lon1,lat1)]
        geom = Polygon(lonlat)
    else:
        geom = None
    
    if geom:
        data = sdata[sdata.intersects(geom)]
    else:
        # return empty dataframe
        data = gpd.DataFrame(data=None, columns=sdata.columns)

    return data

def search_uavsar_eventdate(sdata,adatestr):
    """search by event data"""

    # eventdate format: YYYY-MM-DD
    testdate = np.datetime64(adatestr)

    # create a temporary dataframe
    tempdf = pd.DataFrame()
    tempdf["Time1"]=pd.to_datetime(sdata['Time1']).dt.tz_localize(None)
    tempdf["Time2"]=pd.to_datetime(sdata['Time2']).dt.tz_localize(None)

    mask = (tempdf['Time1']<testdate) & (tempdf['Time2']>testdate)
    data = sdata.loc[mask]

    return data

def search_uavsar(searchdict):
    """search UAVSAR """
    metajson = current_app.config['METADATA']
    # read all the search_data
    searchdata = load_metajson(metajson)
    # searchdict: geometry, flightname, eventdate
    if len(searchdict['flightname']) >=1:
        searchdata = search_uavsar_flightname(searchdata,searchdict['flightname'])
    
    if len(searchdict['geometry']) >=1:
        searchdata = search_uavsar_geometry(searchdata,searchdict['geometry'])

    if len(searchdict['eventdate']) >=1:
        searchdata = search_uavsar_eventdate(searchdata,searchdict['eventdate'])
        
    return searchdata
