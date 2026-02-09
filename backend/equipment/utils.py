"""
Utility functions for CSV parsing and data analysis.
"""

import pandas as pd
from io import StringIO


def parse_csv(file_content):
    """
    Parse CSV content and return a pandas DataFrame.
    
    Args:
        file_content: File content as string or file-like object
        
    Returns:
        pandas DataFrame with the CSV data
        
    Raises:
        ValueError: If CSV is invalid or missing required columns
    """
    try:
        if isinstance(file_content, bytes):
            file_content = file_content.decode('utf-8')
        
        if isinstance(file_content, str):
            df = pd.read_csv(StringIO(file_content))
        else:
            df = pd.read_csv(file_content)
        
        return df
    except Exception as e:
        raise ValueError(f"Failed to parse CSV: {str(e)}")


def validate_csv(df):
    """
    Validate that the DataFrame has all required columns.
    
    Required columns:
    - Equipment Name
    - Type
    - Flowrate
    - Pressure
    - Temperature
    
    Args:
        df: pandas DataFrame
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    
    # Normalize column names (strip whitespace)
    df.columns = df.columns.str.strip()
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    # Check for empty dataframe
    if df.empty:
        return False, "CSV file is empty"
    
    # Validate numeric columns
    numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
    for col in numeric_columns:
        try:
            pd.to_numeric(df[col], errors='raise')
        except (ValueError, TypeError):
            return False, f"Column '{col}' must contain numeric values"
    
    return True, None


def calculate_summary(df):
    """
    Calculate summary statistics from the equipment DataFrame.
    
    Args:
        df: pandas DataFrame with equipment data
        
    Returns:
        Dictionary containing:
        - total_count: Number of equipment records
        - avg_flowrate: Average flowrate
        - avg_pressure: Average pressure  
        - avg_temperature: Average temperature
        - type_distribution: Dict of equipment type counts
    """
    # Clean the dataframe
    df = df.dropna()
    
    # Calculate averages
    total_count = len(df)
    avg_flowrate = round(float(df['Flowrate'].mean()), 2) if total_count > 0 else 0.0
    avg_pressure = round(float(df['Pressure'].mean()), 2) if total_count > 0 else 0.0
    avg_temperature = round(float(df['Temperature'].mean()), 2) if total_count > 0 else 0.0
    
    # Calculate type distribution
    type_distribution = df['Type'].value_counts().to_dict()
    
    return {
        'total_count': total_count,
        'avg_flowrate': avg_flowrate,
        'avg_pressure': avg_pressure,
        'avg_temperature': avg_temperature,
        'type_distribution': type_distribution
    }


def prepare_records(df, dataset):
    """
    Prepare equipment records from DataFrame for database insertion.
    
    Args:
        df: pandas DataFrame with equipment data
        dataset: Dataset model instance
        
    Returns:
        List of EquipmentRecord instances (not saved)
    """
    from .models import EquipmentRecord
    
    records = []
    df = df.dropna()
    
    for _, row in df.iterrows():
        record = EquipmentRecord(
            dataset=dataset,
            equipment_name=str(row['Equipment Name']).strip(),
            equipment_type=str(row['Type']).strip(),
            flowrate=float(row['Flowrate']),
            pressure=float(row['Pressure']),
            temperature=float(row['Temperature'])
        )
        records.append(record)
    
    return records
