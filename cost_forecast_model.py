import pandas as pd
from prophet import Prophet
import csv
def read_records():
    records = []
    try:
        with open('ExpenseRecord.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                records.append(row)
    except FileNotFoundError:
        pass
    return records

# Prepare your data
records_df = pd.DataFrame(read_records(), columns=['id', 'amount', 'date'])
records_df['date'] = pd.to_datetime(records_df['date'])
monthly_data = records_df.resample('M', on='date').sum().reset_index()

# Train Prophet model
model = Prophet()
model.fit(monthly_data.rename(columns={'date': 'ds', 'amount': 'y'}))

# Save the model
import joblib
joblib.dump(model, 'cost_forecast_model.pkl')