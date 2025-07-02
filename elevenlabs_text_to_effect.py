import tempfile

import soundfile as sf
import torch
from elevenlabs import ElevenLabs


class ElevenlabsTextToEffect:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "text to effect"}),
                "api_key": ("STRING", {"default": ""}),
            },
            "optional": {
                "output_format": ("STRING", {"default": "mp3_44100_128"}),
                "duration": ("FLOAT", {
                    "min" : 0.5,
                    "max" : 22.0,
                    "step" : 0.1
                }),
                "prompt_influence": ("FLOAT", {
                    "min" : 0,
                    "max" : 1.0,
                    "default" : 0.3,
                })
            }
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)

    FUNCTION = "do_request"
    CATEGORY = "Custom"

    def do_request(self, api_key, text, duration, prompt_influence, output_format="mp3_44100_128"):
        client = ElevenLabs(api_key=api_key)
        audio_gen = client.text_to_sound_effects.convert(
            output_format=output_format,
            text=text,
            prompt_influence=prompt_influence,
            duration=duration,
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
