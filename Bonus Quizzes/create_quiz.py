import os
import csv
import subprocess
import sys
from PyPDF2 import PdfWriter, PdfReader, PdfMerger
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
os.chdir(os.path.dirname(__file__))


PROBLEM_HEADER_NEW_PAGE = r"""\newpage
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}l l}
    \textbf{Name}:\;\;<<student name>> & \textbf{Section}:\;\;<<section number>>\hspace{2in}\\
    \end{tabular*} \\"""


class Student:
    def __init__(self, name: str, section: str, standards: list[str]):
        self.name = name
        self.section = section
        self.standards = standards
    
    def file_name(self, ext):
        return f"quiz-{self.section}-{self.name.replace(' ', '-')}.{ext}"


def create_problems_include(standards: list[str]):
    def get_tex_for(standard):
        return f"\\input{{{PROBLEM_BANK}{standard}.tex}}"  # this generates path to problem to import

    problems_tex = "\\begin{enumerate}\n"+f"\n{PROBLEM_HEADER_NEW_PAGE}\n".join(map(get_tex_for, standards))+"\n\\end{enumerate}"
    
    return problems_tex


def generate_cover_page_include(standards: list[str]):
    def get_row(standard):
        return f"{standard}: {std_text[standard]} & Q\\ref{{std:{standard}}} & E M P NG"
    
    with open("standards.csv", "r") as f:
        std_text = {std[0]:std[1] for std in csv.reader(f, delimiter=",")}
    
    cover_page_tex = "\\\\ \hline\n".join(map(get_row, standards))

    return cover_page_tex


def generate_precalc_form_pdf(student_name, instructor_name, exam_date, exam_len, calculator_option="", sdc_accom="nan"):
    packet = io.BytesIO()  # I copied this code from the internet. Sorry person i stole from i forgot who you are. TODO: give credit maybe
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(120, 718, student_name)
    can.drawString(100, 698, instructor_name)
    can.drawString(90, 678, "Math 160")
    can.drawString(115, 658, exam_date)
    can.drawString(110, 638, exam_len)
    if calculator_option == "Graphing":
        can.drawString(103, 561, r"X")
    elif calculator_option == "None":
        can.drawString(103, 613, r"X")
    else:
        can.drawString(103, 561, r"X")
        can.drawString(150, 548, r"non-graphing")
    can.drawString(103, 499, r"X")

    if sdc_accom.strip().lower() != "nan":
        can.drawString(300, 718, r"Accommodations: ")
        can.drawString(300, 698, sdc_accom)
    
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfReader(packet)
    # read your existing PDF
    existing_pdf = PdfReader(open("precalcform.pdf", "rb"))
    output = PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    # finally, write "output" to a real file
    output_stream = open("tempprecalc.pdf", "wb")
    output.write(output_stream)
    output_stream.close()


def generate_quiz_tex_for_student(student: Student):
    problem_tex = create_problems_include(student.standards)
    cover_tex = generate_cover_page_include(student.standards)

    with open('quiz_template.tex', 'r') as temp_f:
        filedata = temp_f.read()
        filedata = filedata.replace('<<cover_page>>', cover_tex)
        filedata = filedata.replace('<<problems>>', problem_tex)
        filedata = filedata.replace('<<student name>>', student.name)
        filedata = filedata.replace('<<section number>>', student.section)
        filedata = filedata.replace('<<quiz title>>', QUIZ_TITLE)
        filedata = filedata.replace('<<problem bank>>', PROBLEM_BANK)

    with open(student.file_name("tex"), 'w') as new_file:
        new_file.write(filedata)
    
    return student.file_name("tex")


def generate_student_quizzes_tex(quizzes_csv, clean_up=True, precalc_sections=[]):
    with open(quizzes_csv, "r") as f:
        students = [Student(name=stud[0], section=stud[1], standards=list(filter(None, stud[2:]))) 
                    for stud in csv.reader(f, delimiter=",")]
        
    for student in students:
        if len(student.standards) > 0:
            tex_file = generate_quiz_tex_for_student(student)
            subprocess.run(["pdflatex", tex_file, f"-output-directory={OUTPUT_DIR}{student.section}"])
            subprocess.run(["pdflatex", tex_file, f"-output-directory={OUTPUT_DIR}{student.section}"])
            for section in precalc_sections:
                if student.section == section[0]:
                    # this is so hacky. TODO: make better!
                    generate_precalc_form_pdf(student.name, section[1], section[2], section[3])
                    merger = PdfMerger()

                    merger.append(open("tempprecalc.pdf", 'rb'))
                    merger.append(open("blank.pdf", 'rb'))
                    merger.append(open(f"{OUTPUT_DIR}{student.section}/{student.file_name('pdf')}", 'rb'))

                    with open(f"{OUTPUT_DIR}{student.section}/{student.file_name('pdf')}", "wb") as fout:
                        merger.write(fout)
                    break
        if clean_up:
            try:
                os.remove(student.file_name("tex"))
            except:
                pass
            try:
                os.remove(f"{OUTPUT_DIR}{student.section}/{student.file_name('aux')}")
            except:
                pass
            try:
                os.remove(f"{OUTPUT_DIR}{student.section}/{student.file_name('log')}")
            except:
                pass


################ HOW TO RUN THIS FILE #######################
#### STEP 0 ####
# I recommend using VS code
# In a terminal run the following if you are in a python environment
    # pip install PyPDF2 reportlab csv
# other wise you can run. you may need to include the entire path to python
    # python -m pip install PyPDF2 reportlab csv

#### STEP 0.5 ####
# Modify standards.csv to change teh description of standards. And check it has what you need
# Quiz Title: Math 160, QUIZ_TITLE
QUIZ_TITLE = r"Mod 15 Bonus Assessment Fall 2023"
# You can also change the location of the problem bank and the output destination here
PROBLEM_BANK = "problembank/FA23/"
OUTPUT_DIR = "output/"

#### STEP 1 (Optional) ####
# Create a file named students.csv in the same directory as this file
# This file should have no header
# and each row should be as follows. (With no spaces after the ,)
    # Student Name,Section,Standard1,Standard2,.....

#### Step 1.5 ####
# If some of the section you are generating quiz for need to have a pre-calc form attached
# Add a tuple for each section into the array. 
# Ex ("010", "Ross Flaxman", r"12/8", "50 min")
precalc_forms=[("006", "Ross Flaxman", r"whenever", "50 min")]

#### Step 2 ####
# Run the File with the following command (Note this was written in python 3.11 so you may need to updated to at least that version)
    # Python create_quiz.py
# Or if you did not rename your csv file as in step 1 you can run
    # Python create_quiz.py your_csv_file.csv


students_file = sys.argv[1] if len(sys.argv) > 1 else "students.csv"
generate_student_quizzes_tex(students_file, clean_up=True, precalc_sections=precalc_forms)

# Do after Bonus because i dont want to break things
# TODO: make this read in students as pandas array, so it can take in csv and things can be nice
#       I would like it so there is a single column for standards selected
# TODO: make precalc thing better. make step 1.5 not in the python file maybe?