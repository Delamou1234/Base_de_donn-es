import streamlit as st 
st.title("livres (Gestion de votre Bibliothèque)")
st.badge("DELAMOU Samaké")
st.info("Utilisez le menu de navigation pour accéder aux différentes fonctionnalités de l'autre Application.")
# les boutons
col1,col2 = st.columns(2)
with col1:
    st.button("➕ Nouveau Livre", help="Ajouter un nouveau membre", use_container_width=True)
    st.button("👥 Afficher les Livres", help="Voir la liste des membres", use_container_width=True)
    st.button("✏️ Mettre à jour un Livres", help="Modifier les informations d'un membre", use_container_width=True)
    st.button("🗑️ Supprimer un Livres", help="Retirer un membre de la bibliothèque", use_container_width=True)
  
# les tris
st.sidebar.info("Bibliothèque de gestion de la bibliothèque")
st.sidebar.button("Afficher les retard d'emprunt",help="Les membres qui ont retardés")
st.sidebar.button("Afficher les meilleurs clients",help="Nos 5 meilleurs clients")


