from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


KEY_FILE = Path("aes.key")

def load_key():
    with open(KEY_FILE, "rb") as f:
        key = f.read()

    if len(key) != 32:
        raise ValueError("AES-256 key must be exactly 32 bytes.")

    return key

def decrypt_image(input_path, output_path, aes):

    with open(input_path, "rb") as f:
        encrypted_data = f.read()

    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]

    image_bytes = aes.decrypt(
        nonce,
        ciphertext,
        None
    )

    with open(output_path, "wb") as f:
        f.write(image_bytes)

    print(f"Decrypted: {input_path}")
    print(f"Output:    {output_path}")

def main():
    key = load_key()
    aes = AESGCM(key)

    for image_id in range(1,11):
        input_file = Path(f"image{image_id}.png.enc")
        output_file = Path(f"image{image_id}.png")

        if not input_file.exists():
            print(f"Detected image {image_id} not found.")
            continue

        decrypt_image(input_file, output_file, aes)

if __name__ == "__main__":
    main()
