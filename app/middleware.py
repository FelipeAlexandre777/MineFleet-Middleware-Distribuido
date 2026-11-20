from collections import Counter
from .config import DATA_DIR, CONTROLLER_IDS, QUORUM
from .controller import Controller
from .security import verify
class Middleware:
    def __init__(self):
        self.controllers = [Controller(cid, DATA_DIR/f"{cid}.db") for cid in CONTROLLER_IDS]
    def process(self, vehicle, seq, temperature):
        replies, offline, invalid = [], [], []
        for c in self.controllers:
            try:
                r = c.process(vehicle,seq,temperature)
                if verify(r["result"], c.id, r["signature"]): replies.append(r)
                else: invalid.append(c.id)
            except ConnectionError: offline.append(c.id)
        counts = Counter((r["result"]["vehicle_id"],r["result"]["sequence"],r["result"]["temperature"],r["result"]["decision"]) for r in replies)
        if not counts: return {"success":False,"message":"Nenhuma resposta válida","offline":offline,"invalid":invalid}
        winner, votes = counts.most_common(1)[0]
        if votes < QUORUM:
            return {"success":False,"message":f"Quórum não alcançado: {votes}/4","responses":replies,"offline":offline,"invalid":invalid}
        result = dict(zip(("vehicle_id","sequence","temperature","decision"),winner))
        return {"success":True,"message":f"Quórum aprovado: {votes}/4","result":result,"responses":replies,"offline":offline,"invalid":invalid,"votes":votes}
