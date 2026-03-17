import os
from fastapi import FastAPI, HTTPException, Request
from argon2 import PasswordHasher
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

app = FastAPI()
ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=1) 

users_db = {
    "azamat_admin": {
        "hash": ph.hash("Azamat@2026!Secure"), 
        "role": "admin"
    },
    "talaba_user": {
        "hash": ph.hash("OddiyParol123!"),
        "role": "user"
    }
}


@app.get("/")
async def home(request: Request):
    return {"message": "Xavfsiz tizimga xush kelibsiz, Azamat!"}

@app.get("/admin")
async def admin_page(role: str):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Sizda admin huquqi yo'q!")
    return {"content": "Bu faqat admin (Azamat) uchun maxfiy sahifa."}

@app.get("/encrypt")
async def encrypt_data(text: str):
    key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12) 
    ciphertext = aesgcm.encrypt(nonce, text.encode(), None)
    
    return {
        "original": text,
        "shifrlangan_hex": ciphertext.hex(),
        "nonce_hex": nonce.hex(),
        "key_hex": key.hex()
    }