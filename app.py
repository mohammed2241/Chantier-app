import streamlit as st
import pandas as pd

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Mon Chantier", page_icon="🏗️")

# --- VOTRE LIEN GOOGLE SHEETS ---
# Remplacez le lien ci-dessous par VOTRE lien (celui qui finit par .csv)
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSITcdQPLoiYFNsZAcd9ogxfeb6oCyWf4-L3hBXOrypOUm-g2AZ4S60VpNu0PpJlMf7i1JScEMnci95/pubhtml"

# --- FONCTION POUR CHARGER LES DONNÉES ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(sheet_url)
        # On s'assure que le Matricule est lu comme du texte (pas un nombre)
        df['Matricule'] = df['Matricule'].astype(str)
        return df
    except Exception as e:
        st.error("Erreur de connexion au fichier Excel.")
        return None

# --- INTERFACE DE L'APPLICATION ---
st.title("🏗️ Chantier Connect")
st.write("Bienvenue. Entrez votre matricule pour voir votre solde.")

# Champ de saisie du mot de passe
matricule_input = st.text_input("Votre Matricule (Code Secret)", type="password")

if matricule_input:
    df = load_data()
    
    if df is not None:
        # On cherche la ligne qui correspond au matricule
        user_row = df[df['Matricule'] == matricule_input]
        
        if not user_row.empty:
            # On récupère les infos de la première ligne trouvée
            nom = user_row.iloc[0]['Nom']
            jours = user_row.iloc[0]['Jours']
            solde = user_row.iloc[0]['Solde']
            message = user_row.iloc[0]['Message']
            
            # --- AFFICHAGE DES RÉSULTATS ---
            st.success(f"Salam, {nom} 👋")
            
            # On crée 2 colonnes pour faire joli
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(label="Jours Travaillés", value=f"{jours} Jours")
            
            with col2:
                st.metric(label="Net à Payer", value=f"{solde} DH")
            
            if pd.notna(message):
                st.info(f"Message du bureau : {message}")
                
        else:
            st.error("❌ Matricule incorrect. Essayez encore.")

# Pied de page discret
st.markdown("---")
st.caption("Système sécurisé - Direction du Chantier")
