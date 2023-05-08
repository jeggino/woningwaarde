import streamlit as st
import pandas as pd
import geopandas as gpd
import datetime
from datetime import date,datetime
import pydeck as pdk
from streamlit_echarts import st_echarts,st_pyecharts

# -------------------------------------------------------
st.set_page_config(
    page_title="Amterdam woon[plaan",
    page_icon="🏠",
    layout="wide",
)

# left, right = st.columns([2,3],gap="large")


# # -------------------------------------------------------
# @st.cache_data() 
# def get_data():
#     df_woningwaarde =  gpd.read_file("https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=WONINGWAARDE_2022&THEMA=woningwaarde")
#     df_woningwaarde = df_woningwaarde[['LABEL', 'geometry']]

#     df_corporatiebezit = gpd.read_file("https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=AFWC_2022&THEMA=afwc_2022")
#     df_corporatiebezit = df_corporatiebezit[['Corporatie_woningen','geometry']]

#     df_functiemix = gpd.read_file("https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=FUNCTIEMIX&THEMA=functiemix")
#     df_functiemix = df_functiemix[['WON', 'VZN', 'WRK','geometry']]

#     df_stadsparken = gpd.read_file("https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=PARKPLANTSOENGROEN&THEMA=stadsparken")
#     df_stadsparken  =df_stadsparken[['Oppervlakte_m2', 'geometry']]

#     df_trammetro = gpd.read_file("https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=TRAMMETRO_PUNTEN_2022&THEMA=trammetro")
#     df_trammetro = df_trammetro[['Modaliteit', 'Lijn', 'geometry']]
#     df_trammetro["Lijn"] = df_trammetro["Lijn"].str.split(expand=False,pat="|").apply(lambda x: len(x))

#     df_bouwjaar = gpd.read_file("https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=BOUWJAAR&THEMA=bouwjaar")

#     df_winkelgebieden = gpd.read_file("https://api.data.amsterdam.nl/v1/wfs/winkelgebieden/?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=winkelgebieden&OUTPUTFORMAT=geojson&SRSNAME=urn:ogc:def:crs:EPSG::4326")
#     df_winkelgebieden = df_winkelgebieden[['oppervlakte','categorienaam', 'geometry']]

#     df = gpd.sjoin(df_woningwaarde,df_bouwjaar,how='left').reset_index().dissolve("index",{"LABEL":"first",
#                                                                                            "Bouwjaar":"mean"}
#                                                                                  ).round()

#     df_1 = gpd.sjoin(df,df_corporatiebezit,how='left').reset_index().dissolve("index",{"LABEL":"first",
#                                                                                        "Bouwjaar":"first",
#                                                                                        "Corporatie_woningen":"sum"},
#                                                                               dropna=False
#                                                                              ).round()
#     df_2 = gpd.sjoin(df_1,df_trammetro,how='left').reset_index().dissolve("index",{"LABEL":"first","Bouwjaar":"first",
#                                                                                    "Corporatie_woningen":"first",
#                                                                                    "Lijn":"sum"},
#                                                                           dropna=False).round()

#     df_3 = gpd.sjoin(df_2,df_functiemix,how='left').reset_index().dissolve("index",{"LABEL":"first","Bouwjaar":"first",
#                                                                                     "Corporatie_woningen":"first",
#                                                                                     "Lijn":"first",
#                                                                                     'WON':"sum",
#                                                                                     'VZN':"sum",
#                                                                                     'WRK':"sum"},
#                                                                            dropna=False).round()

#     df_4 = gpd.sjoin(df_3,df_stadsparken,how='left').reset_index().dissolve("index",{"LABEL":"first","Bouwjaar":"first",
#                                                                                     "Corporatie_woningen":"first",
#                                                                                     "Lijn":"first",
#                                                                                     'WON':"first",
#                                                                                     'VZN':"first",
#                                                                                     'WRK':"first",
#                                                                                      "Oppervlakte_m2":"sum"},
#                                                                             dropna=False).round()

