from textwrap import fill
from turtle import fillcolor, st
import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

map = folium.Map(location=[35,-81], zoom_start=4, tiles="Stamen Terrain")
fgv = folium.FeatureGroup(name="Volcanoes")

def determine_col(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange' 
    else:
        return 'red'

for lt,ln,el in zip(lat,lon,elev):
    fgv.add_child(folium.CircleMarker(location=[lt,ln], radius=6, popup=folium.Popup(str(el) + "m",parse_html=True),
     fill_color = determine_col(el), color='grey', fill = True, fill_opacity=0.7))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r',encoding='utf-8-sig').read(),
 style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
  else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("my_map.html")