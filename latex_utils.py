import os
import subprocess
import uuid
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

def write_latex_to_file(latex_content: str, output_dir: str) -> str:
    """
    Writes LaTeX content to a uniquely named .tex file in output_dir.
    Returns the full path to the .tex file.
    """
    os.makedirs(output_dir, exist_ok=True)
    unique_id = str(uuid.uuid4())
    tex_filename = f"{unique_id}.tex"
    tex_path = os.path.join(output_dir, tex_filename)
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    return tex_path

def build_pdflatex_command(tex_path: str, output_dir: str) -> list:
    """
    Returns the pdflatex command as a list for subprocess.
    """
    return [
        'pdflatex',
        '-interaction=nonstopmode',
        '-output-directory', output_dir,
        tex_path
    ]

def run_pdflatex_command(pdflatex_cmd: list, output_dir: str):
    """
    Runs the pdflatex command synchronously in the given directory.
    Returns the subprocess.CompletedProcess instance.
    """
    return subprocess.run(
        pdflatex_cmd,
        capture_output=True,
        text=True,
        check=False,
        cwd=output_dir
    )

def read_pdf_file(pdf_path: str) -> bytes:
    """
    Reads and returns the content of the PDF file.
    """
    with open(pdf_path, 'rb') as f:
        return f.read()

def get_pdf_and_tex_filenames(tex_path: str) -> Tuple[str, str]:
    """
    Given a .tex file path, returns (pdf_filename, pdf_path).
    """
    base = os.path.splitext(os.path.basename(tex_path))[0]
    pdf_filename = f"{base}.pdf"
    pdf_path = os.path.join(os.path.dirname(tex_path), pdf_filename)
    return pdf_filename, pdf_path

def format_pdflatex_error(stderr: str, num_lines: int = 20) -> str:
    lines = stderr.splitlines()
    return '\n'.join(lines[-num_lines:]) if lines else 'No stderr output.'
