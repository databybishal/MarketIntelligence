import logging
import os 
import glob
from datetime import datetime

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

def cleanup_logs(keep=5):
    for prefix in ["runner", "scripts"]:
        files = sorted(glob.glob(os.path.join(log_dir, f"{prefix}_*.log")))
        for f in files[:-keep]:
            os.remove(f)

cleanup_logs(keep=5) # runs once when log.py is imported
today = datetime.today().strftime('%Y%m%d_%H%M%S')

formatter = logging.Formatter("%(asctime)s - %(levelname)s -%(message)s")

def _file_handler(filename):
    handler = logging.FileHandler(os.path.join(log_dir, filename))
    handler.setFormatter(formatter)
    return handler

# Runner logger
runner_logger = logging.getLogger("runner")
runner_logger.setLevel(logging.INFO)
runner_logger.addHandler(_file_handler(f"runner_{today}.log"))
runner_logger.addHandler(logging.StreamHandler())
runner_logger.propagate = False

# Script/SQL logger
script_logger = logging.getLogger("script")
script_logger.setLevel(logging.INFO)
script_logger.addHandler(_file_handler(f"scripts_{today}.log"))
script_logger.propagate = False


