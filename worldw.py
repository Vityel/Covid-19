import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots


W=pd.read_csv('W.csv')
a2=list(W.Country.unique())
country_dict=dict(zip(range(1,len(a2)+1),a2))

def my_date1(dt):
    a= dt.split('-')
    return datetime.date(int(a[0]),int(a[1]),int(a[2]))


W.Date=W.Date.apply(my_date1)
mydayw = list(W.tail(1).Date)[0]

Covid_Rates_w = pd.DataFrame()
mask = (W.Date==mydayw)&(W.Country!='Весь мир')
Today_cases_w = W[mask]

Covid_Rates_w['По количеству текущих<br>больных'] = Today_cases_w.sort_values(by=['Remaining_ill'],ascending = False).Country.reset_index(drop=True)
Covid_Rates_w['По количеству новых'] = Today_cases_w.sort_values(by=['Day_confirmed'],ascending = False).Country.reset_index(drop=True)
Covid_Rates_w['По умершим за день'] = Today_cases_w.sort_values(by=['Day_deaths'],ascending = False).Country.reset_index(drop=True)
Covid_Rates_w['По выздоровевшим<br>за день'] = Today_cases_w.sort_values(by=['Day_recovered'],ascending = False).Country.reset_index(drop=True)
param = {'xgap':0}
def func_fig_w1(region):
    fig_w1 =  ff.create_table(Covid_Rates_w.head(15),height_constant=200,**param)
    fig_w1.update_layout(
                  title_text ='Таблица рейтингов заболеваемости COVID-19 по странам',
                  margin = {'t':50, 'b':100},
                  title_x = 0.5,
                  title_y= 0.95,
                  title_xanchor = "center",
                  title_yanchor = "middle", 
                  
                  width = 900, height = 600,template = 'gridon',
    
    
                  xaxis_title='',yaxis_title = '')
    for i in range(0,4):
        fig_w1.layout.annotations[i].font.size = 10
     
    return fig_w1

country_number = 10
country_towatch = list(Covid_Rates_w['По количеству текущих<br>больных'].head(country_number))

def func_fig_w2(my_country):
    mask = W.Country ==my_country
    fig_w2 = px.bar(W[mask], x='Date', 
             y="Day_confirmed",color ='Day_confirmed',
             title=f'{my_country}: '+'график количества новых заболевших COVID-19 по датам',
              color_continuous_scale= 'jet',text = 'Day_confirmed',
             labels = {'Day_confirmed' : "Новые заболевшие",'Remaining_ill':'Текущие больные'})
    fig_w2.add_trace(
    go.Scatter(
        name='14-дневная скользящая средняя',
        x=W[mask].Date,
        y=W[mask]['MA14_dayconfirmed'],
        mode="lines",
        
        line=go.scatter.Line(color="green"),
        showlegend=True)
     )
    fig_w2.add_trace(
        go.Scatter(
        name = '7-дневная скользящая средняя',
        x=W[mask]['Date'],
        y=W[mask]['MA7_dayconfirmed'],
        mode="lines",

        line=go.scatter.Line(color="red"),
        showlegend=True)
    )
    fig_w2.update_layout(
                  title_x = 0.5,
                  title_y= 0.9,
                  title_xanchor = "center",
                  title_yanchor = "bottom", 
                  legend_x = 0.01,legend_y = 1,
                  width = 900, height = 600,template = 'gridon',
                  xaxis_title='',yaxis_title = ' '
     )
    return fig_w2

def func_fig_w3(my_country):
    mask = W.Country ==my_country
    fig_w3 = go.Figure()
    fig_w3.add_trace(
              go.Bar(x = W.Date,y=W[mask].Change_dayconf,text = W[mask]['Change_dayconf'],textposition = 'inside',hoverinfo='x+y',
                 marker_color = W[mask]['Change_dayconf'],marker_colorscale = 'Temps',marker_colorbar ={'tickmode':'auto',
                                    'title':{'text':'Изменение','side':'top'}}
                    )   
                )
    fig_w3.update_layout(
                  title=f'{my_country}: динамика новых заболевших COVID-19 по дням<br>(изменение относительно предыдущего дня)',
                  title_x = 0.5,
                  title_y= 0.9,
                  title_xanchor = "center",
                  title_yanchor = "bottom", 
                  legend_x = 0.05,legend_y = 0.98,
                  width = 900, height = 600,template = 'gridon',
                  xaxis_title=' ',
                  yaxis_title = ' ')
    return fig_w3

def func_fig_w4(my_country):
    mask = W.Country ==my_country

    fig_w4 = px.bar(W[mask], x='Date', y="Remaining_ill",color ='Remaining_ill',
             title=f'{my_country}: '+'график количества текущих больных COVID-19 по датам',
              color_continuous_scale='jet',text = 'Remaining_ill',
            labels = {'Day_confirmed' : "Новые заболевшие",'Remaining_ill':'Текущие больные'})
    fig_w4.add_trace(
        go.Scatter(
        name='14-дневная скользящая средняя',
        x=W[mask].Date,
        y=W[mask]['MA14_remaining_ill'],
        mode="lines",
        line=go.scatter.Line(color="green"),
        showlegend=True)
     )

    fig_w4.add_trace(
        go.Scatter(
        name = '7-дневная скользящая средняя',
        x=W[mask].Date,
        y=W[mask]['MA7_remaining_ill'],
        mode="lines",
        line=go.scatter.Line(color="red"),
        showlegend=True)
     )
    fig_w4.update_layout(
            title_x = 0.5,
            title_y= 0.9,
            title_xanchor = "center",
            title_yanchor = "bottom", 
            legend_x = 0.01,legend_y = 1,
            width = 900, height = 600,template = 'gridon',
            xaxis_title='Текущие больные = количество выявленных - количество выздоровевших - количество умерших',
            yaxis_title = ' ')
    return fig_w4
