from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from plotly.graph_objects import Layout
from plotly.validator_cache import ValidatorCache

# Haritalar için GeoJson bilgilerini almak için gerekli kütüphaneler
from urllib.request import urlopen
import json


app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {
            'name': 'description',
            'content': 'Türkiye İstatistik Kurumu (TÜİK) konut satış istatistiklerini interaktif olarak gösteren dashboard uygulaması. İl ve ilçe bazında konut satış verileri görselleştirilmektedir.'
        },
        {
            'name': 'keywords',
            'content': 'TÜİK, konut satışları, Türkiye konut istatistikleri, il bazlı konut satışları, ilçe bazlı konut satışları, interaktif dashboard, konut piyasası'
        },
        {
            'name': 'author',
            'content': 'Avşar ÇÖTELİ'
        },
        {
            # Responsive design için
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0'
        },
        # Open Graph etiketleri (sosyal medya paylaşımları için)
        {
            'property': 'og:title',
            'content': 'Türkiye Konut Satışları Dashboard'
        },
        {
            'property': 'og:description',
            'content': 'TÜİK konut satış istatistiklerini interaktif olarak gösteren dashboard uygulaması'
        },
        {
            'property': 'og:type',
            'content': 'website'
        },
        {
            'property': 'og:url',
            'content': 'https://coteli.pythonanywhere.com/'  # Uygulamanızın URL'sini ekleyin
        },
        
    ]
)
#server = app.server

app.title = "Türkiye Konut Satışları Dashboard"

# dataFramelerin düzenlenmesi
df = pd.read_csv("https://raw.githubusercontent.com/coteli/intereactive-dash/main/ilceler.csv")
df_tum_il = df.groupby("il").sum().reset_index()


