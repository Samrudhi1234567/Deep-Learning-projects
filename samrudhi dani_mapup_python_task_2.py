import pandas as pd

import datetime


def calculate_distance_matrix(df)->pd.DataFrame:
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    # Combine bidirectional distances by duplicating rows with reversed 'Toll_A' and 'Toll_B'
    reversed_df = df.copy()
    reversed_df = reversed_df.rename(columns={'Toll_A': 'Temp', 'Toll_B': 'Toll_A', 'Temp': 'Toll_B'})
    concatenated_df = pd.concat([df, reversed_df], ignore_index=True)

    # Group by 'Toll_A' and 'Toll_B' to calculate cumulative distances along known routes
    grouped_distances = concatenated_df.groupby(['Toll_A', 'Toll_B'])['Distance'].sum().reset_index()

    # Create a pivot table to represent the distance matrix
    distance_matrix = grouped_distances.pivot(index='Toll_A', columns='Toll_B', values='Distance').fillna(0)

    # Ensure symmetric matrix accounting for bidirectional distances
    distance_matrix = distance_matrix.add(distance_matrix.T, fill_value=0)
    
    # Set diagonal values to 0
    for i in range(min(distance_matrix.shape)):
        distance_matrix.iloc[i, i] = 0

    return distance_matrix
    #return df


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    # Get all indices except for the diagonal
    indices = df.index.tolist()
    
    # Create combinations of id_start, id_end pairs
    id_start = []
    id_end = []
    distance = []

    for i in range(len(indices)):
        for j in range(len(indices)):
            if i != j:
                id_start.append(indices[i])
                id_end.append(indices[j])
                distance.append(df.iloc[i, j])

    # Create a DataFrame from the combinations
    unrolled_df = pd.DataFrame({
        'id_start': id_start,
        'id_end': id_end,
        'distance': distance
    })

    return unrolled_df
    #return df


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
    # Calculate the average distance for the reference_id
    avg_distance_reference = df[df['id_start'] == reference_id]['distance'].mean()

    # Calculate the threshold range within 10% of the reference value's average
    threshold = 0.1 * avg_distance_reference
    lower_limit = avg_distance_reference - threshold
    upper_limit = avg_distance_reference + threshold

    # Filter 'id_start' values within the specified percentage threshold
    within_threshold_ids = df[(df['id_start'] != reference_id) & 
                              (df['distance'] >= lower_limit) & 
                              (df['distance'] <= upper_limit)]['id_start'].unique()

    # Sort and return the list of 'id_start' values within the threshold
    sorted_ids_within_threshold = sorted(within_threshold_ids.tolist())

    return sorted_ids_within_threshold
    #return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    # Calculate toll rates for each vehicle type based on distance
    df['moto'] = df['distance'] * 0.8
    df['car'] = df['distance'] * 1.2
    df['rv'] = df['distance'] * 1.5
    df['bus'] = df['distance'] * 2.2
    df['truck'] = df['distance'] * 3.6

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    # Define time ranges and corresponding discount factors
    weekday_discounts = {
        (datetime.strptime('00:00:00', '%H:%M:%S').time(), datetime.strptime('10:00:00', '%H:%M:%S').time()): 0.8,
        (datetime.strptime('10:00:00', '%H:%M:%S').time(), datetime.strptime('18:00:00', '%H:%M:%S').time()): 1.2,
        (datetime.strptime('18:00:00', '%H:%M:%S').time(), datetime.strptime('23:59:59', '%H:%M:%S').time()): 0.8
    }
    weekend_discount = 0.7

    # Extract day names and time values
    df['start_day'] = pd.to_datetime(df['start_day']).dt.day_name()
    df['end_day'] = pd.to_datetime(df['end_day']).dt.day_name()
    df['start_time'] = pd.to_datetime(df['start_time']).dt.time
    df['end_time'] = pd.to_datetime(df['end_time']).dt.time

    # Apply discount factors based on time intervals
    for idx, row in df.iterrows():
        if row['start_day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            for time_range, discount in weekday_discounts.items():
                if time_range[0] <= row['start_time'] <= time_range[1]:
                    df.at[idx, 'moto'] *= discount
                    df.at[idx, 'car'] *= discount
                    df.at[idx, 'rv'] *= discount
                    df.at[idx, 'bus'] *= discount
                    df.at[idx, 'truck'] *= discount
                    break
        else:  # Weekend
            df.at[idx, 'moto'] *= weekend_discount
            df.at[idx, 'car'] *= weekend_discount
            df.at[idx, 'rv'] *= weekend_discount
            df.at[idx, 'bus'] *= weekend_discount
            df.at[idx, 'truck'] *= weekend_discount

    return df
