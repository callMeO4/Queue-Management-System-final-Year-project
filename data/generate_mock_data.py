import numpy as np
import pandas as pd


def generate_queue_dataset(num_samples=1000, output_path='queue_dataset.csv'):
  """Generates simulated queue records for training the Linear Regression model."""
  np.random.seed(42)

  # Simulate features based on banking queue characteristics
  queue_length = np.random.randint(0, 15, size=num_samples)
  estimated_duration = np.random.choice(
      [4, 5, 6, 8, 15], size=num_samples
  )  # matches our service durations
  hour_of_day = np.random.randint(
      8, 17, size=num_samples
  )  # Bank operating hours 8 AM to 5 PM

  # Simulate actual wait time with some realistic formula + random noise
  # Longer queue and higher service duration increase wait time; peak hours (around 12-14) add delay
  peak_hour_factor = np.where(
      (hour_of_day >= 12) & (hour_of_day <= 14), 1.5, 1.0
  )
  noise = np.random.normal(0, 2, size=num_samples)

  actual_wait_time = (
      (queue_length * (estimated_duration * 0.4)) * peak_hour_factor
  ) + noise
  actual_wait_time = np.clip(
      actual_wait_time, 1.0, 60.0
  )  # Keep bounds realistic (1 to 60 mins)

  # Create DataFrame
  df = pd.DataFrame({
      'queue_length': queue_length,
      'estimated_duration': estimated_duration,
      'hour_of_day': hour_of_day,
      'actual_wait_time': np.round(actual_wait_time, 2),
  })

  # Save to CSV
  df.to_csv(output_path, index=False)
  print(
      f'Successfully generated {num_samples} simulated records and saved to'
      f' {output_path}'
  )


if __name__ == '__main__':
  generate_queue_dataset()

