from fastapi import FastAPI

app = FastAPI()

#decorador para nombrar una funcion para un path
@app.get('/')
def home():
    return {'hello': 'World'}
