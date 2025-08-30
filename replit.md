# Medical Report Summarizer

## Overview

A Streamlit-based medical document processing application that converts lengthy medical reports into concise, readable summaries. The system serves two primary user types: healthcare professionals who need quick insights from extensive medical documentation, and patients who require simplified explanations of their medical reports in plain language. The application processes both text and PDF medical documents locally, ensuring privacy and data security.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
The application uses **Streamlit** as the web framework, providing an interactive interface with sidebar configuration options and multi-column layouts. The choice of Streamlit enables rapid development of data-focused applications with built-in UI components, making it ideal for medical document processing tools.

### Core Processing Components
The system implements a **modular architecture** with three specialized utility classes:

- **TextProcessor**: Handles medical text preprocessing, including abbreviation expansion and text cleaning. This component addresses the challenge of medical jargon by maintaining a comprehensive mapping of medical abbreviations to full terms.

- **MedicalSummarizer**: Implements rule-based summarization logic with medical domain expertise. Uses pattern recognition to identify clinically important sentences and provides patient-friendly translations of medical terminology.

- **PDFExtractor**: Manages PDF document processing using PyPDF2, with error handling for encrypted documents and text extraction across multiple pages.

### Data Processing Pipeline
The architecture follows a **sequential processing pattern**:
1. Document upload and format detection
2. Text extraction (PDF) or direct processing (TXT)
3. Medical text preprocessing and cleaning
4. Rule-based summarization with configurable options
5. Dual-output generation (professional and patient summaries)

### Privacy and Security Design
The system implements a **privacy-by-design approach**:
- Local processing without external API calls
- No document storage or persistence
- Temporary file handling with automatic cleanup
- Clear privacy notices in the user interface

### Configuration Management
Implements **user-configurable summarization** with options for:
- Summary length control (short/medium/long)
- Content filtering (medications, procedures, recommendations)
- Output format selection (doctor vs patient summaries)

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for the user interface
- **PyPDF2**: PDF text extraction and processing
- **Python Standard Library**: File handling, regular expressions, and text processing utilities

### Development Dependencies
The application relies primarily on Python's standard library and minimal external dependencies to reduce complexity and ensure reliability. The choice of PyPDF2 over alternatives provides robust PDF handling without requiring complex machine learning dependencies.

### No External APIs
The system is designed to operate independently without external API dependencies, ensuring data privacy and reducing latency. This architectural decision prioritizes user privacy over advanced AI capabilities, making it suitable for sensitive medical document processing.