import streamlit as st
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Suivi de Paie Pro", page_icon="🏗️")

# Votre lien CSV
sheet_url = "VOTRE_LIEN_CSV_ICI"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()
        df = df.fillna("0")
        return df
    except:
        return None

# Fonction pour créer le PDF
def create_pdf(name, matricule, solde, history_dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"Recapitulatif de Paie - {name}", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Matricule : {matricule}", ln=True)
    pdf.cell(200, 10, f"Solde Total a percevoir : {solde} DH", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Detail des semaines :", ln=True)
    pdf.set_font("Arial", size=12)
    for sem, val in history_dict.items():
        pdf.cell(200, 10, f"- {sem} : {val}", ln=True)
    return pdf.output(dest="S").encode("latin-1")

st.title("🏗️ Espace Salarié - Chantier")

matricule_saisi = st.text_input("Entrez votre Matricule", type="default").strip()

if matricule_saisi:
    df = load_data()
    if df is not None:
        df['Matricule'] = df['Matricule'].astype(str)
        user_data = df[df['Matricule'] == matricule_saisi]
        
        if not user_data.empty:
            row = user_data.iloc[0]
            st.success(f"✅ Salarié : {row['Nom']}")

            # Affichage du Solde
            st.metric("Solde Total", f"{row['Solde']} DH")

            # Historique
            st.subheader("📅 Historique des pointages")
            cols_semaines = [c for c in df.columns if "Semaine" in c]
            history = {}
            if cols_semaines:
                for sem in cols_semaines:
                    st.write(f"**{sem}** : {row[sem]}")
                    history[sem] = row[sem]
            
            st.markdown("---")
            
            # Bouton PDF
            pdf_bytes = create_pdf(row['Nom'], row['Matricule'], row['Solde'], history)
            st.download_button(
                label="📥 Télécharger mon récapitulatif (PDF)",
                data=pdf_bytes,
                file_name=f"Paye_{row['Nom']}.pdf",
                mime="application/pdf"
            )
            
            if "Message" in row and row['Message'] not in ["0", "nan", ""]:
                st.warning(f"💬 Note : {row['Message']}")
        else:
            st.error("❌ Matricule inconnu.")
