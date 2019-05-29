#Import statements
import geopandas
import pandas as pd
import requests
from shapely.geometry import Point

#Make API request
request_obj = requests.get("https://phl.carto.com/api/v2/sql?q=SELECT * FROM incidents_part1_part2 WHERE dispatch_date_time >= '2011-01-01' AND dispatch_date_time < '2016-01-01'")
request_json = request_obj.json()

#Convert rows (in dict) to df
df = pd.DataFrame.from_dict(request_json['rows'])

#Drop rows missing location data
df = df.dropna(subset=["point_x", "point_y"]) #need geo info to make the match

#Reshape to group by year and crimes for each geo
df['year'] = pd.to_datetime(df['dispatch_date_time']).dt.year
grouped_df = df.groupby(['year','point_x','point_y']).size().reset_index(name='crime_count')

#Convert to geodf
grouped_df['geometry'] = [Point(xy) for xy in zip(grouped_df.point_x, grouped_df.point_y)]
crime_geo = geopandas.GeoDataFrame(grouped_df, geometry='geometry')

#load the evictions data (from geojson) into a geodf
evictions = geopandas.read_file('data/block-groups.geojson')[['GEOID','geometry']]
evictions = evictions.dropna() #Need both columns to make the match

#Merge the geodfs
eviction_merge = geopandas.sjoin(crime_geo, evictions, how="inner", op='intersects')

#Reshape to get year- block_id - count of crimes
eviction_grouped = eviction_merge.groupby(['year','GEOID'])['crime_count'].sum().reset_index(name='crime_count')

#Write out to csv
eviction_grouped.to_csv('data/crime_data.csv')