import streamlit as st
import pandas as pd
import os
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(page_title="Document Annotator", layout="wide")

st.title("📄 Document Classification Annotator")

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
    "2️⃣ Select one document at a time from the list.  "
    "3️⃣ View the preview and choose one or more labels.  "
    "4️⃣ Optionally, add a custom label and comments.  "
    "5️⃣ Save your annotation.  "
    "6️⃣ Download all annotations as CSV."
)

# Upload documents
documents = st.file_uploader("📤 Upload your documents", accept_multiple_files=True, type=["txt", "pdf"], help="Upload text or PDF files for annotation.")

# Store labeled data
if "labeled_data" not in st.session_state:
    st.session_state.labeled_data = []

# Track which documents have been annotated
annotated_docs = {entry["document"] for entry in st.session_state.labeled_data}

# Toggle: Show only unannotated
show_unannotated_only = st.checkbox("🔍 Show only unannotated documents", value=True)

# Render one document at a time using selectbox
if documents:
    doc_names = [doc.name for doc in documents if not show_unannotated_only or doc.name not in annotated_docs]

    if doc_names:
        selected_doc_name = st.selectbox("📂 Select a document to annotate", doc_names)
        selected_doc = next(doc for doc in documents if doc.name == selected_doc_name)
        idx = [doc.name for doc in documents].index(selected_doc_name)

        st.markdown("---")
        st.subheader(f"📄 {selected_doc.name}")

        col1, col2 = st.columns([3, 2], gap="large")

        with col1:
            st.markdown("#### 📑 Document Preview")
            if selected_doc.type == "text/plain":
                try:
                    content = selected_doc.getvalue().decode("utf-8")
                    st.text_area("Document Content", content, height=300, disabled=True, key=f"text_area_{idx}")
                except UnicodeDecodeError:
                    st.error("❌ Cannot display this text file. Try another format.")
            elif selected_doc.type == "application/pdf":
                pdf_data = selected_doc.read()
                pdf_viewer(input=pdf_data, width=1000, height=1200, key=f"pdf_viewer_{idx}")

        with col2:
            st.markdown("#### 🏷️ Annotation")
            selected_labels = st.multiselect("Select one or more categories", list(class_labels.keys()), key=f"multi_label_input_{idx}")
            custom_label = st.text_input("➕ Custom Label (optional)", key=f"custom_label_input_{idx}")
            comment = st.text_area("✍️ Additional Comments", "", height=120, key=f"comment_input_{idx}")

            if st.button("✅ Save Annotation", key=f"submit_btn_{idx}"):
                labels = selected_labels.copy()
                if custom_label:
                    labels.append(custom_label)
                label_string = "; ".join(labels)
                st.session_state.labeled_data.append({"document": selected_doc.name, "labels": label_string, "comment": comment})
                st.success(f"✅ Annotation saved for {selected_doc.name}!")
    else:
        st.info("🎉 All documents have been annotated!")

# Export labeled data to CSV
if st.session_state.labeled_data:
    df = pd.DataFrame(st.session_state.labeled_data)
    st.download_button(
        "📥 Download Annotations as CSV", df.to_csv(index=False), "labeled_documents.csv", "text/csv"
    )
