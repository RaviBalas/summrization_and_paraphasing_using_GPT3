from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import wikipediaapi as wiki
from openai import OpenAI
from fastapi import FastAPI, Request, status

from config import OPENAI_API_KEY
import schemas

app = FastAPI()
templates = Jinja2Templates(directory="./templates")

client = OpenAI(api_key=OPENAI_API_KEY)




origins = ["http://localhost:8000"]


app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)




@app.post("/summrization", responses={200: {"model": schemas.SummrizedTextResponse}})
def summarization(data: schemas.Payload):    
    data = data.dict()
    text = " ".join(data["text"].split())
    response = client.completions.create(model="gpt-3.5-turbo-instruct",
                                         prompt=f"Please summarize the following text:\n {text}",
                                         temperature=0.5,
                                         max_tokens=1024,
                                         n = 1,
                                         stop=None)        
    return JSONResponse(content={"original text":text,"summrized_text":response.choices[0].text})


@app.post("/paraphrasing", responses={200: {"model": schemas.ParaphrasedTextResponse}})
def paraphrasing(data: schemas.Payload):
    data=data.dict()
    text = " ".join(data["text"].split())    
    response = client.completions.create(model="gpt-3.5-turbo-instruct",
                                         prompt=f"Please paraphase the following text:\n {text}",
                                         temperature=0.5,
                                         max_tokens=1024,
                                         n = 1,
                                         stop=None)        
    return JSONResponse(content={"original_text":text,"paraphrasing_text":response.choices[0].text})



# @app.get("/get_sections")
@app.get("/get_sections",responses={
                            200: {"model": schemas.WikiSectionsResponse},
                            404: {"model": schemas.StatusMessage}})
def get_wiki_sections(q: str):
    wiki_wiki = wiki.Wikipedia(user_agent='wikifastapi', language='en', extract_format=wiki.ExtractFormat.WIKI)
    page=wiki_wiki.page(q)
    if page.exists():        
        return JSONResponse(content={"page":q, "sections":{i.title:i.text for i in page.sections}},status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "page not exist."},   status_code=status.HTTP_404_NOT_FOUND)
 



@app.get("/", response_class=HTMLResponse)
def index(request:Request):
    return templates.TemplateResponse("index.html",context={"request":request,
                                                            "get_wiki_sections_url": request.url_for("get_wiki_sections"),
                                                            "summrization_url": request.url_for("summarization"),
                                                            "paraphrasing_url": request.url_for("paraphrasing"),
                                                            })
