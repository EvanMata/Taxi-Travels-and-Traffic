import json
import pandas as pd
from shapely.geometry import Point, Polygon, shape
import sqlite3
import folium
import os

def createheat(x):
    '''
    Use folium to create heatmap for education based on GeoJson file 
    with the boudnaries for the community areas. Essentially, 
    folium does the joining of the information automatically. 
    '''

    df = pd.read_csv("heatmap.csv",names=['tract','timezone','count'])
    df.dropna(inplace=True)
    print(df)

    dat = df.query('timezone==4')

    m = folium.Map([40.782865, -73.965355], zoom_start=11)
    m.choropleth(
        geo_data=open('tract.json').read(),
        data=dat,
        columns=['tract', 'count'],
        key_on='feature.properties.namelsad',
        fill_color='YlGn',
        #line_opacity=0.5
        )

    m.save('final-map.html')