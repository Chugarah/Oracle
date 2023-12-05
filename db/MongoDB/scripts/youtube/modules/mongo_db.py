from pymongo import MongoClient
from bson.objectid import ObjectId


def connect_to_mongodb():
    # Connect to the MongoDB server with authentication
    client = MongoClient(host='localhost', port=27017,
                         username='admin', password='secret')
    return client


def search_video_id_collection(database_name, video_id):
    # Connect to MongoDB
    client = connect_to_mongodb()

    # Select the desired database
    db = client[database_name]

    # Iterate over all collections in the database
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        result = collection.find_one({"video_id": video_id})
        if result:
            return collection_name

    return None


def update_document(database_name, collection_name, video_id, update_data):
    # Connect to MongoDB
    client = connect_to_mongodb()

    # Select the desired database and collection
    db = client[database_name]
    collection = db[collection_name]

    # Retrieve the document based on the video_id
    document = collection.find_one({"video_id": video_id})

    if document:
        # Append the new file object to the 'files' array
        document['files'].append(update_data)

        # Update the document in the collection
        result = collection.update_one(
            {"video_id": video_id}, {"$set": document})

        # Check if the update was successful
        if result.modified_count > 0:
            print("Document updated successfully.")
        else:
            print("No document found for the given ID.")
    else:
        print("No document found for the given ID.")
