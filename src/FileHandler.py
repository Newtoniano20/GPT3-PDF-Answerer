
import PyPDF2

ALLOWED_EXTENSIONS = {'pdf'}
MAX_LEN = 1000
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_pdf_text(path: str):
    reader = PyPDF2.PdfReader(path)
    output = ""
    for i in range(len(reader.pages)):
        if len(output) > MAX_LEN:
            break
        output += reader.pages[i].extract_text()
    return output
