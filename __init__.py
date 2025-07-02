from .elevenlabs_text_to_effect import ElevenlabsTextToEffect
from .elevenlabs_text_to_voice import ElevenlabsTextToVoice

NODE_CLASS_MAPPINGS = {
    "ElevenlabsTextToVoice": ElevenlabsTextToVoice,
    "ElevenlabsTextToEffect": ElevenlabsTextToEffect,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Elevenlabs text to voice": "Create your voice with Elevenlabs API",
    "Elevenlabs text to effect": "Create your effect with Elevenlabs API",
}
