import streamlit as st
import pandas as pd

st.set_page_config(page_title="Consultation Salaire", page_icon="🏗️")

# Votre lien CSV (Vérifiez qu'il est bien à jour)
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSITcdQPLoiYFNsZAcd9ogxfeb6oCyWf4-L3hBXOrypOUm-g2AZ4S60VpNu0PpJlMf7i1JScEMnci95/pub?output=csv"

# On baisse le TTL à 60 secondes pour que vos modifs Excel s'affichent vite
@st.cache_data(ttl=60) 
def load_data():
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()
        # CETTE LIGNE remplace les vides (nan) par 0
        df = df.fillna("0")
        df = df.astype(str)
        return df
    except Exception as e:
        st.error("Erreur de connexion.")
        return None

st.title("🏗️ Espace Salarié - Chantier")

# Ici on change l'exemple pour correspondre à votre vrai tableau
matricule_saisi = st.text_input("Entrez votre Matricule (ex: *******)", type="default").strip()

if matricule_saisi:
    df = load_data()
    if df is not None:
        user_data = df[df['Matricule'] == matricule_saisi]
        
        if not user_data.empty:
            row = user_data.iloc[0]
            st.success(f"✅ Bienvenue, {row['Nom']}")
            
            c1, c2 = st.columns(2)
            # Affichage propre même si c'était vide
            jours_val = row['Jours'] if row['Jours'] != "nan" else "0"
            solde_val = row['Solde'] if row['Solde'] != "nan" else "0"
            
            c1.metric("Jours Travaillés", f"{jours_val} j")
            c2.metric("Solde à percevoir", f"{solde_val} DH")
            
            if "Message" in row and row['Message'] not in ["nan", "0", ""]:
                st.info(f"💬 Message : {row['Message']}")
        else:
            st.error("❌ Matricule non trouvé.")

st.markdown("---")
st.caption("Données actualisées toutes les minutes.")
