from pymongo import MongoClient
import json

# 1. Connect to MongoDB
client = MongoClient( "")
db = client["Dev"]

groups_col = db["group"]
providers_col = db["providers"]

result = []

# 2. Loop through all groups
for group in groups_col.find():
    # extract provider UUIDs from group document
    provider_uuids = [p.get("uuid") for p in group.get("providers", []) if p.get("uuid")]

    # 3. Fetch providers whose uuid matches
    providers = list(providers_col.find({"uuid": {"$in": provider_uuids}}))

    # 4. Append combined result
    result.append({
        "group_id": str(group["_id"]),
        "provider_uuids": provider_uuids,
        "providers": providers
    })


    # Save result into a JSON file
with open("Fetch_Each_Data_output.json", "w") as f:
    json.dump(result, f, indent=4, default=str)

print("✅ Data saved to Fetch_Each_Data_output.json")


# 5. Print output as JSON
print(json.dumps(result, indent=4, default=str))

