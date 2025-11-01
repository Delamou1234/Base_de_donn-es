import streamlit as st
import pandas as pd
import datetime
import io
from PIL import Image

# Configuration de la page
st.set_page_config(
    page_title="Gestion Bibliothèque",
    page_icon="📚",
    layout="wide"
)

# --- Début ajout : authentification simple ---
# États de session pour l'authentification
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = ""

def _logout():
    st.session_state.logged_in = False
    st.session_state.user = ""
    # st.experimental_rerun()  # <-- supprimé, Streamlit rerun automatique suffit

# Si non connecté, afficher le formulaire de connexion et stopper l'exécution du reste
if not st.session_state.logged_in:
    st.title("Gestion Bibliothèque")
    
    # Création de 3 colonnes
    col_left, col_mid, col_right = st.columns(3)
    
    # Colonne de gauche - Image ou texte de bienvenue
    with col_left:
        st.image("https://img.icons8.com/clouds/200/000000/library.png", width=200)
        st.markdown("### Bienvenue à la bibliothèque")
    
    # Colonne du milieu - Informations
    with col_mid:
        st.info("""
        📚 **Le BonLecteur**
        
        Connectez-vous ou créez un compte pour:
        - Emprunter des livres
        - Suivre vos lectures
        - Communiquer avec l'admin
        - Et plus encore!
        """)
    
    # Colonne de droite - Formulaires
    with col_right:
        # Tabs pour switcher entre connexion, création et reset password
        login_tab, signup_tab, reset_tab = st.tabs(["Connexion", "Nouveau compte", "Mot de passe"])
        
        # Onglet Connexion
        with login_tab:
            with st.form("login_form"):
                username = st.text_input("Nom d'utilisateur")
                password = st.text_input("Mot de passe", type="password")
                submit = st.form_submit_button("Se connecter")
                
                if submit:
                    if username == "admin" and password == "admin123":
                        st.session_state.logged_in = True
                        st.session_state.user = "admin"
                        st.session_state.role = "admin"
                    elif username and password == "member123":
                        st.session_state.logged_in = True
                        st.session_state.user = username
                        st.session_state.role = "member"
                    else:
                        st.error("Identifiants invalides")
        
        # Onglet Création de compte
        with signup_tab:
            with st.form("signup_form"):
                new_username = st.text_input("Choisir un nom d'utilisateur")
                new_password = st.text_input("Choisir un mot de passe", type="password")
                confirm_password = st.text_input("Confirmer le mot de passe", type="password")
                email = st.text_input("Email")
                submit_signup = st.form_submit_button("Créer mon compte")
                
                if submit_signup:
                    if not new_username or not new_password:
                        st.error("Tous les champs sont obligatoires")
                    elif new_password != confirm_password:
                        st.error("Les mots de passe ne correspondent pas")
                    else:
                        # Ici vous pouvez ajouter la logique pour sauvegarder le nouveau compte
                        # Pour l'exemple, on utilise une liste en session
                        if 'users' not in st.session_state:
                            st.session_state.users = []
                        
                        st.session_state.users.append({
                            "username": new_username,
                            "password": new_password,  # En production, hasher le mot de passe
                            "email": email,
                            "role": "member"
                        })
                        st.success("Compte créé avec succès! Vous pouvez maintenant vous connecter.")
        
        # Onglet Reset password
        with reset_tab:
            with st.form("reset_form"):
                reset_username = st.text_input("Nom d'utilisateur")
                reset_email = st.text_input("Email de confirmation")
                submit_reset = st.form_submit_button("Réinitialiser mon mot de passe")
                
                if submit_reset:
                    if not reset_username or not reset_email:
                        st.error("Veuillez remplir tous les champs")
                    else:
                        # Ici vous pouvez ajouter la logique pour réinitialiser le mot de passe
                        # Par exemple, envoyer un email avec un lien de réinitialisation
                        st.success("Si le compte existe, un email de réinitialisation vous sera envoyé.")
    
    st.stop()
# --- Fin ajout : authentification simple ---

