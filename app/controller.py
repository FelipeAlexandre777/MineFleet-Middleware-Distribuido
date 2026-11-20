import sqlite3
from .security import sign
class Controller:
    def __init__(self, controller_id, db_path):
        self.id, self.db_path = controller_id, db_path
        self.online, self.divergent = True, False
        with sqlite3.connect(self.db_path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS telemetria (veiculo TEXT, seq INTEGER, temperatura REAL, decisao TEXT, PRIMARY KEY(veiculo,seq))")
    def process(self, vehicle, seq, temperature):
        if not self.online: raise ConnectionError(self.id)
        decision = "ALERTA" if temperature >= 80 else "NORMAL"
        if self.divergent: decision = "NORMAL" if decision == "ALERTA" else "ALERTA"
        with sqlite3.connect(self.db_path) as db:
            db.execute("INSERT OR REPLACE INTO telemetria VALUES (?,?,?,?)", (vehicle,seq,temperature,decision))
        result = {"vehicle_id":vehicle,"sequence":seq,"temperature":temperature,"decision":decision}
        return {"controller_id":self.id,"result":result,"signature":sign(result,self.id)}
