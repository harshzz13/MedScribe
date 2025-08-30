import re
import string
from typing import List

class TextProcessor:
    """
    Text processing utilities for medical documents
    """
    
    def __init__(self):
        # Common medical abbreviations and their expansions
        self.medical_abbreviations = {
            'pt': 'patient',
            'pts': 'patients',
            'hx': 'history',
            'dx': 'diagnosis',
            'tx': 'treatment',
            'rx': 'prescription',
            'sx': 'symptoms',
            'f/u': 'follow-up',
            'w/': 'with',
            'w/o': 'without',
            'c/o': 'complains of',
            'r/o': 'rule out',
            'sob': 'shortness of breath',
            'cp': 'chest pain',
            'bp': 'blood pressure',
            'hr': 'heart rate',
            'rr': 'respiratory rate',
            'temp': 'temperature',
            'wbc': 'white blood cell count',
            'rbc': 'red blood cell count',
            'hgb': 'hemoglobin',
            'hct': 'hematocrit',
            'bun': 'blood urea nitrogen',
            'cr': 'creatinine',
            'na': 'sodium',
            'k': 'potassium',
            'cl': 'chloride',
            'co2': 'carbon dioxide',
            'mg': 'magnesium',
            'po': 'by mouth',
            'iv': 'intravenous',
            'im': 'intramuscular',
            'bid': 'twice daily',
            'tid': 'three times daily',
            'qid': 'four times daily',
            'qd': 'once daily',
            'prn': 'as needed',
            'hs': 'at bedtime',
            'ac': 'before meals',
            'pc': 'after meals'
        }
        
        # Common section headers in medical reports
        self.section_headers = [
            'chief complaint', 'history of present illness', 'past medical history',
            'medications', 'allergies', 'social history', 'family history',
            'review of systems', 'physical examination', 'assessment',
            'plan', 'discharge summary', 'impression', 'recommendations',
            'procedures', 'laboratory results', 'imaging', 'vital signs'
        ]
    
    def clean_text(self, text: str) -> str:
        """
        Clean and preprocess medical text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common OCR artifacts and formatting
        text = re.sub(r'[^\w\s\.,;:!?\-\(\)\/]', '', text)
        
        # Expand medical abbreviations
        text = self._expand_abbreviations(text)
        
        # Clean up punctuation
        text = self._clean_punctuation(text)
        
        # Remove PHI patterns (basic patterns for demo)
        text = self._remove_phi_patterns(text)
        
        return text
    
    def _expand_abbreviations(self, text: str) -> str:
        """
        Expand common medical abbreviations
        """
        words = text.split()
        expanded_words = []
        
        for word in words:
            clean_word = word.lower().strip(string.punctuation)
            if clean_word in self.medical_abbreviations:
                # Preserve original punctuation
                punctuation = ''.join([c for c in word if c in string.punctuation])
                expanded_words.append(self.medical_abbreviations[clean_word] + punctuation)
            else:
                expanded_words.append(word)
        
        return ' '.join(expanded_words)
    
    def _clean_punctuation(self, text: str) -> str:
        """
        Clean and normalize punctuation
        """
        # Fix spacing around punctuation
        text = re.sub(r'\s*([,.;:!?])\s*', r'\1 ', text)
        
        # Remove multiple consecutive punctuation
        text = re.sub(r'([,.;:!?]){2,}', r'\1', text)
        
        # Ensure sentences end with proper punctuation
        sentences = text.split('.')
        cleaned_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and not sentence[-1] in '.!?':
                sentence += '.'
            if sentence:
                cleaned_sentences.append(sentence)
        
        return ' '.join(cleaned_sentences)
    
    def _remove_phi_patterns(self, text: str) -> str:
        """
        Remove basic PHI patterns (simplified for demo)
        """
        # Remove potential SSN patterns
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)
        
        # Remove potential phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
        
        # Remove potential dates (keep only month/year for medical context)
        text = re.sub(r'\b\d{1,2}/\d{1,2}/\d{4}\b', '[DATE]', text)
        
        # Remove potential MRN patterns
        text = re.sub(r'\bMRN:?\s*\d+\b', '[MRN]', text, flags=re.IGNORECASE)
        
        return text
    
    def extract_sections(self, text: str) -> dict:
        """
        Extract different sections from medical text
        """
        sections = {}
        text_lower = text.lower()
        
        for header in self.section_headers:
            headers_pattern = r'\b' + r'\b|\b'.join([re.escape(h) for h in self.section_headers]) + r'\b'
            pattern = rf'\b{re.escape(header)}:?\s*\n?(.*?)(?=\n\s*(?:{headers_pattern})|$)'
            match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            
            if match:
                content = match.group(1).strip()
                if content:
                    sections[header] = content
        
        return sections
    
    def extract_key_information(self, text: str) -> dict:
        """
        Extract key medical information from text
        """
        info = {
            'medications': [],
            'procedures': [],
            'diagnoses': [],
            'vital_signs': {},
            'recommendations': []
        }
        
        # Extract medications (basic pattern matching)
        med_patterns = [
            r'\b(\w+)\s+\d+\s*mg\b',
            r'\b(\w+)\s+\d+\s*mcg\b',
            r'\b(\w+)\s+tablet\b',
            r'\b(\w+)\s+capsule\b'
        ]
        
        for pattern in med_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            info['medications'].extend([med.title() for med in matches])
        
        # Extract procedures (common medical procedures)
        procedure_keywords = [
            'catheterization', 'angioplasty', 'surgery', 'biopsy', 'endoscopy',
            'bronchoscopy', 'colonoscopy', 'echocardiogram', 'CT scan', 'MRI',
            'X-ray', 'ultrasound', 'blood transfusion', 'dialysis'
        ]
        
        for keyword in procedure_keywords:
            if keyword.lower() in text.lower():
                info['procedures'].append(keyword.title())
        
        # Extract vital signs
        vital_patterns = {
            'blood_pressure': r'bp:?\s*(\d+/\d+)',
            'heart_rate': r'hr:?\s*(\d+)',
            'temperature': r'temp:?\s*(\d+\.?\d*)',
            'respiratory_rate': r'rr:?\s*(\d+)'
        }
        
        for vital, pattern in vital_patterns.items():
            match = re.search(pattern, text.lower())
            if match:
                info['vital_signs'][vital] = match.group(1)
        
        # Remove duplicates
        info['medications'] = list(set(info['medications']))
        info['procedures'] = list(set(info['procedures']))
        
        return info
