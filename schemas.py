from pydantic import BaseModel


class Payload(BaseModel):
    text: str



class StatusMessage(BaseModel):
    message: str
    
    
class SummrizedTextResponse(BaseModel):    
    original_text: str
    summrized_text: str
    

class WikiSectionsResponse(BaseModel):    
    page: str
    sections: dict
    
    
class ParaphrasedTextResponse(BaseModel):
    original_text: str
    paraphrasing_text: str