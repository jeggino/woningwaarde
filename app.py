import streamlit as st
import pandas as pd
import geopandas as gpd
import datetime
from datetime import date,datetime
import altair as alt
import pydeck as pdk
import streamlit_folium as stf

from streamlit_echarts import st_echarts,st_pyecharts

import math 

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
data = df["df_woningwaarde"].groupby("LABEL",as_index=False).size()
data_echarts = []
for idx, row in data.iterrows():
    data_echarts.append({"value": row["size"], "name": row["LABEL"]})

st.dataframe(data)

option = {
    "legend": {"top": "bottom"},
    "labelLine": {
        "lineStyle": {
          "color": '#235894'
        }
      },
    "toolbox": {
        "show": False,
        "feature": {
            "mark": {"show": True},
            "dataView": {"show": True, "readOnly": False},
            "restore": {"show": True},
            "saveAsImage": {"show": True},
        },
    },
    "series": [
        {
            "name": "vvdr",
            "type": "pie",
            "radius": [50, 250],
            "center": ["50%", "50%"],
            "roseType": "area",
            "itemStyle": {"borderRadius": 8},
            "data": data_echarts,
        }
    ],
}

events = {
    "click": "function(params) { console.log(params.name); return params.value }",
    "dblclick": None,
    "legendselectchanged": "function(params) { return params.selected }",
}



s = st_echarts(
    options=option, height="600px", events=events, key="render_basic_bar_events"
)


if s is not None:
    
    
    st.write(s)
    
    value_gauge = round((s / data["size"].sum()),2)
   
    liquidfill_option = {
        "series": [{"type": "liquidFill", "data": [value_gauge],
                    'backgroundStyle': {
                            'borderWidth': 5,
                            'borderColor': 'red',
                            'color': 'yellow'
                        }
                   }]
    }
    
   
    st_echarts(liquidfill_option)
    

    
gaugeData = [
  {
    'value': 20,
    'name': 'Perfect',
    'title': {
      'offsetCenter': ['0%', '-30%']
    },
    'detail': {
      'valueAnimation': True,
      'offsetCenter': ['0%', '-20%']
    }
  },
  {
    'value': s,
    'name': 'Good',
    'title': {
      'offsetCenter': ['0%', '0%']
    },
    'detail': {
      'valueAnimation': True,
      'offsetCenter': ['0%', '10%']
    }
  },
  {
    'value': 60,
    'name': 'Commonly',
    'title': {
      'offsetCenter': ['0%', '30%']
    },
    'detail': {
      'valueAnimation': True,
      'offsetCenter': ['0%', '40%']
    }
  }
];

option = {
  'series': [
    {
      'type': 'gauge',
      'startAngle': 90,
      'endAngle': -270,
      'pointer': {
        'show': False
      },
      'progress': {
        'show': True,
        'overlap': False,
        'roundCap': False,
        'clip': False,
        'itemStyle': {
          'borderWidth': 1,
          'borderColor': '#464646'
        }
      },
      'axisLine': {
        'lineStyle': {
          'width': 40
        }
      },
      'splitLine': {
        'show': False,
        'distance': 0,
        'length': 10
      },
      'axisTick': {
        'show': False
      },
      'axisLabel': {
        'show': False,
        'distance': 50
      },
      'data': gaugeData,
      'title': {
        'fontSize': 14
      },
      'detail': {
        'width': 50,
        'height': 14,
        'fontSize': 14,
        'color': 'inherit',
        'borderColor': 'inherit',
        'borderRadius': 20,
        'borderWidth': 1,
        'formatter': '{value}'
      }
    }
  ]
};

st_echarts(option, height="600px")


#------------------------------------
option = {
  'tooltip': {
    'formatter': '{a} <br/>{b} : {c}%'
  },
  'series': [
    {
      'name': 'Pressure',
      'type': 'gauge',
      'progress': {
        'show': True
      },
      'detail': {
        'valueAnimation': True,
        'formatter': '{value}'
      },
      'data': [
        {
          'value': 50,
          'name': 'SCORE'
        }
      ]
    }
  ]
};

st_echarts(option, height="600px")


