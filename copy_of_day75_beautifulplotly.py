# -*- coding: utf-8 -*-
"""Copy of Day75_BeautifulPlotly

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WLAhgIeW92iWsSTyURSsmFyppWfzuquS
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
df_apps = pd.read_csv('apps.csv')
df_apps.head()

df_apps.shape

df_apps.sample(5)

simple_df_apps = df_apps.drop(['Last_Updated', 'Android_Ver'], axis=1)

simple_df_apps.head()

df_apps_clean = simple_df_apps.dropna()
df_apps_clean.head()

df_apps_clean.shape

df_apps_clean = df_apps_clean.drop_duplicates(subset=['App', 'Type', 'Price'])

df_apps_clean.shape

df_apps_clean.sort_values(by=['Rating'], ascending=False)

df_apps_clean.sort_values(by=['Size_MBs']).max()

df_apps_clean.sort_values(by=['Reviews'], ascending=False).head()

ratings = df_apps_clean.Content_Rating.value_counts()

print(ratings)

fig = px.pie(labels=ratings.index, 
             values=ratings.values, 
             title="Content Rating",
             names=ratings.index,
             hole = 0.6)
fig.update_traces(textposition='outside', textinfo='percent+label')
fig.show()

df_apps_clean.info()

df_apps_clean.Installs = df_apps_clean.Installs.astype(str).str.replace(',', "")
df_apps_clean.Installs = pd.to_numeric(df_apps_clean.Installs)
df_apps_clean[['App', 'Installs']].groupby('Installs').count()

df_apps_clean.Price = df_apps_clean.Price.astype(str).str.replace('$', "")
df_apps_clean.Price = pd.to_numeric(df_apps_clean.Price)
df_apps_clean[['App', 'Price']].groupby('Price').count()

df_apps_clean_cheap = df_apps_clean[df_apps_clean['Price'] < 250]
df_apps_clean_cheap.sort_values(by='Price', ascending=False).head()

df_apps_clean_cheap["Revenue_Estimate"] = df_apps_clean_cheap.Installs.mul(df_apps_clean.Price)
df_apps_clean_cheap.sort_values("Revenue_Estimate", ascending=False)[:10]

df_apps_clean_cheap.nunique()

top10_Category = df_apps_clean_cheap.Category.value_counts()[:10]
top10_Category

bar = px.bar(data_frame=top10_Category)
bar.show()

category_installs = df_apps_clean_cheap.groupby('Category').agg({'Installs': pd.Series.sum})
category_installs.sort_values("Installs", ascending=False, inplace=True)
h_bar = px.bar(x = category_installs.Installs,
               y = category_installs.index,
               orientation='h')
 
h_bar.show()

category_installs['App'] = df_apps_clean_cheap.Category.value_counts()
category_installs.head()

scatter = px.scatter(x=category_installs.App,
                     y=category_installs.Installs,
                     color=category_installs.Installs,
                     size=category_installs.App,
                     log_y=True
)

scatter.show()

df_apps_clean_cheap.Genres.value_counts()

stack = df_apps_clean.Genres.str.split(';', expand=True).stack()
print(f'We now have a single column with shape: {stack.shape}')
num_genres = stack.value_counts()
print(f'Number of genres: {len(num_genres)}')

print(stack)

genres_graph = px.bar(stack.value_counts()[:15],  color=num_genres.values[:15], 
                      color_continuous_scale='armyrose')
genres_graph.show()

df_free_vs_paid = df_apps_clean.groupby(["Type", "Category"], as_index=False).agg({'App': pd.Series.count})
df_free_vs_paid.head()

free_vs_paid_graph = px.bar(df_free_vs_paid,
               x='Category',
               y='App',
               title='Free vs Paid Apps by Category',
               color='Type',
               barmode='group')

free_vs_paid_graph.update_layout(xaxis_title='Category',
                    yaxis_title='Number of Apps',
                    xaxis={'categoryorder':'total descending'},
                    yaxis=dict(type='log'))
free_vs_paid_graph.show()

my_boxplot = px.box(df_apps_clean,
                    x="Type",
                    y="Installs",
                    log_y=True,
                    points='all')
my_boxplot.show()

