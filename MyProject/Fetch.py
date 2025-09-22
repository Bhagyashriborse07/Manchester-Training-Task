import json
from bson import json_util
from pymongo import MongoClient

# Connect to MongoDB Atlas
client = MongoClient("")

db = client["Dev"]          # replace with your DB name
collection = db["group"]    # replace with your collection name

# Fetch all documents
data = list(collection.find({}))

# Save to JSON file
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, default=json_util.default, indent=4)

print("Data exported successfully to output.json")

