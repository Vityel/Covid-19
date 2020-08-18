import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots



X=pd.read_csv('X.csv')
a1=list(X.Region.unique())
regions_dict=dict(zip(range(1,len(a1)+1),a1))
def my_date(dt):
    a= dt.split('-')
    return datetime.date(int(a[0]),int(a[1]),int(a[2]))


X.Date=X.Date.apply(my_date)
myday = list(X.tail(1).Date)[0]


covid_rates = pd.DataFrame()
mask = (X.Date==myday)&(X.Region!='Россия')
today_cases = X[mask]
#covid_rates.reset_index(drop=True)

covid_rates['По количеству текущих<br>больных'] = today_cases.sort_values(by=['Remaining_ill'],ascending = False).Region.reset_index(drop=True)
covid_rates['По количеству новых'] = today_cases.sort_values(by=['Day_confirmed'],ascending = False).Region.reset_index(drop=True)
covid_rates['По умершим за день'] = today_cases.sort_values(by=['Day_deaths'],ascending = False).Region.reset_index(drop=True)
covid_rates['По выздоровевшим<br>за день'] = today_cases.sort_values(by=['Day_recovered'],ascending = False).Region.reset_index(drop=True)
param = {'xgap':0}
def func_fig_r1(region):
    fig_r1 =  ff.create_table(covid_rates.head(15),height_constant=200,**param)
    fig_r1.update_layout(
    
                  title_text ='Таблица рейтингов заболеваемости COVID-19 по регионам',
                  margin = {'t':50, 'b':100},
                  title_x = 0.5,
                  title_y= 0.95,
                  title_xanchor = "center",
                  title_yanchor = "top", 
                  
                  width = 900, height = 600,template = 'gridon',
    
    
                  xaxis_title='',yaxis_title = '')
    for i in range(0,4):
        fig_r1.layout.annotations[i].font.size = 10
    return fig_r1



region_number = 10
regions_towatch = list(covid_rates['По количеству текущих<br>больных'].head(region_number))
regions_towatch.append("Россия")


def func_fig_r2(my_region):
    mask = X.Region ==my_region
    fig_r2 = px.bar(X[mask], x='Date', 
             y="Day_confirmed",color ='Day_confirmed',
             title=f'{my_region}: '+'график количества новых заболевших COVID-19 по датам',
              color_continuous_scale= 'jet',text = 'Day_confirmed',
             labels = {'Day_confirmed' : "Новые заболевшие",'Remaining_ill':'Текущие больные'})
    fig_r2.add_trace(
    go.Scatter(
        name='14-дневная скользящая средняя',
        x=X[mask].Date,
        y=X[mask]['MA14_dayconfirmed'],
        mode="lines",
        
        line=go.scatter.Line(color="green"),
        showlegend=True)
    )
    fig_r2.add_trace(
    go.Scatter(
        name = '7-дневная скользящая средняя',
        x=X[mask]['Date'],
        y=X[mask]['MA7_dayconfirmed'],
        mode="lines",
        
        line=go.scatter.Line(color="red"),
        showlegend=True)
    )
    fig_r2.update_layout(
                  title_x = 0.5,
                  title_y= 0.9,
                  title_xanchor = "center",
                  title_yanchor = "bottom", 
                  legend_x = 0.01,legend_y = 1,
                  width = 900, height = 600,template = 'gridon',
    
    
                  xaxis_title='',yaxis_title = ' ')
    return fig_r2


def func_fig_r3(my_region):
    mask = (X.Region ==my_region)
    fig_r3 = go.Figure()
    fig_r3.add_trace(
       go.Bar(x = X[mask].Date,y=X[mask].Change_dayconf,text = X[mask]['Change_dayconf'],textposition = 'inside',hoverinfo='x+y',
                 marker_color = X[mask]['Change_dayconf'],marker_colorscale = 'Temps',marker_colorbar ={'tickmode':'auto',
                                    'title':{'text':'Изменение','side':'top'}}
                    )   
                )
    fig_r3.update_layout(
   
                  title=f'{my_region}: динамика новых заболевших COVID-19 по дням<br>(изменение относительно предыдущего дня)',
                  title_x = 0.5,
                  title_y= 0.9,
                  title_xanchor = "center",
                  title_yanchor = "bottom", 
                  legend_x = 0.05,legend_y = 0.98,
                  width = 900, height = 600,template = 'gridon',
                  xaxis_title=' ',
    yaxis_title = ' '
     )
    return fig_r3

def func_fig_r4(my_region):
    mask = X.Region ==my_region

    fig_r4 = px.bar(X[mask], x='Date', y="Remaining_ill",color ='Remaining_ill',
             title=f'{my_region}: '+'график количества текущих больных COVID-19 по датам',
              color_continuous_scale= 'jet',text = 'Remaining_ill',
            labels = {'Day_confirmed' : "Новые заболевшие",'Remaining_ill':'Текущие больные'})
    fig_r4.add_trace(
     go.Scatter(
        name='14-дневная скользящая средняя',
        x=X[mask].Date,
        y=X[mask]['MA14_remaining_ill'],
        mode="lines",
        
        line=go.scatter.Line(color="green"),
        showlegend=True))
    fig_r4.add_trace(
     go.Scatter(
        name = '7-дневная скользящая средняя',
        x=X[mask].Date,
        y=X[mask]['MA7_remaining_ill'],
        mode="lines",
        
        line=go.scatter.Line(color="red"),
        showlegend=True))
    fig_r4.update_layout(
                  title_x = 0.5,
                  title_y= 0.9,
                  title_xanchor = "center",
                  title_yanchor = "bottom", 
                  legend_x = 0.01,legend_y = 1,
                  width = 900, height = 600,template = 'gridon',
                 xaxis_title='Текущие больные = количество выявленных - количество выздоровевших - количество умерших',
                 yaxis_title = ' ')
    return fig_r4

