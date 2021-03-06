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
There's a GitHub Action file in .github/workflows that does the magic, spinning up a ubuntu-latest runner (limitted to x86!) that actually builds the docker image, tags it and pushes it to the Elastic Container Registry of choice.
For more info please see the following [Tutorial](https://aws.plainenglish.io/build-a-docker-image-and-publish-it-to-aws-ecr-using-github-actions-f20accd774c3).