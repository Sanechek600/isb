import os
import argparse
import logging
import json

from cryptography.hazmat.primitives import serialization

from asymm_enc import AsymmEnc
from symm_enc import SymmEnc
from util import HelpFunc


logging.basicConfig(level=logging.INFO)


def main(operation):
    config_path = "D:\\Study\\OSB\\isb\\lab_3\\settings.json"
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        return
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from the configuration file: {config_path}")
        return
    except Exception as e:
        logging.error(f"Unexpected error reading configuration file: {e}")
        return
    if operation:
        config["operation"] = operation
    match config["operation"]:
        case "generate_rsa_keys":
            asymm_crypt = AsymmEnc()
            private_key, public_key = asymm_crypt.generate_key_pair()
            private_key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            HelpFunc.write_to_file(config["private_key_path"], private_key_pem)
            HelpFunc.write_to_file(config["public_key_path"], public_key_pem)
            logging.info("RSA key pair generated and saved.")

        case "generate_chacha_key":
            symm_enc = SymmEnc()
            chacha_key = symm_enc.generate_noncence()
            asymm_crypt = AsymmEnc()
            public_key_pem = HelpFunc.read_file(config["public_key_path"])
            if not public_key_pem:
                logging.error("Public key file is empty or not found.")
            public_key = serialization.load_pem_public_key(public_key_pem)
            encrypted_chacha_key = asymm_crypt.encrypt_with_public_key(public_key, chacha_key[0])
            HelpFunc.write_to_file(config["encrypted_chacha_key_path"], encrypted_chacha_key)
            HelpFunc.write_to_file(config["chacha_nonce_path"], chacha_key[1])
            logging.info("ChaCha20 key generated and saved.")

        case "encrypt_text":
            try:
                private_key_pem = HelpFunc.read_file(config["private_key_path"])
                if not private_key_pem:
                    logging.error("Private key file is empty or not found.")
                private_key = serialization.load_pem_private_key(private_key_pem, password=None)
                encrypted_chacha_key = HelpFunc.read_file(config["encrypted_chacha_key_path"])
                if not encrypted_chacha_key:
                    logging.error("Encrypted ChaCha20 key file is empty or not found.")
                chacha_nonce = HelpFunc.read_file(config["chacha_nonce_path"])
                if not chacha_nonce:
                    logging.error("ChaCha20 nonce file is empty or not found.")
                asymm_crypt = AsymmEnc()
                decrypted_chacha_key = asymm_crypt.decrypt_with_private_key(private_key, encrypted_chacha_key)
                text_to_encrypt = HelpFunc.read_file(config["text_path"])
                symm_enc = SymmEnc()
                symm_enc.encrypt_text(tuple([decrypted_chacha_key, chacha_nonce]), config["encrypted_text_path"], text_to_encrypt)
                logging.info("Text encrypted and saved.")
            except Exception as e:
                logging.error(f"Error during text encryption: {e}")

        case "decrypt_text":
            try:
                encrypted_chacha_key = HelpFunc.read_file(config["encrypted_chacha_key_path"])
                if not encrypted_chacha_key:
                    logging.error("Encrypted ChaCha20 key file is empty or not found.")
                chacha_nonce = HelpFunc.read_file(config["chacha_nonce_path"])
                if not chacha_nonce:
                    logging.error("ChaCha20 nonce file is empty or not found.")
                private_key_pem = HelpFunc.read_file(config["private_key_path"])
                if not private_key_pem:
                    logging.error("Private key file is empty or not found.")
                private_key = serialization.load_pem_private_key(private_key_pem, password=None)
                asymm_crypt = AsymmEnc()
                decrypted_chacha_key = asymm_crypt.decrypt_with_private_key(private_key, encrypted_chacha_key)
                symm_enc = SymmEnc()
                symm_enc.decrypt_text(tuple([decrypted_chacha_key, chacha_nonce]), config["decrypted_text_path"], config["encrypted_text_path"])
                logging.info("Text decrypted and saved.")
            except Exception as e:
                logging.error(f"Error during text decryption: {e}")

        case _:
            logging.error(f"Unknown operation: {config['operation']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some cryptographic operations.")
    parser.add_argument("--operation", type=str, default= "decrypt_text", help="Operation to perform (overrides the operation in the config file).")
    args = parser.parse_args()
    main(args.operation)