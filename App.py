import streamlit as st
import pandas as pd
import datetime

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

# Initialisation des états de session
if 'show_add_form' not in st.session_state:
    st.session_state.show_add_form = False
if 'show_edit_form' not in st.session_state:
    st.session_state.show_edit_form = False
if 'members' not in st.session_state:
    st.session_state.members = []  # Liste temporaire des membres

# Section principale
tab1, tab2,tab3,tab4,tab5 = st.tabs(["Membres","Livres","Emplacements","Auteurs" ,"Statistiques"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Gestion des Membres")
        if st.button("➕ Nouveau Membre", help="Ajouter un nouveau membre", use_container_width=True):
            st.session_state.show_add_form = True
            st.session_state.show_edit_form = False
        
        if st.button("👥 Liste des Membres", help="Voir la liste des membres", use_container_width=True):
            st.session_state.show_add_form = False
            st.session_state.show_edit_form = False
        
        if st.button("✏️ Modifier un Membre", help="Modifier les informations d'un membre", use_container_width=True):
            st.session_state.show_edit_form = True
            st.session_state.show_add_form = False
        
        if st.button("🗑️ Supprimer un Membre", help="Retirer un membre", use_container_width=True):
            if st.session_state.members:
                member_to_delete = st.selectbox("Sélectionner le membre à supprimer", 
                    [m['nom'] for m in st.session_state.members])
                if st.button("Confirmer la suppression"):
                    st.session_state.members = [m for m in st.session_state.members if m['nom'] != member_to_delete]
                    st.success(f"Membre {member_to_delete} supprimé avec succès!")

    with col2:
        # Formulaire d'ajout
        if st.session_state.show_add_form:
            st.subheader("Ajouter un nouveau membre")
            with st.form("add_member_form"):
                nom = st.text_input("Nom complet*")
                email = st.text_input("Email")
                telephone = st.text_input("Téléphone")
                adresse = st.text_area("Adresse")
                date_inscription = st.date_input("Date d'inscription", value=datetime.date.today())
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("Enregistrer")
                with col2:
                    cancel = st.form_submit_button("Annuler")

                if submit and nom.strip():
                    new_member = {
                        "nom": nom,
                        "email": email,
                        "telephone": telephone,
                        "adresse": adresse,
                        "date_inscription": str(date_inscription)
                    }
                    st.session_state.members.append(new_member)
                    st.success("Membre ajouté avec succès!")
                    st.session_state.show_add_form = False
                elif submit:
                    st.error("Le nom est obligatoire!")
                
                if cancel:
                    st.session_state.show_add_form = False

        # Formulaire de modification
        elif st.session_state.show_edit_form and st.session_state.members:
            st.subheader("Modifier un membre")
            member_to_edit = st.selectbox("Sélectionner le membre à modifier",
                [m['nom'] for m in st.session_state.members])
            
            member = next((m for m in st.session_state.members if m['nom'] == member_to_edit), None)
            if member:
                with st.form("edit_member_form"):
                    nom = st.text_input("Nom complet*", value=member['nom'])
                    email = st.text_input("Email", value=member['email'])
                    telephone = st.text_input("Téléphone", value=member['telephone'])
                    adresse = st.text_area("Adresse", value=member['adresse'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        submit = st.form_submit_button("Mettre à jour")
                    with col2:
                        cancel = st.form_submit_button("Annuler")

                    if submit and nom.strip():
                        # Mise à jour du membre
                        member.update({
                            "nom": nom,
                            "email": email,
                            "telephone": telephone,
                            "adresse": adresse
                        })
                        st.success("Membre mis à jour avec succès!")
                        st.session_state.show_edit_form = False
                    elif submit:
                        st.error("Le nom est obligatoire!")
                    
                    if cancel:
                        st.session_state.show_edit_form = False

        # Affichage de la liste des membres
        if not st.session_state.show_add_form and not st.session_state.show_edit_form:
            st.subheader("Liste des membres")
            if st.session_state.members:
                for member in st.session_state.members:
                    with st.expander(f"📋 {member['nom']}"):
                        st.write(f"Email: {member['email']}")
                        st.write(f"Téléphone: {member['telephone']}")
                        st.write(f"Adresse: {member['adresse']}")
                        st.write(f"Date d'inscription: {member['date_inscription']}")
            else:
                st.info("Aucun membre enregistré pour le moment.")
with tab2:
    st.subheader("Statistiques des emprunts")
    chart_data = pd.DataFrame({
        'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai'],
        'Emprunts': [20, 25, 30, 28, 35]
    })
    st.bar_chart(chart_data.set_index('Mois'))
with tab3:
    st.button("➕ Nouveau Livre", help="Ajouter un nouveau membre", use_container_width=True,key="new_book")
    st.button("👥 Afficher les Livres", help="Voir la liste des membres", use_container_width=True,key="afficher1")
    st.button("✏️ Mettre à jour un Livres", help="Modifier les informations d'un membre", use_container_width=True,key="update_book")
    st.button("🗑️ Supprimer un Livres", help="Retirer un membre de la bibliothèque", use_container_width=True,key="delete")
with tab4:
    st.button("Nouveau membre",help="Ajouter un nouveau membre")
    st.button("Afficher les membres",help="Voir la liste des membres")
    st.button("Mettre à jour un membre",help="Modifier les informations d'un membre")   
    st.button("Supprimer un membre",help="Retirer un membre de la bibliothèque")
with tab5:
   
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
