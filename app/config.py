from pathlib import Path
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
CONTROLLER_IDS = [f"controlador-{i}" for i in range(1, 5)]
QUORUM = 3
SECRET = "segredo-didatico-minefleet"