def func_fig_w5(my_country):
    mask = W.Country ==my_country
    fig_w5 = go.Figure()
    fig_w5.add_trace(
         go.Bar(x = W[mask].Date,y=W[mask].Change_remill,text = W[mask]['Change_remill'],textposition = 'inside',hoverinfo='x+y',
         marker_color = W[mask]['Change_remill'],marker_colorscale = 'Temps',marker_colorbar ={'tickmode':'auto',
        'title':{'text':'Изменение','side':'top'}})     
                )
    fig_w5.update_layout(
                  title=f'{my_country}: динамика текущих больных COVID-19 по дням<br>(изменение относительно предыдущего дня)',
                  title_x = 0.5,
                  title_y= 0.9,
                  title_xanchor = "center",
                  title_yanchor = "bottom", 
                  legend_x = 0.05,legend_y = 0.98,
                  width = 900, height = 600,template = 'gridon',
                  xaxis_title='Текущие больные = количество выявленных - количество выздоровевших - количество умерших',
                  yaxis_title = ' ')
    return fig_w5

delta = datetime.timedelta(14)
past14=mydayw-delta

mask = (W.Date>=past14)&(W.Country.isin(country_towatch))
def my_round(k):
    return round(k,3)
Y = W[mask].groupby(['Country','Date']).Rt.sum().apply(my_round).unstack().reset_index()
Y.dropna(inplace=True)
D = Y.drop('Country',axis = 1).values
x_1=list(Y.columns[1:])
x_2=[]
for i in x_1:
    x_2.append(str(i.day)+'.'+str(i.month)+"."+str(i.year))
    
y_1=list(Y.Country)

def func_fig_w6(my_region):
    fig_w6 = ff.create_annotated_heatmap(D, x=x_2, y=y_1, annotation_text=D,hoverinfo='z',
                                  colorscale='Temps')

    fig_w6.update_layout(
                  width = 900, height = 600,    
    
                  xaxis_title='Динамика коэффициента распространения Rt по странам')

    return fig_w6

mask = (W.Date==mydayw)&(W.Country !='Весь мир')
#Делаем выборку по доле регина в общих случаях выявления заболеваний по России
#df_1=W[mask].sort_values(by=['Rate_ill'],ascending = False)
#Далее заменяем все имена если регион набрал менее 1% в общих случаях по России
df_2 = W[mask].reset_index(drop=True)

for i in range(len(df_2)):
    if df_2.loc[i,'Rate_ill']<1:
        df_2.loc[i,'Country']='Страны менее 1%'

def func_fig_w7(my_region):
    fig_w7 = px.pie(df_2, values='Remaining_ill', names='Country',color_discrete_sequence=px.colors.sequential.Rainbow,
            title=f'Всего текущих больных COVID-19 в мире: {df_2.Remaining_ill.sum()}<br>'+
            f'(на дату: {mydayw})',labels={'Country':'Страна','Remaining_ill':'Текущие больные'})

    fig_w7.update_traces(textinfo='percent+label')
    fig_w7.update_layout(
                #  title=f'{my_region}: динамика текущих больных COVID-19 по дням<br>(изменение относительно предыдущего дня)',
                 margin = {'t':120, 'b':0},
                  title_x = 0.5,
                  title_y= 0.9,
                  width = 900, height=800,
                  title_xanchor = "center",
                  title_yanchor = "bottom")
    return fig_w7

def func_fig_w8(my_region):

    fig_w8  = go.Figure(data=[go.Pie(labels=df_2.Country, values=df_2.Remaining_ill, textinfo='label+percent',
                             insidetextorientation='radial'
                            )])
    fig_w8.update_layout(
                  title=f'Всего текущих больных COVID-19 в мире: {df_2.Remaining_ill.sum()}<br>'+
                  f'(на дату: {mydayw})',
                  title_x = 0.5,
                  title_y= 0.95,
                  width = 900, height=800,
                  title_xanchor = "center",
                  title_yanchor = "bottom")
    return fig_w8

delta = datetime.timedelta(7)
past7=mydayw-delta
mask = (W.Date>=past7)&(W.Country.isin(country_towatch))&(W.Country!='Весь мир')
                                      
box_cases3 = W[mask].groupby(['Country','Date'])['Day_confirmed'].sum()
box_cases4 = W[mask].groupby(['Country','Date'])['Day_recovered'].sum()
new_df3=box_cases3.unstack().T
new_df4=box_cases4.unstack().T
cols1 = list(new_df3.columns)
color_dict1=dict(zip(cols1,['forestgreen','darkblue','goldenrod','magenta','hotpink','grey','maroon','coral','darkorange','lightpink']))

def func_fig_w9(my_region):
    fig_w9 = make_subplots(rows=2, cols=1,specs = [[{}],[{}]],vertical_spacing = 0.03,shared_xaxes=True,
                  subplot_titles=("Box-график распределения по новым заболевшим(в день) за неделю:",
                                 "Box-график распределения по выздоровевшим(в день) за неделю:"))

    for i in cols1:
        fig_w9.add_trace(
        go.Box(x=new_df3[i],name = i,boxmean = True,marker_color = color_dict1.get(i)),row=1,col=1)

    for i in cols1:
        fig_w9.add_trace(
        go.Box(x=new_df4[i],name = i,boxmean=True,marker_color = color_dict1.get(i)),row=2,col=1)


    fig_w9.update_layout(
                 width = 900, height = 1200,
                 showlegend=True,template ='ggplot2')
    return fig_w9
    