#------------------------------------
option = {
  'series': [
    {
      'type': 'gauge',
      'center': ['50%', '60%'],
      'startAngle': 200,
      'endAngle': -20,
      'min': 0,
      'max': 360,
      'splitNumber': 12,
      'itemStyle': {
        'color': '#FFAB91'
      },
      'progress': {
        'show': True,
        'width': 30
      },
      'pointer': {
        'show': False
      },
      'axisLine': {
        'lineStyle': {
          'width': 30
        }
      },
      'axisTick': {
        'distance': -45,
        'splitNumber': 5,
        'lineStyle': {
          'width': 2,
          'color': '#999'
        }
      },
      'splitLine': {
        'distance': -52,
        'length': 14,
        'lineStyle': {
          'width': 3,
          'color': '#999'
        }
      },
      'axisLabel': {
        'distance': -20,
        'color': '#999',
        'fontSize': 20
      },
      'anchor': {
        'show': False
      },
      'title': {
        'show': False
      },
      'detail': {
        'valueAnimation': True,
        'width': '60%',
        'lineHeight': 40,
        'borderRadius': 8,
        'offsetCenter': [0, '-15%'],
        'fontSize': 60,
        'fontWeight': 'bolder',
        'formatter': '{value} °C',
        'color': 'inherit'
      },
      'data': [
        {
          'value': 20
        }
      ]
    },
    {
      'type': 'gauge',
      'center': ['50%', '60%'],
      'startAngle': 200,
      'endAngle': -20,
      'min': 0,
      'max': 360,
      'itemStyle': {
        'color': '#FD7347'
      },
      'progress': {
        'show': True,
        'width': 8
      },
      'pointer': {
        'show': False
      },
      'axisLine': {
        'show': False
      },
      'axisTick': {
        'show': False
      },
      'splitLine': {
        'show': False
      },
      'axisLabel': {
        'show': False
      },
      'detail': {
        'show': False
      },
      'data': [
        {
          'value': 20
        }
      ]
    }
  ]
};

st_echarts(
    options=option, height="600px")


#------------------------------------
options = {
    "title": {"text": "某站点用户访问来源", "subtext": "纯属虚构", "left": "center"},
    "tooltip": {"trigger": "item"},
    "legend": {
        "orient": "vertical",
        "left": "left",
    },
    "series": [
        {
            "name": "访问来源",
            "type": "pie",
            "radius": "50%",
            "data": [
                {"value": 1048, "name": "搜索引擎"},
                {"value": 735, "name": "直接访问"},
                {"value": 580, "name": "邮件营销"},
                {"value": 484, "name": "联盟广告"},
                {"value": 300, "name": "视频广告"},
            ],
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)",
                }
            },
        }
    ],
}
st.markdown("Select a legend, see the detail")
events = {
    "legendselectchanged": "function(params) { return params.selected }",
}
s = st_echarts(
    options=options, events=events, height="600px", key="render_pie_events"
)
if s is not None:
    st.write(s)
    
    
data = [
  [
    [28604, 77, 17096869, 'Australia', 1990],
    [31163, 77.4, 27662440, 'Canada', 1990],
    [1516, 68, 1154605773, 'China', 1990],
    [13670, 74.7, 10582082, 'Cuba', 1990],
    [28599, 75, 4986705, 'Finland', 1990],
    [29476, 77.1, 56943299, 'France', 1990],
    [31476, 75.4, 78958237, 'Germany', 1990],
    [28666, 78.1, 254830, 'Iceland', 1990],
    [1777, 57.7, 870601776, 'India', 1990],
    [29550, 79.1, 122249285, 'Japan', 1990],
    [2076, 67.9, 20194354, 'North Korea', 1990],
    [12087, 72, 42972254, 'South Korea', 1990],
    [24021, 75.4, 3397534, 'New Zealand', 1990],
    [43296, 76.8, 4240375, 'Norway', 1990],
    [10088, 70.8, 38195258, 'Poland', 1990],
    [19349, 69.6, 147568552, 'Russia', 1990],
    [10670, 67.3, 53994605, 'Turkey', 1990],
    [26424, 75.7, 57110117, 'United Kingdom', 1990],
    [37062, 75.4, 252847810, 'United States', 1990]
  ],
  [
    [44056, 81.8, 23968973, 'Australia', 2015],
    [43294, 81.7, 35939927, 'Canada', 2015],
    [13334, 76.9, 1376048943, 'China', 2015],
    [21291, 78.5, 11389562, 'Cuba', 2015],
    [38923, 80.8, 5503457, 'Finland', 2015],
    [37599, 81.9, 64395345, 'France', 2015],
    [44053, 81.1, 80688545, 'Germany', 2015],
    [42182, 82.8, 329425, 'Iceland', 2015],
    [5903, 66.8, 1311050527, 'India', 2015],
    [36162, 83.5, 126573481, 'Japan', 2015],
    [1390, 71.4, 25155317, 'North Korea', 2015],
    [34644, 80.7, 50293439, 'South Korea', 2015],
    [34186, 80.6, 4528526, 'New Zealand', 2015],
    [64304, 81.6, 5210967, 'Norway', 2015],
    [24787, 77.3, 38611794, 'Poland', 2015],
    [23038, 73.13, 143456918, 'Russia', 2015],
    [19360, 76.5, 78665830, 'Turkey', 2015],
    [38225, 81.4, 64715810, 'United Kingdom', 2015],
    [53354, 79.1, 321773631, 'United States', 2015]
  ]
];
option_2 = {
  'legend': {
    'right': '10%',
    'top': '3%',
    'data': ['1990', '2015']
  },
  'grid': {
    'left': '8%',
    'top': '10%'
  },
  'xAxis': {
    'splitLine': {
      'lineStyle': {
        'type': 'dashed'
      }
    }
  },
  'yAxis': {
    'splitLine': {
      'lineStyle': {
        'type': 'dashed'
      }
    },
    'scale': True
  },
  'series': [
    {
      'name': '1990',
      'data': data[0],
      'type': 'scatter',
      'symbolSize': 'function (data) {return Math.sqrt(data[2]) / 5e2;}',
      'emphasis': {
        'focus': 'series',
        'label': {
          'show': True,
          'formatter': 'function (param) {return param.data[3];}',
          'position': 'top'
        }
      },
      'itemStyle': {
        'shadowBlur': 10,
        'shadowColor': 'rgba(120, 36, 50, 0.5)',
        'shadowOffsetY': 5,
      }
    },
    {
      'name': '2015',
      'data': data[1],
      'type': 'scatter',
      'symbolSize': 'function (data) { return Math.sqrt(data[2]) / 5e2;}',
      'emphasis': {
        'focus': 'series',
        'label': {
          'show': True,
#           formatter: function (param) {
#             return param.data[3];
#           },
          'position': 'top'
        }
      },
      'itemStyle': {
        'shadowBlur': 10,
        'shadowColor': 'rgba(25, 100, 150, 0.5)',
        'shadowOffsetY': 5,
        
      }
    }
  ]
};
st_echarts(
    options=option_2, height="600px")




