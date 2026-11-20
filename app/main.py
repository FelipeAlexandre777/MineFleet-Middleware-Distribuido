from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .middleware import Middleware
app = FastAPI(title="MineFleet - Middleware Distribuído", version="1.0")
system = Middleware()
class Telemetry(BaseModel):
    vehicle_id: str = "CAM-042"
    sequence: int = Field(default=1, ge=1)
    temperature: float = Field(default=85, ge=-50, le=200)
class Change(BaseModel):
    online: bool | None = None
    divergent: bool | None = None
@app.get("/")
def home(): return {"projeto":"MineFleet","docs":"/docs"}
@app.get("/controllers")
def status():
    return {"quorum_required":3,"controllers":[{"id":c.id,"online":c.online,"divergent":c.divergent,"database":c.db_path.name} for c in system.controllers]}
@app.post("/telemetry")
def telemetry(data:Telemetry):
    result=system.process(data.vehicle_id,data.sequence,data.temperature)
    if result["success"]:
        result["actuator_action"]="Alerta simulado" if result["result"]["decision"]=="ALERTA" else "Nenhuma ação necessária"
    return result
@app.post("/controllers/{controller_id}/simulate")
def simulate(controller_id:str, change:Change):
    c=next((x for x in system.controllers if x.id==controller_id),None)
    if c is None: raise HTTPException(404,"Controlador não encontrado")
    if change.online is not None: c.online=change.online
    if change.divergent is not None: c.divergent=change.divergent
    return {"message":"Atualizado","id":c.id,"online":c.online,"divergent":c.divergent}
@app.post("/controllers/restore")
def restore():
    for c in system.controllers: c.online=True; c.divergent=False
    return {"message":"Todos restaurados"}
