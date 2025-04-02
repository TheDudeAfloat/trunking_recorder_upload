import datetime
import logging
import os

import requests

module_logger = logging.getLogger('trunk_recorder_upload.trunking_recorder_handler')

def get_call_targets(call_data: dict):
    default_target = {
        "targetid": "",
        "targetlabel": "",
        "targettag": ""
    }
    call_targets = default_target.copy()
    call_targets['targetid'] = call_data.get('talkgroup')
    call_targets['targetlabel'] = call_data.get('talkgroup_description')
    call_targets['targettag'] = call_data.get('talkgroup_tag')
    return call_targets

def get_talkgroup_info(system_name, call_data: dict):
    default_talkgroup_data = {
            "callTargets": [],
            "receiver": "",
            "receiverVCO": 0,
            "frequency": "",
            "sourceid": "",
            "sourcelabel": "",
            "sourcetag": "",
            "lcn": "",
            "voiceservice": "",
            "systemid": "",
            "systemlabel": "",
            "systemtype": "",
            "siteid": "",
            "sitelabel": "",
            "calltype": "1"
    }
    talkgroup_info = default_talkgroup_data.copy()
    talkgroup_info['callTargets'].append(get_call_targets(call_data))
    talkgroup_info['receiver'] = f"Trunk-Recorder {system_name}"
    talkgroup_info['frequency'] = call_data.get('freq')
    talkgroup_info['systemid'] = system_name
    return talkgroup_info

def get_iso_time(epoch_timestamp: int):
    dt = datetime.datetime.fromtimestamp(epoch_timestamp, datetime.timezone.utc)
    return dt.isoformat(timespec='microseconds').replace('+00:00', 'Z')

def create_meta_data(config_data, system_name: str, call_data: dict, audio_wav_path: str):
    default_metadata = {
        "apiAuthID": "",
        "apiKey": "",
        "callAudioFormat": "wav",
        "recordedCall": {
            "callText": None,
            "talkGroupInfo": {},
            "startTime": "",
            "callDuration": 0,
            "startPositionSec": "00:00:00"
        }
    }

    meta_data = default_metadata.copy()
    meta_data['apiAuthID'] = config_data.get('apiAuthID')
    meta_data['apiKey'] = config_data.get('apiKey')
    meta_data['recordedCall']['talkGroupInfo'] = get_talkgroup_info(system_name, call_data)
    meta_data['recordedCall']['startTime'] = get_iso_time(call_data.get('start_time'))
    meta_data['recordedCall']['callDuration'] = call_data.get('call_length')
    return meta_data

def upload_metadata(config_data, system_name: str, call_data: dict, audio_wav_path: str):
    metadata = create_meta_data(config_data, system_name, call_data, audio_wav_path)
    module_logger.debug(metadata)
    metadata_url_path = config_data.get('api_url') + "/api/callupload"
    try:
        headers = {'Content-Type': 'application/json'}
        r = requests.post(metadata_url_path, headers=headers, json=metadata)

        if r.status_code == 200:
            response = r.json()
            module_logger.info(f"Call metadata uploaded: {response.get('CallAudioID')}")
            return response.get("CallAudioID")
        else:
            return None
    except Exception as e:
        module_logger.error(f"Unexpected error while uploading call metadata: {e}")
        return None

def upload_audio(config_data, call_id: str, audio_wav_path: str):
    audio_url_path = config_data.get('api_url') + "/api/callaudioupload/" + call_id
    module_logger.debug(audio_url_path)
    try:
        file_size = os.path.getsize(audio_wav_path)

        headers = {'Content-Type': 'audio/wav', 'Content-Length': str(file_size)}
        with open(audio_wav_path, 'rb') as audio_file:
            r = requests.post(audio_url_path, headers=headers, data=audio_file)

        if r.status_code == 200:
            module_logger.info("Audio file Upload successful!")
        else:
            module_logger.error(f"Upload failed with status code: {r.status_code}")
            module_logger.error(f"Response: {r.text}")
    except Exception as e:
        module_logger.error(f"Unexpected error when uploading audio: {e}")
