import pandas as pd
import numpy as np

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
    # Pivot the DataFrame to create the matrix
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')
    
    # Fill diagonal values with 0
    for i in range(min(car_matrix.shape)):
        car_matrix.iloc[i, i] = 0
    
    return car_matrix
    #return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    # Add a new column 'car_type' based on conditions
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.Series(np.select(conditions, choices, default='Unknown'))
    
    # Calculate count of occurrences for each car_type
    car_type_counts = df['car_type'].value_counts().sort_index().to_dict()
    
    return car_type_counts
    #return dict()


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()
    
    # Retrieve indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    
    # Sort indices in ascending order
    bus_indexes.sort()
    
    return bus_indexes
    #return list()


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    # Calculate average 'truck' values for each route
    avg_truck_per_route = df.groupby('route')['truck'].mean()
    
    # Filter routes where the average 'truck' value is greater than 7
    filtered_routes = avg_truck_per_route[avg_truck_per_route > 7].index.tolist()
    
    # Sort the list of routes
    filtered_routes.sort()
    
    return filtered_routes
    #return list()


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    # Apply conditions to modify matrix values
    modified_matrix = matrix.copy()
    for i in range(modified_matrix.shape[0]):
        for j in range(modified_matrix.shape[1]):
            value = modified_matrix.iloc[i, j]
            if value > 20:
                modified_matrix.iloc[i, j] = round(value * 0.75, 1)
            else:
                modified_matrix.iloc[i, j] = round(value * 1.25, 1)
    
    return modified_matrix
    #return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    # Combine 'startDay' and 'startTime' columns to create a single datetime column
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    # Calculate the duration of each event
    df['duration'] = df['end_datetime'] - df['start_datetime']

    # Group by 'id' and 'id_2' and check if each pair covers a full 24-hour and 7-day period
    time_validity = df.groupby(['id', 'id_2']).apply(lambda x: (
        x['duration'].min() >= pd.Timedelta(days=7) and
        x['start_datetime'].dt.floor('D').nunique() == 7
    ))

    return time_validity
    #return pd.Series()
