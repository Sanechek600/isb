import os, struct
import logging

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import (Cipher, 
                                                    algorithms)
from util import HelpFunc

KEY_LENGTH = 32

logging.basicConfig(level=logging.INFO)

class SymmEnc:
    """
    Symmetric Cryptography class for encryption and decryption.

    Methods:
        generate_key(): Generates a symmetric key of specified length.
        encrypt_text(sym_key, encrypted_text_path, text): Encrypts the given text using the symmetric key and saves the encrypted text to a file.
        decrypt_text(sym_key, decrypted_text_path, ciphertext): Decrypts the given ciphertext using the symmetric key and saves the decrypted text to a file.
    """

    def generate_noncence(self) -> tuple:
        """
        Generates a symmetric key of the specified length and a nonce. I don't know what a nonce is, hence the name.

        Returns:
            bytes: The generated symmetric key.
        """
        try:
            nonce = os.urandom(8)
            counter = 0
            full_nonce = struct.pack("<Q", counter) + nonce
            return tuple([os.urandom(KEY_LENGTH), full_nonce])
        except Exception as e:
            logging.error(f"Failed to generate key: {e}")
    

    def encrypt_text(self, key_nonce: tuple, encrypted_text_path: str, text: str) -> None:
        """
        Encrypts the given text using the symmetric key and saves the resulting text to a file.

        Args:
            key_nonce (tuple of bytes): The symmetric key and the nonce.
            encrypted_text_path (bytes): The path where the encrypted text will be saved.
            text (bytes): The text to be encrypted.
        """
        try:
            cipher = Cipher(algorithms.ChaCha20(key_nonce[0], key_nonce[1]), mode=None)
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(text) + encryptor.finalize()

            HelpFunc.write_to_file(encrypted_text_path, ciphertext[16:])
        except Exception as e:
            logging.error(f"Failed to encrypt text: {e}")
    

    def decrypt_text(self, key_nonce: tuple, decrypted_text_path: str, ciphertext_path: str) -> None:
        """
        Decrypts the given rtext using the symmetric key and saves the decrypted text into a file.

        Args:
            key_nonce (tuple of bytes): The symmetric key and the nonce.
            decrypted_text_path (str): The path where the decrypted text will be saved.
            ciphertext_path (str): The ciphertext to be decrypted.
        """
        try:
            ciphertext = HelpFunc.read_file(ciphertext_path)

            cipher = Cipher(algorithms.ChaCha20(key_nonce[0], key_nonce[1]), mode=None)
            decryptor = cipher.decryptor()

            plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            with open(decrypted_text_path, "wb") as decrypted_text_file:
                decrypted_text_file.write(plaintext)
        except Exception as e:
            logging.error(f"Failed to decrypt text: {e}")