import streamlit as st
import pandas as pd
import geopandas as gpd
import datetime
from datetime import date,datetime
import altair as alt
import pydeck as pdk
import streamlit_folium as stf

from streamlit_echarts import st_echarts

# -------------------------------------------------------
st.set_page_config(
    page_title="Amterdam woon[plaan",
    page_icon="🏠",
    layout="wide",
)


# -------------------------------------------------------
@st.cache_data() 
def get_data():
    df_woningwaarde =  gpd.read_file("https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=WONINGWAARDE_2022&THEMA=woningwaarde")
    df_corporatiebezit = gpd.read_file("https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=AFWC_2022&THEMA=afwc_2022")
    df_functiemix = gpd.read_file("https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=FUNCTIEMIX&THEMA=functiemix")
    df_functiekaart = gpd.read_file("https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=FUNCTIEKAART&THEMA=functiekaart")
    df_MAX_SNELHEID = gpd.read_file("https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=DERTIG&THEMA=30km")
    df_stadsparken = gpd.read_file("https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=PARKPLANTSOENGROEN&THEMA=stadsparken")
    df_geluid = gpd.read_file("https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=GELUID_VERKEER||1&THEMA=geluid")
    df_trammetro = gpd.read_file("https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=TRAMMETRO_PUNTEN_2022&THEMA=trammetro")
    df_bouwjaar = gpd.read_file("https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=BOUWJAAR&THEMA=bouwjaar")
    df_winkelgebieden = gpd.read_file("https://api.data.amsterdam.nl/v1/wfs/winkelgebieden/?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=winkelgebieden&OUTPUTFORMAT=geojson&SRSNAME=urn:ogc:def:crs:EPSG::4326")
    return dict(zip(["df_woningwaarde","df_corporatiebezit","df_functiemix","df_functiekaart","df_MAX_SNELHEID","df_stadsparken","df_geluid", ],
                    [df_woningwaarde,df_corporatiebezit,df_functiemix,df_functiekaart,df_MAX_SNELHEID,df_stadsparken,df_geluid, ]))


# -------------------------------------------------------
df = get_data()


# -------------------------------------------------------
sidebar = st.sidebar


# -------------------------------------------------------
data = df["df_woningwaarde"].groupby("LABEL",as_index=False).size().to_json()
st_dataframe(data)

options = {
    "tooltip": {"trigger": "item"},
    "legend": {"top": "5%", "left": "center"},
    "series": [
        {
            "name": "访问来源",
            "type": "pie",
            "radius": ["40%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {
                "borderRadius": 10,
                "borderColor": "#fff",
                "borderWidth": 2,
            },
            "label": {"show": False, "position": "center"},
            "emphasis": {
                "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
            },
            "labelLine": {"show": False},
            "data": [
                {"value": 1048, "name": "Alberto"},
                {"value": 735, "name": "tommaso"},
                {"value": 580, "name": "Pasquale"},
                {"value": 484, "name": "Romina"},
                {"value": 300, "name": "Luigi"},
            ],
        }
    ],
}
st_echarts(
    options=options, height="500px",
)
