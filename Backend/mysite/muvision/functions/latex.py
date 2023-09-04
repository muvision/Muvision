from pylatex import Document, Section, Subsection, Command, Math, NoEscape
from pylatex.utils import italic, NoEscape
import os


def write_latex(lines):
    # Takes in an array of strings and writes them to a LaTeX document
    doc = Document('basic')
    for line in lines:
        doc.append(NoEscape(r"$$" + line + r"$$"))
    doc.generate_pdf(clean_tex=False)
    doc.generate_tex()
    tex = doc.dumps()  # The document as string in LaTeX syntax
