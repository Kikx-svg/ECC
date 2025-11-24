#!/usr/bin/env python3
import sys, random, base64, hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

#Paramètres de la courbe
A, B, P, G = 35, 3, 101, (2, 9)

#Fonctions ECC
def inv(a): return pow(a, -1, P)

def add(p, q):
    if not p: return q
    if not q: return p
    x1, y1 = p
    x2, y2 = q
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    s = ((3*x1*x1 + A) * inv(2*y1) if p == q else (y2 - y1) * inv((x2 - x1) % P)) % P
    x3 = (s*s - x1 - x2) % P
    y3 = (s*(x1 - x3) - y1) % P
    return (x3, y3)

def mul(k, p):
    r = None
    while k:
        if k & 1: r = add(r, p)
        p, k = add(p, p), k >> 1
    return r

#Clés
def genkey(n=1000):
    k = random.randint(1, n)
    Q = mul(k, G)
    open("monECC.priv", "w", encoding="utf-8").write(base64.b64encode(str(k).encode()).decode())
    open("monECC.pub", "w", encoding="utf-8").write(base64.b64encode(f"{Q[0]};{Q[1]}".encode()).decode())
    print(" Clés générées : monECC.priv / monECC.pub")

def loadkey(f, priv=False):
    try:
        data = open(f, "r", encoding="utf-8").read().strip()
        data = base64.b64decode(data).decode("utf-8", errors="ignore")
        return int(data) if priv else tuple(map(int, data.split(';')))
    except Exception as e:
        raise ValueError(f"Erreur de lecture clé {f}: {e}")

#Hash secret partagé
def derive(S):
    h = hashlib.sha256(f"{S[0]}{S[1]}".encode()).digest()
    return h[:16], h[16:32]

# AES
def pad(b):
    p = padding.PKCS7(128).padder()
    return p.update(b) + p.finalize()

def unpad(b):
    u = padding.PKCS7(128).unpadder()
    return u.update(b) + u.finalize()

#Chiffrement / Déchiffrement
def crypt(pub, msg):
    Q = loadkey(pub)
    k = random.randint(1, 1000)
    R, S = mul(k, G), mul(k, Q)
    iv, key = derive(S)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    enc = cipher.encryptor().update(pad(msg.encode())) + cipher.encryptor().finalize()
    print(f"{R[0]};{R[1]}:{base64.b64encode(enc).decode()}")

def decrypt(priv, data):
    k = loadkey(priv, True)
    (x, y), blob = map(int, data.split(':')[0].split(';')), base64.b64decode(data.split(':')[1])
    S = mul(k, (x, y))
    iv, key = derive(S)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    dec = cipher.decryptor().update(blob) + cipher.decryptor().finalize()
    print(unpad(dec).decode())

# --- Aide
def help():
    print("""
==============================
     MonECC - Aide (Help)
==============================

Commandes disponibles :
  keygen
      ➤ Génère une paire de clés (monECC.pub / monECC.priv)
      ➤ Exemple :
          python script-ecc.py keygen

  crypt <fichier_pub> "<message>"
      ➤ Chiffre un message avec la clé publique
      ➤ Exemple :
          python script-ecc.py crypt monECC.pub "Bonjour le monde"

  decrypt <fichier_priv> "<texte_chiffré>"
      ➤ Déchiffre un message avec la clé privée
      ➤ Exemple :
          python script-ecc.py decrypt monECC.priv "25;78:SGVsbG8gV29ybGQ="

  help
      ➤ Affiche ce guide

--------------------------------
  Auteur : Killian Deleval
  Cours : Sécurité / ECC - ESGI
--------------------------------
""")

#CLI
if len(sys.argv) < 2:
    help()
else:
    cmd = sys.argv[1]
    if cmd == "keygen": genkey()
    elif cmd == "crypt" and len(sys.argv) > 3: crypt(sys.argv[2], sys.argv[3])
    elif cmd == "decrypt" and len(sys.argv) > 3: decrypt(sys.argv[2], sys.argv[3])
    elif cmd == "help": help()
    else: print("Commande ou argument manquant. Tapez : python script-ecc.py help")
