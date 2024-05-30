import json
import os

from typing import Dict
from enum import Enum


ALPH_LOWER = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALPH_UPPER = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


class Mode(Enum):
    ENCRYPT = 1
    DECRYPT = 2


def save_key(filename: str, key: dict) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(key, file, ensure_ascii=False)


def save_text(filename: str, text: str) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)


def generate_key(shift: int, filename: str) -> Dict[str, str]:
    """
    Creates a .json file with a generated key

    Args:
        shift (int): shift value for caesar cypher
        filename (str): name of the .json file to save the key in 

    Returns:
        Dictionary with the key
    """
    shifted_lower = ALPH_LOWER[shift % len(ALPH_LOWER):] + ALPH_LOWER[:shift % len(ALPH_LOWER)]
    shifted_upper = ALPH_UPPER[shift % len(ALPH_UPPER):] + ALPH_UPPER[:shift % len(ALPH_UPPER)]
    key = dict(zip(ALPH_LOWER, shifted_lower)) | dict(zip(ALPH_UPPER, shifted_upper))

    save_key(filename, key)
    return key


def process(in_file: str, out_file: str, shift: int, key_file: str, mode: Mode) -> None:
    """
    Creates a .txt file with processed text and a .json file with the key
    Ignores non-alphabetic characters

    Args:
        in_file (str): name of the input file
        out_file (str): name of the output file
        shift (int): shift value for caesar cypher
        key_file (str): name of the .json file to save the key in
        mode (Mode): ENCRYPT or DECRYPT 

    Throws:
        FileNotFoundError: if the input file is not found
    """
    try:
        with open(in_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print("Input file not found. Please check the file path.")
    
    key = generate_key(shift, key_file)

    match mode:
        case Mode.ENCRYPT:
            processed_text = ''.join(key.get(char, char) if char.isalpha() else char for char in text)
        case Mode.DECRYPT:
            reversed_key = {v: k for k, v in key.items()} 
            processed_text = ''.join(reversed_key.get(char, char) if char.isalpha() else char for char in text)

    save_text(out_file, processed_text)


if __name__ == '__main__':
    try:
        with open(os.path.join("lab_1", "task1", "settings.json"), 'r', encoding='utf-8') as json_file:
            config = json.load(json_file)

        process(config["input_file"], config["encrypted_file"], config["shift"], config["key"], Mode.ENCRYPT)
        process(config["encrypted_file"], config["decrypted_file"], config["shift"], config["key"], Mode.DECRYPT)

    except FileNotFoundError:
        print("Config file not found. Please ensure the config file exists in the specified path.")
    except json.JSONDecodeError:
        print("Config file is not valid JSON.")
    except KeyError as e:
        print(f"Key {e} not found in the config file.")