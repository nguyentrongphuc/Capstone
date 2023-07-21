# Capstone - Table of Contents   
1. [Overview](#overview)
2. [Font End URL](#font-end-url)
3. [APIs Document](#apis-document)
4. [Postman](#postman)
5. [Project dependencies and Local development](#project-dependencies-and-local-development)
6. [Authentication](#authentication)
7. [AWS deployment instructions](#aws-deployment-instructions)

# Overview

Capstone is provide to view, add new, delete vehicles

- Add new Make or Model
- Modify existed Make
- Delete Make and Model

![image](images/capstone-vehicle-info.png)

# Font End URL

http://a69e21d0efe8345ab95207dd2e1343c2-1886797275.us-east-2.elb.amazonaws.com/

# APIs Document

# Postman

# Project dependencies and Local development
## Prerequisite and project dependencies
- Docker desktop 
- Git
- Code editor (e.g. Visual Studio code)
- Postgres DB
- AWS Account
- Python and some library you can see [here](src/backend/requirements.txt)
- Termial or CMD

## Project structure (main files)

These are the files relevant for the current project:
```bash
.
├── Dockerfile
├── aws .
│       ├── auth
│       │       └── auth.py
│       ├── config
│       │       ├── prod.py
│       │       └── test.py
│       ├── aws-auth-patch.yml          # A sample EKS Cluster configMap file. 
│       ├── capstone_api.yml            # This is file that aws codebuild is using to create docker on EC2/POD/Node
│       ├── trust.json                  # TODO - Used for creating an IAM role for Codebuild
│       ├── iam-role-policy.json
│       └── ci-cd-codepipeline.cfn.yml  # TODO - YAML template to create CodePipeline pipeline and CodeBuild resources
├── src/backend.
│       ├── main.py	                    # APs and one endpoint for simple fontend
│       ├── test_main.py                # TODO - Unit Test file		
│       └── requirements.txt
├── buildspec.yml                       # project builder
│
└── README.MD                           # documentation

```

## Steps to run the App Locally
The following steps describe how to run the Flask API locally with the standard Flask server, so that you can test endpoints before you containerize the app:

### 1. Install python dependencies
These dependencies are kept in a requirements.txt file in the root directory of the repository. To install them, go to the project directory that you’ve just downloaded, and run the command:
```bash
# Assuming you are in the Capstone/src/backend/ directory
pip install -r requirements.txt
```
### 2. Set up the environment
You will need the following two places available in your terminal environment:

- authentication environments places in [auth.py](src/backend/auth/auth.py)
    ```python
    ALGORITHMS = [os.environ.get('ALGORITHMS', 'RS256')]
    API_AUDIENCE = os.environ.get('API_AUDIENCE', 'phuc')
    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN', 'phucnguyen.us.auth0.com')
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID', 'J804TumgtEPJ9Sr0MY6opWIu3SmgROM9')
    AUTH0_CALLBACK_URL = os.environ.get('AUTH0_CALLBACK_URL', 'http://127.0.0.1:5000/')
    ```
- database environments config place in [prod.py](src/backend/config/prod.py)

    ```python
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1:5432')  
    DB_USER = os.environ.get('DB_USER', 'postgres')  
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'P%40ssw0rd')    
    DB_NAME = os.environ.get('DB_NAME', 'vehicleinfo')  
    DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
    ```

- notes: if you run with unit testing, the config place in [test.py](src/backend/config/test.py)


To add these to your terminal environment, run the following: 
```bash 
export ALGORITHMS='RS256' 
export API_AUDIENCE='phuc'
....

# Verify 
echo $ALGORITHMS 
echo $API_AUDIENCE
```

### 3. Run the app
Run the app using the Flask server, from the root directory of the downloaded repository, run:

```bash
# Assuming you are in the Capstone/src/backend/ directory
FLASK_APP=main.py FLASK_DEBUG=True flask run

# anothe way you can try to run 
python3 main.py

```

Open http://127.0.0.1:5000/ in a new browser - It will give you a response as
![image](images/homepage.png)

# Authentication

# AWS deployment instructions

We are using CI/CD pipeline and Github repository
![image](images/overview.png)

