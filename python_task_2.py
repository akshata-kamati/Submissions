import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here

    import pandas as pd

def calculate_distance_matrix(dataset):
   
    distance_matrix = dataset.pivot(index='id_1', columns='id_2', values='distance').fillna(0)

    
    distance_matrix += distance_matrix.T

    for id_1 in distance_matrix.index:
        for id_2 in distance_matrix.columns:
            if id_1 != id_2 and distance_matrix.at[id_1, id_2] == 0:
                # Find intermediate points for known routes
                intermediate_points = distance_matrix.index.intersection([id_1, id_2])
                for intermediate_point in intermediate_points:
                    if intermediate_point != id_1 and intermediate_point != id_2:
                        distance_matrix.at[id_1, id_2] += (
                            distance_matrix.at[id_1, intermediate_point] +
                            distance_matrix.at[intermediate_point, id_2]
                        )

  
    distance_matrix.values[[range(len(distance_matrix))]*2] = 0

    return distance_matrix




def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
import pandas as pd

def unroll_distance_matrix(distance_matrix):
    
    unrolled_distances = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

   
    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            if id_start != id_end:
                distance = distance_matrix.at[id_start, id_end]
                unrolled_distances = unrolled_distances.append({
                    'id_start': id_start,
                    'id_end': id_end,
                    'distance': distance
                }, ignore_index=True)

    return unrolled_distances





def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here

  import pandas as pd

def find_ids_within_ten_percentage_threshold(distance_df, reference_value):
    
    reference_avg_distance = distance_df[distance_df['id_start'] == reference_value]['distance'].mean()

    
    threshold = 0.1 * reference_avg_distance

   
    within_threshold = distance_df[
        (distance_df['id_start'] != reference_value) &
        (distance_df['distance'] >= (reference_avg_distance - threshold)) &
        (distance_df['distance'] <= (reference_avg_distance + threshold))
    ]

   
    result_ids = within_threshold['id_start'].unique().tolist()
    result_ids.sort()

    return result_ids




def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here

   import pandas as pd

def calculate_toll_rate(distance_df):
   
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    
    for vehicle_type, coefficient in rate_coefficients.items():
        distance_df[vehicle_type] = distance_df['distance'] * coefficient

    return distance_df




def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

   import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time

def calculate_time_based_toll_rates(time_df):

    time_intervals = {
        'weekday_morning': (time(0, 0), time(10, 0)),
        'weekday_afternoon': (time(10, 0), time(18, 0)),
        'weekday_evening': (time(18, 0), time(23, 59, 59)),
        'weekend_all_day': (time(0, 0), time(23, 59, 59))
    }
    
    discount_factors = {
        'weekday_morning': 0.8,
        'weekday_afternoon': 1.2,
        'weekday_evening': 0.8,
        'weekend_all_day': 0.7
    }

    
    time_df['start_day'] = time_df['start_timestamp'].dt.day_name()
    time_df['start_time'] = time_df['start_timestamp'].dt.time
    time_df['end_day'] = time_df['end_timestamp'].dt.day_name()
    time_df['end_time'] = time_df['end_timestamp'].dt.time


    for interval, (start_time, end_time) in time_intervals.items():
        mask = ((time_df['start_time'] >= start_time) & (time_df['start_time'] <= end_time))
        mask = mask | ((time_df['end_time'] >= start_time) & (time_df['end_time'] <= end_time))
        mask = mask & (time_df['start_day'] != time_df['end_day'])  # Ensure full 24-hour period

        time_df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= discount_factors[interval]

    return time_df


