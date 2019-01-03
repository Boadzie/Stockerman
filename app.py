import dash
import dash_core_components as dcc
import dash_html_components as html 
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime


app = dash.Dash()


nsdq = pd.read_csv("Data/NASDAQcompanylist.csv")
nsdq.set_index("Symbol", inplace=True)

options = []
for tic in nsdq.index:
    mydict={}
    mydict["label"] = str(nsdq.loc[tic]["Name"]) + " " + tic
    mydict["value"] = tic
    options.append(mydict)

external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css", ]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["http://code.jquery.com/jquery-3.3.1.min.js",
               "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js})
 

app.layout = html.Div(children=
    [   html.Div(children=[html.H1("Stock Ticker", className="text-center")], className="col-md-12"),
        html.Div(children=[
        html.H3("Enter a Stock symbol: "),
        dcc.Dropdown(id="my_stock_picker", 
            options= options,
            value=["TSLA"], 
            multi=True,
            className="form-control p-0"),
        html.Br(),
        html.H3("Select a start and end data: "),
        html.Div(className="form-control p-0",
            children= 
              dcc.DatePickerRange(id="my_date_picker",
                min_date_allowed=datetime(2015, 1, 1),
                max_date_allowed=datetime.today(),
                start_date=datetime(2018, 1, 1),
                end_date=datetime.today(),
        )
        ),
        html.Button(id="submit_button", n_clicks=0, className="btn btn-block btn-success mt-2", children="Update")
    ], className="col-md-3"),
        html.Div(children=[
            dcc.Graph(id="my_graph", figure={
                "data":[{"x":[1, 2, 3], "y":[1,4, 6]}], "layout":{"title":"Default title"}
            })
        ],  className="col-md-9"),

        html.Div(id="footer-div", className="col-md-12 mt-5", children=[
            html.Footer(id="footer", className="bg-dark text-white p-4 text-center sticky-footer mt-5 mb-0", children=[
                html.P("Data Diger Group, 2019.")
            ])
        ])
        
    ],
     className="row m-5"
   
)


@app.callback(Output("my_graph", "figure"), 
   [Input("submit_button", "n_clicks")],
   [State("my_stock_picker", "value"),
    State("my_date_picker", "start_date"),
    State("my_date_picker", "end_date")
   ])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], "%Y-%m-%d")
    end  = datetime.strptime(end_date[:10], "%Y-%m-%d")
    
    traces = []
    for tic in stock_ticker:
        df = web.DataReader(tic, "iex", start, end)
        traces.append({"x":df.index, "y": df["close"], "name":tic})


    fig ={"data": traces, 
    "layout":{"title": stock_ticker}}
    return fig


if __name__== "__main__":
    app.run_server(debug=True)