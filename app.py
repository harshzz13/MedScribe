import streamlit as st
import tempfile
import os
from utils.text_processor import TextProcessor
from utils.summarizer import MedicalSummarizer
from utils.pdf_extractor import PDFExtractor

# Page configuration
st.set_page_config(
    page_title="Medical Report Summarizer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🏥 Medical Report Summarizer")
    st.markdown("Convert lengthy medical documents into concise summaries for both doctors and patients")
    
    # Initialize processors
    text_processor = TextProcessor()
    summarizer = MedicalSummarizer()
    pdf_extractor = PDFExtractor()
    
    # Sidebar
    with st.sidebar:
        st.header("Instructions")
        st.markdown("""
        1. Upload a medical report (TXT or PDF)
        2. Select summary type
        3. Review generated summaries
        
        **Privacy Notice**: Files are processed locally and not stored.
        """)
        
        # Summary options
        st.subheader("Summary Options")
        summary_length = st.selectbox(
            "Summary Length",
            ["Short (2-3 sentences)", "Medium (4-5 sentences)", "Long (6-8 sentences)"]
        )
        
        include_medications = st.checkbox("Include medications", value=True)
        include_procedures = st.checkbox("Include procedures", value=True)
        include_recommendations = st.checkbox("Include recommendations", value=True)
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Upload Medical Report")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["txt", "pdf"],
            help="Upload TXT or PDF medical reports"
        )
        
        if uploaded_file is not None:
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # Process file
            try:
                if uploaded_file.type == "application/pdf":
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    try:
                        text_content = pdf_extractor.extract_text(tmp_file_path)
                    finally:
                        os.unlink(tmp_file_path)
                else:
                    text_content = str(uploaded_file.read(), "utf-8")
                
                if not text_content.strip():
                    st.error("The uploaded file appears to be empty or the text could not be extracted.")
                    return
                
                # Display original text in expandable section
                with st.expander("View Original Text"):
                    st.text_area("Original Content", text_content, height=200, disabled=True)
                
                # Process text
                processed_text = text_processor.clean_text(text_content)
                
                if not processed_text.strip():
                    st.error("No meaningful text could be extracted from the document.")
                    return
                
                # Generate summaries
                with st.spinner("Generating summaries..."):
                    options = {
                        'length': summary_length.split()[0].lower(),
                        'include_medications': include_medications,
                        'include_procedures': include_procedures,
                        'include_recommendations': include_recommendations
                    }
                    
                    doctor_summary = summarizer.generate_doctor_summary(processed_text, options)
                    patient_summary = summarizer.generate_patient_summary(processed_text, options)
                
                # Store summaries in session state for display
                st.session_state.doctor_summary = doctor_summary
                st.session_state.patient_summary = patient_summary
                st.session_state.original_length = len(text_content.split())
                st.session_state.doctor_length = len(doctor_summary.split())
                st.session_state.patient_length = len(patient_summary.split())
                
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                return
    
    with col2:
        st.subheader("Generated Summaries")
        
        if hasattr(st.session_state, 'doctor_summary'):
            # Statistics
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric("Original Words", st.session_state.original_length)
            with col_stat2:
                st.metric("Doctor Summary", st.session_state.doctor_length)
            with col_stat3:
                st.metric("Patient Summary", st.session_state.patient_length)
            
            # Doctor summary
            st.markdown("### 👨‍⚕️ Professional Summary")
            st.info("**For Healthcare Professionals**")
            st.markdown(st.session_state.doctor_summary)
            
            # Patient summary
            st.markdown("### 👤 Patient-Friendly Summary")
            st.info("**For Patients and Families**")
            st.markdown(st.session_state.patient_summary)
            
            # Download options
            st.markdown("### 📥 Download Summaries")
            col_download1, col_download2 = st.columns(2)
            
            with col_download1:
                st.download_button(
                    label="Download Doctor Summary",
                    data=st.session_state.doctor_summary,
                    file_name="doctor_summary.txt",
                    mime="text/plain"
                )
            
            with col_download2:
                st.download_button(
                    label="Download Patient Summary",
                    data=st.session_state.patient_summary,
                    file_name="patient_summary.txt",
                    mime="text/plain"
                )
        else:
            st.info("Upload a medical report to generate summaries")
            
            # Example format display
            st.markdown("### Example Output Format")
            
            with st.expander("Professional Summary Example"):
                st.markdown("""
                **Chief Complaint**: Chest pain and shortness of breath
                
                **Diagnosis**: Acute myocardial infarction (STEMI)
                
                **Treatment**: Emergency cardiac catheterization with stent placement
                
                **Medications**: Aspirin 81mg daily, Metoprolol 25mg BID, Atorvastatin 40mg daily
                
                **Follow-up**: Cardiology in 1 week, primary care in 2 weeks
                """)
            
            with st.expander("Patient-Friendly Summary Example"):
                st.markdown("""
                You came to the hospital because of chest pain and trouble breathing. 
                Tests showed you had a heart attack. Doctors opened the blocked blood vessel 
                in your heart and placed a small tube (stent) to keep it open. You've been 
                given medicines to protect your heart and prevent future problems. 
                Please follow up with your heart doctor next week and your regular doctor 
                in two weeks.
                """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>This tool is for educational purposes. "
        "Always consult healthcare professionals for medical advice.</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