# Sidebar : bouton déconnexion
with st.sidebar:
    if st.session_state.logged_in:
        st.write(f"Connecté en tant que: {st.session_state.user}")
        if st.button("Se déconnecter"):
            _logout()

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

# Ajouter ces états de session en haut du fichier après les états des membres
if 'books' not in st.session_state:
    st.session_state.books = []
if 'locations' not in st.session_state:
    st.session_state.locations = []
if 'authors' not in st.session_state:
    st.session_state.authors = []

# --- Début ajout : initialisation réservations et users ---
if 'reservations' not in st.session_state:
    st.session_state.reservations = []  # liste des réservations
if 'users' not in st.session_state:
    st.session_state.users = []         # comptes créés en session (ex: signup)
if 'role' not in st.session_state:
    st.session_state.role = None        # "admin" ou "member"
# --- Fin ajout : initialisation réservations et users ---

# Pour chaque section, ajouter ces états
for item in ['book', 'location', 'author']:
    if f'show_add_{item}_form' not in st.session_state:
        st.session_state[f'show_add_{item}_form'] = False
    if f'show_edit_{item}_form' not in st.session_state:
        st.session_state[f'show_edit_{item}_form'] = False

# --- Début ajout : initialisation messagerie ---
if 'chat_messages' not in st.session_state:
    # chaque message: {"sender": str, "role": "member"|"admin", "type":"text"|"audio", "content": str or bytes, "ts": str}
    st.session_state.chat_messages = []
# --- Fin ajout : initialisation messagerie ---

