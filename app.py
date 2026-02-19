import streamlit as st
import pandas as pd
from fpdf import FPDF
import unicodedata

st.set_page_config(page_title="Suivi de Paie Pro", page_icon="🏗️")

# --- LIEN GOOGLE SHEETS (Mettez le vôtre ici) ---
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

def safe_str(text):
    """Nettoie le texte pour éviter les erreurs PDF"""
    s = str(text)
    return "".join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').replace('\u202f', ' ').replace('\xa0', ' ')

def create_pdf(name, matricule, solde, history_dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"Recapitulatif de Paie - {safe_str(name)}", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Matricule : {safe_str(matricule)}", ln=True)
    pdf.cell(200, 10, f"Solde Total : {safe_str(solde)} DH", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Detail des semaines :", ln=True)
    
    pdf.set_font("Arial", size=12)
    for sem, val in history_dict.items():
        pdf.cell(200, 10, f"- {safe_str(sem)} : {safe_str(val)}", ln=True)
    
    return pdf.output(dest="S").encode("latin-1", errors="replace")

st.title("🏗️ Espace Salarié - Chantier")

matricule_saisi = st.text_input("Entrez votre Matricule").strip()

if matricule_saisi:
    df = load_data()
    if df is not None:
        df['Matricule'] = df['Matricule'].astype(str).str.strip()
        user_data = df[df['Matricule'] == matricule_saisi]
        
        if not user_data.empty:
            row = user_data.iloc[0]
            st.success(f"✅ Salarié : {row['Nom']}")
            st.metric("Solde Total", f"{row['Solde']} DH")

            st.subheader("📅 Historique")
            cols_semaines = [c for c in df.columns if "Semaine" in c]
            history = {}
            for sem in cols_semaines:
                st.write(f"**{sem}** : {row[sem]}")
                history[sem] = row[sem]
            
            st.markdown("---")
            
            # Génération du bouton PDF
            try:
                pdf_data = create_pdf(row['Nom'], row['Matricule'], row['Solde'], history)
                st.download_button(
                    label="📥 Télécharger mon récapitulatif (PDF)",
                    data=pdf_data,
                    file_name=f"Paye_{matricule_saisi}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Erreur technique PDF. Essayez de simplifier les noms dans Excel.")
            
            if "Message" in row and str(row['Message']) not in ["0", "nan", ""]:
                st.warning(f"💬 Note : {row['Message']}")
        else:
            st.error("❌ Matricule inconnu.")
