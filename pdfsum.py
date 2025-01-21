# import streamlit as st
# from transformers import pipeline
# from PyPDF2 import PdfReader

# # Initialize the summarizer
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# def extract_text_from_pdf(pdf_file):
#     """Extract text from an uploaded PDF file."""
#     try:
#         reader = PdfReader(pdf_file)
#         text = ""
#         for page in reader.pages:
#             page_text = page.extract_text()
#             if page_text:  # Skip pages with no text
#                 text += page_text + "\n"
#         return text
#     except Exception as e:
#         raise ValueError(f"Error extracting text from PDF: {e}")

# def split_text_into_chunks(text, max_chunk_size=1024):
#     """Split the text into smaller chunks for summarization."""
#     chunks = []
#     while len(text) > max_chunk_size:
#         split_point = text.rfind(". ", 0, max_chunk_size) + 1  # Split at the last sentence boundary
#         if split_point == 0:  # No sentence boundary found, split arbitrarily
#             split_point = max_chunk_size
#         chunks.append

# # Streamlit Dashboard
# st.title("PDF Summarizer")
# st.write("Upload a PDF file to get a summarized version of its content.")

# uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

# if uploaded_file is not None:
#     # Extract text from the PDF
#     st.write("Processing your PDF...")
#     try:
#         pdf_text = extract_text_from_pdf(uploaded_file)
#         st.write("PDF content extracted successfully.")
        
#         # Display extracted text (optional)
#         with st.expander("View Extracted Text"):
#             st.text_area("Extracted Text", pdf_text, height=300)
        
#         # Summarize the extracted text
#         if st.button("Summarize"):
#             st.write("Generating summary...")
#             summary = summarizer(pdf_text, max_length=130, min_length=30, do_sample=False)
#             st.subheader("Summary")
#             st.write(summary[0]["summary_text"])
#     except Exception as e:
#         st.error(f"An error occurred while processing the PDF: {str(e)}")

import streamlit as st
from transformers import pipeline
import pdfplumber

# Initialize the summarizer
summarizer = pipeline("summarization", model="t5-small")

def extract_text_from_pdf(pdf_file):
    """Extract text from an uploaded PDF file using pdfplumber."""
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        if not text.strip():
            raise ValueError("No extractable text found in the PDF.")
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {e}")

def split_text_into_chunks(text, max_chunk_size=1024):
    """Split the text into smaller chunks for summarization."""
    chunks = []
    while len(text) > max_chunk_size:
        split_point = text.rfind(". ", 0, max_chunk_size) + 1  # Find the last full sentence
        if split_point == 0:  # No sentence boundary found, split arbitrarily
            split_point = max_chunk_size
        chunks.append(text[:split_point])
        text = text[split_point:]
    if text:
        chunks.append(text)
    return chunks

def summarize_text(chunks):
    """Summarize each chunk of text with dynamic max_length."""
    summaries = []
    for chunk in chunks:
        input_length = len(chunk.split())  # Approximate token count
        max_length = max(48, int(input_length * 0.8))  # Set max_length to 80% of input length
        summary = summarizer(chunk, max_length=max_length, min_length=10, do_sample=False)
        summaries.append(summary[0]["summary_text"])
    return summaries

# Streamlit Dashboard
st.title("PDF Summarizer")
st.write("Upload a PDF file to get a summarized version of its content.")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        # Extract text from the PDF
        st.write("Processing your PDF...")
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.write("PDF content extracted successfully.")
        
        # Display extracted text (optional)
        with st.expander("View Extracted Text"):
            st.text_area("Extracted Text", pdf_text, height=300)
        
        # Summarize the extracted text
        if st.button("Summarize"):
            st.write("Generating summary...")
            chunks = split_text_into_chunks(pdf_text)
            summaries = summarize_text(chunks)
            full_summary = " ".join(summaries)
            st.subheader("Summary")
            st.write(full_summary)
    except Exception as e:
        st.error(f"An error occurred while processing the PDF: {str(e)}")
