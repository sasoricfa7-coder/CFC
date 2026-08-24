![Projet](https://img.shields.io/badge/Projet-CFC-blueviolet?style=for-the-badge) ![Statut](https://img.shields.io/badge/Statut-%C3%A0%20coder-yellow?style=for-the-badge) ![Langage](https://img.shields.io/badge/Langage-Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Licence](https://img.shields.io/badge/Licence-AGPLv3%2B-green?style=for-the-badge)

# 🐍 FICHE — Prototype Python de la logique du Coffre-Fort CFC

> 🎯 **Objectif** : valider la logique métier du coffre-fort en Python pur, sans blockchain, sans dépendance externe — avant toute traduction en Solidity.

---

## 📦 Dépendances

![Aucune](https://img.shields.io/badge/Dépendances-Aucune-success?style=flat-square)

Python pur, testable directement en console. Rien à installer.

---

## 🧱 Structure de données

```python
class Verrou:
    def __init__(self, proprietaire, montant, temps_deverrouillage):
        self.proprietaire = proprietaire
        self.montant = montant
        self.temps_deverrouillage = temps_deverrouillage
        self.retire = False
```

---

## 🏗️ Classe principale

```python
class CoffreFortCFC:
    POINTS_BASE_FRAIS = 10        # 0.1% = 10 / 10000
    DUREE_MIN_VERROU = 86400      # 1 jour en secondes

    def __init__(self, destinataire_frais: str):
        self.destinataire_frais = destinataire_frais
        self.verrous = {}
        self.prochain_id_verrou = 0
```

---

## 🔒 Fonction 1 — `verrouiller(proprietaire, montant, duree_secondes, temps_actuel)`

| Étape | Comportement |
|---|---|
| 1️⃣ | Si `montant <= 0` → 🔴 lève `ValueError("Montant nul")` |
| 2️⃣ | Si `duree_secondes < DUREE_MIN_VERROU` → 🔴 lève `ValueError("Durée trop courte")` |
| 3️⃣ | Crée un `Verrou(proprietaire, montant, temps_actuel + duree_secondes)` |
| 4️⃣ | Stocke dans `self.verrous[self.prochain_id_verrou]`, incrémente `prochain_id_verrou` |
| 5️⃣ | 🟢 Retourne `id_verrou` |

> 💡 **Note technique** : `temps_actuel` est un paramètre, pas `time.time()` interne — ça permet de tester "et si on est 6 mois plus tard" sans attendre 6 mois réels.

---

## ⏳ Fonction 2 — `prolonger_verrou(id_verrou, proprietaire, secondes_supplementaires)`

| Étape | Comportement |
|---|---|
| 1️⃣ | Si `id_verrou` n'existe pas → 🔴 lève `KeyError` |
| 2️⃣ | Si `proprietaire` incorrect → 🔴 lève `PermissionError("Pas le propriétaire")` |
| 3️⃣ | Si déjà `retire` → 🔴 lève `ValueError("Déjà retiré")` |
| 4️⃣ | Si `secondes_supplementaires <= 0` → 🔴 lève `ValueError` |
| 5️⃣ | 🟢 `temps_deverrouillage += secondes_supplementaires` |

> ✅ **Aucun frais prélevé ici** — c'est le point clé de la logique CFC.

---

## 🔓 Fonction 3 — `deverrouiller(id_verrou, proprietaire, temps_actuel)`

| Étape | Comportement |
|---|---|
| 1️⃣ | Vérifie le propriétaire |
| 2️⃣ | Vérifie `not retire` |
| 3️⃣ | Si `temps_actuel < temps_deverrouillage` → 🔴 lève `ValueError("Encore verrouillé")` |
| 4️⃣ | ⚠️ Marque `retire = True` **avant** tout calcul (pattern vérifier-modifier-transférer) |
| 5️⃣ | Calcule `frais = montant * POINTS_BASE_FRAIS // 10000` |
| 6️⃣ | 🟢 Retourne `{"montant_proprietaire": montant - frais, "frais": frais}` |

---

## 📋 Fonction 4 — `obtenir_verrous(proprietaire)`

Retourne la liste des `Verrou` appartenant à `proprietaire`.

---

## ✅ Checklist de validation

- [ ] `verrouiller()` refuse montant nul et durée trop courte
- [ ] `prolonger_verrou()` refuse si pas propriétaire, ne prélève **jamais** de frais
- [ ] `deverrouiller()` refuse avant `temps_deverrouillage`, calcule le bon frais *(ex: 1000 → frais=1)*
- [ ] Double `deverrouiller()` sur le même verrou échoue proprement
- [ ] Script de simulation en bas du fichier : créer un verrou → avancer le temps artificiellement → prolonger → déverrouiller

---

> 📨 **Prochaine étape** : une fois validé et testé en console, renvoie le fichier — on vérifie la logique ensemble avant de penser à Solidity ou au site.
