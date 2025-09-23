from pymongo import MongoClient
import json


def get_db_connection(uri: str, db_name: str):
    """Connect to MongoDB and return the database object."""
    client = MongoClient(uri, tls=True)
    return client[db_name]


def fetch_group_with_providers(groups_col, providers_col):
    """
    Fetch all groups and their related providers.
    Returns a list of dictionaries.
    """
    results = []

    for group in groups_col.find():
        # Extract provider UUIDs
        provider_uuids = [p.get("uuid") for p in group.get("providers", []) if p.get("uuid")]

        if not provider_uuids:
            continue  # skip groups with no providers

        # Fetch provider details for these UUIDs
        providers = list(providers_col.find({"uuid": {"$in": provider_uuids}}))

        # Combine group and provider info
        results.append({
            "group_id": str(group.get("_id")),
            "group_name": group.get("general_information", [{}])[0].get("name", "Unknown"),
            "provider_uuids": provider_uuids,
            "providers": providers
        })

    return results


def save_to_json(data, filename="Provider_Using_Function.json"):
    """Save data to JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, default=str, ensure_ascii=False)
    print(f"✅ Data has been saved to {filename}")


def main():
    # MongoDB connection info
    uri = "mongodb+srv://bhagyashree:test123@cluster0.roswjud.mongodb.net/mydatabase?retryWrites=true&w=majority"
    db_name = "Dev"

    # Connect to DB and get collections
    db = get_db_connection(uri, db_name)
    groups_col = db["group"]
    providers_col = db["providers"]

    # Optional: print one sample provider
    sample_provider = providers_col.find_one()
    print("Sample provider:", sample_provider)

    # Fetch groups with their providers
    results = fetch_group_with_providers(groups_col, providers_col)

    # Save results to JSON
    save_to_json(results)


if __name__ == "__main__":
    main()
