import os
from crewai import Agent, Task, Crew, Process, LLM
from langchain.agents import load_tools
import textwrap
from pydantic import BaseModel , Field
from typing import List,Optional
from crewai.tools import tool
from tavily import TavilyClient
from scrapegraph_py import Client
from crewai.tasks.task_output import TaskOutput
import json
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit interface
st.set_page_config(page_title="Analyse d'Équipe de Football", page_icon="⚽", layout="wide")

st.title("Analyse d'Équipe de Football")
st.write("Cet outil analyse les performances et tactiques d'une équipe de football.")

# Input for team name
team_name = st.text_input("Nom de l'équipe à analyser", "Real Madrid")

# Initialize output directory
output_dir = "./ai-agent-output"
os.makedirs(output_dir, exist_ok=True)

# Get API keys from environment variables
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SCRAPE_API_KEY = os.getenv("SCRAPE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

search_=TavilyClient(api_key=TAVILY_API_KEY)

basic_llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    api_key=GEMINI_API_KEY,
    verbose=True
)
class SuggestedSearchQueries(BaseModel):
    queries: List[str] = Field(..., title="Suggested search queries to be passed to the search engine",
                               min_items=1, max_items=20)
keywords_searcher_agent = Agent(
    role="Senior Football Data Researcher",
    goal ="\n".join(["Générer une liste pertinente de mots-clés et requêtes de recherche sur l'équipe adverse pour passer a le agent suivant",
           "Les requêtes doivent être variées et rechercher des éléments spécifiques"
    ]),
    backstory="\n".join(["Expert en recherche de données dans le domaine du football.",
                "Vous savez quelles informations sont les plus pertinentes pour analyser",
                "une équipe de football et vous pouvez formuler des requêtes de recherche",
                "précises pour obtenir ces informations."]),

    llm= basic_llm,
    verbose=True,
)
keywords_searcher_task = Task(
    description= """Générez une liste complète de mots-clés et de requêtes de recherche pour l'équipe {team_name}.
                Ces mots-clés doivent couvrir:
                - Données générales sur l'équipe (effectif, entraîneur, classement actuel,joueurs)
                - Tactiques et formations utilisées récemment
                - Résultats des 10 derniers matchs
                - Joueurs clés et leurs statistiques
                - Forces et faiblesses identifiées par les médias
                - point fort et faible de equipe
                 -tu peut generer 20 mots-clés
                 -La requête de recherche doit atteindre une page Web de Football pour le equipe, et non une page de blog ou de liste

                Formatez votre réponse comme une liste structurée de requêtes de recherche.
            """,
    expected_output="Un objet JSON contenant une liste de requêtes de recherche suggérées.",
    output_json=SuggestedSearchQueries,
    output_file=os.path.join(output_dir,"steep_1"),
    agent=keywords_searcher_agent

)
class SingleSearchResulte(BaseModel):
  Nom_de_la_source : str
  URL :str
  Type_d_information_disponible : str
  score : float
class AllSearchResulte(BaseModel):
  results : List[SingleSearchResulte]

@tool
def search_engine_tool(query:str):
  """Useful for search-based queries. Use this to find current information about any query related pages using a search engine"""
  return search_.search(query)

data_sources_researcher_agent=Agent(
    role ="Search Engine Agent",
    goal="Identifier les meilleures sources de données fiables sur l'équipe adverse",
    backstory="""
                Spécialiste des sources d'information sur le football. Vous connaissez
                les sites web, les bases de données et les plateformes les plus fiables
                pour trouver des informations détaillées sur les équipes de football,
                leurs performances récentes et leurs tactiques.
            """,
            verbose=True,
            llm=basic_llm,
            tools=[search_engine_tool]
)

data_sources_researcher_task=Task(
    description=f"""
                À partir des mots-clés fournis par keywords_searcher, recherchez et identifiez les meilleures sources
                de données sur l'équipe de fautball.

                Vous devez trouver:
                - Sites officiels (club, ligues)
                - Sites d'analyse tactique de football
                - Bases de données statistiques de football
                - Articles récents d'analyse de leurs performances
                - Sites spécialisés dans l'analyse des matchs

                Pour chaque source, indiquez son nom, son URL et le type d'information qu'on peut y trouver.
                Concentrez-vous particulièrement sur les sources qui fournissent des informations sur
                les 5 derniers matchs de l'équipe.
                Ignorer tous les résultats de recherche avec un score de confiance inférieur
            """,

            expected_output="""
                Un objet JSON contenant une liste de 8-12 sources de données pertinentes, avec pour chacune:
                - Nom de la source
                - URL
                - Type d'information disponible
                - score (notée de 1 à 5)
            """,
    output_json=AllSearchResulte,
    output_file=os.path.join(output_dir,"steep_2"),
    agent=data_sources_researcher_agent

)
scripe_client = Client(api_key=SCRAPE_API_KEY)

