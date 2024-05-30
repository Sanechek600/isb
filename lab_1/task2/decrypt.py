import json
import os
from lab_1.task1.encrypt import save_text


def load_settings(path: str) -> any:
    with open(path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def decrypt_text(input_file, key_file, output_file) -> None:

    """
    Creates an output_file with the text from input_file decrypted via key_file 

    Args:
        text_file (str): File containing the encrypted text
        dictionary_file (str): JSON file containing the dictionary for decryption
        output_file (str): File to which the decrypted text will be saved
    """

    try:
        key = load_settings(key_file)

        decrypted_text = ""
        key = {u: v for v, u in key.items()}

        with open(input_file, 'r', encoding='utf-8') as f:
            encrypted_text = f.read()
            for char in encrypted_text:
                decrypted_char = key.get(char, char)
                decrypted_text += decrypted_char

        save_text(output_file, decrypted_text)

        print("Decrypted text saved to: ", output_file)

    except FileNotFoundError:
        print("File not found. Please check the file paths.")
    except Exception as e:
        print("An error occurred:", e)


if __name__ == '__main__':
    try:
        config = load_settings(os.path.join("lab_1","task2","settings.json"))
        decrypt_text(config["text_file"], config["dictionary_file"], config["output_file"])

    except FileNotFoundError:
        print("Config file not found. Please ensure the config file exists in the specified path.")
    except json.JSONDecodeError:
        print("Config file is not valid JSON.")
    except KeyError as e:
        print(f"Key {e} not found in the config file.")
    except Exception as e:
        print("An error occurred:", e)