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