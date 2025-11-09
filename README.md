# 🖥️ Outil de Diagnostic Système avec Interface Graphique

Un outil moderne de diagnostic système avec une interface graphique intuitive construite avec Python et ttkbootstrap.

## ✨ Fonctionnalités

- 🖥️ **Diagnostic Windows** : Affichage des informations système, CPU, mémoire et disques
- 🗄️ **Vérification MySQL** : Vérification de la connectivité MySQL
- 🌐 **Scan Réseau** : Analyse du réseau et des hôtes
- ⚠️ **Audit d'Obsolescence** : Détection des systèmes obsolètes (EOL)
- 📊 **Base EOL** : Consultation de la base de données End-of-Life
- 💎 **Interface Moderne** : Design moderne avec thème sombre

## 🛠️ Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étape 1 : Cloner le dépôt

```bash
git clone https://github.com/feras2345/outil-diagnostic-gui.git
cd outil-diagnostic-gui
```

### Étape 2 : Créer le dossier data

```bash
mkdir data
```

### Étape 3 : Installer les dépendances

```bash
pip install -r requirements.txt
```

### Étape 4 : Ajouter vos fichiers de données

Copiez vos fichiers JSON de diagnostic dans le dossier `data/` :

```
data/
├── windows_diagnostic_20251106_213357.json
├── mysql_check_20251106_212747.json
├── network_scan_20251107_090850.json
├── audit_obsolescence_20251107_143612.json
└── eol_database_20251106_212818.json
```

## 🚀 Utilisation

### Lancer l'application

```bash
python main.py
```

### Navigation

1. **Menu de gauche** : Sélectionnez le module de diagnostic souhaité
2. **Zone principale** : Consultez les résultats et les informations détaillées
3. **Charger fichier JSON** : Importez un fichier JSON personnalisé
4. **Rafraîchir** : Retour à l'écran d'accueil

## 📝 Structure du Projet

```
outil-diagnostic-gui/
├── main.py              # Fichier principal de l'application
├── requirements.txt     # Dépendances Python
├── README.md            # Documentation
└── data/                # Dossier pour les fichiers JSON
    ├── windows_diagnostic_*.json
    ├── mysql_check_*.json
    ├── network_scan_*.json
    ├── audit_obsolescence_*.json
    └── eol_database_*.json
```

## 💻 Technologies Utilisées

- **Python 3** : Langage de programmation
- **Tkinter** : Interface graphique native Python
- **ttkbootstrap** : Thèmes modernes pour Tkinter
- **psutil** : Informations système
- **mysql-connector-python** : Connexion MySQL

## 🎓 Exemples de Données JSON

### Diagnostic Windows

```json
{
  "timestamp": "2025-11-06T21:33:56.827868",
  "hostname": "DESKTOP-UA7LL9T",
  "os": "Windows",
  "os_version": "10.0.26100",
  "cpu_percent": 5.1,
  "memory_percent": 56.2
}
```

### Vérification MySQL

```json
{
  "timestamp": "2025-11-06T21:27:39.070924",
  "host": "192.168.10.21",
  "status": "CRITICAL",
  "connection": false
}
```

## ❓ Dépannage

### Erreur : Module ttkbootstrap introuvable

```bash
pip install ttkbootstrap
```

### Erreur : Fichier JSON non trouvé

Vérifiez que vos fichiers JSON sont bien dans le dossier `data/` et que les noms correspondent.

## 👥 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📜 Licence

Ce projet est sous licence MIT.

## 👤 Auteur

Créé par feras2345

---

⭐ Si ce projet vous aide, n'oubliez pas de lui donner une étoile sur GitHub !
