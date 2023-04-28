import fastapi
import pymysql
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel



def conecta():
    cnx = pymysql.connect(
        user="cafi@projetocelso", password="senai@mange2023", host="projetocelso.mariadb.database.azure.com", port=3306,
        database="projeto_rfid"
    )
    cursor = cnx.cursor()

    return cursor, cnx


app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get")
def get():
    cursor, cnx = conecta()
    cursor.execute("SELECT * FROM cadastro")
    cadastro = cursor.fetchall()
    cnx.close()
    cursor.close()
    return {"message": cadastro}


class Datapost(BaseModel):
    nome: str
    id: str

class Datadelete(BaseModel):
    nome: str

@app.post("/post")
def post(data: Datapost):
    cursor, cnx = conecta()
    cursor.execute(f"INSERT INTO cadastro(nome, id) values (%s, %s)", (data.nome, data.id))
    cnx.commit()
    cnx.close()
    cursor.close()
    return {"nome": data.nome, "id": data.id}


@app.post("/delete")
def delete(data: Datadelete):
    cursor, cnx = conecta()
    cursor.execute(f"DELETE FROM cadastro WHERE nome = '{data.nome}'")
    cnx.commit()
    cnx.close()
    cursor.close()
    return {'message': "Usuário deletado"}


if __name__ ==  '__main__':
   import uvicorn
   uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
