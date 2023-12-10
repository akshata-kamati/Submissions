import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here

import pandas as pd
def generate_car_matrix(dataset):
car_matrix = dataset.pivot(index='id_1', columns='id_2', values='car').fillna(0)
car_matrix.values[[range(len(car_matrix))]*2] = 0
return car_matrix


    


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here

import pandas as pd
def get_type_count(dataset):
    dataset['car_type'] = pd.cut(dataset['car'],
                                 bins=[-float('inf'), 15, 25, float('inf')],
                                 labels=['low', 'medium', 'high'],
                                 include_lowest=True, right=False)

    type_counts = dataset['car_type'].value_counts().to_dict()
    sorted_type_counts = {key: type_counts[key] for key in sorted(type_counts)}
     return sorted_type_counts




def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here

   import pandas as pd

def get_bus_indexes(dataset):
   
    bus_mean = dataset['bus'].mean()

  
    bus_indexes = dataset[dataset['bus'] > 2 * bus_mean].index.tolist()

    bus_indexes.sort()

    return bus_indexes





def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here

    import pandas as pd

def filter_routes(dataset):
    
    route_avg_truck = dataset.groupby('route')['truck'].mean()

    
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()


    selected_routes.sort()

    return selected_routes





def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here

  import pandas as pd

def multiply_matrix(result_matrix):
   
    modified_matrix = result_matrix.copy()

   
    modified_matrix[modified_matrix > 20] *= 0.75
    modified_matrix[modified_matrix <= 20] *= 1.25

   
    modified_matrix = modified_matrix.round(1)

    return modified_matrix





def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here

  import pandas as pd

def check_timestamp_completeness(dataset):
    
    dataset['start_timestamp'] = pd.to_datetime(dataset['startDay'] + ' ' + dataset['startTime'])
    dataset['end_timestamp'] = pd.to_datetime(dataset['endDay'] + ' ' + dataset['endTime'])

    
    completeness_check = (
        (dataset['end_timestamp'] - dataset['start_timestamp'] == pd.Timedelta(days=1) - pd.Timedelta(seconds=1)) &
        (dataset['start_timestamp'].dt.dayofweek == 0) &
        (dataset['end_timestamp'].dt.dayofweek == 6)
    )

 
    completeness_series = completeness_check.groupby(['id', 'id_2']).all()

    return completeness_series



