import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff

yandex_world = pd.read_csv('yandex_world.csv')
yandex_world.rename(columns = {'Дата':'Date','Страна':'Country','Заражений':'Confirmed','Выздоровлений':'Recovered',
                               'Смертей':'Deaths','Смертей за день':'Day_deaths',
                               'Заражений за день':'Day_confirmed','Выздоровлений за день':'Day_recovered'},inplace = True)
for i in range(yandex_world.shape[0]):
    a= yandex_world.Date[i].split('.')
    yandex_world.Date[i]=datetime.date(int(a[2]),int(a[1]),int(a[0]))

df3_temp = yandex_world.groupby('Date').sum()
df3_temp['Country']='Весь мир'

z5= pd.concat([yandex_world,df3_temp.reset_index()],axis = 0)
z5.reset_index()
yandex_world = z5


mydayw = list(yandex_world.tail(1).Date)[0]

W = pd.DataFrame()
country_dict = {}
yandex_world['Rt'] = 1
yandex_world['Rt2'] = 1
yandex_world['Rate_conf'] = 0
yandex_world['Rate_ill'] = 0

temp_Df = yandex_world.groupby(['Country','Date']).sum()

# Ниже enumerate  для составления словаря из имен регионов {i:j} , для расчетов можно было использовать только j

for i,j in enumerate(temp_Df.index.get_level_values(0).unique()):
    temp_Df2 =  temp_Df.loc[j]
    temp1 = temp_Df2['Day_confirmed'].rolling(4).sum()/(temp_Df2["Day_confirmed"].rolling(8).sum()-

                                                              temp_Df2["Day_confirmed"].rolling(4).sum())
    temp2 = temp_Df2['Confirmed'].rolling(4).sum()/(temp_Df2['Confirmed'].rolling(8).sum()-

                                                              temp_Df2['Confirmed'].rolling(4).sum())
    temp_Df2['Rt'] = round(temp1,3)
    temp_Df2['Rt2'] = round(temp2,3)
    temp_Df2['Country'] = j
    temp_Df2['Remaining_ill']=temp_Df2['Confirmed']-temp_Df2['Recovered']-temp_Df2['Deaths']
    temp_Df2['MA7_dayconfirmed']=temp_Df2['Day_confirmed'].rolling(window=7).mean()
    temp_Df2['MA14_dayconfirmed']=temp_Df2['Day_confirmed'].rolling(window=14).mean()
    temp_Df2['MA7_remaining_ill']=temp_Df2['Remaining_ill'].rolling(window=7).mean()
    temp_Df2['MA14_remaining_ill']=temp_Df2['Remaining_ill'].rolling(window=14).mean()
    
    temp_Df2['Change_dayconf'] = 0
    for k in range(1,temp_Df2.shape[0]):
        temp_Df2['Change_dayconf'].iloc[k]=temp_Df2['Day_confirmed'].iloc[k]-temp_Df2['Day_confirmed'].iloc[k-1]
    temp_Df2['Change_remill'] = 0
    for k in range(1,temp_Df2.shape[0]):
        temp_Df2['Change_remill'].iloc[k]=temp_Df2['Remaining_ill'].iloc[k]-temp_Df2['Remaining_ill'].iloc[k-1]
    
    

   #Генератор DF  на каждый регион(сидит в цикле):
   # globals()['x' + str(i)] = temp_df2.reset_index()
    
    W = pd.concat([W,temp_Df2.reset_index()],axis = 0)
    country_dict[i]=j
    W = W.reset_index(drop=True)

    # Добавляем колонки расчитанные сколько доля их в процентах от суммарного показателя в мире
mask = W.Country == 'Весь мир'
temp_Df = W[mask][['Date','Confirmed','Remaining_ill']]
temp_Df.index = temp_Df.Date
temp_Df.drop(columns =['Date'], inplace = True)

world_date = list(temp_Df.index)
world_conf = list(temp_Df.Confirmed)
world_ill = list(temp_Df.Remaining_ill)
world_dict_conf = dict(zip(world_date,world_conf))
world_dict_ill = dict(zip(world_date,world_ill))

for i in range(len(W)):
    W.loc[i,'Rate_conf']=100*W.loc[i,'Confirmed']/world_dict_conf.get(W.loc[i,'Date'])
    W.loc[i,'Rate_ill']=100*W.loc[i,'Remaining_ill']/world_dict_ill.get(W.loc[i,'Date'])

Covid_Rates_w = pd.DataFrame()
mask = (W.Date==mydayw)&(W.Country!='Весь мир')
Today_cases_w = W[mask]

Covid_Rates_w['По количеству текущих больных'] = Today_cases_w.sort_values(by=['Remaining_ill'],ascending = False).Country.reset_index(drop=True)
Covid_Rates_w['По количеству новых'] = Today_cases_w.sort_values(by=['Day_confirmed'],ascending = False).Country.reset_index(drop=True)
Covid_Rates_w['По умершим за день'] = Today_cases_w.sort_values(by=['Day_deaths'],ascending = False).Country.reset_index(drop=True)
Covid_Rates_w['По выздоровевшим за день'] = Today_cases_w.sort_values(by=['Day_recovered'],ascending = False).Country.reset_index(drop=True)

def func_fig_w1(region):
    fig_w1 =  ff.create_table(Covid_Rates_w.head(15))
    fig_w1.update_layout(
                  title_text ='Таблица рейтингов заболеваемости COVID-19 по странам',
                  margin = {'t':100, 'b':100},
                  title_x = 0.5,
                  title_y= 0.95,
                  title_xanchor = "center",
                  title_yanchor = "middle", 
                  
                  width = 900, height = 600,template = 'gridon',
    
    
                  xaxis_title='',yaxis_title = '')
     
    return fig_w1

country_number = 5
country_towatch = list(Covid_Rates_w['По количеству текущих больных'].head(country_number))

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
                  legend_x = 0.05,legend_y = 0.95,
                  width = 900, height = 600,template = 'gridon',
                  xaxis_title='',yaxis_title = ' '
     )
    return fig_w2

def func_fig_w3(my_country):
    mask = W.Country ==my_country
    fig_w3 = go.Figure()
    fig_w3.add_trace(
              go.Bar(x = W.Date,y=W[mask].Change_dayconf,text = W[mask]['Change_dayconf'],textposition = 'inside',
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
            legend_x = 0.05,legend_y = 0.98,
            width = 900, height = 600,template = 'gridon',
            xaxis_title='Текущие больные = количество выявленных - количество выздоровевших - количество умерших',
            yaxis_title = ' ')
    return fig_w4
def func_fig_w5(my_country):
    mask = W.Country ==my_country
    fig_w5 = go.Figure()
    fig_w5.add_trace(
         go.Bar(x = W[mask].Date,y=W[mask].Change_remill,text = W[mask]['Change_remill'],textposition = 'inside',
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

mask = (W.Date>=datetime.date(2020,7,30))&(W.Country.isin(country_towatch))

Y = W[mask].groupby(['Country','Date']).Rt.sum().unstack().reset_index()
Y.dropna(inplace=True)
D = Y.drop('Country',axis = 1).values
x_1=list(Y.columns[1:])
x_2=[]
for i in x_1:
    x_2.append(str(i.day)+'.'+str(i.month)+"."+str(i.year))
    
y_1=list(Y.Country)

def func_fig_w6(my_region):
    fig_w6 = ff.create_annotated_heatmap(D, x=x_2, y=y_1, annotation_text=D,
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