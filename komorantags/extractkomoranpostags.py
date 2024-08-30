import openpyxl
import pandas as pd

def extract_columns(input_file, output_excel, output_text):
    # Load the workbook and select the active worksheet
    wb = openpyxl.load_workbook(input_file)
    ws = wb.active

    # Initialize lists to store the extracted data
    column_g = []
    column_h = []

    # Iterate through the rows
    for row in ws.iter_rows(min_col=7, max_col=8, values_only=True):
        if row[0] is not None:  # Check if column G has a value
            column_g.append(row[0])
            column_h.append(row[1])

    # Create a DataFrame
    df = pd.DataFrame({'Column G': column_g, 'Column H': column_h})

    # Save to Excel
    df.to_excel(output_excel, index=False)

    # Save to text file
    with open(output_text, 'w') as f:
        for g, h in zip(column_g, column_h):
            f.write(f"{g} - {h}\n")

    print(f"Data extracted and saved to {output_excel} and {output_text}")

# Usage
input_file = 'Korean POS tags comparison chart.xlsx'
output_excel = 'output.xlsx'
output_text = 'output.txt'

extract_columns(input_file, output_excel, output_text)