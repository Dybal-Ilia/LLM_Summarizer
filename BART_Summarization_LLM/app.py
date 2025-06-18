
#importing libraries
import gradio as gr
import PyPDF2
import logging
from summarizer import TextSummarizer

#setting logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#creating a summary model
summarizer = TextSummarizer()


"""To create a summary it's essential to gather the text. It was decided to give users
an opportunity to work with .txt and .pdf files. Why no .docx? The answer is that most
of documents are presented as .pdf for their better readability. Thus, it's not a big deal
for a user to convert their .docx files into .pdf. extract_text_from_file function is aimed
at gathering texts from users' files in fact."""


def extract_text_from_file(file):
    #checking whether the file is uploaded or user inserts their text manually
    if file is None:
        return None

    file_path = file.name

    #extracting from .txt
    if file_path.endswith('.txt'):

        #reaing a file as utf-8 encoded
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    #extracting from .pdf
    elif file_path.endswith('.pdf'):
        try:

            #reading a file as binary
            with open(file_path, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text

        #just in case some unknown issues occur
        except Exception as e:
            logger.error(f"Seems like an error occurred...Can't read your PDF-file: {e}")
            return None
    else:

        #in case user uploads an unsupported file
        raise ValueError("Seems like an error occurred... Use .pdf or .txt")


def summarize_text(input_text, uploaded_file):
    try:

        #extracting text from file if uploaded, else using users' manually inserted text
        text = extract_text_from_file(uploaded_file) if uploaded_file else input_text

        #checking whether the text is provided
        if not text or not text.strip():
            return "Seems like an error occurred... Check whether the input is not empty"

        logger.info("Starting summarization process...")
        summary = summarizer.summarize(text)
        return summary

    #raising an exception in case something goes wrong
    except Exception as e:
        logger.error(f"Seems like an error occurred... Summarization failed: {e}")
        return f"Error: {str(e)}"

#building gradio interface
iface = gr.Interface(
    fn=summarize_text,
    inputs=[
        gr.Textbox(lines=10, placeholder="Paste your text here...", label="Input Text"),
        gr.File(label="Upload .txt or .pdf file")
    ],
    outputs=gr.Textbox(label="Summary"),
    title="Text Summarization (Project for Ifortex)",
    description="Paste text or upload a .txt/.pdf file to generate a concise summary using BART model"
)


if __name__ == "__main__":
    iface.launch()