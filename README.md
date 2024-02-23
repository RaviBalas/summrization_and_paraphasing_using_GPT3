## Wiki Summarisation & Paraphrasing Using GTP-3 Turbo
this project fetch various sections by topic from wikipedia, and summrizing and paraphasing text using openai GPT-3 Turbo model.



### Installation

1. Clone the repository:

```bash
git clone https://github.com/RaviBalas/summrization_and_paraphasing_using_GPT3.git
```

2. Set your environment variable

```bash
OPENAI_API_KEY="" # generate your api key from openai 
```
3. run using Docker

```bash
#Build docker image.
sudo docker build -t backend .

#Run  docker image
 sudo  docker run  -it --name wiki_backend -p  80:80 backend

```
4.run without docker imstallation

```bash
#install requirements
pip install -r requirements.txt

#run project
uvicorn main:app --reload
```



## swagger API documentation
browse http://localhost:8000/docs

## Homepage
browse http://localhost:8000
