import json
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import webbrowser
from threading import Timer

# JSON data
json_data = '''
[
  {
    "State": "Alabama",
    "Total": 5028090,
    "WhiteTotal": 3329010,
    "BlackTotal": 1326343,
    "IndianTotal": 21122,
    "AsianTotal": 69808,
    "HawaiianTotal": 2253,
    "OtherTotal": 279556,
    "TwoOrMoreTotal": 185632,
    "Institutions": {
      "Schools": [
        {
          "Name": "School A",
          "Type": "Public",
          "TotalStudents": 500
        },
        {
          "Name": "School B",
          "Type": "Private",
          "TotalStudents": 300
        }
      ],
      "Colleges": [
        {
          "Name": "College A",
          "Type": "Community",
          "TotalStudents": 1200
        },
        {
          "Name": "College B",
          "Type": "University",
          "TotalStudents": 1500
        }
      ]
    }
  },
  {
    "State": "Alaska",
    "Total": 734821,
    "WhiteTotal": 450472,
    "BlackTotal": 23395,
    "IndianTotal": 104957,
    "AsianTotal": 47464,
    "HawaiianTotal": 11209,
    "OtherTotal": 97324,
    "TwoOrMoreTotal": 82727,
    "Institutions": {
      "Schools": [
        {
          "Name": "Harvard-Westlake School",
          "Type": "Public",
          "TotalStudents": 500
        },
        {
          "Name": "Phillips Exeter Academy",
          "Type": "Private",
          "TotalStudents": 300
        }
      ],
      "Colleges": [
        {
          "Name": "Harvard University",
          "Type": "Community",
          "TotalStudents": 1200
        },
        {
          "Name": "Stanford University",
          "Type": "University",
          "TotalStudents": 1500
        }
      ]
    }
  },
  {
    "State": "Arizona",
    "Total": 7172280,
    "WhiteTotal": 4781701,
    "BlackTotal": 327077,
    "IndianTotal": 297590,
    "AsianTotal": 240642,
    "HawaiianTotal": 14116,
    "OtherTotal": 1511155,
    "TwoOrMoreTotal": 961794,
    "Institutions": {
      "Schools": [
        {
          "Name": "The Lawrenceville School ",
          "Type": "Public",
          "TotalStudents": 500
        },
        {
          "Name": "Sidwell Friends School",
          "Type": "Private",
          "TotalStudents": 300
        }
      ],
      "Colleges": [
        {
          "Name": "Massachusetts Institute of Technology (MIT)",
          "Type": "Community",
          "TotalStudents": 1200
        },
        {
          "Name": "Santa Monica College",
          "Type": "University",
          "TotalStudents": 1500
        }
      ]
    }
  },
  {
    "State": "Arkansas",
    "Total": 3018670,
    "WhiteTotal": 2193344,
    "BlackTotal": 456693,
    "IndianTotal": 16840,
    "AsianTotal": 47413,
    "HawaiianTotal": 11117,
    "OtherTotal": 293258,
    "TwoOrMoreTotal": 203476,
    "Institutions": {
      "Schools": [
        {
          "Name": "Santa Monica School",
          "Type": "Public",
          "TotalStudents": 500
        },
        {
          "Name": "Stuyvesant High School",
          "Type": "Private",
          "TotalStudents": 300
        }
      ],
      "Colleges": [
        {
          "Name": "CMiami Dade College",
          "Type": "Community",
          "TotalStudents": 1200
        },
        {
          "Name": "City College of San Francisco",
          "Type": "University",
          "TotalStudents": 1500
        }
      ]
    }
  }
]
'''

# Parse the JSON data
data_dict = json.loads(json_data)

