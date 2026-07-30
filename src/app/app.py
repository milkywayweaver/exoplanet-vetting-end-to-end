from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(SCRIPT_DIR))
from inference import predict

import mlflow
MODEL_URI = SCRIPT_DIR/'artifacts/'
model = mlflow.pyfunc.load_model(
    model_uri=str(MODEL_URI),
    model_config={'skops_trusted_types':['modules.aslt.ASLT']}
)

class TESSData(BaseModel):
    ra: float
    dec: float
    st_pmra: float
    st_pmdec: float
    pl_tranmid: float
    pl_orbper: float
    pl_trandurh: float
    pl_trandep: float
    pl_rade: float
    pl_insol: float
    pl_eqt: float
    st_tmag: float
    st_dist: float
    st_teff: float
    st_logg: float
    st_rad: float
    
app = FastAPI()

APP_DIR = Path(__file__).resolve().parent
app.mount('/static',StaticFiles(directory=APP_DIR/'static'),name='static')

@app.get('/',response_class=FileResponse)
async def index():
    return FileResponse(APP_DIR/'index.html')

@app.post('/data/',status_code=201)
async def receive_data(data:TESSData):
    data_dict = data.model_dump()
    print(f'DATA :{data_dict} -------------------------------------')
    
    preds = predict(data_dict,model)
    return preds