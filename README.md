usage: text2speech.py [-h] [--voice_speed {neutral,slow,fast}] [--export] language text

Convert text to speech

positional arguments:
  language              Language code (e.g., "vi", "fr")
  text                  Text to convert to speech

options:
  -h, --help            show this help message and exit
  --voice_speed {neutral,slow,fast}
                        Voice speed (neutral, slow, fast)
  --export              Export the audio to an MP3 file in output folder
