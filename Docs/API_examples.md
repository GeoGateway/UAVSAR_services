# API Example
## Metadata 

### Get metadata
```
/metadata
/metadata/uid<int:uid>
```
### Search metadata 
```
/metadata/search?[geometry | flightname | eventdate] 

geometry: Point,Rectangle,Line,Polygon
flightname: any string part in dataname
eventdate: YYYYMMDD, the date between Time1 and Time2
search return in json, the result is in "data"
```
The return is in json format, "data" holds the records  
```
{
  "data": "", 
  "eventdate": "", 
  "flightname": "", 
  "geometry": "", 
  "result": 0
}
```
Search samples
```
/metadata/search?flightname=26518
/metadata/search?geometry=Point:(33.94697109585554, -118.07714843749999)
/metadata/search?geometry=Rectangle:((33.343343561567, -118.69238281249999), (34.34703015733175, -117.04443359374999))
/metadata/search?geometry=Line:(34.72713264415401, -119.37353515624999),(33.67311969894201, -117.76953124999999),(33.983418330994276, -116.20947265624999),(32.4021911686893, -116.91259765624999)
/metadata/search?geometry=Polygon:(34.05626592724434, -117.59374999999999),(33.572488142047554, -118.38476562499999),(32.837100401791204, -117.25317382812499),(33.4809029903106, -116.73681640624999)
```