from pydantic import BaseModel, Field
from typing import List, Optional

class JoueurPerformance(BaseModel):
    nom: str = Field(..., title="Nom complet du joueur")
    poste: str = Field(..., title="Poste occupé par le joueur dans le match")
    minutes_jouees: int = Field(..., title="Nombre de minutes jouées par le joueur")
    buts: int = Field(..., title="Nombre de buts marqués")
    passes_decisives: int = Field(..., title="Nombre de passes décisives")
    tirs: int = Field(..., title="Nombre de tirs tentés")
    duels_gagnes: int = Field(..., title="Nombre de duels gagnés")
    notes: Optional[str] = Field(title="Commentaires ou observations sur la performance du joueur", default=None)

class SingleMatchAnalysis(BaseModel):
    page_url: str = Field(..., title="L'URL de la page source du match analysé")
    date_match: str = Field(..., title="Date du match")
    adversaire: str = Field(..., title="Nom de l'équipe adverse")
    score_final: str = Field(..., title="Score final du match (ex: 2-1)")

    competition: Optional[str] = Field(title="Compétition ou tournoi (ex: Liga, Champions League)", default=None)
    lieu: Optional[str] = Field(title="Lieu du match (domicile ou extérieur)", default=None)

    formation_utilisee: str = Field(..., title="Système de jeu ou formation utilisée (ex: 4-3-3)")
    possession_balle: str = Field(..., title="Pourcentage de possession de balle (ex: 55%)")

    stats_offensives: dict = Field(..., title="Statistiques offensives (ex: {'tirs': 12, 'tirs_cadres': 5, 'occasions_nettes': 3})")
    stats_defensives: dict = Field(..., title="Statistiques défensives (ex: {'tacles': 15, 'interceptions': 8, 'duels_gagnes': 20})")

    joueurs_titulaires: List[str] = Field(..., title="Liste des joueurs titulaires avec leurs positions (ex: ['Courtois (GK)', 'Carvajal (RB)', ...])")
    performances_joueurs_cles: List[JoueurPerformance] = Field(..., title="Performances détaillées des joueurs clés")

    moments_decisifs: List[str] = Field(..., title="Description des moments décisifs (ex: but à la 75e, carton rouge...)")
    changements_tactiques: List[str] = Field(..., title="Liste des changements tactiques effectués pendant le match")

    points_forts_observes: List[str] = Field(..., title="Forces tactiques remarquées chez l'adversaire")
    faiblesses_observees: List[str] = Field(..., title="Faiblesses ou vulnérabilités de l'adversaire")
    style_de_jeu: Optional[str] = Field(title="Style de jeu global de l'équipe adverse (ex: jeu de possession, contre-attaque...)", default=None)

    agent_recommendation_rank: int = Field(..., title="Importance du match pour l'analyse stratégique (de 1 à 5, 5 = très pertinent)")
    agent_recommendation_notes: List[str] = Field(..., title="Observations de l'agent expliquant pourquoi ce match est pertinent ou non pour la préparation")

class AllMatchAnalysis(BaseModel):
  Match : List[SingleMatchAnalysis]

@tool
def web_scraping_tool(page_url:str):
  """
  Un outil d'IA pour aider un agent à extraire une page Web
  Example
  web_scraping_tool(
    page_url="https://www.realmadrid.com/es-ES",
  """
  details = scripe_client.smartscraper(
      website_url=page_url,
      user_prompt="Extract ```json\n" + SingleMatchAnalysis.schema_json() +"```\n From the web page"

  )
  return{
      "page_url":page_url,
      "details":details
  }

data_collector_agent = Agent(
            role="web scraping agent",
            goal=" to Collecter et organiser des données détaillées sur les 10 derniers matchs de l'équipe adverse",
            backstory="""
                L'agent est conçu pour vous aider à trouver les donnes requises à partir de n'importe quelle URL de site web. Ces informations seront utilisées pour  générer un rapport structuré, précis et exhaustif sur l'équipe adverse.
                Expert en collecte et organisation de données footballistiques.
                Vous savez extraire les statistiques pertinentes, les formations,
                les événements clés des matchs et les performances individuelles des joueurs.
                Vous êtes méticuleux et organisez les données de manière structurée.
            """,
            verbose=True,
            llm =basic_llm,
            tools=[web_scraping_tool]

        )
