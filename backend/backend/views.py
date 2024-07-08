from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import pandas as pd
import os

import plotly.express as px
import plotly.io as pio
import numpy as np

from django.http import HttpResponse
from django_plotly_dash import DjangoDash
from dash import html
from dash import dcc


@csrf_exempt
def get_data(request):

    # Construct the file path
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, 'data', 'PeriodStats.csv')

    try:
        data = pd.read_csv(file_path)

        fig = px.line(data, x='Time Period', y='Prior', title='DOFS over Time')

        # Convert plot to HTML
        plot_json = fig.to_json()

        print("Plot JSON: ", plot_json)

        # Return the plot HTML wrapped in an HttpResponse
        return JsonResponse({'plot_json': plot_json})

        # Filter the data

    except Exception as e:
        print("Error: ", e)
        return JsonResponse({"message": "Data not found", "error": str(e)})
    
@csrf_exempt
def dash_view(request):
    app = DjangoDash('SimpleExample')

    app.layout = html.Div([
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'NYC'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ])

    return HttpResponse(app.index_string)
