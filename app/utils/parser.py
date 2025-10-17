# app/utils/parser.py
import pandas as pd


def parse_file_in_memory(buffer, file_type, mappings):
    """
    Parses an in-memory buffer, renames columns based on user mapping, and validates.
    """
    try:
        if file_type == 'xlsx':
            df = pd.read_excel(buffer, engine='openpyxl')
        elif file_type == 'csv':
            df = pd.read_csv(buffer)
        else:
            raise ValueError("Unsupported file type. Use .xlsx or .csv")
    except Exception as e:
        raise ValueError(f"File is corrupted or not a valid {file_type} file.")

    # Invert the mapping for renaming: { 'User Column': 'Tally Column' }
    rename_map = {v: k for k, v in mappings.items() if v}
    if not all(col in df.columns for col in rename_map.keys()):
        raise ValueError("One of the mapped columns does not exist in the file.")

    df.rename(columns=rename_map, inplace=True)

    # --- Validation and Sanitization on standardized columns ---
    required_cols = {'Date', 'Party', 'Amount'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Mapping is incomplete. Please map all required Tally fields.")

    try:
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y%m%d')
        df['Amount'] = pd.to_numeric(df['Amount'])
    except Exception as e:
        raise ValueError(f"Data type error after mapping. Check the data in your mapped columns. Details: {e}")

    df.dropna(subset=['Date', 'Party', 'Amount'], inplace=True)

    return df