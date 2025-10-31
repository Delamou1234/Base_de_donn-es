import streamlit as st 
st.title("Auteurs (Gestion de votre Bibliothèque)")
st.badge("DELAMOU Samaké")
st.info("Utilisez le menu de navigation pour accéder aux différentes fonctionnalités de l'autre Application.")
# les boutons
st.button("Nouveau membre",help="Ajouter un nouveau membre")
st.button("Afficher les membres",help="Voir la liste des membres")
st.button("Mettre à jour un membre",help="Modifier les informations d'un membre")   
st.button("Supprimer un membre",help="Retirer un membre de la bibliothèque")

# les tris
st.sidebar.info("Bibliothèque de gestion de la bibliothèque")
st.sidebar.button("Afficher les retard d'emprunt",help="Les membres qui ont retardés")
st.sidebar.button("Afficher les meilleurs clients",help="Nos 5 meilleurs clients")


