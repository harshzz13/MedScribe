import PyPDF2
import io
from typing import Optional

class PDFExtractor:
    """
    Extract text content from PDF files
    """
    
    def __init__(self):
        pass
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract text from PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            text_content = ""
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Check if PDF is encrypted
                if pdf_reader.is_encrypted:
                    # Try to decrypt with empty password
                    try:
                        pdf_reader.decrypt("")
                    except:
                        raise Exception("PDF is password protected and cannot be read")
                
                # Extract text from all pages
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    if page_text:
                        text_content += page_text + "\n"
                
                # Clean up the extracted text
                text_content = self._clean_extracted_text(text_content)
                
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
        
        return text_content
    
    def extract_text_from_bytes(self, pdf_bytes: bytes) -> str:
        """
        Extract text from PDF bytes
        
        Args:
            pdf_bytes: PDF file as bytes
            
        Returns:
            Extracted text content
        """
        try:
            text_content = ""
            
            pdf_file = io.BytesIO(pdf_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Check if PDF is encrypted
            if pdf_reader.is_encrypted:
                try:
                    pdf_reader.decrypt("")
                except:
                    raise Exception("PDF is password protected and cannot be read")
            
            # Extract text from all pages
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                if page_text:
                    text_content += page_text + "\n"
            
            # Clean up the extracted text
            text_content = self._clean_extracted_text(text_content)
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
        
        return text_content
    
    def _clean_extracted_text(self, text: str) -> str:
        """
        Clean up text extracted from PDF
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        import re
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Preserve paragraph breaks
        text = re.sub(r'[ \t]+', ' ', text)       # Normalize spaces
        
        # Remove common PDF artifacts
        text = re.sub(r'\x0c', '', text)          # Remove form feed characters
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)  # Remove control characters
        
        # Fix broken words (common in PDF extraction)
        text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)  # Rejoin hyphenated words
        
        # Clean up spacing around punctuation
        text = re.sub(r'\s+([,.;:!?])', r'\1', text)
        
        # Ensure single spaces between words
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def get_pdf_info(self, pdf_path: str) -> dict:
        """
        Get metadata information about PDF
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with PDF metadata
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                info = {
                    'num_pages': len(pdf_reader.pages),
                    'is_encrypted': pdf_reader.is_encrypted,
                    'metadata': {}
                }
                
                # Extract metadata if available
                if pdf_reader.metadata:
                    metadata = pdf_reader.metadata
                    info['metadata'] = {
                        'title': metadata.get('/Title', ''),
                        'author': metadata.get('/Author', ''),
                        'subject': metadata.get('/Subject', ''),
                        'creator': metadata.get('/Creator', ''),
                        'producer': metadata.get('/Producer', ''),
                        'creation_date': metadata.get('/CreationDate', ''),
                        'modification_date': metadata.get('/ModDate', '')
                    }
                
                return info
                
        except Exception as e:
            return {'error': f"Error reading PDF info: {str(e)}"}
    
    def validate_pdf(self, pdf_path: str) -> tuple[bool, str]:
        """
        Validate if file is a readable PDF
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Check if it has pages
                if len(pdf_reader.pages) == 0:
                    return False, "PDF file contains no pages"
                
                # Check if encrypted and can be decrypted
                if pdf_reader.is_encrypted:
                    try:
                        pdf_reader.decrypt("")
                    except:
                        return False, "PDF is password protected"
                
                # Try to extract text from first page
                first_page = pdf_reader.pages[0]
                test_text = first_page.extract_text()
                
                return True, "PDF is valid and readable"
                
        except Exception as e:
            return False, f"Invalid PDF file: {str(e)}"
