import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Consultation Salaire Chantier", page_icon="🏗️")

# LIEN GOOGLE SHEETS (Assurez-vous d'avoir bien mis le lien .csv ici)
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSITcdQPLoiYFNsZAcd9ogxfeb6oCyWf4-L3hBXOrypOUm-g2AZ4S60VpNu0PpJlMf7i1JScEMnci95/pub?output=csv"

@st.cache_data(ttl=600) # Rafraîchit les données toutes les 10 min
def load_data():
    try:
        # Lecture du CSV
        df = pd.read_csv(sheet_url)
        # Nettoyage des noms de colonnes au cas où il y aurait des espaces
        df.columns = df.columns.str.strip()
        # On force tout en texte pour la comparaison
        df = df.astype(str)
        return df
    except Exception as e:
        st.error("⚠️ Connexion à la base de données impossible. Vérifiez le lien .csv")
        return None

# Interface
st.title("🏗️ Espace Salarié - Chantier")
st.write("Entrez votre matricule pour consulter vos informations.")

matricule_saisi = st.text_input("Matricule (ex: AX7K9P2L)", type="default").strip()

if matricule_saisi:
    df = load_data()
    
    if df is not None:
        # Recherche du matricule
        user_data = df[df['Matricule'] == matricule_saisi]
        
        if not user_data.empty:
            row = user_data.iloc[0]
            st.success(f"✅ Bienvenue, {row['Nom']}")
            
            # Affichage des compteurs
            c1, c2 = st.columns(2)
            c1.metric("Jours Travaillés", f"{row['Jours']} j")
            c2.metric("Solde à percevoir", f"{row['Solde']} DH")
            
            # Message si présent
            if row['Message'] != "nan" and row['Message'] != "":
                st.info(f"💬 Message : {row['Message']}")
        else:
            st.error("❌ Matricule non trouvé. Vérifiez votre saisie.")

st.markdown("---")
st.caption("Actualisé en temps réel à partir du bureau de pointage.")
