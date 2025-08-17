import tempfile

import soundfile as sf
import torch
from elevenlabs import ElevenLabs


class ElevenlabsTextToSpeech:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "text to speech"}),
                "api_key": ("STRING", {"default": ""}),
                "voice_id": ("STRING", {"default": ""}),
                "model_id": ([
                 "eleven_multilingual_v2",
                 "eleven_flash_v2_5",
                 "eleven_turbo_v2_5",
                 "eleven_turbo_v2",
                 "eleven_flash_v2",
                 "eleven_english_sts_v2",
                 "eleven_multilingual_sts_v2",
                 "eleven_multilingual_v1",
                 "eleven_monolingual_v1"
                ], {"default": "eleven_multilingual_v2"}),
            },
            "optional": {
                "seed": ("STRING", {"default": ""}),
                "apply_text_normalization": (["auto", "on", "off"], {"default": "auto"}),
                "voice_settings_stability": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "voice_settings_use_speaker_boost": ("BOOLEAN", {"default": True}),
                "voice_settings_similarity_boost": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 1.0, "step": 0.01}),
                "voice_settings_style": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "voice_settings_speed": ("FLOAT", {"default": 1.0, "min": 0.5, "max": 2.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)

    CATEGORY = "Elevenlabs API integration by 奥利奥"
    FUNCTION = "execute"

    def __init__(self):
        self.elevenlabs = None

    def setup_elevenlabs(self, api_key):
        if self.elevenlabs is None:
            self.elevenlabs = ElevenLabs(api_key=api_key)

    def convert_text_to_voice(self, text, api_key, voice_id, model_id, seed, apply_text_normalization,
                             stability, use_speaker_boost, similarity_boost, style, speed):
        self.setup_elevenlabs(api_key)
        voice_settings = {
            "stability": stability,
            "use_speaker_boost": use_speaker_boost,
            "similarity_boost": similarity_boost,
            "style": style,
            "speed": speed
        }
        audio_gen = self.elevenlabs.text_to_speech.convert(
            voice_id=voice_id,
            output_format="mp3_44100_128",
            text=text,
            model_id=model_id,
            seed=seed if seed else None,
            apply_text_normalization=apply_text_normalization if apply_text_normalization != "auto" else None,
            voice_settings=voice_settings
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

    def execute(self, text, api_key, voice_id, model_id, seed, apply_text_normalization,
                voice_settings_stability, voice_settings_use_speaker_boost,
                voice_settings_similarity_boost, voice_settings_style, voice_settings_speed):
        return self.convert_text_to_voice(
            text, api_key, voice_id, model_id, seed, apply_text_normalization,
            voice_settings_stability, voice_settings_use_speaker_boost,
            voice_settings_similarity_boost, voice_settings_style, voice_settings_speed
        )
