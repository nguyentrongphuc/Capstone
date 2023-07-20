import os

TESTING = False

# Connect to the database 
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1:5432')  
DB_USER = os.environ.get('DB_USER', 'postgres')  
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'P%40ssw0rd')    
DB_NAME = os.environ.get('DB_NAME', 'vehicleinfo')  
DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False
