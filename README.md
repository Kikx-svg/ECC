# 🧩 Utilisation du script ECC

Ce script permet de chiffrer et déchiffrer des messages à l’aide d’un système basé sur les **courbes elliptiques (ECC)**.

---

## ⚙️ Installation

1. Avoir Python installé sur ton ordinateur.  
2. Installer la bibliothèque nécessaire
   pip install cryptography

1. Générer une paire de clés
python script-ecc.py keygen

2. Chiffrer un message
python script-ecc.py crypt monECC.pub "Le code c'est difficile"

   Le programme affiche un texte chiffré du type : 25;78:SGVsbG8gV29ybGQ=

3. Déchiffrer un message
python script-ecc.py decrypt monECC.priv "25;78:SGVsbG8gV29ybGQ="

Résultat : Le code c'est difficile

Afficher l’aide
python script-ecc.py help

Killian Deleval
Projet cours de Sécurité / ECC - ESGI


