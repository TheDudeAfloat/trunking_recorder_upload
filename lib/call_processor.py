import logging

from lib.trunking_recorder_handler import upload_metadata, upload_audio

module_logger = logging.getLogger('trunk_recorder_upload.call_processor')


def process_tr_call(config_data, system_name: str, call_data: dict, audio_wav_path: str):
    call_id = upload_metadata(config_data, system_name, call_data, audio_wav_path)
    upload_audio(config_data, call_id, audio_wav_path)

def process_tr_call_mp3(config_data, system_name: str, call_data: dict, audio_mp3_path: str):
    call_id = upload_metadata(config_data, system_name, call_data, audio_mp3_path)
    upload_audio(config_data, call_id, audio_mp3_path)