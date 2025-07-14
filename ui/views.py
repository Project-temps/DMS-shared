"""Views for handling UI interactions and data display."""

import json
import logging

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

from data_management.calculate_thi import calculate_thi  # Import the function

def get_thi_data(request):
    germany_data, poland_data = calculate_thi()
    thi_data = pd.concat(
        [
            germany_data[["datetime", "thi"]].assign(country="Germany"),
            poland_data[["datetime", "thi"]].assign(country="Poland"),
        ],
        ignore_index=True,
    )
    thi_data_json = thi_data.to_json(orient="records", date_format="iso")
    return JsonResponse(thi_data_json, safe=False)

# Views for static pages
def index(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def courses(request):
    return render(request, 'courses.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def calculate_statistics(chart_data):
    statistics = {}
    for farm in chart_data:
        farm_name = farm['name']
        statistics[farm_name] = {}
        for param in farm.keys():
            if param.startswith('values_'):
                values = farm[param]
                statistics[farm_name][param] = {
                    'min': min(values) if values else 0,
                    'max': max(values) if values else 0,
                    'mean': sum(values) / len(values) if values else 0
                }
    return statistics

def process_dataframes(days=90):
    try:
        logger.debug("Starting process_dataframes with days: %s", days)
        
        # Load data
        df1 = pd.read_csv('data/processed/Germany/hourly_merged_sensor_data.csv')
        df2 = pd.read_csv('data/processed/Poland/hourly_merged_sensor_data.csv')
        logger.debug("Loaded dataframes: df1 shape %s, df2 shape %s", df1.shape, df2.shape)

        # Convert datetime column to pandas datetime
        df1['datetime'] = pd.to_datetime(df1['datetime'])
        df2['datetime'] = pd.to_datetime(df2['datetime'])
        logger.debug("Converted datetime columns")

        # Convert cutoff_datetime to timezone-aware datetime (matching the data)
        cutoff_datetime = max(df1['datetime'].max(), df2['datetime'].max()) - pd.Timedelta(days=days)
        logger.debug("Cutoff datetime: %s", cutoff_datetime)

        # Filter the data for the last `days` days
        df1_filtered = df1[df1['datetime'] >= cutoff_datetime]
        df2_filtered = df2[df2['datetime'] >= cutoff_datetime]
        logger.debug("Filtered dataframes: df1_filtered shape %s, df2_filtered shape %s", df1_filtered.shape, df2_filtered.shape)

        # Check if dataframes are empty
        if df1_filtered.empty or df2_filtered.empty:
            logger.warning("Filtered dataframes are empty! Returning empty chart data.")
            return [
                {'name': 'Germany Farm', 'dates': [], 'values1': [], 'values2': []},
                {'name': 'Poland Farm', 'dates': [], 'values1': [], 'values2': []}
            ]

        # Dynamically extract all columns except 'datetime'
        parameters = [col for col in df1_filtered.columns if col not in ['datetime']]


        # Prepare data for visualization
        chart_data = [
            {
                'name': 'Germany Farm',
                'dates': df1_filtered['datetime'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
                **{f'values_{param}': df1_filtered[param].fillna(0).tolist() for param in parameters}
            },
            {
                'name': 'Poland Farm',
                'dates': df2_filtered['datetime'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
                **{f'values_{param}': df2_filtered[param].fillna(0).tolist() for param in parameters}
            }
        ]

        # Temporary extraction for debugging
        chart_data_limited = [
            {
                'name': chart_data[0]['name'],
                'dates': chart_data[0]['dates'],
                'values1': chart_data[0].get('values_co2', []),  # Assuming 'co2' as values1
                'values2': chart_data[0].get('values_nh3', []),  # Assuming 'nh3' as values2
            },
            {
                'name': chart_data[1]['name'],
                'dates': chart_data[1]['dates'],
                'values1': chart_data[1].get('values_co2', []),  # Assuming 'co2' as values1
                'values2': chart_data[1].get('values_nh3', []),  # Assuming 'nh3' as values2
            }
        ]

        return chart_data, parameters

    except Exception as e:
        logger.error("Error processing dataframes: %s", e)
        raise




# API view to get chart data
def get_chart_data(request):
    days = int(request.GET.get('days', 90))  # Default to 90 days if not specified
    chart_data, parameters = process_dataframes(days)  # Call the function to process dataframes
    statistics = calculate_statistics(chart_data)  # Calculate statistics

    return JsonResponse({'data': chart_data, 'statistics': statistics})

def dashboard(request):
    logger.info("Rendering dashboard view")
    days = int(request.GET.get('days', 90))  # Default to 90 days if not specified
    chart_data, parameters = process_dataframes(days)  # Call the new function to process dataframes
    logger.debug("Dashboard parameters: %s", parameters)

    chart_data_json = json.dumps(chart_data, ensure_ascii=False)
    return render(request, 'dashboard.html', {
        'chart_data': chart_data_json,
        'parameters': parameters  # Pass parameters to the template
    })

def allerts(request):
    """Display threshold information and placeholder alert stats."""
    return render(request, 'allerts.html')

def contact(request):
    return render(request, 'contact.html')

def survey(request):
    return render(request, 'survey.html')

def communication(request):
    return render(request, 'communication.html')  # Ensure this matches your template name