def func_fig_r5(my_region):
    mask = X.Region ==my_region

    fig_r5 = go.Figure()
    fig_r5.add_trace(
              go.Bar(x = X[mask].Date,y=X[mask].Change_remill,text = X[mask]['Change_remill'],textposition = 'inside',hoverinfo='x+y',
                
                marker_color = X[mask]['Change_remill'],marker_colorscale = 'Temps',marker_colorbar ={'tickmode':'auto',
                                    'title':{'text':'Изменение','side':'top'}})     
                )
    fig_r5.update_layout(
                  title=f'{my_region}: динамика текущих больных COVID-19 по дням<br>(изменение относительно предыдущего дня)',
                  title_x = 0.5,
                  title_y= 0.9,
                  title_xanchor = "center",
                  title_yanchor = "bottom", 
                  legend_x = 0.05,legend_y = 0.98,
                  width = 900, height = 600,template = 'gridon',
                  xaxis_title='Текущие больные = количество выявленных - количество выздоровевших - количество умерших',
                  yaxis_title = ' ')
    return fig_r5

delta = datetime.timedelta(14)
past14=myday-delta
mask = (X.Date>=past14)&(X.Region.isin(regions_towatch))
def my_round(k):
    return round(k,3)

Z = X[mask].groupby(['Region','Date']).Rt.sum().apply(my_round).unstack().reset_index()
Z.dropna(inplace=True)
d = Z.drop('Region',axis = 1).values
x1=list(Z.columns[1:])
x2=[]
for i in x1:
    x2.append(str(i.day)+'.'+str(i.month)+"."+str(i.year))
    
y=list(Z.Region)
def func_fig_r6(my_region):
    fig_r6 = ff.create_annotated_heatmap(d, x=x2, y=y, annotation_text=d,hoverinfo='z',
                                  colorscale='Temps')

    fig_r6.update_layout(
                  
                  
                  width = 900, height = 600,    
    
                  xaxis_title='Динамика коэффициента распространения Rt по регионам')
    return fig_r6

mask = (X.Date==myday)&(X.Region!='Россия')
#mask = (X.Date==myday)
#Делаем выборку по доле регина в общих случаях выявления заболеваний по России
df=X[mask].sort_values(by=['Rate_ill'],ascending = False)
#Далее заменяем все имена если регион набрал менее 1% в общих случаях по России
df2 = X[mask].reset_index(drop=True)
print(len(df2))

for i in range(len(df2)):
    if df2.loc[i,'Rate_ill']<1:
        df2.loc[i,'Region']='Регионы менее 1%'
def func_fig_r7(my_region):
    fig_r7 = px.pie(df2, values='Remaining_ill', names='Region',color_discrete_sequence=px.colors.sequential.Rainbow,
            title=f'Всего текущих больных COVID-19 в России: {df2.Remaining_ill.sum()}<br>'+
            f'(на дату: {myday})',labels={'Region':'Регион','Remaining_ill':'Текущие больные'})

    fig_r7.update_traces(textinfo='percent+label')
    fig_r7.update_layout(
        
                #  title=f'{my_region}: динамика текущих больных COVID-19 по дням<br>(изменение относительно предыдущего дня)',
                 margin = {'t':120, 'b':0},
                  title_x = 0.5,
                  title_y= 0.9,
                  width = 900, height=800,
                  title_xanchor = "center",
                  title_yanchor = "bottom")
                     
    return fig_r7

def func_fig_r8(my_region):
    fig_r8 = go.Figure(data=[go.Pie(labels=df2.Region, values=df2.Remaining_ill, textinfo='label+percent',
                             insidetextorientation='radial'
                            )])
    fig_r8.update_layout(
                title=f'Всего текущих больных COVID-19 в России: {df2.Remaining_ill.sum()}<br>'+
                f'(на дату: {myday})',
                  title_x = 0.5,
                  title_y= 0.95,
                  width = 900, height=800,
                  title_xanchor = "center",
                  title_yanchor = "bottom")
                     
    return fig_r8

delta = datetime.timedelta(7)
past7=myday-delta
mask = (X.Date>=past7)&(X.Region.isin(regions_towatch))&(X.Region!='Россия')
                                      
box_cases1 = X[mask].groupby(['Region','Date'])['Day_confirmed'].sum()
box_cases2 = X[mask].groupby(['Region','Date'])['Day_recovered'].sum()
new_df1=box_cases1.unstack().T
cols = list(new_df1.columns)
color_dict=dict(zip(cols,['forestgreen','darkblue','goldenrod','magenta','hotpink','grey','maroon','coral','darkorange','lightpink']))
new_df2=box_cases2.unstack().T
def func_fig_r9(my_region):
    fig_r9 = make_subplots(rows=2, cols=1,specs = [[{}],[{}]],vertical_spacing = 0.03,shared_xaxes=True,
                  subplot_titles=("Box-график распределения по новым заболевшим(в день) за неделю:",
                                 "Box-график распределения по выздоровевшим(в день) за неделю:"))

    for i in cols:
        fig_r9.add_trace(
        go.Box(x=new_df1[i],name = i,boxmean = True,marker_color = color_dict.get(i)),row=1,col=1)

    for i in cols:
        fig_r9.add_trace(
        go.Box(x=new_df2[i],name = i,boxmean=True,marker_color = color_dict.get(i)),row=2,col=1)

    fig_r9.update_layout(
                  width = 900, height = 1200,
                 showlegend=True,template ='ggplot2')
    return fig_r9


