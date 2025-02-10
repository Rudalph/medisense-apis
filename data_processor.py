import pandas as pd

def process_sample_data():
    # Create a sample DataFrame
    data = {
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['New York', 'London', 'Paris']
    }
    
    df = pd.DataFrame(data)
    
    # Perform some processing
    result = {
        'average_age': df['age'].mean(),
        'total_records': len(df),
        'cities': df['city'].tolist()
    }
    
    return result