from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Query, Path
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


#validaciones query parameters

@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters" 
        ), 
    age: str = Query(
        ...,
        titel="Person age",
        description="this is the person's name. It's required"
        )
    ):
    return {'name':name, 'age':age}

#validations path parameters
#if there are 2 methos with the same name in python, the last one will be the method that will execute
@app.get('/person/details/{person_id}')
def show_person(
    person_id: int = Path(..., gt = 0)
):
    return {person_id: 'It exists!'}