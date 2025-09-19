
from pymongo import MongoClient
import json


client = MongoClient("mongodb+srv://bhagyashree:test123@cluster0.roswjud.mongodb.net/mydatabase?retryWrites=true&w=majority",tls=True)
db = client["Dev"]

groups_col = db["group"]
providers_col = db["providers"]

sample_provider = providers_col.find_one()
print(sample_provider)


result = []

# 2. Loop through all groups
for group in groups_col.find():
    # Extract provider UUIDs from group
    provider_uuids = [p.get("uuid") for p in group.get("providers", []) if p.get("uuid")]

    # 3. Fetch provider details for those UUIDs
    providers = list(providers_col.find({"uuid": {"$in": provider_uuids}}))

    # 4. Combine group + providers
    result.append({
        "group_id": str(group["_id"]),
        "group_name": group.get("general_information", [{}])[0].get("name"),
        "provider_uuids": provider_uuids,
        "providers": providers
    })

# 5. Save result into JSON file
with open("Providers_output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4, default=str, ensure_ascii=False)

print("✅ Data has been saved to Providers_output.json")
