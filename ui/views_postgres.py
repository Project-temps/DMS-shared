"""Views for interacting with PostgreSQL-backed data."""

from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import json
import logging
from django.db import connections
from django.core.cache import cache

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
    return render(request, 'index.html')
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
        farm_name = farm.get('name')
        # Convert the dictionary to a DataFrame
        df = pd.DataFrame(farm)
        # Select only columns that contain the parameter values
        value_cols = [col for col in df.columns if col.startswith('values_')]
        
        # Use Pandas aggregation to compute min, max, and mean for each parameter
        agg_stats = df[value_cols].agg(['min', 'max', 'mean'])
        # Convert the aggregated DataFrame to a dictionary for easier use
        statistics[farm_name] = agg_stats.to_dict()
    return statistics

def process_dataframes(days=90):
    try:
        logger.debug("Starting process_dataframes with days: %s", days)
        connection = connections['postgres']
        cache_key = f'chart_data_{days}'
        if cached := cache.get(cache_key):
            return cached
        # First, query to get the max datetime from both tables
        max_germany_date_query = "SELECT MAX(datetime) as max_date FROM germany_data"
        max_poland_date_query = "SELECT MAX(datetime) as max_date FROM poland_data"
        
        germany_max_date = pd.read_sql(max_germany_date_query, connection)['max_date'][0]
        poland_max_date = pd.read_sql(max_poland_date_query, connection)['max_date'][0]
        
        # Convert to datetime if they're not already
        if not pd.api.types.is_datetime64_any_dtype(germany_max_date):
            germany_max_date = pd.to_datetime(germany_max_date)
        if not pd.api.types.is_datetime64_any_dtype(poland_max_date):
            poland_max_date = pd.to_datetime(poland_max_date)
        
        # Calculate cutoff date based on the latest date in either dataset
        cutoff_datetime = max(germany_max_date, poland_max_date) - pd.Timedelta(days=days)
        logger.debug("Cutoff datetime: %s", cutoff_datetime)
        
        # Format the cutoff date for SQL
        cutoff_str = cutoff_datetime.strftime('%Y-%m-%d %H:%M:%S')
        
        # Now query the data with the calculated cutoff date
        germany_query = f"""
            SELECT * FROM germany_data
            WHERE datetime >= '{cutoff_str}'
            ORDER BY datetime
        """
        
        poland_query = f"""
            SELECT * FROM poland_data
            WHERE datetime >= '{cutoff_str}'
            ORDER BY datetime
        """
        
        # Load data directly into pandas DataFrames
        df1 = pd.read_sql(germany_query, connection)
        df2 = pd.read_sql(poland_query, connection)
        
        logger.debug("Loaded dataframes from DB: df1 shape %s, df2 shape %s", df1.shape, df2.shape)

        # Check if dataframes are empty
        if df1.empty or df2.empty:
            logger.warning("Dataframes are empty! Returning empty chart data.")
            return [
                {'name': 'Germany Farm', 'dates': [], 'values1': [], 'values2': []},
                {'name': 'Poland Farm', 'dates': [], 'values1': [], 'values2': []}
            ], []

        # Convert datetime column to pandas datetime if it's not already
        if not pd.api.types.is_datetime64_any_dtype(df1['datetime']):
            df1['datetime'] = pd.to_datetime(df1['datetime'])
        if not pd.api.types.is_datetime64_any_dtype(df2['datetime']):
            df2['datetime'] = pd.to_datetime(df2['datetime'])
        
        logger.debug("Processed datetime columns")

        # Dynamically extract all columns except 'datetime'
        parameters = [col for col in df1.columns if col != 'datetime']
        #df1['datetime'] = df2['datetime']
        # Prepare data for visualization
        chart_data = [
            {
                'name': 'Germany Farm',
                'dates': df1['datetime'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
                **{f'values_{param}': df1[param].fillna(0).tolist() for param in parameters}
            },
            {
                'name': 'Poland Farm',
                'dates': df2['datetime'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
                **{f'values_{param}': df2[param].fillna(0).tolist() for param in parameters}
            }
        ]
        cache.set(cache_key, (chart_data, parameters), timeout=300)
        return chart_data, parameters

    except Exception as e:
        logger.error("Error processing dataframes from database: %s", e)
        raise




# API view to get chart data
def get_chart_data(request):
    days = int(request.GET.get('days', 90))  # Default to 90 days if not specified
    chart_data, parameters = process_dataframes(days)  # Call the function to process dataframes
    statistics = calculate_statistics(chart_data)  # Calculate statistics

    return JsonResponse({'data': chart_data, 'statistics': statistics})

def dashboard(request):
    days = int(request.GET.get('days', 90))  # Default to 90 days if not specified
    chart_data, parameters = process_dataframes(days)  # Call the new function to process dataframes
    print(parameters)

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