#---------------------------
import pyecharts.options as opts
from pyecharts.charts import Pie

"""
Gallery 使用 pyecharts 1.1.0
参考地址: https://echarts.apache.org/examples/editor.html?c=pie-nest

目前无法实现的功能:

1、暂无
"""


inner_x_data = ["直达", "营销广告", "搜索引擎"]
inner_y_data = [335, 679, 1548]
inner_data_pair = [list(z) for z in zip(inner_x_data, inner_y_data)]

outer_x_data = ["直达", "营销广告", "搜索引擎", "邮件营销", "联盟广告", "视频广告", "百度", "谷歌", "必应", "其他"]
outer_y_data = [335, 310, 234, 135, 1048, 251, 147, 102]
outer_data_pair = [list(z) for z in zip(outer_x_data, outer_y_data)]

c = (
    Pie()
    .add(
        series_name="访问来源",
        data_pair=inner_data_pair,
        radius=[0, "30%"],
        label_opts=opts.LabelOpts(position="inner"),
    )
    .add(
        series_name="访问来源",
        radius=["40%", "55%"],
        data_pair=outer_data_pair,
        label_opts=opts.LabelOpts(
            position="outside",
            formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
            background_color="#eee",
            border_color="#aaa",
            border_width=1,
            border_radius=4,
            rich={
                "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                "abg": {
                    "backgroundColor": "#e3e3e3",
                    "width": "100%",
                    "align": "right",
                    "height": 22,
                    "borderRadius": [4, 4, 0, 0],
                },
                "hr": {
                    "borderColor": "#aaa",
                    "width": "100%",
                    "borderWidth": 0.5,
                    "height": 0,
                },
                "b": {"fontSize": 16, "lineHeight": 33},
                "per": {
                    "color": "#eee",
                    "backgroundColor": "#334455",
                    "padding": [2, 4],
                    "borderRadius": 2,
                },
            },
        ),
    )
    .set_global_opts(legend_opts=opts.LegendOpts(pos_left="left", orient="vertical"))
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        )
    )
    
)

st_pyecharts(c,height="600px")


#-----------------------
from pyecharts import options as opts
from pyecharts.charts import EffectScatter
from pyecharts.faker import Faker

c_w = (
    EffectScatter()
    .add_xaxis(Faker.choose())
    .add_yaxis("", Faker.values())
    .set_global_opts(
        title_opts=opts.TitleOpts(title="EffectScatter-显示分割线"),
        xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
        yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
    )
)

st_pyecharts(c_w,height="600px")
