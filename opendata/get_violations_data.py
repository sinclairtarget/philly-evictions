#Import statements
import geopandas
import pandas as pd
import requests
from shapely.geometry import Point

#Make API request
request_obj = requests.get("https://phl.carto.com/api/v2/sql?q=SELECT *, ST_Y(the_geom) AS lat, ST_X(the_geom) AS lng FROM li_unsafe WHERE violationdate >= '2009-01-01' AND violationdate < '2016-01-01'")
request_json = request_obj.json()

#Convert rows (in dict) to df
df = pd.DataFrame.from_dict(request_json['rows'])

#Drop rows missing location data
df = df.dropna(subset=["lat", "lng"])

#Reshape to group by year and crimes for each geo
df['year'] = pd.to_datetime(df['violationdate']).dt.year
grouped_df = df.groupby(['year','lng','lat']).size().reset_index(name='violations_count')

#Convert to geodf
grouped_df['geometry'] = [Point(xy) for xy in zip(grouped_df.lng, grouped_df.lat)]
violations_geo = geopandas.GeoDataFrame(grouped_df, geometry='geometry')

#load the evictions data (from geojson) into a geodf
evictions = geopandas.read_file('data/block-groups.geojson')[['GEOID','geometry']]
evictions = evictions.dropna() #Need both columns to make the match

#Merge the geodfs
violations_merge = geopandas.sjoin(violations_geo, evictions, how="inner", op='intersects')

#Reshape to get year- bloc_id - count of violations
violations_grouped = violations_merge.groupby(['year','GEOID'])['violations_count'].sum().reset_index(name='violations_count')
#Write out to csv
violations_grouped.to_csv('../data/violations.csv')
