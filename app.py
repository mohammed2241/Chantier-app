import streamlit as st
import pandas as pd
from fpdf import FPDF
import unicodedata

st.set_page_config(page_title="Suivi de Paie Pro", page_icon="🏗️")

# --- REMPLACEZ LE LIEN CI-DESSOUS ---
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSITcdQPLoiYFNsZAcd9ogxfeb6oCyWf4-L3hBXOrypOUm-g2AZ4S60VpNu0PpJlMf7i1JScEMnci95/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()
        df = df.fillna("0")
        return df
    except:
        return None

# Fonction pour nettoyer les accents (évite le plantage du PDF)
def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    return "".join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

# Fonction de création du PDF
def create_pdf(name, matricule, solde, history_dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    name_clean = clean_text(name)
    pdf.cell(200, 10, f"Recapitulatif de Paie - {name_clean}", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Matricule : {clean_text(matricule)}", ln=True)
    pdf.cell(200, 10, f"Solde Total a percevoir : {solde} DH", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Detail des semaines :", ln=True)
    
    pdf.set_font("Arial", size=12)
    for sem, val in history_dict.items():
        pdf.cell(200, 10, f"- {clean_text(sem)} : {clean_text(val)}", ln=True)
    
    return pdf.output(dest="S").encode("latin-1")

st.title("🏗️ Espace Salarié - Chantier")
st.write("Consultez vos jours travaillés et téléchargez votre reçu.")

matricule_saisi = st.text_input("Entrez votre Matricule", type="default").strip()

if matricule_saisi:
    df = load_data()
    if df is not None:
        # Nettoyage automatique du matricule pour éviter les erreurs de frappe
        df['Matricule'] = df['Matricule'].astype(str).str.strip()
        user_data = df[df['Matricule'] == matricule_saisi]
        
        if not user_data.empty:
            row = user_data.iloc[0]
            st.success(f"✅ Salarié : {row['Nom']}")

            # Affichage du Solde Principal
            st.metric("Solde Total à percevoir", f"{row['Solde']} DH")

            # Affichage de l'Historique (Semaines)
            st.subheader("📅 Historique des pointages")
            cols_semaines = [c for c in df.columns if "Semaine" in c]
            history = {}
            for sem in cols_semaines:
                st.write(f"**{sem}** : {row[sem]}")
                history[sem] = row[sem]
            
            st.markdown("---")
            
            # BOUTON DE TÉLÉCHARGEMENT PDF
            try:
                pdf_bytes = create_pdf(row['Nom'], row['Matricule'], row['Solde'], history)
                st.download_button(
                    label="📥 Télécharger mon récapitulatif (PDF)",
                    data=pdf_bytes,
                    file_name=f"Paye_{clean_text(row['Nom'])}.pdf",
                    mime="application/pdf"
