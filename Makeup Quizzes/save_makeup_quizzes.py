import os
import pandas as pd
from PyPDF2 import PdfWriter, PdfReader, PdfMerger
import io
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import glob
os.chdir(os.path.dirname(__file__))

OUTPUT_DIR = "output/"

from StringSimilarity import cost_of_alignment


MAKEUP_QUIZ_EXCEL = r"C:\Users\jorqu\OneDrive - Colostate\160SP24\SharedMeetingsUploads\Makeup-Quizzes.xlsx" 
MAKEUP_QUIZ_EXCEL_SHEET = r"Unit3"
#r"C:\Users\jorqu\OneDrive - Colostate\160SP24\Makeup-Quizzes.xlsx"


### AS of now the program does not care about the name of the pdf file just the folder that pdf is in.
### and as long as the folder is something similar to "Mod 1 Quiz" then everything will work. Really
### the only thing that matters is the order of words. For example "Quiz Mod 1" would be bad. 
### This also work for reassessments or Bonus quizzes just give the name of the directory the bonus 
### quizzes are in: for example "..../Mod7Reassessment/Mod7ReassessQuiz" if that directory contains
### the directories that the bonus quiz create_quiz.py file would output
QUIZZES_LOCATIONS = [
    r"C:\Users\jorqu\OneDrive - Colostate\160SP24\Unit 1 - Modules 1 to 4\Module 1 Intro2Limits\102 Mod1Quiz\Mod1QuizDALT.pdf",
    r"C:\Users\jorqu\OneDrive - Colostate\160SP24\Unit 1 - Modules 1 to 4\Module 2 Continuity Limits\102 Module 2 Quizzes\Quiz Module 2Alt1.pdf",
    r"C:\Users\jorqu\OneDrive - Colostate\160SP24\Unit 1 - Modules 1 to 4\Module 3 OneSided Infinity\Mod3Reassessment\Mod3ReassessQuizA.pdf",
    r"C:\Users\jorqu\OneDrive - Colostate\160SP24\Unit 1 - Modules 1 to 4\Module 4 IndeterminateAROC\Mod4Exam\Mod4ExamVersionAlt.pdf",
    r"C:\Users\jorqu\OneDrive - Colostate\160SP24\Unit 2 - Modules 5 to 8\Module 5 IntroToDerivatives\Mod 5 Quiz\Quiz Module 5 C6pmALT.pdf",
    r"C:\Users\jorqu\OneDrive - Colostate\160SP24\Unit 2 - Modules 5 to 8\Module 6 Interpreting Derivatives\102 Mod 6 Quizzes\Mod6quizAlternate2SP24.pdf",
    r"C:/Users/jorqu/OneDrive - Colostate/160SP24/Unit 2 - Modules 5 to 8/Module 7 Derivative Shortcuts/Mod7Reassessment/ReassessmentQuizzes",
    r"C:\Users\jorqu\OneDrive - Colostate\160SP24\Unit 2 - Modules 5 to 8\Module 8 Chain Rule and Implicit\zzzdrafts\102 Mod8ExamVersions\Mod 8 Ver B SP24.pdf",
    r"C:\Users\jorqu\OneDrive - Colostate\160SP24\Unit 3 - Modules 9 to 12\Module 9 Linearization and Theorems\Module 9 Quizzes\Mod9quizAlternate.pdf",
    r"C:\Users\jorqu\OneDrive - Colostate\160SP24\Unit 3 - Modules 9 to 12\Module 10 Optimization\Module 10 Quizzes\Mod10quizMondayAndAlt.pdf",
    r"C:/Users/jorqu/OneDrive - Colostate/160SP24/Unit 3 - Modules 9 to 12/Module 11 Derivative Applications/Mod11Reassessment/ReassessmentQuizzes"
]


