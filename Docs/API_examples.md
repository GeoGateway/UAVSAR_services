# API Example
## Metadata 

Get Metadata
```
GET /metadata

{
  "metadata": "/Projects/UAVSAR_services/Data/metadata.geojson", 
  "status": 1255
}

```

Get metadata for a dataset, return geojson
```
GET /metadata/uid<int:uid>

{"type": "FeatureCollection", "features": [{"id": "1500", "type": "Feature", "properties": {"Dataname": "SnJoaq_34301_17104-012_17123-000_0047d_s01_L090HH_01", "Description": "San Joaquin Valley - SMAP, CA", "GPSAltitude": 12494.3177, "LatSpace": -5.6e-05, "Lines": 18409, "LonSpace": 5.6e-05, "PegHead": -16.967283, "PegLat": 35.908607, "PegLon": -119.694612, "PhaseSign": -1.0, "RadarDirection": "Left", "Samples": 10563, "StartLat": 36.351852, "StartLon": -120.145166, "TerrainHeight": 46.619474, "Time1": "28-Sep-2017 21:27:29 UTC", "Time2": "14-Nov-2017 20:25:49 UTC", "UID": 1500, "URL": "http://uavsar.jpl.nasa.gov/cgi-bin/product.pl?jobName=SnJoaq_34301_17104-012_17123-000_0047d_s01_L090_01", "Version": 2, "Wavelength": 23.840355}, "geometry": {"type": "Polygon", "coordinates": [[[-120.13920428, 36.25816013], [-119.90183008, 36.33171937], [-119.56216752, 35.42541775], [-119.79956305, 35.35081684], [-120.13920428, 36.25816013]]]}}]}
```