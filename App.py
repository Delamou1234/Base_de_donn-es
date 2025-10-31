import streamlit as st
#import mysql.connector
#from mysql.connector import Error
import datetime

# ...existing code...
# Configuration de la connexion à la base de données
#def create_db_connection():
#    try:
#        connection = mysql.connector.connect(
#            host="localhost",
#            user="root",
#            password="votre_mot_de_passe",
#            database="library_db"
#        )
#        return connection
#    except Error as e:
#        st.error(f"Erreur de connexion à MySQL: {e}")
#        return None

# Initialisation de la connexion
#conn = create_db_connection()

st.title("Base de données pour la gestion d'une bibliothèque")
st.write("""
Cette application Streamlit permet de gérer une base de données pour une bibliothèque.
Elle inclut des fonctionnalités pour ajouter, afficher, mettre à jour et supprimer des livres, des auteurs et des emprunteurs.
""")

# Initialiser l'état pour afficher le formulaire si nécessaire
if "show_add_member_form" not in st.session_state:
    st.session_state.show_add_member_form = False
if "members" not in st.session_state:
    st.session_state.members = []  # stockage temporaire en session

# les boutons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("➕ Nouveau membre", help="Ajouter un nouveau membre"):
        st.session_state.show_add_member_form = True
with col2:
    st.button("Afficher les membres", help="Voir la liste des membres")
with col3:
    st.button("Mettre à jour un membre", help="Modifier les informations d'un membre")   
with col4:
    st.button("Supprimer un membre", help="Retirer un membre de la bibliothèque")

# Formulaire d'ajout : s'affiche seulement quand on a cliqué sur "Nouveau membre"
if st.session_state.show_add_member_form:
    st.markdown("### ➕ Enregistrer un nouveau membre")
    with st.form("add_member_form"):
        nom = st.text_input("Nom complet")
        email = st.text_input("Email")
        telephone = st.text_input("Téléphone")
        adresse = st.text_area("Adresse")
        date_inscription = st.date_input("Date d'inscription", value=datetime.date.today())
        submit = st.form_submit_button("Enregistrer")
        cancel = st.form_submit_button("Annuler")

        if submit:
            if not nom.strip():
                st.error("Le nom est requis.")
            else:
                member = {
                    "nom": nom.strip(),
                    "email": email.strip(),
                    "telephone": telephone.strip(),
                    "adresse": adresse.strip(),
                    "date_inscription": str(date_inscription)
                }
                # Enregistrement temporaire en session
                st.session_state.members.append(member)

                # Option : insertion en base de données si create_db_connection() est activée
                # try:
                #     if conn is not None and conn.is_connected():
                #         cursor = conn.cursor()
                #         sql = "INSERT INTO members (nom, email, telephone, adresse, date_inscription) VALUES (%s, %s, %s, %s, %s)"
                #         cursor.execute(sql, (member["nom"], member["email"], member["telephone"], member["adresse"], member["date_inscription"]))
                #         conn.commit()
                #         cursor.close()
                # except Exception as e:
                #     st.warning(f"Impossible d'enregistrer en base: {e}")

                st.success("Membre enregistré avec succès.")
                st.session_state.show_add_member_form = False

        if cancel:
            st.session_state.show_add_member_form = False

# Afficher les membres en session (exemple)
if st.session_state.members:
    st.markdown("#### Membres enregistrés (session)")
    for i, m in enumerate(st.session_state.members, 1):
        st.write(f"{i}. {m['nom']} — {m.get('email','')} — {m.get('telephone','')}")

# Vérification de la connexion
#if conn is not None and conn.is_connected():
#    st.success("Connecté à la base de données MySQL!")
#else:
#    st.error("Échec de la connexion à la base de données")

st.write("Utilisez le menu de navigation pour accéder aux différentes fonctionnalités.")
st.badge("DELAMOU Samaké")
st.sidebar.info("Bibliothèque de gestion de la bibliothèque")
st.sidebar.button("Afficher les retard d'emprunt",help="Les membres qui ont retardés")
# ...existing code...