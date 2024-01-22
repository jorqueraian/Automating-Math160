import os
import csv
import subprocess
import sys
import pandas as pd
from PyPDF2 import PdfWriter, PdfReader, PdfMerger
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
os.chdir(os.path.dirname(__file__))

OUTPUT_DIR = "output/"

from StringSimilarity import cost_of_alignment


MAKEUP_QUIZ_EXCEL = r"C:\Users\jorqu\OneDrive - Colostate\160SP24\MeetingsUploads\Makeup-Quizzes.xlsx" 
#r"C:\Users\jorqu\OneDrive - Colostate\160SP24\Makeup-Quizzes.xlsx"

QUIZZES_LOCATIONS = [
    r"C:\Users\jorqu\OneDrive - Colostate\160SP24\Unit 1 - Modules 1 to 4\Module 1 Intro2Limits\102 Mod1Quiz\Mod1QuizDALT.pdf",
    r"C:\Users\jorqu\OneDrive - Colostate\160FA23\Unit 1 - Modules 1 to 4\Module 1 Intro2Limits\102 Mod1Quiz\Mod2QuizDAlt.pdf"
]


def generate_precalc_form(student_name, instructor_name, exam_date, exam_len, calculator_option="Non-Graphing"):
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

    return "tempprecalc.pdf"


def get_makeup_files_to_print(csvfile):
    def get_date_interval():
        from datetime import date, timedelta
        today = date.today()
        end_date = today + timedelta(days=10)
        return f"{today.strftime('%m/%d')} - {end_date.strftime('%m/%d')}"
    def parse_calculator(option_str):
        # This is over kill and entirely unneeded
        if len(option_str) == 0:
            return "Non-Graphing"
        options = ["Graphing","Non-Graphing","None","Yes"]
        best_match = None
        for option in options:
            cost = cost_of_alignment(option.lower(), option_str.lower(), 1, 1, 1) # may want to adjust these
            cost_per_char = cost / (len(option)+len(option_str))  # and these
            if best_match is None or cost_per_char < best_match[1]:
                best_match = (option, cost_per_char)
        return "Non-Graphing" if best_match[0] == "Yes" else best_match[0]
    def parse_quiz(quiz_str):  # this is buggy and may fail in the input string for quiz isnt close enough to the file name!
        def clean_str(input_str):
            # Remove .pdf or what ever
            # Make lowercase and remove whitespace
            # remove _ or -
            return str(input_str).split('\\')[-1].split('.')[0].lower().strip().replace('_', '').replace('-', '').replace(',', '').replace(' ', '')
        # This is over kill and entirely unneeded
        quizfile_names = [clean_str(qfile) for qfile in QUIZZES_LOCATIONS]
        best_match = None
        for ind, quiz_option in enumerate(quizfile_names):
            print(clean_str(quiz_str))
            cost = cost_of_alignment(clean_str(quiz_str)+"alt", quiz_option, 1, 1, 1) # may want to adjust these
            cost_per_char = cost / (len(quiz_option)+len(quiz_str))  # and these
            if best_match is None or cost_per_char < best_match[1]:
                best_match = (ind, cost_per_char)
        return QUIZZES_LOCATIONS[best_match[0]]
    
    makeups_df = pd.read_excel(open(csvfile, 'rb'), sheet_name='Sheet1', skiprows=[0])
    makeups_to_print = makeups_df[makeups_df["Printed"] != True]
    
    for ind in makeups_to_print.index:
        precalc_form = generate_precalc_form(makeups_to_print["Student Name"][ind],
                              makeups_to_print["Instructor Name"][ind],
                              get_date_interval(), makeups_to_print["Time limit"][ind],
                              parse_calculator(makeups_to_print["Calculator"][ind]))
        makeup_quiz = parse_quiz(makeups_to_print["Quiz"][ind])

        merger = PdfMerger()

        merger.append(open(precalc_form, 'rb'))
        merger.append(open("blank.pdf", 'rb'))  # this is super hacky but idc
        merger.append(open(makeup_quiz, 'rb'))
        merger.write(f'{OUTPUT_DIR}{makeups_to_print["Student Name"][ind]}-{makeups_to_print["Instructor Name"][ind]}-{makeups_to_print["Quiz"][ind]}.pdf')
        merger.close()

get_makeup_files_to_print(MAKEUP_QUIZ_EXCEL)