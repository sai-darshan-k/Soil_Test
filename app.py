from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load all sheets from the Excel file
excel_file = "Soil_Labs_By_State1.xlsx"
df_all_sheets = pd.read_excel(excel_file, sheet_name=None)  # Read all sheets into a dictionary of DataFrames

@app.route("/")
def index():
    """Render HTML template with all unique states."""
    # Combine all dataframes into one
    df_combined = pd.concat(df_all_sheets.values(), ignore_index=True)
    
    # Get unique states from all sheets
    states = df_combined['State'].dropna().unique().tolist()
    return render_template("soil_labs.html", states=states)

@app.route("/get_districts", methods=["GET"])
def get_districts():
    """Fetch unique districts based on the selected state from all sheets."""
    state = request.args.get("state")
    if state:
        # Combine all dataframes into one and filter by state
        df_combined = pd.concat(df_all_sheets.values(), ignore_index=True)

        # Clean state names to avoid issues with special characters or spaces
        df_combined['State'] = df_combined['State'].str.replace('&', 'and').str.strip()

        # Clean the input state as well
        state_clean = state.replace('&', 'and').strip()

        # Get unique districts for the selected state
        districts = df_combined[df_combined['State'] == state_clean]['District'].dropna().unique().tolist()

        return jsonify(districts)
    
    return jsonify([]) 


@app.route("/get_data", methods=["GET"])
def get_data():
    state = request.args.get("state")
    district = request.args.get("district")

    if state and district:
        # Combine all dataframes into one and filter by state and district
        df_combined = pd.concat(df_all_sheets.values(), ignore_index=True)
        data_filtered = df_combined[(df_combined['State'] == state) & (df_combined['District'] == district)]

        if data_filtered.empty:
            return jsonify([])

        return jsonify(data_filtered.to_dict(orient="records"))

    return jsonify([])  # Return empty if either state or district is not provided

if __name__ == "__main__":
    app.run(debug=True)