app.layout = dbc.Container(html.Div(children=[
    # Başlık ve GitHub linki için flex container - justify-content: space-between ekledik
    html.Div([
        html.H1('Türkiye Konut Satış Sayıları', className="mt-5 mb-0"),
        html.A(
            html.Img(
                src="https://raw.githubusercontent.com/gilbarbara/logos/main/logos/github-icon.svg",
                height="35px"
            ),
            href="https://github.com/coteli/intereactive-dash",
            target="_blank",
            className="mt-5"
        )
    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
    
    html.Hr(),
    
    # "Yıl Seçiniz" ibaresini kaldırdık
    dcc.Slider(
        df['yil'].min(),
        df['yil'].max(),
        step=None,
        value=df['yil'].max(),
        marks={str(yil): str(yil) for yil in df['yil'].unique()},
        id='yil-slider',
        className="p-3 mb-4"
    ),
    
    html.Div([
        html.H3(id='harita-baslik'),
        dbc.Spinner(dcc.Graph(id='harita-yillik'),
                    size="lg", color="rgb(227, 96, 11)"),
    ]),

    html.Hr(),

    html.Div([
        dbc.Row([
            dbc.Col(
                [
                    dbc.Spinner(dcc.Graph(id='ilceler'), size="lg",
                                color="rgb(227, 96, 11)")
                ]),
            dbc.Col(
                [
                    dbc.Spinner(dcc.Graph(id='aylar'), size="lg",
                                color="rgb(227, 96, 11)")
                ]),
        ])
    ]),

    html.Hr(),
]))


# Yıllara Göre Konut Satışları Haritası
@app.callback(
    Output('harita-yillik', 'figure'),
    Input('yil-slider', 'value'))
def update_figure(selected_yil):
    filtered_df = df[df.yil == selected_yil]

    with urlopen('https://raw.githubusercontent.com/cihadturhan/tr-geojson/master/geo/tr-cities-utf8.json') as response:
        geojson = json.load(response)
    geojson["features"][2]["properties"] = {'name': 'Afyonkarahisar'}

    fig = px.choropleth(filtered_df.groupby(["yil", "il"]).sum().reset_index(), 
                        geojson=geojson, 
                        color="satis",
                        locations="il", 
                        featureidkey="properties.name",
                        color_continuous_scale=["White", "Green", "Red"])
    
    fig.update_geos(
        visible=False,
        center=dict(lat=39, lon=35.5),
        projection_scale=7,
        scope="asia"
    )
    
    fig.update_layout(
        margin={"t": 0, "b": 0, "l": 0},
        transition_duration=500,
        clickmode='event+select',
        height=500,
        dragmode=False,
    )
    
    return fig


# Harita başlığı için yeni callback
@app.callback(
    Output('harita-baslik', 'children'),
    Input('yil-slider', 'value'))
def update_title(selected_yil):
    return f"{selected_yil} Yılı Konut Satışları Haritası"


# İlçelere Göre Konut Satış Sayıları
@app.callback(
    Output('ilceler', 'figure'),
    Input('harita-yillik', 'clickData'),  # dropdown yerine harita tıklama verisini kullanıyoruz
    Input('yil-slider', 'value'))
def update_figure(clickData, selected_yil):
    if clickData is None:  # İlk yüklemede veya tıklama olmadığında varsayılan il
        selected_il = "Ankara"
    else:
        selected_il = clickData['points'][0]['location']
    
    filtered_df = df[df.il == selected_il]
    filtered_df = filtered_df[filtered_df.yil == selected_yil]

    fig = px.bar(filtered_df.groupby(["ilce"]).sum().reset_index().sort_values(by="satis"),
                 x="satis", y='ilce', orientation='h',
                 title=f"{selected_yil} Yılı {selected_il} İli İlçelere Göre Konut Satışları",
                 labels={'satis': 'Konut Satışları', 'ilce': 'İlçeler'})
    fig.update_traces(marker_color="rgba(227, 96, 11, 0.93)",
                      hoverlabel_bgcolor="rgba(49, 100, 150, 0.8)")
    fig.update_layout(plot_bgcolor="white", title_x=0.5)
    fig.update_xaxes(gridcolor="rgb(230,230,230)")
    fig.update_yaxes(gridcolor="rgb(230,230,230)")

    return fig

# Aylara Göre Konut Satış Sayıları
@app.callback(
    Output('aylar', 'figure'),
    Input('harita-yillik', 'clickData'),  # dropdown yerine harita tıklama verisini kullanıyoruz
    Input('yil-slider', 'value'))
def update_figure(clickData, selected_yil):
    if clickData is None:  # İlk yüklemede veya tıklama olmadığında varsayılan il
        selected_il = "Ankara"
    else:
        selected_il = clickData['points'][0]['location']
    
    filtered_df = df[df.il == selected_il]
    filtered_df = filtered_df[filtered_df.yil == selected_yil]

    fig = px.bar(filtered_df.groupby(["il", "yil", "ay", "ay-isim"]).sum().reset_index(),
                 x="ay-isim", y='satis',
                 title=f"{selected_yil} Yılı {selected_il} İli Aylara Göre Konut Satışları",
                 labels={'satis': 'Konut Satışları', 'ay-isim': 'Aylar'})
    fig.update_traces(marker_color="rgba(227, 96, 11, 0.93)",
                      hoverlabel_bgcolor="rgba(49, 100, 150, 0.8)")
    fig.update_layout(plot_bgcolor="white", title_x=0.5)
    fig.update_xaxes(gridcolor="rgb(230,230,230)")
    fig.update_yaxes(gridcolor="rgb(230,230,230)")

    return fig

# Alt bölüm başlığı için callback güncelleme
@app.callback(
    Output('alt-bolum-baslik', 'children'),
    Input('harita-yillik', 'clickData'),  # dropdown yerine harita tıklama verisini kullanıyoruz
    Input('yil-slider', 'value'))
def update_alt_bolum_baslik(clickData, selected_yil):
    if clickData is None:  # İlk yüklemede veya tıklama olmadığında varsayılan il
        selected_il = "Ankara"
    else:
        selected_il = clickData['points'][0]['location']
    return f"{selected_yil} Yılı {selected_il} İli İlçelere ve Aylara Göre Konut Satışları"


if __name__ == '__main__':
    app.run_server()
