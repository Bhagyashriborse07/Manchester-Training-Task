from pymongo import MongoClient
import json

client = MongoClient(
    "mongodb+srv://bhagyashree:test123@cluster0.roswjud.mongodb.net/?retryWrites=true&w=majority",
    tls=True
)


db = client["Dev"]
groups_col = db["group"]

# 3. Fetch all documents
data = list(groups_col.find({}))

# 4. Print results
for doc in data:
    print(doc)

# 5. Save results to JSON file
with open("groups_output.json", "w") as f:
    json.dump(data, f, default=str, indent=4)

print("✅ Data fetched and saved to groups_output.json")