data_collector_task = Task(
    description="""
                À partir des sources identifiées, collectez des données détaillées sur les 10 derniers
                matchs de l'équipe .

                Pour chaque match, recueillez:
                 - Date et adversaire
                - Score final
                - Formation utilisée
                - Possession de balle
                - Statistiques offensives (tirs, tirs cadrés, occasions nettes, etc.)
                - Statistiques défensives (tacles, interceptions, duels gagnés, etc.)
                - Joueurs titulaires et leurs positions
                - Joueurs clés et leurs performances
                - Moments décisifs du match
                - Changements tactiques effectués pendant le match

                Compilez ces informations dans un rapport structuré.
            """,
               expected_output="Un objet JSON contenant les détails des equipe et des Matches " ,
               output_json=AllMatchAnalysis,
                output_file=os.path.join(output_dir,"steep_3"),
                agent=data_collector_agent
)

            
def callback(output: TaskOutput):
                st.success("Analyse terminée!")
                st.write(f"""
                      Raw Output :{output.raw}
                      """)

data_analyst_agent= Agent(
    role ="Agent auteur du rapport d'analyse des adversaire ",
    goal="Analyser les données collectées et produire un rapport tactique complet",
    backstory="""
                Expert en analyse tactique du football avec une expérience dans l'analyse
                des adversaires pour les équipes professionnelles. Vous savez interpréter
                les statistiques, repérer les tendances tactiques, identifier les forces et
                faiblesses d'une équipe, et formuler des recommandations stratégiques.
                Vous produisez des rapports clairs et actionnables pour les entraîneurs.
            """,
    verbose=True,
    llm=basic_llm

)

data_analyst_task=Task(
    description=""" Analysez en profondeur les données collectées sur les 10 derniers matchs de l'équipe {team_name}
     et produisez un rapport d'analyse tactique complet.

     Votre analyse doit inclure :

        1. PROFIL TACTIQUE :
          - Formation(s) préférentielle(s)
          - Style de jeu (possession, contre-attaque, pressing, etc.)
          - Transitions offensives et défensives
          - Phases arrêtées (types, forces et faiblesses)
          - Comportement sans ballon (bloc équipe, pressing, repli)

        2. FORCES IDENTIFIÉES :
          - Points forts collectifs
          - Zones du terrain où l'équipe excelle
          - Joueurs particulièrement performants

        3. FAIBLESSES EXPLOITABLES :
          - Vulnérabilités tactiques
          - Zones du terrain à cibler
          - Joueurs en difficulté

        4. JOUEURS CLÉS :
          - Profil détaillé des 3-4 joueurs les plus importants
          - Leurs forces et faiblesses individuelles
          - Comment les neutraliser

        5. DONNÉES PHYSIQUES ET INTENSITÉ :
          - Distance moyenne parcourue par match
          - Nombre de sprints/intensité
          - Niveau d'agressivité (fautes, duels)

        6. TENDANCES RÉCENTES ET DYNAMIQUE :
          - Évolution tactique sur les 5 derniers matchs
          - Résultats récents et niveau de confiance
          - Changements d'effectif ou retour de blessés

        7. RECOMMANDATIONS STRATÉGIQUES :
          - Formation à adopter contre cette équipe
          - Approche tactique recommandée
          - Duels clés à cibler
          - Conseils spécifiques pour contrer leurs points forts

        Conclusion avec un résumé clair des points d'action prioritaires.
            """,
    agent=data_analyst_agent,
            expected_output="""
                Un rapport d'analyse tactique complet et actionnable, structuré selon les sections demandées,
                avec des recommandations claires et pratiques pour l'entraîneur.
            """,
    callback=callback,
    output_file=os.path.join(output_dir,"rappord.md"),
)
from concurrent.futures import process
system_crew =Crew(
    agents=[
        keywords_searcher_agent,
        data_sources_researcher_agent,
        data_collector_agent,
        data_analyst_agent,



    ],
        tasks=[
            keywords_searcher_task,
            data_sources_researcher_task,
            data_collector_task,
            data_analyst_task,
        ],
    process =Process.sequential

)

# Add Streamlit button to start analysis
if st.button("Lancer l'analyse"):
    with st.spinner("Analyse en cours..."):
        try:
            # Create progress bar
            progress_bar = st.progress(0)
            
            # Run the crew
            system_crew = Crew(
                agents=[
                    keywords_searcher_agent,
                    data_sources_researcher_agent,
                    data_collector_agent,
                    data_analyst_agent,
                ],
                tasks=[
                    keywords_searcher_task,
                    data_sources_researcher_task,
                    data_collector_task,
                    data_analyst_task,
                ],
                process=Process.sequential
            )

            # Update progress bar
            progress_bar.progress(25)
            
            # Run analysis
            results = system_crew.kickoff(
                inputs={
                    "team_name": team_name,
                }
            )
            
            # Update progress bar
            progress_bar.progress(100)
            
            # Display results
            
            
            
            # if isinstance(results, dict) and "output" in results:
            #     rapport = results["output"]
            # else:
            #     rapport = results  # ou adapte selon la structure exacte

            # sections = rapport.split('\n\n')  # ou adapte selon la structure
            # for section in sections:
            #     st.markdown(section)
            
        except Exception as e:
            st.error(f"Une erreur est survenue: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("Développé avec pour l'analyse de football")
