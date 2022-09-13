from enum import Enum
from typing import Optional
from pydantic import BaseModel
from pydantic import Field
from fastapi import FastAPI, Query, Path
from fastapi import Body
app = FastAPI()

#Models
class HairColor(Enum):
    white ='white'
    brown = 'brow'
    black = 'black'
    blonde ='blonde'
    red = 'red'
class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=1,
        max_length=50
        )
    last_name: str= Field(
        ..., 
        min_length=1,
        max_length=50
        )
    age: int= Field(
        ..., 
        gt=0,
        le=115

        )
    hair_color:  Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

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


#Validation: Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person Id",
        description= "This is the peron id",
        gt = 0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results