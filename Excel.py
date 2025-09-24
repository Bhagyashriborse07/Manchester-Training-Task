import json
import pandas as pd
import os

json_file = "data.json"

# Make sure the file exists
if not os.path.exists(json_file):
    raise FileNotFoundError(f"JSON file not found: {json_file}")

# Load JSON data
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# List to store rows
rows = []

# Loop through each item (medical group)
for item in data:
    # Extract general information
    general_info = item.get("general_information", [{}])[0]
    group_name = general_info.get("name", "")
    included_tins = [str(t.get("tin")) for t in general_info.get("included_tins", [])]

    # Loop through providers
    for provider in item.get("providers", []):
        provider_uuid = provider.get("uuid", "")

        # Loop through locations
        for loc in provider.get("locations", []):
            loc_uuid = loc.get("location_uid", "")
            create_date = loc.get("create_date", {}).get("$date") if isinstance(loc.get("create_date"), dict) else loc.get("create_date")
            term_date = loc.get("term_date")
            is_active = loc.get("isActive", False)

            # Create a row for Excel
            row = {
                "Group Name": group_name,
                "Included TINs": ", ".join(included_tins),
                "Provider UUID": provider_uuid,
                "Location UUID": loc_uuid,
                "Location Create Date": create_date,
                "Location Term Date": term_date,
                "Location Active": is_active
            }
            rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)

# Save Excel file in the same folder
excel_file = "providers_data.xlsx"
df.to_excel(excel_file, index=False, engine='openpyxl')

print(f"Excel file created successfully: {excel_file}")
