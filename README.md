You probably want the main branch of this from https://github.com/TheGreatCodeholio/trunking_recorder_upload/

I have added a few changes

1. I changed the default CallText parameter so that if you have Transcription setup it will transcribe the audio correctly
2. I added logic to the metadata creation so that it will upload the list of Unit IDs and Unit Tags to Trunking Recorder. TRing doesn't handle multiple unit IDs correctly so it is a bit of a hack but it does show them correctly. However after talking to Jason from TRing it may mess with searching by Unit IDs which isn't available anyway so may not be a big deal. But be warned, it is a hack
3. I have added support for MP3. If you pass an MP3 file in, it will detect the extension and properly upload an MP3 instead of a WAV file. Makes a huge difference for capacity on the TRing server. You will first need to encode the MP3 and pass the MP3 filename to the script. If you pass a WAV it will work as expected in the upstream.   
