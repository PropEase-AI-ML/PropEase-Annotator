import streamlit as st
import pandas as pd
import os
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(page_title="Document Annotator", layout="wide")

st.title("📄 PropEase - Document Classification Annotator")

st.markdown("### Upload documents and annotate them with labels and comments.")

st.markdown("#### Available Document Classes")

class_labels = {
    "EPC (Energy Performance Certificate)": "A rating of the building's energy efficiency",
    "EPB (Energy Performance of Buildings)": "Compliance documentation for energy regulations",
    "Asbestos Report": "Mandatory documentation assessing the presence of asbestos",
    "Environmental Assessment": "Reports on soil, water, or other environmental risks",
    "Fire Safety Certificates": "Compliance documentation with fire regulations",
    "Lift Inspection Reports": "Maintenance and safety inspection reports for elevators",
    "Boiler Inspection Reports": "Compliance with heating installation requirements",
    "Electrical Inspection Reports": "Certification for electrical safety and compliance",
    "Water Quality Certification": "If applicable, particularly for drinking water or pools",
    "Accessibility Compliance Report": "Ensuring adherence to laws for disabled access"
}

with st.expander("ℹ️ Click here to see available document classes"):
    for label, description in class_labels.items():
        st.markdown(f"**{label}**: {description}")

st.markdown("### How to Annotate")
st.info(
    "1️⃣ Upload your document(s).  "
    "2️⃣ View the document preview on the left.  "
    "3️⃣ Select the correct label from the dropdown on the right.  "
    "4️⃣ Optionally, add any extra comments regarding the document.  "
    "5️⃣ Click 'Submit Annotation' to save your label and comment.  "
    "6️⃣ Download the annotated results as a CSV file."
)

# Upload documents
documents = st.file_uploader("📤 Upload your documents", accept_multiple_files=True, type=["txt", "pdf"], help="Upload text or PDF files for annotation.")

# Store labeled data
if "labeled_data" not in st.session_state:
    st.session_state.labeled_data = []

# Display documents for annotation
if documents:
    for idx, doc in enumerate(documents):
        st.markdown("---")
        st.subheader(f"📄 {doc.name}")
        
        col1, col2 = st.columns([3, 2], gap="large")
        
        with col1:
            st.markdown("#### 📑 Document Preview")
            if doc.type == "text/plain":
                try:
                    content = doc.getvalue().decode("utf-8")
                    st.text_area("Document Content", content, height=300, disabled=True, key=f"text_area_{idx}")
                except UnicodeDecodeError:
                    st.error("❌ Cannot display this text file. Try another format.")
            elif doc.type == "application/pdf":
                pdf_data = doc.read()
                pdf_viewer(input=pdf_data, width=500, height=600)
        
        with col2:
            st.markdown("#### 🏷️ Annotation")
            label = st.selectbox("Select the appropriate category", list(class_labels.keys()), key=f"label_input_{idx}")
            comment = st.text_area("✍️ Additional Comments", "", height=120, key=f"comment_input_{idx}")
            
            if st.button("✅ Save Annotation", key=f"submit_btn_{idx}"):
                st.session_state.labeled_data.append({"document": doc.name, "label": label, "comment": comment})
                st.success(f"✅ Annotation saved for {doc.name}!")

# Export labeled data to CSV
if st.session_state.labeled_data:
    df = pd.DataFrame(st.session_state.labeled_data)
    st.download_button(
        "📥 Download Annotations as CSV", df.to_csv(index=False), "labeled_documents.csv", "text/csv"
    )