def generate_precalc_form(student_name, instructor_name, exam_date, exam_len, calculator_option="Non-Graphing", sdc_accom="nan"):
    packet = io.BytesIO()  # I copied this code from the internet. Sorry person i stole from i forgot who you are. TODO: give credit maybe
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(120, 718, student_name)
    can.drawString(100, 698, instructor_name)
    can.drawString(90, 678, "Math 160")
    can.drawString(115, 658, exam_date)
    can.drawString(110, 638, str(exam_len))  # This broke once when i didnt have the str and i could never really figure out why
    if calculator_option == "Graphing":
        can.drawString(103, 561, r"X")
    elif calculator_option == "None":
        can.drawString(103, 613, r"X")
    else:
        can.drawString(103, 561, r"X")
        can.drawString(150, 548, r"non-graphing")
    can.drawString(103, 524, r"X")

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

    return "tempprecalc.pdf"


def get_makeup_files_to_print(excelfile, excel_sheet_name, match_threshold=None, default_quiz_override=None):
    def get_date_interval(date_input=""):
        from datetime import date, timedelta
        date_given = pd.to_datetime(str(date_input).replace(',', ' '), errors='coerce')
        if date_given == date_given:
            start_date = date_given
        else:
            start_date = date.today()
        end_date = start_date + timedelta(days=11)
        return f"{start_date.strftime('%m/%d')} - {end_date.strftime('%m/%d')}"
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
        # Actually this function is insanely overkill. There is absolutely 0 reasons for me
        # to use StringSimilarity.py here. literally zero
        # but it makes me seem cool!! So im keeping it
        def clean_str(input_str, path_ind=-1):
            # path_ind -1 for file name or default, -2 for folder name and 0
            # Remove .pdf or what ever
            # Make lowercase and remove whitespace
            # remove _ or -
            return re.sub(r'^\d+', '', re.split(r"[\\\/]", str(input_str))[path_ind].split('.')[0].lower()).strip().replace('_', '').replace('-', '').replace(',', '').replace(' ', '').replace("quizzes","quiz").replace("module","mod").replace("versions","")
        # This is over kill and entirely unneeded. Its also so funny that the clean_quiz function will probably make it so there is a perfect matching every time! and the string alignment is 1000% overkill. But at this point im keeping it as is
        quizfile_names = [clean_str(qfile, -2) for qfile in QUIZZES_LOCATIONS]
        best_match = None
        for ind, quiz_option in enumerate(quizfile_names):
            mod_num = re.search(r"\d+", quiz_option).group(0)
            if match_threshold is not None and re.search(mod_num, quiz_str) is None:
                continue
            cost = cost_of_alignment(clean_str(quiz_str), quiz_option, 1, 1, 1) # may want to adjust these
            cost_per_char = cost / (len(quiz_option)+len(quiz_str))  # and these
            if (best_match is None and (match_threshold is None or cost_per_char <= match_threshold)) or (best_match is not None and cost_per_char < best_match[1]):
                best_match = (ind, cost_per_char)
        if best_match is not None:
            # print(clean_str(QUIZZES_LOCATIONS[best_match[0]],-2))
            print(best_match[0]+1, best_match[1])
            return QUIZZES_LOCATIONS[best_match[0]], clean_str(QUIZZES_LOCATIONS[best_match[0]],-2)
        else:
            return None, None
    
    # TODO: read this https://stackoverflow.com/questions/26521266/using-pandas-to-pd-read-excel-for-multiple-worksheets-of-the-same-workbook
    makeups_df = pd.read_excel(open(excelfile, 'rb'), sheet_name=excel_sheet_name, skiprows=[0,1])
    makeups_to_print = makeups_df[makeups_df["Printed"] != True]
    
    for ind in makeups_to_print.index:
        precalc_form = generate_precalc_form(makeups_to_print["Student Name"][ind],
                              makeups_to_print["Instructor Name"][ind],
                              get_date_interval(makeups_to_print["Date"][ind]), makeups_to_print["Time limit"][ind],
                              parse_calculator(makeups_to_print["Calculator"][ind]), "nan")
        makeup_quiz, quiz_name = parse_quiz(makeups_to_print["Quiz"][ind])
        
        if makeup_quiz is None:
            print(f'Could Not match {'\033[1m'}{makeups_to_print["Quiz"][ind]}{'\033[0m'} to a known quiz for student: {makeups_to_print["Student Name"][ind]} and instructor: {makeups_to_print["Instructor Name"][ind]}')
            print('This quiz was skipped. To ignore this and go with best match anyway please set match_threshold=None\n')
            continue
        elif makeup_quiz[-3:] != "pdf":
            import sys
            sys.path.insert(-1, r'../Bonus Quizzes')
            import create_quiz
            sys.path.remove(r'../Bonus Quizzes')

            # TODO: Make this use string similarity algo, but also maybe done, too mu
            section_str = "0"*(max(0,3-len(str(makeups_to_print["Section"][ind])))) + str(makeups_to_print["Section"][ind])
            
            best_match = None
            for sec_dir in glob.glob(f"{makeup_quiz}/*/"):
                sec_dir_name = re.split(r"[\\\/]", sec_dir)[-2]
                # TODO: Make this use string similarity algo, unless the section str is in the directory name
                if section_str in sec_dir_name:
                    how_to_not_code = create_quiz.Student(makeups_to_print["Student Name"][ind], sec_dir_name, [])
                    makeup_quiz = f"{sec_dir}/{how_to_not_code.file_name('pdf')}"
                    continue
                else:
                    # Im using the string similarity to find the directory to look in?
                    cost = cost_of_alignment(re.sub(r'^\d+ *(noon)* *', '', sec_dir_name), makeups_to_print["Instructor Name"][ind], 1, 1, 1) # may want to adjust these
                    cost_per_char = cost / (len(re.sub(r'^\d+ *', '', sec_dir_name))+len(makeups_to_print["Instructor Name"][ind]))  # and these
                    if (best_match is None) or (cost_per_char < best_match[1]):
                        best_match = (sec_dir, cost_per_char)
            
            if best_match is not None:
                how_to_not_code = create_quiz.Student(makeups_to_print["Student Name"][ind], re.split(r"[\\\/]", best_match[0])[-2], [])
                makeup_quiz = f"{best_match[0]}/{how_to_not_code.file_name('pdf')}"
            
            if best_match is None or not os.path.isfile(makeup_quiz):
                # would be cool to run create_quiz.py if needed. maybe if comment was the standards needed
                print(f'Could Not match {'\033[1m'}{makeups_to_print["Quiz"][ind]}{'\033[0m'} to a known quiz for student: {makeups_to_print["Student Name"][ind]} and instructor: {makeups_to_print["Instructor Name"][ind]}')
                print(f"Quiz file not found: {makeup_quiz}")
                if default_quiz_override is not None:
                    print("Using provided default_quiz_override")
                    makeup_quiz = default_quiz_override
                else:
                    print('This quiz was skipped. Trying setting default_quiz_override to something \n')
                    continue
        
        merger = PdfMerger()

        merger.append(open(precalc_form, 'rb'))
        merger.append(open("blank.pdf", 'rb'))  # this is super hacky but idc
        merger.append(open(makeup_quiz, 'rb'))
        merger.write(f'{OUTPUT_DIR}{makeups_to_print["Student Name"][ind]}-{makeups_to_print["Instructor Name"][ind]}-{quiz_name}.pdf')
        merger.close()

        print(f'{makeups_to_print["Student Name"][ind]} - {makeups_to_print["Instructor Name"][ind]} - {quiz_name}\n')

        # clean file sys
        os.remove(precalc_form)


default_quiz_override=r"C:\Users\jorqu\OneDrive - Colostate\160SP24\Unit 3 - Modules 9 to 12\Module 11 Derivative Applications\Mod11Reassessment\ReassessmentQuizzes\Entire Quiz\Entire Quiz - Mod 11 Reassessment.pdf"
# for some reason if the makeup quizzes file is open when you run this things wont work. I have literally no idea why
get_makeup_files_to_print(MAKEUP_QUIZ_EXCEL, MAKEUP_QUIZ_EXCEL_SHEET, match_threshold=0.025, default_quiz_override=default_quiz_override)