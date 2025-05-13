

# ⚽ AI Coach Assistant

AI Coach Assistant est un outil d'analyse tactique intelligent conçu pour aider les entraîneurs de football à préparer leurs matchs. En automatisant la collecte d'informations et en générant des rapports précis, cet assistant fournit des recommandations stratégiques basées sur l'analyse de données et l'intelligence artificielle.

## 🚀 Objectif du projet

Offrir un outil autonome capable d'assister les analystes et entraîneurs sportifs dans la prise de décision, à travers des analyses précises, personnalisables, et exploitables.

## 📊 Fonctionnalités principales

 - Analyse des 5 derniers matchs d'une équipe adverse

 - Extraction d'informations clés : formation, style de jeu, joueurs clés, faiblesses tactiques

 - Recommandations stratégiques pour contrer l'adversaire

 - Scraping intelligent de sites web spécifiques à partir d'URL données

 - Structure de données précise avec Pydantic

## 🚧 Technologies utilisées

 - LangChain : Orchestration des agents conversationnels

 - CrewAI : Coordination entre agents pour réaliser des tâches complexes

 - Replicate & Gemini : Utilisation de modèles LLM puissants (DeepSeek, Gemini, etc.)

 - BeautifulSoup & Requests : Scraping web pour la collecte de données

 - Tavily : Recherche contextuelle avancée

 - scrapegraph_py : Extraction d'informations structurées à partir de pages web

 - Python (>= 3.10)

 - Pydantic : Validation et structuration des données

 - Streamlit : Interface utilisateur web simple et interactive

 - dotenv : Gestion sécurisée des variables d'environnement

## 🚀 Lancer le projet

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/votre-utilisateur/ai-coach-assistant.git
   cd ai-coach-assistant
2. **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
4. **Configurer les clés API :**
   ***dans le fichier .env :***
  -  GEMINI_API_KEY="........" 
  -  SCRAPE_API_KEY ="......." 
  -  AVILY_API_KEY ="......."
4. **Exécuter l’analyse :**
    ```bash
    streamlit run projet.py

   
### 📄 Exemple de rapport généré
**Le système génère un rapport structuré comme suit :**

- Profil tactique

- Forces identifiées

- Faiblesses exploitables

- Joueurs clés

- Recommandations stratégiques

***Exemple complet dans le dossier /ai-agent-output/.***