#     return df_4


# # -------------------------------------------------------
# df = get_data()


# # -------------------------------------------------------
# from sklearn.preprocessing import MinMaxScaler
# import sklearn.cluster as cluster
# from kneed import KneeLocator

# @st.cache_data(experimental_allow_widgets=True) 
# def analysis_cluster():
#     df_segmentation = df[['geometry', 'LABEL','WON','VZN', 'WRK']]

#     # Standardizing the features
#     df_feature = df_segmentation.iloc[:,2:]
#     x_MinMax = MinMaxScaler().fit_transform(df_feature)
#     kmeans_kwargs = {
#         "init": "random",
#         "n_init": 10,
#         "max_iter": 300,
#         "random_state": 42,
#     }

#     # A list holds the SSE values for each k
#     sse = []
#     for k in range(2, 11):
#         kmeans = cluster.KMeans(n_clusters=k, **kmeans_kwargs)
#         kmeans.fit(x_MinMax)
#         sse.append(kmeans.inertia_)

#     kl = KneeLocator(
#         range(2, 11), sse, curve="convex", direction="decreasing"
#     )


#     # -------------------------------------------------------
#     option_clusters = st.sidebar.number_input(f'The best number of cluster is {kl.elbow}, but you can play aroud',
#                                               min_value=2, max_value=8,step=1,value=kl.elbow)

#     kmeans = cluster.KMeans(n_clusters=option_clusters,init="k-means++")
#     kmeans = kmeans.fit(x_MinMax)

#     df_segmentation['Clusters'] = kmeans.labels_ + 1
    
#     return df_segmentation, option_clusters, x_MinMax


# # -------------------------------------------------------
# df_segmentation, option_clusters, x_MinMax = analysis_cluster()


# # -------------------------------------------------------
# import altair as alt
# import seaborn as sns


# PALETTE = [ 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r']
# option_palette = st.sidebar.selectbox('Palette',PALETTE,index=4)
# palette = sns.color_palette(option_palette,n_colors=option_clusters)


# option_outliers = left.checkbox('outliers')

# source = df_segmentation.melt(id_vars="Clusters",value_vars=['WON','VZN', 'WRK'])

# chart = alt.Chart(source).mark_boxplot(ticks=True,outliers=option_outliers).encode(
#     x=alt.X("Clusters:N", title=None, axis=alt.Axis(labels=False, ticks=False), scale=alt.Scale(padding=1)), 
#     y=alt.Y("value:Q"), 
#     color = alt.Color("Clusters:N", scale=alt.Scale(range=palette.as_hex())),
#     column=alt.Column('variable:N', sort=['WON','VZN', 'WRK'], header=alt.Header(orient='bottom'))
# ).properties(
#     width=100
# ).configure_facet(
#     spacing=7
# ).configure_view(
#     stroke=None
# )
    

# # -------------------------------------------------------
# import pydeck as pdk

# option_tootip = st.sidebar.selectbox('',('WON','VZN', 'WRK'))

# colors = dict(zip(list(range(1,option_clusters+1)),
#                   palette
#                  )
#              )

# df_segmentation['Color'] = df_segmentation['Clusters'].map(colors)
# df_segmentation['Color'] = df_segmentation["Color"].apply(lambda x: [round(i * 255) for i in x])


# polygon_layer = pdk.Layer(
#     'GeoJsonLayer',
#     df_segmentation,
#     opacity=1,
#     stroked=True,
#     filled=True,
#     extruded=True,
#     get_elevation=option_tootip,
#     elevation_scale=0.01,
#     wireframe=True,
#     get_fill_color='Color',
#     get_line_color=[255, 255, 255],
#     pickable=True,
# )

# INITIAL_VIEW_STATE = pdk.ViewState(
#     latitude=52.374119, 
#     longitude=4.895906,
#     zoom=10,
#     pitch=35,
#     bearing=0
# )

