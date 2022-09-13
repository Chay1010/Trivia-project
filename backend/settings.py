from dotenv import load_dotenv
import os
load_dotenv()

db_name = os.environ.get("db_name")
db_user = os.environ.get("db_user")
db_password = os.environ.get("db_password")
db_name_test = os.environ.get("db_name_test")