# Dealing with coordinates
Very often we require working with some form of positional information. From GPS based Latitude-Longitude, to localised metre-based grids.

Below are two popular methods to allow conversion between Lat-Lon degrees, and UTM grids in meters.


## Using UTM
UTM is a lightweight fast library that does one thing - converts coordinates between Lat-Lon and WGS84 UTM. 

~~~python
import utm
~~~

UTM provides the functions `from_latlon` and `to_latlon`

`from_latlon` has two arguments:

- latitude, a single value or array of values
- longitude, a single value or array of values

and returns

- Easing, UTM coordinate(s) in meters
- Northing, UTM coordinate(s) in meters
- Zone, UTM zone number
- Letter, letter designation of the UTM zone

~~~python
E,N,Z,L = utm.from_latlon(-42.123,156.99)
~~~

`to_latlon` takes 4 arguments:

- Easting, single or array
- Northing, single or array
- Zone, UTM zone number
- Letter, letter designation of the UTM zone

this returns:

- latitude, single value or array
- longitude, single value or array

~~~python
lat,lon = utm.to_latlon(5322344,65143,55,'S')
~~~


### example
Combining with our reading of CSVs, a good example is to load a log file in Lat/Lon and convert to UTM. Wo can them do grid based operations, such as offseting by a fixed distance in meters.

~~~python
import matplotlib.pyplot as plt
import pandas as pd
import utm

# Load data with Lat/Lon positions
log = pd.read_csv('logfiles/log_20220408_001.csv',header=2,skipinitialspace=True)

# convert to UTM coordinates. For Pandas data we use the .values to get the underlying array of values
E,N,Z,L = utm.from_latlon(log.vcc_pos_latitude_fb.values, log.vcc_pos_longitude_fb.values)

# create a plot of the lat/Lon and UTM data
fig,ax = plt.subplots(1,2,figsize=(16,6))
ax[0].plot(log.vcc_pos_longitude_fb, log.vcc_pos_latitude_fb)
ax[1].plot(E, N)

# shift the UTM data by 10m in each direction
E+=10
N+=10

# convert to Lat/Lon and plot against the original
lat,lon = utm.to_latlon(E,N,Z,L)
ax[0].plot(lon, lat,'.',markersize=.1)
~~~


## Using PyProj
PyProj is the python implementation of the Proj library, a fully featured generic coordinate tranformation software. Often UTM is enough, and can be faster for basic conversions. PROJ supports all CRSs, even allows custom definition of CRSs. Beyond coordinate transformation, it also provides Geodetic calculations which can be useful. Proj forms the backbone of QGIS, OpenLayers, and now even SonarWiz

~~~python
import pyproj
~~~

### Coordinate transforms
we make an instance of the Proj class, and define the CRS we wish to use as the basis of our conversion. This can be the simple string (like used in QGIS), or we can be more explicit. The following create equivalent objects:

~~~python
prj = pyproj.Proj(proj='utm', zone=55, ellps='WGS84')
prj = pyproj.Proj('epsg:32755')
~~~

to convert Lat-Lon, we just call the object. Note that for Proj the order is Lon-Lat:

~~~python
E,N = prj(156.999,-41.123)
~~~

The arguments can be single values, or arrays.

To convert back, we just add the `inverse=True` argument

~~~python
lon,lat = prj(E,N,inverse=True)
~~~


### Geodetic Caculations (Great Circle calculations)
The Geod class provides some useful functions related to distance/bearing calculation on Lat/Lon data based on the Great Circle of the underlying ellipse.

~~~python
geod = pyproj.Geod(ellps='WGS84')
~~~

A common operation is to determine a location based on an initial point and some offset given as distance and angle. the `fwd` function will take as arguments:

- lon, initial longitude as single or array
- lat, initial latitude as single or array
- azimuth, angle from start to finish as single or array
- distance, distance in meters as single or array

this returns:
- lon, longitude(s) of result
- lat, latitude(s) of result
- asimuth, angle(s) from result back to initial 

~~~python
lat_1 = -41.123
lon_1 = 156.999
fwd_az = 15.0
dist = 1000.

lon_2, lat_2, az_back = geod.fwd(lon_1,lat_1,fwd_az,dist)
~~~

the `inv` function computes the inverse, where two sets of coordinates are given and the forward and back azimuths are returned in addition to the great-circle distance

~~~python
lat_1 = -41.123
lon_1 = 156.999
lat_2 = -41.114
lon_2 = 157.002

fwd_a, bck_a, dist = geod.inv(lon_1, lat_1, lon_2, lat_2)
~~~

#### example

~~~python
import pyproj

#prj = pyproj.Proj(proj='utm', zone=55, ellps='WGS84')
prj = pyproj.Proj('epsg:32755')

E,N = prj(156.999,-41.123)

lon,lat = prj(E,N,inverse=True)

geod = pyproj.Geod(ellps='WGS84')

lat_1 = -41.123
lon_1 = 156.999
fwd_az = 15.0
dist = 1000.

lon_2, lat_2, az_back = geod.fwd(lon_1,lat_1,fwd_az,dist)

lat_2 = -41.114
lon_2 = 157.002

fwd_a, bck_a, dist = geod.inv(lon_1, lat_1, lon_2, lat_2)
~~~