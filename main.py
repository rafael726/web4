from dash import Dash, html, dash_table, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd


app = Dash(__name__)
app.title = 'Tablero de Control'


df = pd.read_csv('superstore.csv', delimiter=';', parse_dates=['Order Date', 'Ship Date'])
df2 = df[
  ['Province', 'Sales', 'Customer Segment']
].groupby(['Province', 'Customer Segment'], as_index=False).sum('Sales')


print(df2.info())


app.layout = html.Div([
  html.H1('Tablero de Control'),
  dcc.Tabs(id='tabs', value='tab1', children=[
    dcc.Tab(label='Tabla de Datos', value='tab1'),
    dcc.Tab(label='Histograma', value='tab2'),
    dcc.Tab(label='Scatter', value='tab3'),
    dcc.Tab(label='Barras Apiladas', value='tab4'),
  ]),
  html.Div(id='contenido'),
])


@callback(Output('contenido', 'children'), Input('tabs', 'value'))
def actualizar(tab):
  if tab == 'tab1' :
    return dash_table.DataTable(data=df.to_dict('records'), page_size=12)
  elif tab == 'tab2':
    return  dcc.Graph(figure=px.histogram(df, x='Province', y='Sales', histfunc='avg'))
  elif tab == 'tab3':
    return dcc.Graph(figure=px.scatter(df, x='Order Date', y='Sales', color='Customer Segment'))
  else:
    return dcc.Graph(figure=px.bar(df2, x='Province', y='Sales', color='Customer Segment'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)