# fastingWebAPI
A package that builds a web api based on [bgchof](https://github.com/ddppddpp/bgchof).  

Based on [FastAPI](https://fastapi.tiangolo.com)  

## Usage:

### Python venv

Clone the reporitory on your system:  
`
git clone https://github.com/ddppddpp/fastingWebAPI
`  
Create and activate a new python virtual environment  
`  
python -m venv .venv
source .venv/bin/activate
`  
install needed packages according to requirements.txt  
`  
pip install -r requirements.txt
`  
start uvircorn like  
`  
uvicorn main:app --host 0.0.0.0 --port 80000
`  
start a browser and go to [localhost:8000](http://localhost:8000)  

### Docker container

Build an image using the supplied Dockerfile and start a container, exposing a port of your desire.  

### AWS Lambda

To setup a container-based serverless function on AWS use the supplied dockerfile Dockerfile.aws.lambda. Please note it uses an environment variable to override the cache file location, as apparently '/tmp' is the only directory with write access in AWS Lambda.
To push a new version of the image use the following instructions (user/region dependable):

` 
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 310391119521.dkr.ecr.eu-central-1.amazonaws.com
`


`docker build -f Dockerfile.aws.lambda -t orthodox-fasting/fastapi-lambda .`


` 
docker tag orthodox-fasting/fastapi-lambda:latest 310391119521.dkr.ecr.eu-central-1.amazonaws.com/orthodox-fasting/fastapi-lambda:latest
` 


`docker push 310391119521.dkr.ecr.eu-central-1.amazonaws.com/orthodox-fasting/fastapi-lambda:latest`


Copy the image URI from the [GUI](https://eu-central-1.console.aws.amazon.com/ecr/repositories/private/310391119521/orthodox-fasting/fastapi-lambda?region=eu-central-1) and [Deploy New Image](https://eu-central-1.console.aws.amazon.com/lambda/home?region=eu-central-1#/functions/orthodox-fasting?tab=code)