# Section principale (ajout de l'onglet "Messagerie")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Membres","Livres","Emplacements","Auteurs","Statistiques","Messagerie"])

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
with tab2:  # Livres
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Gestion des Livres")
        if st.button("➕ Nouveau Livre", help="Ajouter un nouveau livre", use_container_width=True):
            st.session_state.show_add_book_form = True
            st.session_state.show_edit_book_form = False
        
        if st.button("📚 Liste des Livres", help="Voir la liste des livres", use_container_width=True):
            st.session_state.show_add_book_form = False
            st.session_state.show_edit_book_form = False
        
        if st.button("✏️ Modifier un Livre", use_container_width=True):
            st.session_state.show_edit_book_form = True
            st.session_state.show_add_book_form = False
        
        if st.button("🗑️ Supprimer un Livre", use_container_width=True):
            if st.session_state.books:
                book_to_delete = st.selectbox("Sélectionner le livre à supprimer", 
                    [b['titre'] for b in st.session_state.books])
                if st.button("Confirmer la suppression", key="del_book"):
                    st.session_state.books = [b for b in st.session_state.books if b['titre'] != book_to_delete]
                    st.success(f"Livre {book_to_delete} supprimé!")

    with col2:
        if st.session_state.show_add_book_form:
            st.subheader("Ajouter un nouveau livre")
            with st.form("add_book_form"):
                titre = st.text_input("Titre*")
                auteur = st.text_input("Auteur*")
                isbn = st.text_input("ISBN")
                annee = st.number_input("Année de publication", min_value=1800, max_value=2025)
                categorie = st.selectbox("Catégorie", ["Roman", "Science", "Histoire", "Poésie", "Autre"])
                quantite = st.number_input("Quantité", min_value=1, value=1)
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("Enregistrer")
                with col2:
                    cancel = st.form_submit_button("Annuler")

                if submit and titre.strip() and auteur.strip():
                    new_book = {
                        "titre": titre,
                        "auteur": auteur,
                        "isbn": isbn,
                        "annee": annee,
                        "categorie": categorie,
                        "quantite": quantite
                    }
                    st.session_state.books.append(new_book)
                    st.success("Livre ajouté avec succès!")
                    st.session_state.show_add_book_form = False
                elif submit:
                    st.error("Titre et auteur sont obligatoires!")
        
        # Formulaire de modification
        elif st.session_state.show_edit_book_form and st.session_state.books:
            st.subheader("Modifier un livre")
            book_to_edit = st.selectbox("Sélectionner le livre à modifier",
                [b['titre'] for b in st.session_state.books])
            
            book = next((b for b in st.session_state.books if b['titre'] == book_to_edit), None)
            if book:
                with st.form("edit_book_form"):
                    titre = st.text_input("Titre*", value=book['titre'])
                    auteur = st.text_input("Auteur*", value=book['auteur'])
                    isbn = st.text_input("ISBN", value=book['isbn'])
                    annee = st.number_input("Année de publication", min_value=1800, max_value=2025, value=book['annee'])
                    categorie = st.selectbox("Catégorie", ["Roman", "Science", "Histoire", "Poésie", "Autre"], index=["Roman", "Science", "Histoire", "Poésie", "Autre"].index(book['categorie']))
                    quantite = st.number_input("Quantité", min_value=1, value=book['quantite'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        submit = st.form_submit_button("Mettre à jour")
                    with col2:
                        cancel = st.form_submit_button("Annuler")

                    if submit and titre.strip() and auteur.strip():
                        # Mise à jour du livre
                        book.update({
                            "titre": titre,
                            "auteur": auteur,
                            "isbn": isbn,
                            "annee": annee,
                            "categorie": categorie,
                            "quantite": quantite
                        })
                        st.success("Livre mis à jour avec succès!")
                        st.session_state.show_edit_book_form = False
                    elif submit:
                        st.error("Titre et auteur sont obligatoires!")
                    
                    if cancel:
                        st.session_state.show_edit_book_form = False

        # Affichage de la liste des livres
        if not st.session_state.show_add_book_form and not st.session_state.show_edit_book_form:
            st.subheader("Liste des livres")
            if st.session_state.books:
                for book in st.session_state.books:
                    with st.expander(f"📖 {book['titre']}"):
                        st.write(f"Auteur: {book['auteur']}")
                        st.write(f"ISBN: {book['isbn']}")
                        st.write(f"Année: {book['annee']}")
                        st.write(f"Catégorie: {book['categorie']}")
                        st.write(f"Quantité: {book['quantite']}")
            else:
                st.info("Aucun livre enregistré pour le moment.")
            # Ajouter après l'affichage de la liste des livres
            if st.session_state.role == "member" and st.session_state.books:
                st.divider()
                st.subheader("🎯 Réserver un livre")
                with st.form("reservation_form"):
                    livre = st.selectbox("Choisir un livre", 
                        [b['titre'] for b in st.session_state.books if b['quantite'] > 0])
                    date_debut = st.date_input("Date de début", 
                        min_value=datetime.date.today(),
                        max_value=datetime.date.today() + datetime.timedelta(days=30))
                    duree = st.number_input("Durée (jours)", min_value=1, max_value=30, value=7)
                    submit_res = st.form_submit_button("Réserver")
                    
                    if submit_res:
                        book = next((b for b in st.session_state.books if b['titre'] == livre), None)
                        if book and book['quantite'] > 0:
                            reservation = {
                                "membre": st.session_state.user,
                                "livre": livre,
                                "date_debut": str(date_debut),
                                "duree": duree,
                                "statut": "En attente",
                                "date_reservation": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            st.session_state.reservations.append(reservation)
                            book['quantite'] -= 1
                            st.success("Réservation effectuée avec succès!")
                        else:
                            st.error("Ce livre n'est plus disponible.")

with tab3:  # Emplacements
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Gestion des Emplacements")
        if st.button("➕ Nouvel Emplacement", use_container_width=True):
            st.session_state.show_add_location_form = True
            st.session_state.show_edit_location_form = False
        
        if st.button("📍 Liste des Emplacements", use_container_width=True):
            st.session_state.show_add_location_form = False
            st.session_state.show_edit_location_form = False

    with col2:
        if st.session_state.show_add_location_form:
            st.subheader("Ajouter un nouvel emplacement")
            with st.form("add_location_form"):
                code = st.text_input("Code étagère*")
                section = st.text_input("Section")
                etage = st.number_input("Étage", min_value=0)
                description = st.text_area("Description")
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("Enregistrer")
                with col2:
                    cancel = st.form_submit_button("Annuler")

                if submit and code.strip():
                    new_location = {
                        "code": code,
                        "section": section,
                        "etage": etage,
                        "description": description
                    }
                    st.session_state.locations.append(new_location)
                    st.success("Emplacement ajouté avec succès!")
                    st.session_state.show_add_location_form = False

        # Formulaire de modification
        elif st.session_state.show_edit_location_form and st.session_state.locations:
            st.subheader("Modifier un emplacement")
            location_to_edit = st.selectbox("Sélectionner l'emplacement à modifier",
                [l['code'] for l in st.session_state.locations])
            
            location = next((l for l in st.session_state.locations if l['code'] == location_to_edit), None)
            if location:
                with st.form("edit_location_form"):
                    code = st.text_input("Code étagère*", value=location['code'])
                    section = st.text_input("Section", value=location['section'])
                    etage = st.number_input("Étage", min_value=0, value=location['etage'])
                    description = st.text_area("Description", value=location['description'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        submit = st.form_submit_button("Mettre à jour")
                    with col2:
                        cancel = st.form_submit_button("Annuler")

                    if submit and code.strip():
                        # Mise à jour de l'emplacement
                        location.update({
                            "code": code,
                            "section": section,
                            "etage": etage,
                            "description": description
                        })
                        st.success("Emplacement mis à jour avec succès!")
                        st.session_state.show_edit_location_form = False
                    elif submit:
                        st.error("Le code étagère est obligatoire!")
                    
                    if cancel:
                        st.session_state.show_edit_location_form = False

        # Affichage de la liste des emplacements
        if not st.session_state.show_add_location_form and not st.session_state.show_edit_location_form:
            st.subheader("Liste des emplacements")
            if st.session_state.locations:
                for location in st.session_state.locations:
                    with st.expander(f"📍 {location['code']}"):
                        st.write(f"Section: {location['section']}")
                        st.write(f"Étage: {location['etage']}")
                        st.write(f"Description: {location['description']}")
            else:
                st.info("Aucun emplacement enregistré pour le moment.")
with tab4:  # Auteurs
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Gestion des Auteurs")
        if st.button("➕ Nouvel Auteur", use_container_width=True):
            st.session_state.show_add_author_form = True
            st.session_state.show_edit_author_form = False
        
        if st.button("👥 Liste des Auteurs", use_container_width=True):
            st.session_state.show_add_author_form = False
            st.session_state.show_edit_author_form = False

    with col2:
        if st.session_state.show_add_author_form:
            st.subheader("Ajouter un nouvel auteur")
            with st.form("add_author_form"):
                nom = st.text_input("Nom complet*")
                nationalite = st.text_input("Nationalité")
                biographie = st.text_area("Biographie")
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("Enregistrer")
                with col2:
                    cancel = st.form_submit_button("Annuler")

                if submit and nom.strip():
                    new_author = {
                        "nom": nom,
                        "nationalite": nationalite,
                        "biographie": biographie
                    }
                    st.session_state.authors.append(new_author)
                    st.success("Auteur ajouté avec succès!")
                    st.session_state.show_add_author_form = False

        # Formulaire de modification
        elif st.session_state.show_edit_author_form and st.session_state.authors:
            st.subheader("Modifier un auteur")
            author_to_edit = st.selectbox("Sélectionner l'auteur à modifier",
                [a['nom'] for a in st.session_state.authors])
            
            author = next((a for a in st.session_state.authors if a['nom'] == author_to_edit), None)
            if author:
                with st.form("edit_author_form"):
                    nom = st.text_input("Nom complet*", value=author['nom'])
                    nationalite = st.text_input("Nationalité", value=author['nationalite'])
                    biographie = st.text_area("Biographie", value=author['biographie'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        submit = st.form_submit_button("Mettre à jour")
                    with col2:
                        cancel = st.form_submit_button("Annuler")

                    if submit and nom.strip():
                        # Mise à jour de l'auteur
                        author.update({
                            "nom": nom,
                            "nationalite": nationalite,
                            "biographie": biographie
                        })
                        st.success("Auteur mis à jour avec succès!")
                        st.session_state.show_edit_author_form = False
                    elif submit:
                        st.error("Le nom est obligatoire!")
                    
                    if cancel:
                        st.session_state.show_edit_author_form = False

        # Affichage de la liste des auteurs
        if not st.session_state.show_add_author_form and not st.session_state.show_edit_author_form:
            st.subheader("Liste des auteurs")
            if st.session_state.authors:
                for author in st.session_state.authors:
                    with st.expander(f"✍️ {author['nom']}"):
                        st.write(f"Nationalité: {author['nationalite']}")
                        st.write(f"Biographie: {author['biographie']}")
            else:
                st.info("Aucun auteur enregistré pour le moment.")
with tab5:
    st.subheader("Statistiques avancées")
    st.write("Ici, vous pouvez afficher des statistiques détaillées sur les emprunts, les retards, et plus encore.")

# --- Début ajout : interface Messagerie ---
with tab6:
    st.subheader("Messagerie (Membres ↔ Admin)")
    
    # Affichage des messages
    if st.session_state.chat_messages:
        for msg in st.session_state.chat_messages:
            ts = msg.get("ts", "")
            sender = msg["sender"]
            role = msg["role"]
            
            with st.container():
                st.markdown(f"**{sender} — {ts}**")
                
                if msg["type"] == "text":
                    st.markdown(f"> {msg['content']}")
                elif msg["type"] == "audio":
                    st.audio(msg["content"])
                elif msg["type"] == "image":
                    st.image(msg["content"], caption=f"Image de {sender}")
    else:
        st.info("Aucun message pour le moment.")

    st.divider()
    # Interface d'envoi
    st.write("Envoyer un message")
    
    tab_text, tab_audio, tab_image = st.tabs(["Texte", "Audio", "Image"])
    
    with tab_text:
        with st.form("text_message_form"):
            text = st.text_area("Message")
            submit_text = st.form_submit_button("Envoyer texte")
            if submit_text and text:
                st.session_state.chat_messages.append({
                    "sender": st.session_state.user,
                    "role": st.session_state.get("role","member"),
                    "type": "text",
                    "content": text,
                    "ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success("Message envoyé")

    with tab_audio:
        audio_file = st.file_uploader("Choisir un fichier audio", type=['wav', 'mp3', 'ogg'])
        if audio_file is not None:
            st.audio(audio_file)
            if st.button("📤 Envoyer l'audio"):
                audio_bytes = audio_file.read()
                st.session_state.chat_messages.append({
                    "sender": st.session_state.user,
                    "role": st.session_state.get("role","member"),
                    "type": "audio",
                    "content": audio_bytes,
                    "ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success("Audio envoyé!")

    with tab_image:
        uploaded_file = st.file_uploader("Choisir une image", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Aperçu de l\'image')
            if st.button("📤 Envoyer l'image"):
                # Convertir l'image en bytes pour le stockage
                img_buffer = io.BytesIO()
                image.save(img_buffer, format="PNG")
                
                st.session_state.chat_messages.append({
                    "sender": st.session_state.user,
                    "role": st.session_state.get("role","member"),
                    "type": "image",
                    "content": img_buffer.getvalue(),
                    "ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success("Image envoyée!")

# Ajouter dans la sidebar pour l'admin
with st.sidebar:
    if st.session_state.get("role") == "admin":
        st.divider()
        st.subheader("Réservations en attente")
        pending = [r for r in st.session_state.reservations if r['statut'] == "En attente"]
        if pending:
            for res in pending:
                with st.expander(f"📚 {res['livre']} - {res['membre']}"):
                    st.write(f"Date: {res['date_debut']}")
                    st.write(f"Durée: {res['duree']} jours")
                    if st.button("✅ Approuver", key=f"apr_{res['date_reservation']}"):
                        res['statut'] = "Approuvé"
                        st.success("Réservation approuvée!")
                    if st.button("❌ Refuser", key=f"ref_{res['date_reservation']}"):
                        res['statut'] = "Refusé"
                        # Remettre le livre en stock
                        book = next((b for b in st.session_state.books if b['titre'] == res['livre']), None)
                        if book:
                            book['quantite'] += 1
                        st.error("Réservation refusée!")
        else:
            st.info("Aucune réservation en attente")
# Sidebar
st.sidebar.title("Navigation")


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