# tooltip = {"text": "Cluster: {Clusters} \n WON: {WON} \n VZN: {VZN} \n WRK: {WRK}"}

# r = pdk.Deck(
#     [polygon_layer],
#     initial_view_state=INITIAL_VIEW_STATE,
#     tooltip = tooltip,
#     map_style = "light_no_labels",
# )


# #-----------------------------
# with left:
#     st.altair_chart(chart, use_container_width=False,theme=None)
    
# with right:
#     st.pydeck_chart(pydeck_obj=r, use_container_width=True)
    
#     def filter_by_viewport(widget_instance, payload):
        
#         return payload['data']
            
#     st.write(r.deck_widget.on_click(filter_by_viewport))
       
    
# #-----------------------------
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from yellowbrick.classifier import ClassPredictionError
# from streamlit_yellowbrick import st_yellowbrick
# from sklearn.neural_network import MLPClassifier
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.svm import SVC
# from sklearn.gaussian_process import GaussianProcessClassifier
# from sklearn.gaussian_process.kernels import RBF
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
# from sklearn.naive_bayes import GaussianNB
# from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

# MODELS = [
#     "Nearest Neighbors",
#     "Linear SVM",
#     "RBF SVM",
#     "Gaussian Process",
#     "Decision Tree",
#     "Random Forest",
#     "Neural Net",
#     "AdaBoost",
#     "Naive Bayes",
#     "QDA",
# ]

# classifiers = [
#     KNeighborsClassifier(3),
#     SVC(kernel="linear", C=0.025),
#     SVC(gamma=2, C=1),
#     GaussianProcessClassifier(1.0 * RBF(1.0)),
#     DecisionTreeClassifier(max_depth=5),
#     RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
#     MLPClassifier(alpha=1, max_iter=1000),
#     AdaBoostClassifier(),
#     GaussianNB(),
#     QuadraticDiscriminantAnalysis(),
# ]

# dict_models = dict(zip(MODELS,classifiers))

# option_model = st.sidebar.selectbox("Select a model", MODELS, index=0)

# #Create classification dataset
# X = x_MinMax
# y = df_segmentation["Clusters"]


# # Perform 80/20 training/test split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,
#                                                     random_state=42)
# # Instantiate the classification model and visualizer
# visualizer = ClassPredictionError(
#     dict_models[option_model], 
# )

# # Fit the training data to the visualizer
# visualizer.fit(X_train, y_train)

# # Evaluate the model on the test data
# visualizer.score(X_test, y_test)

# # Draw visualization
# st_yellowbrick(visualizer) 


# #-----------------------------------
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events
import streamlit as st
from streamlit_plotly_events import plotly_events

import pandas as pd
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

import plotly.express as px

fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
selected_points = plotly_events(fig, click_event=True, hover_event=True)


# df_folium = df_segmentation
# df_folium["long"] = df_segmentation.centroid.x
# df_folium["lat"] = df_segmentation.centroid.y

# source = df_segmentation
# fig = px.scatter_mapbox(source, lat="lat", lon="long", hover_name="Clusters", hover_data=["Clusters"],color="Clusters",
#                         zoom=8, height=300)
# fig.update_layout(
#     mapbox_style="white-bg",
#     mapbox_layers=[
#         {
#             "below": 'traces',
#             "sourcetype": "raster",
#             "sourceattribution": "United States Geological Survey",
#             "source": [
#                 "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
#             ]
#         }
#       ])
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.update_layout(mapbox_style="open-street-map")

# selected_points = plotly_events(fig, click_event=True, hover_event=True)
# st.write(selected_points)




# import folium
# from streamlit_folium import st_folium

# df_folium = df_segmentation
# df_folium["long"] = df_segmentation.centroid.x
# df_folium["lat"] = df_segmentation.centroid.y

