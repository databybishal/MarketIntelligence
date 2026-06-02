import logging
import os 
import glob
from datetime import datetime

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

def cleanup_logs(keep=5):
    for prefix in ["runner", "scripts", "ingestion", "silver_layer_transformation", "gold_layer_transformation"]:
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

# ingestion logger
ingestion_logger = logging.getLogger("ingestion")
ingestion_logger.setLevel(logging.INFO)
ingestion_logger.addHandler(_file_handler(f"ingestion_{today}.log"))
ingestion_logger.addHandler(logging.StreamHandler())
ingestion_logger.propagate = False

#transformation logger
silver_transformation_logger = logging.getLogger("silver_layer_transformation")
silver_transformation_logger.setLevel(logging.INFO)
silver_transformation_logger.addHandler(_file_handler(f"silver_transformation_{today}.log"))
silver_transformation_logger.addHandler(logging.StreamHandler())
silver_transformation_logger.propagate = False


#transformation logger
gold_layer_transformation_logger = logging.getLogger("gold_layer_transformation")
gold_layer_transformation_logger.setLevel(logging.INFO)
gold_layer_transformation_logger.addHandler(_file_handler(f"gold_layer_transformation_{today}.log"))
gold_layer_transformation_logger.addHandler(logging.StreamHandler())
gold_layer_transformation_logger.propagate = False

#
