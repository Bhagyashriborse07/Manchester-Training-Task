import json
import pandas as pd
import os

# JSON file path (make sure data.json is in the same folder)
json_file = "FetchAllData.json"

# Check if file exists
if not os.path.exists(json_file):
    raise FileNotFoundError(f"JSON file not found: {json_file}")

# Load JSON data
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# List of columns based on your Google Sheet
columns = [
    "Group Name",
    "Group Description",
    "Included TINs",
    "Provider UUID",
    "Provider First Name",
    "Provider Last Name",
    "Provider Specialty",
    "Location UUID",
    "Location Create Date",
    "Location Term Date",
    "Location Active",
    "Provider Phone",
    "Provider Email",
    "Provider Fax",
    "Provider Address",
    "Tax ID",
    "Tax Name",
    # Add all other columns from your Sheet here
]

# List to store rows
rows = []

for item in data:
    general_info = item.get("general_information", [{}])[0]
    group_name = general_info.get("name", "")
    group_desc = general_info.get("description", "")
    included_tins = ", ".join(str(t.get("tin")) for t in general_info.get("included_tins", []))

    tax_info = item.get("tax_information", {})
    tax_id = tax_info.get("tax_id", "")
    tax_name = tax_info.get("name_on_W9", "")

    for provider in item.get("providers", []):
        provider_uuid = provider.get("uuid", "")
        first_name = provider.get("first_name", "")  # Update key if JSON has different field
        last_name = provider.get("last_name", "")
        specialty = provider.get("specialty", "")

        phone = provider.get("phone", "")
        email = provider.get("email", "")
        fax = provider.get("fax", "")
        address = provider.get("address", "")

        for loc in provider.get("locations", []):
            loc_uuid = loc.get("location_uid", "")
            create_date = loc.get("create_date", {}).get("$date") if isinstance(loc.get("create_date"), dict) else loc.get("create_date")
            term_date = loc.get("term_date")
            is_active = loc.get("isActive", False)

            # Build a row dictionary
            row = {
                "Group Name": group_name,
                "Group Description": group_desc,
                "Included TINs": included_tins,
                "Provider UUID": provider_uuid,
                "Provider First Name": first_name,
                "Provider Last Name": last_name,
                "Provider Specialty": specialty,
                "Location UUID": loc_uuid,
                "Location Create Date": create_date,
                "Location Term Date": term_date,
                "Location Active": is_active,
                "Provider Phone": phone,
                "Provider Email": email,
                "Provider Fax": fax,
                "Provider Address": address,
                "Tax ID": tax_id,
                "Tax Name": tax_name
            }
            rows.append(row)

# Create DataFrame with the exact column order
df = pd.DataFrame(rows, columns=columns)

# Save Excel file
excel_file = "Fetch_All_Data.xlsx"
df.to_excel(excel_file, index=False, engine='openpyxl')

print(f"Excel file created successfully: {excel_file}")
