#!/usr/bin/env python

from typing import Dict, Tuple
from core_system.TTS.aws_polly import AWSPolly
from core_system.TTS.engine_wrapper import TTSEngine


TTSProviders = {
    "AWSPolly": AWSPolly,
}


def save_text_to_mp3(reddit_obj,username,voice="AWSPolly") -> Tuple[int, int]:  
    text_to_mp3 = TTSEngine(get_case_insensitive_key_value(TTSProviders, voice), reddit_obj,path=username)
    return text_to_mp3.run()


def get_case_insensitive_key_value(input_dict, key):
    return next(
        (value for dict_key, value in input_dict.items() if dict_key.lower() == key.lower()),
        None,
    )
