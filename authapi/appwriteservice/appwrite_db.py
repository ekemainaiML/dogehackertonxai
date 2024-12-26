import secrets
from authapi.appwriteservice.appwritecloud import client, APPWRITE_DB_ID, APPWRITE_COLLECTION_ID
from appwrite.services.databases import Databases
import sys

sys.path.append('../')

databases = Databases(client)

class CRUD:
   def __init__(self):
      self.db_id = APPWRITE_DB_ID
      self.coll_id = APPWRITE_COLLECTION_ID

   def get_all_users(self):
      result = databases.list_documents(
         database_id=self.db_id,
         collection_id=self.coll_id
      )

      print(type(result))
      return result

   def create_user(self, data: dict):
      result = databases.create_document(
         database_id=self.db_id,
         collection_id=self.coll_id,
         document_id=secrets.token_hex(8),
         data=data
      )

      return result

   def retrieve_users(self, username: str):
      result = databases.get_document(
         database_id=self.db_id,
         collection_id=self.coll_id,
         document_id=username
      )

      return result

   def update_user(self, username: str, data):
      result = databases.update_document(
         database_id=self.db_id,
         collection_id=self.coll_id,
         document_id=username,
         data=data
      )

      return result

   def delete_user(self, username: str):
      result = databases.delete_document(
         database_id=self.db_id,
         collection_id=self.coll_id,
         document_id=username,
      )

      return result