# Prepare data for the bar chart
bar_data = []
for state_data in data_dict:
    state = state_data['State']
    bar_data.append({
        'State': state,
        'White': state_data['WhiteTotal'],
        'Black': state_data['BlackTotal'],
        'Indian': state_data['IndianTotal'],
        'Asian': state_data['AsianTotal'],
        'Hawaiian': state_data['HawaiianTotal'],
        'Other': state_data['OtherTotal'],
        'TwoOrMore': state_data['TwoOrMoreTotal'],
        'TotalSchools': sum(school['TotalStudents'] for school in state_data['Institutions']['Schools']),
        'TotalColleges': sum(college['TotalStudents'] for college in state_data['Institutions']['Colleges'])
    })

# Convert to DataFrame
df_bar = pd.DataFrame(bar_data)

# Initialize Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div(children=[
    html.H1("Population Distribution in Selected States", style={'textAlign': 'center'}),
    
    dcc.Graph(
        id='state-bar-chart',
        figure=px.bar(
            df_bar,
            x='State',
            y=['White', 'Black', 'Indian', 'Asian', 'Hawaiian', 'Other', 'TwoOrMore'],
            labels={'value': 'Population Count', 'variable': 'Race/Ethnicity'},
            title='Population by Race and Ethnicity'
        ).update_layout(
            xaxis_tickangle=-45,
            barmode='group',
            title_x=0.5
        ),
        style={'margin': '0 auto', 'width': '80%'}
    ),
    
    html.Div(id='hidden-charts', children=[
        dcc.Graph(
            id='state-pie-chart',
            figure=px.pie(),
            style={'display': 'none', 'margin': '0 auto', 'width': '60%'}
        ),
        
        html.Div(id='institutions-data', children=[
            html.H3(id='institutions-title', style={'textAlign': 'center'}),
            dcc.Graph(id='state-institution-bar-chart', style={'display': 'none', 'margin': '0 auto', 'width': '80%'})
        ])
    ])
])

# Callback to update pie chart
@app.callback(
    [Output('state-pie-chart', 'figure'),
     Output('state-pie-chart', 'style')],
    Input('state-bar-chart', 'clickData')
)
def update_pie_chart(clickData):
    if clickData is None:
        return px.pie(), {'display': 'none'}

    selected_state = clickData['points'][0]['x']
    state_data = df_bar[df_bar['State'] == selected_state].iloc[0]
    
    fig = px.pie(
        names=['White', 'Black', 'Indian', 'Asian', 'Hawaiian', 'Other', 'TwoOrMore'],
        values=[state_data['White'], state_data['Black'], state_data['Indian'], state_data['Asian'], state_data['Hawaiian'], state_data['Other'], state_data['TwoOrMore']],
        title=f'Population Breakdown for {selected_state}'
    )
    return fig, {'display': 'block', 'margin': '0 auto', 'width': '60%'}

# Callback to update institutions data
@app.callback(
    [Output('institutions-data', 'style'),
     Output('institutions-title', 'children'),
     Output('state-institution-bar-chart', 'figure'),
     Output('state-institution-bar-chart', 'style')],
    Input('state-bar-chart', 'clickData')
)
def update_institution_chart(clickData):
    if clickData is None:
        return {'display': 'none'}, '', px.bar(x=[], y=[]), {'display': 'none'}

    selected_state = clickData['points'][0]['x']
    state_data = next(item for item in data_dict if item["State"] == selected_state)
    school_data = state_data['Institutions']['Schools']
    college_data = state_data['Institutions']['Colleges']

    institution_names = [school['Name'] for school in school_data] + [college['Name'] for college in college_data]
    institution_totals = [school['TotalStudents'] for school in school_data] + [college['TotalStudents'] for college in college_data]
    
    fig = px.bar(
        x=institution_names,
        y=institution_totals,
        title=f'Total Students in Institutions for {selected_state}',
        labels={'value': 'Total Students', 'variable': 'Institution Type'}
    ).update_layout(title_x=0.5)

    return {'display': 'block'}, f'Institutions in {selected_state}', fig, {'display': 'block', 'margin': '0 auto', 'width': '80%'}

# Open the app automatically in the browser
def open_browser():
    webbrowser.open_new("http://localhost:8050/")

# Run app
if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(debug=True)