# dictionary_colors = dict(zip(df_folium["Clusters"].unique(),list(folium.map.Icon.color_options)))
# df_folium["Color"] = df_folium["Clusters"].map(dictionary_colors)

# source = df_folium.iloc[:1000,:]

# m = folium.Map(location=[source["lat"].mean(),source["long"].mean()])
# folium.TileLayer('cartodbpositron').add_to(m)

# dictionar_layers = {}
# for i in df_folium["Clusters"].unique():
#     dictionar_layers[i] = folium.FeatureGroup(name=f'Clusters {i}', show=False)

# for key in dictionar_layers.keys():
#     m.add_child(dictionar_layers[key])

# for row, columns in source.iterrows():
    
#     folium.Marker(
#         [columns["lat"], columns["long"]], 
#         tooltip=columns["Clusters"],
#         icon=folium.Icon(color=columns["Color"], icon="glyphicon-map-marker"),
#     ).add_to(dictionar_layers[columns["Clusters"]])

# folium.map.LayerControl(position='topright', collapsed=True, autoZIndex=True).add_to(m)

# c1, c2 = st.columns([2,1])
# with c1:
#     output = st_folium(
#         m
#     )

# with c2:
#     st.write(output)

    
    


















# # -------------------------------------------------------
# # -------------------------------------------------------
# # --------------TO CHECK---------------------------------
# # -------------------------------------------------------
# # -------------------------------------------------------
# sidebar = st.sidebar


# # -------------------------------------------------------
# data = df["df_woningwaarde"].groupby("LABEL",as_index=False).size()
# data_echarts = []
# for idx, row in data.iterrows():
#     data_echarts.append({"value": row["size"], "name": row["LABEL"]})

# st.dataframe(data)

# option = {
#     "legend": {"top": "bottom"},
#     "labelLine": {
#         "lineStyle": {
#           "color": '#235894'
#         }
#       },
#     "toolbox": {
#         "show": False,
#         "feature": {
#             "mark": {"show": True},
#             "dataView": {"show": True, "readOnly": False},
#             "restore": {"show": True},
#             "saveAsImage": {"show": True},
#         },
#     },
#     "series": [
#         {
#             "name": "vvdr",
#             "type": "pie",
#             "radius": [50, 250],
#             "center": ["50%", "50%"],
#             "roseType": "area",
#             "itemStyle": {"borderRadius": 8},
#             "data": data_echarts,
#         }
#     ],
# }

# events = {
#     "click": "function(params) { console.log(params.name); return params.value }",
#     "dblclick": None,
#     "legendselectchanged": "function(params) { return params.selected }",
# }



# s = st_echarts(
#     options=option, height="600px", events=events, key="render_basic_bar_events"
# )


# if s is not None:
    
    
#     st.write(s)
    
#     value_gauge = round((s / data["size"].sum()),2)
   
#     liquidfill_option = {
#         "series": [{"type": "liquidFill", "data": [value_gauge],
#                     'backgroundStyle': {
#                             'borderWidth': 5,
#                             'borderColor': 'red',
#                             'color': 'yellow'
#                         }
#                    }]
#     }
    
   
#     st_echarts(liquidfill_option)
    

    
# gaugeData = [
#   {
#     'value': 20,
#     'name': 'Perfect',
#     'title': {
#       'offsetCenter': ['0%', '-30%']
#     },
#     'detail': {
#       'valueAnimation': True,
#       'offsetCenter': ['0%', '-20%']
#     }
#   },
#   {
#     'value': s,
#     'name': 'Good',
#     'title': {
#       'offsetCenter': ['0%', '0%']
#     },
#     'detail': {
#       'valueAnimation': True,
#       'offsetCenter': ['0%', '10%']
#     }
#   },
#   {
#     'value': 60,
#     'name': 'Commonly',
#     'title': {
#       'offsetCenter': ['0%', '30%']
#     },
#     'detail': {
#       'valueAnimation': True,
#       'offsetCenter': ['0%', '40%']
#     }
#   }
# ];

