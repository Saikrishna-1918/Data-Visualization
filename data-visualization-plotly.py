import json
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import webbrowser

# Updated JSON data for states, including institutions
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
  }
]
'''

# Parse the JSON data
data_dict = json.loads(json_data)

# Prepare the data for the bar chart
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

# Convert to DataFrame for bar chart
df_bar = pd.DataFrame(bar_data)

# Initialize the Dash app
app = Dash(__name__)

# App layout with CSS for styling
app.layout = html.Div(style={
    'font-family': 'Arial', 
    'background-color': '#f9f9f9', 
    'padding': '20px',
    'max-width': '800px',  # Limit the max width of the layout
    'margin': '0 auto'  # Center the layout
}, children=[
    html.H1("Population Distribution in Selected States", style={
        'textAlign': 'center', 
        'color': '#333',
        'margin-bottom': '20px'  # Spacing below the title
    }),
    
    # Bar chart
    dcc.Graph(
        id='state-bar-chart',
        figure=px.bar(
            df_bar, 
            x='State', 
            y=df_bar.columns[1:7],  # Only population data
            title='Population by Race and Ethnicity',
            labels={'value': 'Population Count', 'variable': 'Race/Ethnicity'},
            template='plotly_white',  # Light background for charts
            color_discrete_sequence=px.colors.qualitative.Bold  # Custom color scheme
        ).update_layout(
            title_font_size=22,
            title_x=0.5,
            xaxis_tickangle=-45,
            xaxis_title=None,
            yaxis_title='Population Count',
            hovermode="x unified",
            margin=dict(l=40, r=40, t=40, b=40),
            legend_title_text='Race/Ethnicity',
            legend=dict(yanchor="top", y=0.5, xanchor="left", x=1.05),  # Legend to the right
            height=250,  # Smaller height for the bar chart
            width=600  # Smaller width for the bar chart
        )
    ),

    # Spacing between charts
    html.Div(style={'height': '20px'}),  # Add space between bar and pie chart

    # Row for Population and Institutions data
    html.Div(style={'display': 'flex', 'justify-content': 'space-between'}, children=[
        # Pie chart
        html.Div(style={'flex': '1', 'margin-right': '10px'}, children=[
            dcc.Graph(
                id='state-pie-chart',
                # Initially empty pie chart
                figure=px.pie(title='Click a state in the bar chart to see the population breakdown.').update_layout(
                    title_font_size=18,
                    title_x=0.5,
                    margin=dict(l=40, r=40, t=40, b=40),
                    height=250,
                    width=300
                )
            )
        ]),
        
        # Institutions Data Section
        html.Div(style={'flex': '1', 'margin-left': '10px'}, children=[
            html.Div(id='institutions-data', style={'display': 'none'}, children=[
                html.H3(id='institutions-title', style={'textAlign': 'center', 'color': '#333'}),
                dcc.Graph(id='state-institution-bar-chart')
            ])
        ])
    ])
])

# Callback to update the pie chart based on bar chart clicks
@app.callback(
    Output('state-pie-chart', 'figure'),
    Input('state-bar-chart', 'clickData')
)
def update_pie_chart(clickData):
    if clickData is None:
        # Return an empty pie chart if no state is selected
        return px.pie(title='Click a state in the bar chart to see the population breakdown.').update_layout(
            title_font_size=18,
            title_x=0.5,
            margin=dict(l=40, r=40, t=40, b=40),
            height=250,
            width=300
        )

    # Get the selected state
    selected_state = clickData['points'][0]['x']
    
    # Get the data for the selected state
    state_data = df_bar[df_bar['State'] == selected_state].iloc[0]
    
    # Create the pie chart
    fig = px.pie(
        names=state_data.index[1:7],
        values=state_data[1:7],
        title=f'Population Breakdown for {selected_state}',
        labels={'value': 'Population Count', 'variable': 'Race/Ethnicity'}
    )
    fig.update_layout(
        title_font_size=18,
        title_x=0.5,
        margin=dict(l=40, r=40, t=40, b=40),
        height=250,
        width=300
    )
    
    return fig

# Callback to update the institutions data section based on bar chart clicks
@app.callback(
    Output('institutions-data', 'style'),
    Output('institutions-title', 'children'),
    Output('state-institution-bar-chart', 'figure'),
    Input('state-bar-chart', 'clickData')
)
def update_institution_chart(clickData):
    if clickData is None:
        # Return hidden institutions data if no state is selected
        return {'display': 'none'}, '', px.bar(x=[], y=[])

    # Get the selected state
    selected_state = clickData['points'][0]['x']
    
    # Get institutions data for the selected state
    state_data = next(item for item in data_dict if item["State"] == selected_state)
    school_data = state_data['Institutions']['Schools']
    college_data = state_data['Institutions']['Colleges']

    # Prepare data for the institutions bar chart
    institution_names = [school['Name'] for school in school_data] + [college['Name'] for college in college_data]
    institution_totals = [school['TotalStudents'] for school in school_data] + [college['TotalStudents'] for college in college_data]
    
    # Create the institutions bar chart
    fig = px.bar(
        x=institution_names,
        y=institution_totals,
        title=f'Total Students in Institutions for {selected_state}',
        labels={'value': 'Total Students', 'variable': 'Institution Type'},
        template='plotly_white',
        color_discrete_sequence=px.colors.qualitative.Bold
    ).update_layout(
        title_font_size=22,
        title_x=0.5,
        xaxis_tickangle=-45,
        yaxis_title='Total Students',
        hovermode="x unified",
        margin=dict(l=40, r=40, t=40, b=40),
        height=250,
        width=600
    )
    
    return {'display': 'block'}, f'Institutions in {selected_state}', fig

# Run the Dash app
if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:8050/')  # Open in the default web browser
    app.run_server(debug=True)
