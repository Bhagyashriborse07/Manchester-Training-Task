import json
import pandas as pd

# Load JSON data from data.json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# List to store rows
rows = []

# Loop through each medical group
for item in data:
    general_info = item.get("general_information", [{}])[0]
    group_name = general_info.get("name", "")
    group_description = general_info.get("description", "")
    included_tins = [str(t.get("tin")) for t in general_info.get("included_tins", [])]

    # Loop through providers
    for provider in item.get("providers", []):
        provider_uuid = provider.get("uuid", "")
        # If provider first_name, last_name exist in JSON
        first_name = provider.get("first_name", "")
        last_name = provider.get("last_name", "")
        npi = provider.get("npi", "")
        dea = provider.get("dea", "")
        email = provider.get("email", "")
        phone = provider.get("phone", "")

        # Loop through locations for the provider
        for loc in provider.get("locations", []):
            loc_uuid = loc.get("location_uid", "")
            create_date = loc.get("create_date", {}).get("$date") if isinstance(loc.get("create_date"), dict) else loc.get("create_date")
            term_date = loc.get("term_date")
            is_active = loc.get("isActive", False)

            # Example for location address, phone if exists
            loc_address = loc.get("address", "")
            loc_phone = loc.get("phone", "")

            # Create row for Excel
            row = {
                "Provider UUID": provider_uuid,
                "First Name": first_name,
                "Last Name": last_name,
                "NPI": npi,
                "DEA": dea,
                "Email": email,
                "Phone": phone,
                "Group Name": group_name,
                "Group Description": group_description,
                "Group TINs": ", ".join(included_tins),
                "Location UUID": loc_uuid,
                "Location Address": loc_address,
                "Location Phone": loc_phone,
                "Location Create Date": create_date,
                "Location Term Date": term_date,
                "Location Active": is_active
            }
            rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)

# Save to Excel file
excel_file = "Excel1_providers_data.xlsx"
df.to_excel(excel_file, index=False, engine='openpyxl')

print(f"Excel file created successfully: {excel_file}")
