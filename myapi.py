from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

names = ['yoyo', 'nono', 'mummu']
unions = ['Altia', 'Strattia', 'Cumllia']
exports = ['Milo', 'Paper', 'Cocoa']
nations_ = dict(zip(names, unions, exports))


nations = {
    0: {
        "name": "Yoyo",
        "union": "Altia",
        "primary_export": "Cocoa"
    },
    1: {
        "name": "Nono",
        "union": "Strattia",
        "primary_export": "Paper"
    },
    2: {
        "name": "Moyo",
        "union": "Cumllia",
        "primary_export": "Milo"
    }
}


class Nation(BaseModel):
    name: str
    union: str
    primary_export: str


class UpdateNation(BaseModel):
    name: Optional[str] = None
    union: Optional[str] = None
    primary_export: Optional[str] = None


@app.get("/")
def index():
    return {'name': 'api data set for the Nations of One project'}


@app.get("/{tokenID}")
def get_nation(tokenID: int = Path(None, description="The tokenID of the nation")):
    return nations[tokenID]
