import streamlit as st
import os
from dotenv import load_dotenv
from mistralai import Mistral

# Configuration de la page
st.set_page_config(
    page_title="Titraille Assistant",
    page_icon="🇫🇷",
    layout="wide"
)

def load_environment():
    """Charge les variables d'environnement et vérifie la clé API"""
    load_dotenv()
    
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        st.error("❌ Clé API Mistral non trouvée. Veuillez créer un fichier .env avec votre MISTRAL_API_KEY")
        st.stop()
    
    return api_key

def generate_titles(client, model, article_content, tone):
    """Génère 5 titres pour l'article donné"""
    
    # Prompts système personnalisés selon le ton
    tone_prompts = {
        "Informatif (SEO)": "Tu es un Secrétaire de Rédaction expérimenté dans un grand média français. Tu proposes 5 titres informatifs et optimisés pour le SEO, sans guillemets. Privilégie la clarté et l'information factuelle.",
        "Accrocheur (Clickbait)": "Tu es un Secrétaire de Rédaction expérimenté dans un grand média français. Tu proposes 5 titres accrocheurs et percutants qui donnent envie de cliquer, sans guillemets. Utilise des formules qui intriguent et captent l'attention.",
        "Jeu de mots": "Tu es un Secrétaire de Rédaction expérimenté dans un grand média français. Tu proposes 5 titres créatifs avec des jeux de mots, calembours ou références culturelles françaises, sans guillemets. Sois original et spirituel.",
        "Réseaux Sociaux": "Tu es un Secrétaire de Rédaction expérimenté dans un grand média français. Tu proposes 5 titres optimisés pour les réseaux sociaux, courts et impactants, sans guillemets. Privilégie l'engagement et le partage."
    }
    
    system_prompt = tone_prompts.get(tone, tone_prompts["Informatif (SEO)"])
    
    try:
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user", 
                "content": f"Voici l'article pour lequel je veux 5 titres :\n\n{article_content}"
            }
        ]
        
        response = client.chat.complete(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        st.error(f"❌ Erreur lors de l'appel à l'API Mistral : {str(e)}")
        return None

def main():
    """Fonction principale de l'application"""
    
    # Chargement des variables d'environnement
    api_key = load_environment()
    
    # Initialisation du client Mistral
    client = Mistral(api_key=api_key)
    
    # Interface utilisateur
    st.title("🇫🇷 Titraille Assistant")
    st.markdown("*Générateur de titres pour journalistes avec IA*")
    
    # Sidebar avec les options
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Sélection du ton
        tone = st.selectbox(
            "📝 Ton du titre",
            options=[
                "Informatif (SEO)", 
                "Accrocheur (Clickbait)", 
                "Jeu de mots", 
                "Réseaux Sociaux"
            ],
            index=0
        )
        
        # Sélection du modèle
        model = st.selectbox(
            "🤖 Modèle IA",
            options=[
                "mistral-large-latest",
                "mistral-medium-latest", 
                "mistral-small-latest"
            ],
            index=0
        )
        
        st.markdown("---")
        st.markdown("**💡 Conseils :**")
        st.markdown("• Collez votre article complet")
        st.markdown("• Choisissez le ton adapté")
        st.markdown("• L'IA génère 5 propositions")
    
    # Interface principale
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📄 Votre article")
        article_content = st.text_area(
            "Collez le contenu de votre article ici :",
            height=400,
            placeholder="Entrez le texte de votre article pour générer des titres percutants..."
        )
    
    with col2:
        st.subheader("🎯 Titres générés")
        
        if st.button("✨ Générer les titres", type="primary", use_container_width=True):
            if not article_content.strip():
                st.warning("⚠️ Veuillez d'abord saisir le contenu de votre article.")
            else:
                with st.spinner("🔄 Génération des titres en cours..."):
                    titles = generate_titles(client, model, article_content, tone)
                    
                    if titles:
                        st.success("✅ Titres générés avec succès !")
                        
                        # Affichage des titres
                        st.markdown("### 📋 Propositions de titres :")
                        
                        # Séparer les titres (supposant qu'ils sont numérotés ou séparés)
                        title_lines = [line.strip() for line in titles.split('\n') if line.strip()]
                        
                        for i, title in enumerate(title_lines, 1):
                            # Nettoyer le titre (supprimer numérotation si présente)
                            clean_title = title
                            if title.startswith(f"{i}.") or title.startswith(f"{i})"):
                                clean_title = title[2:].strip()
                            elif title.startswith("- "):
                                clean_title = title[2:].strip()
                            
                            st.markdown(f"**{i}.** {clean_title}")
                        
                        # Option de copie
                        st.markdown("---")
                        with st.expander("📋 Copier tous les titres"):
                            st.code(titles, language=None)

if __name__ == "__main__":
    main()