"""Run the machine learning prediction model on sensor data."""
import numpy as np
import pandas as pd
from keras.models import load_model
import joblib
import plotly.express as px
import os
from data_management.data_loader import load_data 

current_directory = os.path.dirname(os.path.abspath(__file__))

# Cache objects so that heavy assets are only loaded when a prediction is made
model = None
scaler = None
target_scaler = None


def _load_assets():
    """Load the ML model and scalers if they haven't been loaded yet."""
    global model, scaler, target_scaler
    if model is None:
        model = load_model(os.path.join(current_directory, "model.h5"))
    if scaler is None:
        scaler = joblib.load(os.path.join(current_directory, "scaler.pkl"))
    if target_scaler is None:
        target_scaler = joblib.load(
            os.path.join(current_directory, "target_scaler.pkl")
        )
    
def make_prediction(n_past=7 * 24, n_future=12):
    """Run the prediction model on loaded sensor data."""
    _load_assets()
    data = load_data()
    
    # data_path = os.path.join(current_directory, 'train_cleaned_dataset_modified.csv')
    # data = pd.read_csv(data_path)
    input_columns = ["CH4_w-out", "CH4_s-out", "CH4_n-out", "CH4_e-out", "CH4_n-in", "CH4_m-in", "CH4_m-in-up", "CH4_s-in", "CH4_w-in", "CH4_e-in", "TEMP", "Ver_w", "Hor_w", "CH4_in_mean", "CH4_out_mean","CO2_n-in","CO2_m-in","CO2_m-in-up","CO2_s-in","CO2_w-in","CO2_e-in"]
    selected_features = ["CH4_in_mean"]
    
    df = data[input_columns].values
    df_scaled = scaler.transform(df)
    df_frame_scaled = np.array([df_scaled[i:i+n_past] for i in range(len(df) - n_past)])
    predictions_scaled = model.predict(df_frame_scaled)
    predictions = target_scaler.inverse_transform(predictions_scaled)
    
    dates_input = data['Date'][:predictions.shape[0]]
    dates_output = data['Date'][predictions.shape[0]:]
    desired_record_to_plot = predictions[-1]
    date_range = pd.date_range(start=pd.to_datetime(dates_output.iloc[-1]) + pd.Timedelta(hours=1), 
                                        periods = n_future, 
                                        freq='H')
    
    last_date = pd.to_datetime(data['Date'].iloc[-1])
    predictions_df = pd.DataFrame({
        'Prediction': desired_record_to_plot,
        'Date': date_range
    })
    
    fig = px.line(predictions_df, x='Date', y='Prediction', title=f'Prediction for {selected_features[0]}')
    
    # fig_html = fig.to_html(full_html=False)
    # context = {                    
    #     'fig_html': fig_html,
    #     'selected_features': selected_features,
    # }

 
    # JsonResponse({'plot_html': context['plotly_figure']})

    return fig

