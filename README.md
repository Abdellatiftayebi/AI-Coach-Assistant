"# AI-Coach-Assistant" 

# ⚽ AI Coach Assistant avec Crewai

AI Coach Assistant est un assistant intelligent conçu pour aider les entraîneurs de football à analyser les équipes adverses, formuler des stratégies de jeu et générer des rapports tactiques détaillés à partir de données collectées automatiquement.

## 🧠 Objectif du projet

Développer un système basé sur l'intelligence artificielle capable de :

- Collecter et extraire automatiquement des informations à partir de sources web (pages officielles, articles, résultats de match, etc.).
- Analyser les performances et les tactiques d'une équipe adverse.
- Générer des rapports complets à destination des entraîneurs.
- Proposer des recommandations stratégiques adaptées.

## 🔍 Fonctionnalités principales

- 🔎 **Extraction d’informations** à partir d’URL ciblées.
- 🧾 **Génération automatique de rapports tactiques** (formations, points forts/faibles, recommandations).
- 🤖 **Agents multi-rôles** collaborant pour l'analyse (ex. : Data Researcher, Analyste Tactique, Stratégiste).
- 🗣️ Support du **langage naturel** pour la génération de contenu (LLM).
- 📊 Analyse basée sur les **5 derniers matchs** de l’adversaire.

## 🛠️ Technologies utilisées

- `LangChain` pour l'orchestration des agents.
- `Replicate` pour l’intégration de modèles LLM externes (ex. : DeepSeek).
- `BeautifulSoup` & `Requests` pour le scraping web.
- `Python` (>= 3.10)
- `Pydantic` pour la structuration des données.
- `OpenAI` ou `HuggingFace` pour les LLM selon la configuration.

## 🚀 Lancer le projet

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/votre-utilisateur/ai-coach-assistant.git
   cd ai-coach-assistant
2. **Installer les dépendances :** 
    pip install -r requirements.txt
3. **Configurer les clés API :**
   dans le fichier .env :
       - GEMINI_API_KEY="........" 
       - SCRAPE_API_KEY ="......." 
       - TAVILY_API_KEY ="......."
4. **Exécuter l’analyse :**
    python main.py

   
### 📄 Exemple de rapport généré
**Le système génère un rapport structuré comme suit :**

- Profil tactique

- Forces identifiées

- Faiblesses exploitables

- Joueurs clés

- Recommandations stratégiques

***Exemple complet dans le dossier /ai-agent-output/.***
