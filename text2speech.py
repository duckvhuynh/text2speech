import requests
import base64
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import re
import argparse

def split_text_by_punctuation(text, max_length):
    sentences = re.split(r'(?<=[.,!?;])\s+', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 > max_length:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence
        else:
            if current_chunk:
                current_chunk += ' ' + sentence
            else:
                current_chunk = sentence
                
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def text_to_speech(language, text, voice_speed="neutral"):
    MAX_LENGTH = 200
    
    chunks = split_text_by_punctuation(text, MAX_LENGTH)
    audio_segments = []
    
    for chunk in chunks:
        url = "https://translate-pa.googleapis.com/v1/textToSpeech"
        
        params = {
            "client": "gtx",
            "language": language,
            "text": chunk,
            "voice_speed": 1,
            "key": "AIzaSyDLEeFI5OtFBwYBIoK_jj5m32rZK5CkCXA"
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            audio_content = base64.b64decode(response.json()["audioContent"])
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                temp_audio.write(audio_content)
                temp_audio_path = temp_audio.name
            
            audio_segment = AudioSegment.from_file(temp_audio_path)
            
            if voice_speed == "slow":
                audio_segment = audio_segment._spawn(audio_segment.raw_data, overrides={'frame_rate': int(audio_segment.frame_rate * 0.8)})
            elif voice_speed == "fast":
                audio_segment = audio_segment._spawn(audio_segment.raw_data, overrides={'frame_rate': int(audio_segment.frame_rate * 1.3)})
            
            audio_segments.append(audio_segment)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return
    
    if audio_segments:
        combined_audio = sum(audio_segments[1:], audio_segments[0])
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_combined:
            combined_audio.export(temp_combined.name, format="mp3")
            temp_combined_path = temp_combined.name
        
        play(combined_audio)

def main():
    parser = argparse.ArgumentParser(description='Convert text to speech')
    parser.add_argument('language', type=str, help='Language code (e.g., "vi", "fr")')
    parser.add_argument('text', type=str, help='Text to convert to speech')
    parser.add_argument('--voice_speed', type=str, default="neutral", 
                        choices=["neutral", "slow", "fast"], 
                        help='Voice speed (neutral, slow, fast)')
    
    args = parser.parse_args()
    text_to_speech(args.language, args.text, args.voice_speed)

if __name__ == "__main__":
    main()