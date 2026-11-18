import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


class QueueWaitTimePredictor:

  def __init__(self):
    self.model = LinearRegression()
    self.is_trained = False

  def train_model(self, data_path: str):
    """Trains the Linear Regression model using historical or simulated queue data."""
    # Load dataset (expected features: queue_length, estimated_duration, hour_of_day, actual_wait_time)
    df = pd.read_csv(data_path)

    X = df[['queue_length', 'estimated_duration', 'hour_of_day']]
    y = df['actual_wait_time']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train Linear Regression model
    self.model.fit(X_train, y_train)
    self.is_trained = True

    # Evaluate model using Mean Absolute Error (MAE) as outlined in proposal
    predictions = self.model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)

    print(f'Model trained successfully. Test MAE: {mae:.2f} minutes')
    return mae

  def predict_wait_time(
      self, queue_length: int, estimated_duration: float, hour_of_day: int
  ) -> float:
    """Predicts waiting time for a new customer request."""
    if not self.is_trained:
      # Fallback default calculation if model isn't fitted yet
      return float(queue_length * estimated_duration)

    input_data = pd.DataFrame(
        [[queue_length, estimated_duration, hour_of_day]],
        columns=['queue_length', 'estimated_duration', 'hour_of_day'],
    )

    predicted_time = self.model.predict(input_data)[0]
    return max(0.0, float(predicted_time))  # Ensure wait time is not negative

