from enum import Enum
from typing import Optional
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from fastapi import FastAPI, Query, Path, Form, Header, Cookie, UploadFile, File
from fastapi import Body
from fastapi import status
from fastapi import HTTPException
app = FastAPI()

#Models
class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example='aaaa')
    message: str = Field(default='Login Succesfully')


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

class PersonBase(BaseModel):
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
    

class Person(PersonBase):
    password: str = Field(..., min_length=8)

class PersonOut(PersonBase):
    pass
    
#decorador para nombrar una funcion para un path
@app.get(
    path='/', 
    status_code=status.HTTP_200_OK
    )
def home():
    return {'hello': 'World'}



#Request and response body
@app.post(
    path='/person/new',
     response_model=PersonOut,
     status_code=status.HTTP_201_CREATED
     )
def create_person(person: Person = Body()):
    return person


#validaciones query parameters

@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK
    )
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
persons = [1,2,3,4,5]
@app.get(
    path='/person/details/{person_id}',
    status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(..., gt = 0)
):
    if not person_id in persons:
        raise( 
            HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This person doesn't exist!"
                )
            )
            
    return {person_id: 'It exists!'}


#Validation: Request Body
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK
    )
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
#Forms
@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
    
)
def login(username: str = Form(...), passowrd: str = Form(...)):
    return LoginOut(username=username)


# Cookies and Headers
@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK
)
def contact(first_name: str = Form(
    ...,
    max_length=20,
    min_length=1
    ),
    last_name: str = Form(
    ...,
    max_length=20,
    min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
    ):
    return user_agent

#files
@app.post(
    path='/post-image'
    )
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }
