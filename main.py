from lib2to3.pytree import Node
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Body
app = FastAPI()

#Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] 
    is_married: Optional[bool] 

#decorador para nombrar una funcion para un path
@app.get('/')
def home():
    return {'hello': 'World'}



#Request and response body
@app.post('/person/new')
def create_person(person: Person = Body()):
    return person


