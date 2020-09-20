import pandas as pd
from flask import Flask
from flask import render_template, request, redirect
from pyecharts.charts import EffectScatter, Bar, Line, WordCloud, Map, Grid, Pie
from pyecharts.charts import Scatter
import numpy as np
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType, SymbolType, ThemeType
from pyecharts.charts import Bar, Tab, Line, Map, Timeline
from pyecharts.faker import Faker

app = Flask(__name__)


# 2013年-2017年世界各地区GDP总量
@app.route('/gpd_map')
def index_bar():
    df2 = pd.read_csv("./static/data/gdp.csv")
    tl = Timeline()
    for i in range(2013, 2018):
        map0 = (
            Map()
                .add(
                "", list(zip(list(df2.地区.unique()), list(df2["{}".format(i)]))), "world", is_map_symbol_show=False
            )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="{}年世界各地区GDP总量".format(i), subtitle="",
                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="black", font_size=16,
                                                                                     font_style="italic")),
                visualmap_opts=opts.VisualMapOpts(max_=15000000000000),
            )
        )
        tl.add(map0, "{}年".format(i))
    return render_template('index.html',
                           myechart=tl.render_embed(),
                           text=''' 从上面的模型中，我们可以看出近五年来，东南沿海地区的GDP生产总值在国内是较高的
                            以2018年为例，广东，浙江，山东三地的数值都要超过了80000。而西北地区的数值是偏低的
                            以2018年为例，西藏，青海，宁夏三地的数值都要低于10000''')


# 2013-2017世界各地区旅游总收入与GDP总量对比
@app.route('/traver_gdp')
def index_bar_every_1_tp():
    df = pd.read_csv("./static/data/lvyou.csv")
    df2 = pd.read_csv("./static/data/gdp.csv")

    x = list(df.地区)
    tl = Timeline()
    for i in range(2013, 2018):
        bar = (
            Bar()
                .add_xaxis(x)
                .add_yaxis("世界各地区旅游总收入", list(df["{}".format(i)]))
                .add_yaxis("世界各地区GDP总量", list(df2["{}".format(i)]))
                .reversal_axis()
                .set_global_opts(title_opts=opts.TitleOpts("{}年世界各地区旅游总收入与GDP总量对比".format(i)),
                                 datazoom_opts=opts.DataZoomOpts(orient="vertical"))
                .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
            )
        )
        tl.add(bar, "{}年".format(i))
    return render_template('index.html',
                           myechart=tl.render_embed(),
                           text='''
                           总体上看世界各地区旅游总收入是和与GDP总量成正比的，从图表数据看两者都有些增长，但增长有些波动总体上还是趋向平稳的
                           ''')


# 个别国家的迁移人数对比
@app.route('/pie')
def index_bar_every():
    df4 = pd.read_csv("./static/data/qianyi.csv")
    c = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(df4.地区, df4['2017'])],
            radius=["30%", "75%"],
            center=["25%", "50%"],
            rosetype="radius",
        )
            .add(
            "",
            [list(z) for z in zip(df4.地区, df4['2012'])],
            radius=["30%", "75%"],
            center=["75%", "50%"],
            rosetype="area",
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="迁移人数对比"))
    )
    return render_template('index.html',
                           myechart=c.render_embed(),
                           text='''
                           从上面图的走势，我们可以看出，United States迁移人数最多。
                           ''')


# 世界各地区旅游总收入
@app.route('/traverse_map')
def index_bar_every_4():
    prevention = request.args.get("city")

    df5 = pd.read_csv(r'./static/data/lvyou.csv')
    tl = Timeline()
    for i in range(2013, 2018):
        map0 = (
            Map()
                .add(
                "", list(zip(list(df5.地区.unique()), list(df5["{}".format(i)]))), "world", is_map_symbol_show=False
            )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="{}年世界各地区旅游总收入".format(i), subtitle="",
                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="black", font_size=16,
                                                                                     font_style="italic")),
                visualmap_opts=opts.VisualMapOpts(max_=70000000000),

            )
        )
        tl.add(map0, "{}年".format(i))
    return render_template('index.html',
                           myechart=tl.render_embed(),
                           text='''
                           从上面图的走势，我们可以看出，世界各地区旅游总收入较多的国家分别是United States、France、Germany、China等国家。
                          ''')


@app.route('/pm25')
def index_bar_every_2():
    df3 = pd.read_csv(r'./static/data/pm2.5.csv')
    df3.index = ['Australia', 'Canada', 'China', 'France', 'United Kingdom', 'Japan', 'Russia', 'United States']
    map0 = (
        Line()
            .add_xaxis(
            [pd.to_datetime('01/01/{y}'.format(y=x), format="%m/%d/%Y") for x in df3.columns.values.tolist()[1:]])
            .add_yaxis("中国", df3.loc["China", :].values.tolist()[1:])
            .add_yaxis("美国", df3.loc["United States", :].values.tolist()[1:])
            .add_yaxis("澳大利亚", df3.loc["Australia", :].values.tolist()[1:])
            .add_yaxis("英国", df3.loc["United Kingdom", :].values.tolist()[1:])
            .add_yaxis("日本", df3.loc["Japan", :].values.tolist()[1:])
            .add_yaxis("俄罗斯", df3.loc["Russia", :].values.tolist()[1:])
            .set_global_opts(title_opts=opts.TitleOpts(title="PM2.5污染量对比"), datazoom_opts=opts.DataZoomOpts())
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False), )
    )
    return render_template('index.html',
                           myechart=map0.render_embed(),
                           text='''由上面看可以看出，从2010年到2008年各国的pm2.5都在下降，
                           其中数中国的pm2.5值下降趋势最大。 ''')


# 数据总览
@app.route('/')
def index_bar_every_x():
    data1 = pd.read_csv(r"./static/data/gdp.csv")
    data2 = pd.read_csv(r"./static/data/lvyou.csv")
    data3 = pd.read_csv(r"./static/data/pm2.5.csv")
    data4 = pd.read_csv(r"./static/data/qianyi.csv")
    data1_x = data1.columns.values
    data2_x = data2.columns.values
    data3_x = data3.columns.values
    data4_x = data4.columns.values

    data1_y = data1.values.tolist()
    data2_y = data2.values.tolist()
    data3_y = data3.values.tolist()
    data4_y = data4.values.tolist()
    return render_template("index.html", data1_x=data1_x[1:], data2_x=data2_x[1:], data3_x=data3_x[1:],
                           data4_x=data4_x[1:], data1_y=data1_y, data2_y=data2_y, data3_y=data3_y, data4_y=data4_y,
                           a=1)


if __name__ == '__main__':
    app.run(debug=True)
