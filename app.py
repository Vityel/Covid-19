import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from russiax import * 
from worldw import * 

chart_dict_r = {'Новые заболевшие':func_fig_r2, 'Изменения в новых больных':func_fig_r3,
'Текущие больные':func_fig_r4,'Изменения в текущих больных':func_fig_r5, 'Rt':func_fig_r6,
'Всего больных':func_fig_r7,'Рейтинги':func_fig_r1,'Boxes':func_fig_r9}

chart_dict_w = {'Новые заболевшие':func_fig_w2, 'Изменения в новых больных':func_fig_w3,
'Текущие больные':func_fig_w4,'Изменения в текущих больных':func_fig_w5, 'Rt':func_fig_w6,
'Всего больных':func_fig_w7,'Рейтинги':func_fig_w1,'Boxes':func_fig_w9}

app = dash.Dash(__name__)
server = app.server

app.title='COVID-19 в динамике'
app.layout = html.Div(id="wrapper",
           children =[ 

    html.Div(id="headerwrap",
     children=[

        html.Div(id="header",
         children=[
         html.H1('Динамика заболеваемости COVID-19')
         ])

     ]),
          
    html.Div(id="leftcolumnwrap",
     children=[
        
        html.Div(id="leftcolumn",
         children=[

             
         html.H2('Анализ динамики:'),
         html.Hr(),
         dcc.RadioItems(
                id='chart-type',
                options=[{'label': i, 'value': i} for i in chart_dict_r.keys()],
                value='Новые заболевшие',
                labelStyle={'display': 'flex','justify-content': 'left','align-items': 'left'}
                )

         ])

     ]),

    html.Div(id="contentwrap",
     children=[
        
        html.Div(id="content",
         children=[

             html.H2('Страна/Регион'),
         dcc.RadioItems(
             id='area',
             options=[{'label': k, 'value': k} for k in ['Россия','Весь мир']],
             value='Россия',
             labelStyle={'display': 'inline-block'}),
         html.Hr(),
         dcc.Dropdown(
                id='regions'
            ),



         html.Hr(),
         dcc.Graph(id='main-graph')


         ])
                                                     
     ]),
                                             
    html.Div(id="footerwrap",
     children=[

        html.Div(id="footer",
         children=[
         html.H3('Данные: Яндекс'),
         html.H3('Разработка сайта: Виталий Елагин, vityel@gmail.com'),
         
         ])
                                                                         
     ])
                                                                
 ])                                 
@app.callback(
    [Output('regions', 'options'),Output('regions', 'value')],
    [Input('area', 'value')])
def set_regions_options(selected_area):
    if selected_area=="Россия":
        return [{'label': i, 'value': i} for i in regions_dict.values() ],'Москва'      #regions_dict.get(42)
    else: return [{'label': i, 'value': i} for i in country_dict.values() ],'США'       #country_dict.get(134)

# @app.callback(
#     Output('regions', 'value'),
#     [Input('regions', 'options')])
# def set_regions_value(available_options):
#     return available_options[41]['value']


@app.callback(
    Output('main-graph', 'figure'),
    [Input('regions', 'value'),Input('chart-type', 'value')]
    )
def update_figure(selected_region,chart_type):
    if selected_region in regions_dict.values():
        return chart_dict_r[chart_type](selected_region)
    else: return chart_dict_w[chart_type](selected_region)



if __name__ == '__main__':
    app.run_server(debug=True)