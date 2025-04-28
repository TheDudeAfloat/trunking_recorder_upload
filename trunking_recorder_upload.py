import argparse
import os
import time

from lib.audio_file_handler import load_call_json
from lib.call_processor import process_tr_call, process_tr_call_mp3
from lib.config_handler import load_config_file
from lib.logging_handler import CustomLogger

# ─── App Metadata & Paths ─────────────────────────────────────────────────────
app_name        = "trunk_recorder_upload"
__version__     = "1.0"
root_path       = os.getcwd()
config_file     = "config.json"
config_path     = os.path.join(root_path, 'etc', config_file)
log_dir         = os.path.join(root_path, 'log')
log_file        = os.path.join(log_dir, f"{app_name}.log")

# ─── Ensure log directory exists ───────────────────────────────────────────────
os.makedirs(log_dir, exist_ok=True)

# ─── Setup Logging ─────────────────────────────────────────────────────────────
logging_instance = CustomLogger(1, app_name, log_file)
try:
    config_data = load_config_file(config_path)
    logging_instance.set_log_level(config_data["log_level"])
    logger = logging_instance.logger
    logger.info(f"{app_name} v{__version__} starting up")
except Exception as e:
    print(f"[ERROR] Unable to load config ({config_path}): {e}")
    time.sleep(5)
    exit(1)

# ─── Argument Parsing ───────────────────────────────────────────────────────────
def parse_arguments():
    parser = argparse.ArgumentParser(
        description=f"{app_name} v{__version__}: upload trunk recorder audio"
    )
    parser.add_argument(
        "-s", "--system_short_name", required=True,
        help="System Short Name."
    )
    parser.add_argument(
        "-a", "--audio_file", required=True,
        help="Path to audio file (either .wav or .mp3)."
    )
    return parser.parse_args()

# ─── Main Logic ────────────────────────────────────────────────────────────────
def main():
    args = parse_arguments()
    audio_path = args.audio_file
    root, ext = os.path.splitext(audio_path.lower())

    logger.info(f"Processing file: {audio_path}")

    # load the matching JSON
    json_path = f"{root}.json"
    call_data = load_call_json(json_path)
    if not call_data:
        logger.error(f"Failed to load call JSON: {json_path}")
        exit(1)

    # dispatch to the correct processor
    if ext == ".mp3":
        logger.debug("Detected MP3 → using process_tr_call_mp3")
        process_tr_call_mp3(
            config_data,
            args.system_short_name,
            call_data,
            audio_path
        )
    else:
        logger.debug("Assuming WAV → using process_tr_call")
        process_tr_call(
            config_data,
            args.system_short_name,
            call_data,
            audio_path
        )

if __name__ == "__main__":
    main()