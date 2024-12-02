from pymongo import MongoClient
from .utils import dbLocation
from django.http import JsonResponse, HttpResponse
from pymongo import MongoClient
import logging

# databases = get_database_client()
# client = MongoClient(databases)
# db = client.server_db
# lights_collection = db.lighting_users



# client, ssh_tunnel = get_database_client()

client2 = MongoClient(dbLocation)

logger = logging.getLogger(__name__)


def print_example(request):
    
    try:
        
        db2 = client2['server_db']  # Replace 'server_db' with your database name
        
        # Access the collection
        user_collection = db2['user']  # Replace 'user' with your collection name
        
        # Fetch documents
        x = user_collection.find({}, {"_id": 0})  # Query all documents, excluding `_id`
        documents_list = list(x)  # Convert cursor to list
        
        # Return documents or an appropriate message
        if documents_list:
            return JsonResponse(documents_list, safe=False)
        else:
            return JsonResponse({'message': "No documents found"})
    except Exception as e:
        # Handle and log connection or query errors
        return JsonResponse({'error': f"MongoDB connection or query failed: {str(e)}"})
    
    