# option = {
#   'series': [
#     {
#       'type': 'gauge',
#       'startAngle': 90,
#       'endAngle': -270,
#       'pointer': {
#         'show': False
#       },
#       'progress': {
#         'show': True,
#         'overlap': False,
#         'roundCap': False,
#         'clip': False,
#         'itemStyle': {
#           'borderWidth': 1,
#           'borderColor': '#464646'
#         }
#       },
#       'axisLine': {
#         'lineStyle': {
#           'width': 40
#         }
#       },
#       'splitLine': {
#         'show': False,
#         'distance': 0,
#         'length': 10
#       },
#       'axisTick': {
#         'show': False
#       },
#       'axisLabel': {
#         'show': False,
#         'distance': 50
#       },
#       'data': gaugeData,
#       'title': {
#         'fontSize': 14
#       },
#       'detail': {
#         'width': 50,
#         'height': 14,
#         'fontSize': 14,
#         'color': 'inherit',
#         'borderColor': 'inherit',
#         'borderRadius': 20,
#         'borderWidth': 1,
#         'formatter': '{value}'
#       }
#     }
#   ]
# };

# st_echarts(option, height="600px")


# #------------------------------------
# option = {
#   'tooltip': {
#     'formatter': '{a} <br/>{b} : {c}%'
#   },
#   'series': [
#     {
#       'name': 'Pressure',
#       'type': 'gauge',
#       'progress': {
#         'show': True
#       },
#       'detail': {
#         'valueAnimation': True,
#         'formatter': '{value}'
#       },
#       'data': [
#         {
#           'value': 50,
#           'name': 'SCORE'
#         }
#       ]
#     }
#   ]
# };

# st_echarts(option, height="600px")


# #------------------------------------
# option = {
#   'series': [
#     {
#       'type': 'gauge',
#       'center': ['50%', '60%'],
#       'startAngle': 200,
#       'endAngle': -20,
#       'min': 0,
#       'max': 360,
#       'splitNumber': 12,
#       'itemStyle': {
#         'color': '#FFAB91'
#       },
#       'progress': {
#         'show': True,
#         'width': 30
#       },
#       'pointer': {
#         'show': False
#       },
#       'axisLine': {
#         'lineStyle': {
#           'width': 30
#         }
#       },
#       'axisTick': {
#         'distance': -45,
#         'splitNumber': 5,
#         'lineStyle': {
#           'width': 2,
#           'color': '#999'
#         }
#       },
#       'splitLine': {
#         'distance': -52,
#         'length': 14,
#         'lineStyle': {
#           'width': 3,
#           'color': '#999'
#         }
#       },
#       'axisLabel': {
#         'distance': -20,
#         'color': '#999',
#         'fontSize': 20
#       },
#       'anchor': {
#         'show': False
#       },
#       'title': {
#         'show': False
#       },
#       'detail': {
#         'valueAnimation': True,
#         'width': '60%',
#         'lineHeight': 40,
#         'borderRadius': 8,
#         'offsetCenter': [0, '-15%'],
#         'fontSize': 60,
#         'fontWeight': 'bolder',
#         'formatter': '{value} °C',
#         'color': 'inherit'
#       },
#       'data': [
#         {
#           'value': 20
#         }
#       ]
#     },
#     {
#       'type': 'gauge',
#       'center': ['50%', '60%'],
#       'startAngle': 200,
#       'endAngle': -20,
#       'min': 0,
#       'max': 360,
#       'itemStyle': {
#         'color': '#FD7347'
#       },
#       'progress': {
#         'show': True,
#         'width': 8
#       },
#       'pointer': {
#         'show': False
#       },
#       'axisLine': {
#         'show': False
#       },
#       'axisTick': {
#         'show': False
#       },
#       'splitLine': {
#         'show': False
#       },
#       'axisLabel': {
#         'show': False
#       },
#       'detail': {
#         'show': False
#       },
#       'data': [
#         {
#           'value': 20
#         }
#       ]
#     }
#   ]
# };

