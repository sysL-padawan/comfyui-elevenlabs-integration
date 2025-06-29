import tempfile

import soundfile as sf
import torch
from elevenlabs import ElevenLabs


class ElevenlabsRequestNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "text to speech"}),
                "api_key": ("STRING", {"default": ""}),
                "voice_id": ("STRING", {"default": ""}),
                "model_id": ("STRING", {"default": "eleven_multilingual_v2"}),
            },
            "optional": {
                "output_format": ("STRING", {"default": "mp3_44100_128"}),
            }
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)

    FUNCTION = "do_request"
    CATEGORY = "Custom"

    def do_request(self, api_key, text, voice_id, model_id, output_format="mp3_44100_128"):
        client = ElevenLabs(api_key=api_key)
        audio_gen = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format=output_format,
            text=text,
            model_id=model_id,
        )

        audio_bytes = b"".join(audio_gen)

        with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp_mp3:
            tmp_mp3.write(audio_bytes)
            tmp_mp3.flush()
            data, sample_rate = sf.read(tmp_mp3.name, dtype='float32')

        if data.ndim == 1:
            audio = data
        else:
            audio = data.mean(axis=1)
        audio_tensor = torch.from_numpy(audio).unsqueeze(0).unsqueeze(0).float()
        return ({"waveform": audio_tensor, "sample_rate": sample_rate},)