import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Gestion Bibliothèque",
    page_icon="📚",
    layout="wide"
)

# En-tête
col1, col2 = st.columns([2,1])
with col1:
    st.title("📚 BIBLIOTHEQUE LE BONLECTEUR")
    st.badge("DELAMOU Samaké")
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/2702/2702134.png", width=100)

# Métriques principales
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Membres", value="120", delta="↑ 5")
with col2:
    st.metric(label="Livres Disponibles", value="450", delta="-3")
with col3:
    st.metric(label="Emprunts en cours", value="45", delta="↑ 2")
with col4:
    st.metric(label="Retards", value="12", delta="-2")

# Section principale
tab1, tab2,tab3,tab4,tab5 = st.tabs(["Membres","Livres","Emplacements","Auteurs" ,"Statistiques"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dernières activités")
        st.info("📋 Liste des 5 dernières actions")
        activities = """
        - Jean Dupont a emprunté "Le Petit Prince"
        - Marie Martin a rendu "1984"
        - Nouveau membre: Sophie Dubois
        - Paul Henri a prolongé son emprunt
        - Mise à jour: Lucas Bernard
        """
        st.markdown(activities)

with tab2:
    st.subheader("Statistiques des emprunts")
    chart_data = pd.DataFrame({
        'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai'],
        'Emprunts': [20, 25, 30, 28, 35]
    })
    st.bar_chart(chart_data.set_index('Mois'))
with tab3:
    st.button("➕ Nouveau Livre", help="Ajouter un nouveau membre", use_container_width=True)
    st.button("👥 Afficher les Livres", help="Voir la liste des membres", use_container_width=True)
    st.button("✏️ Mettre à jour un Livres", help="Modifier les informations d'un membre", use_container_width=True)
    st.button("🗑️ Supprimer un Livres", help="Retirer un membre de la bibliothèque", use_container_width=True)
with tab4:
    st.button("Nouveau membre",help="Ajouter un nouveau membre")
    st.button("Afficher les membres",help="Voir la liste des membres")
    st.button("Mettre à jour un membre",help="Modifier les informations d'un membre")   
    st.button("Supprimer un membre",help="Retirer un membre de la bibliothèque")
with tab5:
    st.subheader("Analyse des Retards")
    delay_data = pd.DataFrame({
        'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai'],
        'Retards': [5, 7, 6, 4, 3]
    })
    st.line_chart(delay_data.set_index('Mois'))
# Sidebar
st.sidebar.title("Navigation")
st.sidebar.info("Bibliothèque de gestion de la bibliothèque")

with st.sidebar:
    st.subheader("Filtres rapides")
    st.button("📊 Afficher les retards d'emprunt", help="Les membres qui ont retardés")
    st.button("🏆 Afficher les meilleurs clients", help="Nos 5 meilleurs clients")
    
    st.divider()
    st.subheader("Recherche rapide")
    st.text_input("Rechercher un membre...")
    st.selectbox("Catégorie de livre", ["Tous", "Roman", "Science", "Histoire", "Poésie"])

# Footer
st.divider()
st.caption("© 2025 - Application de gestion complète de bibliothèque")