# st_echarts(
#     options=option, height="600px")


# #------------------------------------
# options = {
#     "title": {"text": "某站点用户访问来源", "subtext": "纯属虚构", "left": "center"},
#     "tooltip": {"trigger": "item"},
#     "legend": {
#         "orient": "vertical",
#         "left": "left",
#     },
#     "series": [
#         {
#             "name": "访问来源",
#             "type": "pie",
#             "radius": "50%",
#             "data": [
#                 {"value": 1048, "name": "搜索引擎"},
#                 {"value": 735, "name": "直接访问"},
#                 {"value": 580, "name": "邮件营销"},
#                 {"value": 484, "name": "联盟广告"},
#                 {"value": 300, "name": "视频广告"},
#             ],
#             "emphasis": {
#                 "itemStyle": {
#                     "shadowBlur": 10,
#                     "shadowOffsetX": 0,
#                     "shadowColor": "rgba(0, 0, 0, 0.5)",
#                 }
#             },
#         }
#     ],
# }
# st.markdown("Select a legend, see the detail")
# events = {
#     "legendselectchanged": "function(params) { return params.selected }",
# }
# s = st_echarts(
#     options=options, events=events, height="600px", key="render_pie_events"
# )
# if s is not None:
#     st.write(s)
    





# #---------------------------
# import pyecharts.options as opts
# from pyecharts.charts import Pie

# """
# Gallery 使用 pyecharts 1.1.0
# 参考地址: https://echarts.apache.org/examples/editor.html?c=pie-nest

# 目前无法实现的功能:

# 1、暂无
# """


# inner_x_data = ["直达", "营销广告", "搜索引擎"]
# inner_y_data = [335, 679, 1548]
# inner_data_pair = [list(z) for z in zip(inner_x_data, inner_y_data)]

# outer_x_data = ["直达", "营销广告", "搜索引擎", "邮件营销", "联盟广告", "视频广告", "百度", "谷歌", "必应", "其他"]
# outer_y_data = [335, 310, 234, 135, 1048, 251, 147, 102]
# outer_data_pair = [list(z) for z in zip(outer_x_data, outer_y_data)]

# c_pie = (
#     Pie()
#     .add(
#         series_name="访问来源",
#         data_pair=inner_data_pair,
#         radius=[0, "30%"],
#         label_opts=opts.LabelOpts(position="inner"),
#     )
#     .add(
#         series_name="访问来源",
#         radius=["40%", "55%"],
#         data_pair=outer_data_pair,
#         label_opts=opts.LabelOpts(
#             position="outside",
#             formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
#             background_color="#eee",
#             border_color="#aaa",
#             border_width=1,
#             border_radius=4,
#             rich={
#                 "a": {"color": "#999", "lineHeight": 22, "align": "center"},
#                 "abg": {
#                     "backgroundColor": "#e3e3e3",
#                     "width": "100%",
#                     "align": "right",
#                     "height": 22,
#                     "borderRadius": [4, 4, 0, 0],
#                 },
#                 "hr": {
#                     "borderColor": "#aaa",
#                     "width": "100%",
#                     "borderWidth": 0.5,
#                     "height": 0,
#                 },
#                 "b": {"fontSize": 16, "lineHeight": 33},
#                 "per": {
#                     "color": "#eee",
#                     "backgroundColor": "#334455",
#                     "padding": [2, 4],
#                     "borderRadius": 2,
#                 },
#             },
#         ),
#     )
#     .set_global_opts(legend_opts=opts.LegendOpts(pos_left="left", orient="vertical"))
#     .set_series_opts(
#         tooltip_opts=opts.TooltipOpts(
#             trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
#         )
#     )
    
# )




