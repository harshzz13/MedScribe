import re
from typing import Dict, List
from utils.text_processor import TextProcessor

class MedicalSummarizer:
    """
    Rule-based medical text summarizer for generating doctor and patient summaries
    """
    
    def __init__(self):
        self.text_processor = TextProcessor()
        
        # Key sentence indicators for medical importance
        self.important_indicators = [
            'diagnosis', 'diagnosed', 'treatment', 'medication', 'procedure',
            'surgery', 'admission', 'discharge', 'follow-up', 'recommendation',
            'condition', 'symptoms', 'chief complaint', 'assessment', 'plan'
        ]
        
        # Patient-friendly medical term translations
        self.patient_translations = {
            'myocardial infarction': 'heart attack',
            'hypertension': 'high blood pressure',
            'diabetes mellitus': 'diabetes',
            'cerebrovascular accident': 'stroke',
            'pneumonia': 'lung infection',
            'gastroenteritis': 'stomach bug',
            'urinary tract infection': 'bladder infection',
            'angina': 'chest pain',
            'arrhythmia': 'irregular heartbeat',
            'tachycardia': 'fast heart rate',
            'bradycardia': 'slow heart rate',
            'dyspnea': 'trouble breathing',
            'syncope': 'fainting',
            'edema': 'swelling',
            'hemorrhage': 'bleeding',
            'fracture': 'broken bone',
            'laceration': 'cut',
            'contusion': 'bruise',
            'antibiotic': 'infection medicine',
            'analgesic': 'pain medicine',
            'catheterization': 'procedure to open blocked blood vessels',
            'angioplasty': 'procedure to open blocked blood vessels',
            'stent': 'small tube to keep blood vessels open',
            'biopsy': 'tissue sample test',
            'CT scan': 'detailed X-ray',
            'MRI': 'detailed body scan',
            'echocardiogram': 'heart ultrasound',
            'endoscopy': 'camera examination',
            'prognosis': 'outlook',
            'acute': 'sudden',
            'chronic': 'long-term'
        }
    
    def generate_doctor_summary(self, text: str, options: Dict) -> str:
        """
        Generate a professional summary for healthcare providers
        """
        # Extract key information
        key_info = self.text_processor.extract_key_information(text)
        sections = self.text_processor.extract_sections(text)
        
        # Identify important sentences
        important_sentences = self._extract_important_sentences(text, options['length'])
        
        # Build professional summary
        summary_parts = []
        
        # Add chief complaint/presentation if available
        if 'chief complaint' in sections:
            summary_parts.append(f"**Chief Complaint**: {sections['chief complaint'][:200]}...")
        
        # Add diagnosis information
        diagnosis_info = self._extract_diagnosis_info(text)
        if diagnosis_info:
            summary_parts.append(f"**Diagnosis**: {diagnosis_info}")
        
        # Add treatment information
        treatment_info = self._extract_treatment_info(text, key_info)
        if treatment_info:
            summary_parts.append(f"**Treatment**: {treatment_info}")
        
        # Add medications if requested
        if options['include_medications'] and key_info['medications']:
            meds = ', '.join(key_info['medications'][:5])  # Limit to 5 medications
            summary_parts.append(f"**Medications**: {meds}")
        
        # Add procedures if requested
        if options['include_procedures'] and key_info['procedures']:
            procedures = ', '.join(key_info['procedures'][:3])  # Limit to 3 procedures
            summary_parts.append(f"**Procedures**: {procedures}")
        
        # Add recommendations if requested
        if options['include_recommendations']:
            recommendations = self._extract_recommendations(text)
            if recommendations:
                summary_parts.append(f"**Follow-up**: {recommendations}")
        
        # Add vital signs if significant
        if key_info['vital_signs']:
            vitals = self._format_vitals(key_info['vital_signs'])
            if vitals:
                summary_parts.append(f"**Vital Signs**: {vitals}")
        
        # Combine summary parts
        summary = '\n\n'.join(summary_parts)
        
        # Ensure appropriate length
        summary = self._adjust_summary_length(summary, options['length'])
        
        return summary if summary else "Unable to generate professional summary from the provided text."
    
    def generate_patient_summary(self, text: str, options: Dict) -> str:
        """
        Generate a patient-friendly summary in plain language
        """
        # Extract key information
        key_info = self.text_processor.extract_key_information(text)
        
        # Build patient-friendly summary
        summary_parts = []
        
        # Explain reason for visit
        reason = self._extract_patient_reason(text)
        if reason:
            summary_parts.append(reason)
        
        # Explain what was found/diagnosed
        diagnosis = self._extract_patient_diagnosis(text)
        if diagnosis:
            summary_parts.append(diagnosis)
        
        # Explain treatment in simple terms
        treatment = self._extract_patient_treatment(text, key_info)
        if treatment:
            summary_parts.append(treatment)
        
        # Explain medications in simple terms
        if options['include_medications'] and key_info['medications']:
            med_explanation = self._explain_medications_to_patient(key_info['medications'])
            if med_explanation:
                summary_parts.append(med_explanation)
        
        # Explain next steps
        if options['include_recommendations']:
            next_steps = self._extract_patient_next_steps(text)
            if next_steps:
                summary_parts.append(next_steps)
        
        # Combine into flowing narrative
        summary = ' '.join(summary_parts)
        
        # Translate medical terms
        summary = self._translate_for_patients(summary)
        
        # Ensure appropriate length and tone
        summary = self._adjust_patient_summary(summary, options['length'])
        
        return summary if summary else "We are unable to create a simple summary of your medical report at this time. Please ask your doctor to explain your results."
    
    def _extract_important_sentences(self, text: str, length: str) -> List[str]:
        """
        Extract sentences containing important medical information
        """
        sentences = re.split(r'[.!?]+', text)
        important_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:  # Skip very short sentences
                continue
                
            # Score sentence based on important keywords
            score = 0
            sentence_lower = sentence.lower()
            
            for indicator in self.important_indicators:
                if indicator in sentence_lower:
                    score += 1
            
            if score > 0:
                important_sentences.append((sentence, score))
        
        # Sort by importance and select based on length preference
        important_sentences.sort(key=lambda x: x[1], reverse=True)
        
        max_sentences = {'short': 3, 'medium': 5, 'long': 8}.get(length, 5)
        return [sent[0] for sent in important_sentences[:max_sentences]]
    
    def _extract_diagnosis_info(self, text: str) -> str:
        """
        Extract diagnosis information from text
        """
        diagnosis_patterns = [
            r'diagnosis:?\s*([^.\n]+)',
            r'diagnosed with\s+([^.\n]+)',
            r'impression:?\s*([^.\n]+)',
            r'assessment:?\s*([^.\n]+)'
        ]
        
        for pattern in diagnosis_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_treatment_info(self, text: str, key_info: Dict) -> str:
        """
        Extract treatment information
        """
        treatment_patterns = [
            r'treatment:?\s*([^.\n]+)',
            r'treated with\s+([^.\n]+)',
            r'plan:?\s*([^.\n]+)'
        ]
        
        for pattern in treatment_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # If no explicit treatment found, use procedures
        if key_info['procedures']:
            return ', '.join(key_info['procedures'][:2])
        
        return ""
    
    def _extract_recommendations(self, text: str) -> str:
        """
        Extract follow-up recommendations
        """
        rec_patterns = [
            r'follow[-\s]?up:?\s*([^.\n]+)',
            r'recommendation:?\s*([^.\n]+)',
            r'discharge.*?instructions:?\s*([^.\n]+)'
        ]
        
        for pattern in rec_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _format_vitals(self, vitals: Dict) -> str:
        """
        Format vital signs for professional summary
        """
        vital_strings = []
        for vital, value in vitals.items():
            if vital == 'blood_pressure':
                vital_strings.append(f"BP {value}")
            elif vital == 'heart_rate':
                vital_strings.append(f"HR {value}")
            elif vital == 'temperature':
                vital_strings.append(f"Temp {value}°F")
            elif vital == 'respiratory_rate':
                vital_strings.append(f"RR {value}")
        
        return ', '.join(vital_strings)
    
    def _extract_patient_reason(self, text: str) -> str:
        """
        Extract reason for visit in patient-friendly language
        """
        patterns = [
            r'chief complaint:?\s*([^.\n]+)',
            r'presenting complaint:?\s*([^.\n]+)',
            r'came.*?because of\s+([^.\n]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                reason = match.group(1).strip()
                return f"You came to the hospital because of {reason.lower()}."
        
        return "You came to the hospital for medical care."
    
    def _extract_patient_diagnosis(self, text: str) -> str:
        """
        Extract diagnosis in patient-friendly language
        """
        diagnosis = self._extract_diagnosis_info(text)
        if diagnosis:
            return f"Tests and examinations showed that you have {diagnosis.lower()}."
        return ""
    
    def _extract_patient_treatment(self, text: str, key_info: Dict) -> str:
        """
        Extract treatment in patient-friendly language
        """
        treatment = self._extract_treatment_info(text, key_info)
        if treatment:
            return f"Doctors provided treatment including {treatment.lower()}."
        return ""
    
    def _explain_medications_to_patient(self, medications: List[str]) -> str:
        """
        Explain medications in patient-friendly terms
        """
        if not medications:
            return ""
        
        if len(medications) == 1:
            return f"You have been given medicine called {medications[0]} to help with your condition."
        else:
            med_list = ', '.join(medications[:3])  # Limit to 3 medications
            return f"You have been given medicines including {med_list} to help with your condition."
    
    def _extract_patient_next_steps(self, text: str) -> str:
        """
        Extract next steps in patient-friendly language
        """
        recommendations = self._extract_recommendations(text)
        if recommendations:
            return f"Please {recommendations.lower()}"
        return "Please follow up with your doctor as recommended."
    
    def _translate_for_patients(self, text: str) -> str:
        """
        Replace medical terms with patient-friendly language
        """
        for medical_term, patient_term in self.patient_translations.items():
            text = re.sub(r'\b' + re.escape(medical_term) + r'\b', patient_term, text, flags=re.IGNORECASE)
        
        return text
    
    def _adjust_summary_length(self, summary: str, length: str) -> str:
        """
        Adjust summary length based on preference
        """
        sentences = re.split(r'[.!?]+', summary)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        max_sentences = {'short': 3, 'medium': 5, 'long': 8}.get(length, 5)
        
        if len(sentences) > max_sentences:
            summary = '. '.join(sentences[:max_sentences]) + '.'
        
        return summary
    
    def _adjust_patient_summary(self, summary: str, length: str) -> str:
        """
        Adjust patient summary length and ensure appropriate tone
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', summary)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        max_sentences = {'short': 2, 'medium': 4, 'long': 6}.get(length, 4)
        
        if len(sentences) > max_sentences:
            summary = '. '.join(sentences[:max_sentences]) + '.'
        
        # Ensure summary ends appropriately
        if not summary.endswith('.'):
            summary += '.'
        
        return summary
