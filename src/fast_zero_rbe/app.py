from http import HTTPStatus

from fastapi import FastAPI

from fast_zero_rbe.routers import auth, users
from fast_zero_rbe.schemas import Message

app = FastAPI(title='Minha API BALA!')

app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}