# #-----------------------
# from pyecharts import options as opts
# from pyecharts.charts import EffectScatter
# from pyecharts.faker import Faker

# c_w = (
#     EffectScatter()
#     .add_xaxis(Faker.choose())
#     .add_yaxis("", Faker.values())
#     .set_global_opts(
#         title_opts=opts.TitleOpts(title="EffectScatter-显示分割线"),
#         xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
#         yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
#     )
# )

# st_pyecharts(c_w,height="600px")


# #----------------------------------
# from pyecharts.charts import Line
# df_line = df["df_corporatiebezit"].groupby("Bouwjaar_rond",as_index=False).size().tail(20)

# c = (
#     Line()
#     .add_xaxis(df_line["Bouwjaar_rond"].tolist())
#     .add_yaxis(
#         "Points",
#        [1, 3, 9, 27, 81, 247, 741, 2223, 6669],
#         markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
#         markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min"),opts.MarkPointItem(type_="max")]),
#         linestyle_opts=opts.LineStyleOpts(color="green", width=4, type_="dashed"))
#     .set_global_opts(title_opts=opts.TitleOpts(title="Line-MarkPoint"))
# )
# st_pyecharts(c,height="600px")


# #-----------------
# from pyecharts import options as opts
# from pyecharts.charts import Scatter
# from pyecharts.faker import Faker

# c_scatter = (
#     Scatter()
#     .add_xaxis(list(range(10)))
#     .add_yaxis("Serie 1", Faker.values())
#     .add_yaxis("Serie 2", Faker.values())
#     .set_global_opts(
#         title_opts=opts.TitleOpts(title="Scatter-VisualMap(Size)"),
#         visualmap_opts=opts.VisualMapOpts(type_="size", max_=150, min_=20),
#     )
# )




# # -------------------------------------------------------
# sidebar = st.sidebar
# row_1_1,row_1_2 = st.columns([3,2], gap="large")
# row_1_2_tab1, row_1_2_tab2 = row_1_2.tabs(["Pie-chart 🥧", "Sunburst-chart ☀️"])
# "---"
# row_2_1, row_2_2 = st.columns([3,1], gap="large")
# "---"
# row_3_1,row_3_2 = st.columns([1,6], gap="large")

# with row_2_1:
#     st_pyecharts(c_scatter,height="600px")
    
# with row_2_2:
#     st_pyecharts(c_pie,height="600px")
    

# #-----------------------------------
# from st_on_hover_tabs import on_hover_tabs

# st.header("Custom tab component for on-hover navigation bar")
# st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

# with st.sidebar:
#         tabs = on_hover_tabs(tabName=['Dashboard', 'Money', 'Economy'], 
#                              iconName=['dashboard', 'money', 'economy'],
#                              styles = {'navtab': {'background-color':'#111',
#                                                   'color': '#818181',
#                                                   'font-size': '15px',
#                                                   'transition': '.6s',
#                                                   'white-space': 'nowrap',
#                                                   'text-transform': 'uppercase'},
#                                        'tabOptionsStyle': {':hover :hover': {'color': 'red',
#                                                                       'cursor': 'pointer'}},
#                                        'iconStyle':{'position':'fixed',
#                                                     'left':'7.5px',
#                                                     'text-align': 'left'},
#                                        'tabStyle' : {'list-style-type': 'none',
#                                                      'margin-bottom': '30px',
#                                                      'padding-left': '30px'}},
#                              key="1")
        
        

# if tabs =='Dashboard':
#     st.title("Navigation Bar")
#     st.write('Name of option is {}'.format(tabs))
#     genre = st.sidebar.radio("What\'s your favorite movie genre",('Comedy', 'Drama', 'Documentary'))

# elif tabs == 'Money':
#     st.title("Paper")
#     st.write('Name of option is {}'.format(tabs))

# elif tabs == 'Economy':
#     st.title("Tom")
#     st.write('Name of option is {}'.format(tabs))
    

