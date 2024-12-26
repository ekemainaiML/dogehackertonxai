import secrets
from authapi.appwriteservice.appwritecloud import client, APPWRITE_DB_ID, APPWRITE_COLLECTION_ID
from appwrite.services.databases import Databases
import sys

sys.path.append('../')

databases = Databases(client)

#result = databases.create(
#    database_id=secrets.token_hex(8),
#    name='auth_db')
# print(result)

# Create a collection
#collection = databases.create_collection(
#    database_id=APPWRITE_DB_ID,
#    collection_id=secrets.token_hex(8),
#    name='users'
#)

# define attributes
result1 = databases.create_string_attribute(
     database_id = APPWRITE_DB_ID,
     collection_id = APPWRITE_COLLECTION_ID,
     key = 'fullname',
     size = 100,
     required= True
 )

result2 = databases.create_string_attribute(
     database_id = APPWRITE_DB_ID,
     collection_id = APPWRITE_COLLECTION_ID,
     key = 'username',
     size = 50,
     required= True
)

result3 = databases.create_string_attribute(
    database_id = APPWRITE_DB_ID,
    collection_id= APPWRITE_COLLECTION_ID,
    key = 'password',
    size = 255,
    required= True
)

result4 = databases.create_string_attribute(
    database_id = APPWRITE_DB_ID,
    collection_id= APPWRITE_COLLECTION_ID,
    key = 'token',
    size = 255,
    required = False
)

result5 = databases.create_boolean_attribute(
    database_id = APPWRITE_DB_ID,
    collection_id= APPWRITE_COLLECTION_ID,
    key = 'signup',
    required= False
)

result6 = databases.create_boolean_attribute(
    database_id = APPWRITE_DB_ID,
    collection_id= APPWRITE_COLLECTION_ID,
    key = 'loggedin',
    required = False
)

result7 = databases.create_datetime_attribute(
    database_id = APPWRITE_DB_ID,
    collection_id= APPWRITE_COLLECTION_ID,
    key = 'createdat',
    required = False
)

result8 = databases.create_datetime_attribute(
    database_id = APPWRITE_DB_ID,
    collection_id= APPWRITE_COLLECTION_ID,
    key = 'tokenexpires',
    required = False
)

# print(result)


# result = db.list_documents(
#     db_id,db_collection_id
# )

# print(result)