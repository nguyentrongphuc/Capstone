import os

TESTING = False

# Connect to the database 
DB_HOST = os.environ('DB_HOST', '127.0.0.1:5432')  
DB_USER = os.environ('DB_USER', 'postgres')  
DB_PASSWORD = os.environ('DB_PASSWORD', 'P%40ssw0rd')  


# DB_HOST = os.getenv('DB_HOST', 'vehicleinfo.cpozezvwnhgr.us-east-2.rds.amazonaws.com:5432')  
# DB_USER = os.getenv('DB_USER', 'postgres')  
# DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')  
DB_NAME = os.environ('DB_NAME', 'vehicleinfo')  
DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = DB_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False