### DO NOT MODIFY THIS FILE UNLESS YOU ARE CONFIDENT IN THE CHANGES
### MOST MODIFICATIONS SHOULD BE DONE IN THE GradescopeConfig.py FILE
### including selecting what assignment to export and some of the class configs


# Im going to try this: https://pypi.org/project/gradescope/
# but really im using this https://github.com/mooey5775/gradescope/tree/master which used the above

from GradescopeConfig import *
import re
import pandas as pd
import os
import bs4
import json

os.chdir(os.path.dirname(__file__))

OUTPUT_DIR = "output/"


def try_extract_rubric_score(rubric_items, standard, grade):
    # super sloppy fix but for now its fine
    # add in some miss-spelling catchers. Like gradeable instead of gradable etc
    try:
        return rubric_items[get_standard_rubric_key(standard, grade.value)]
    except KeyError:
        try: # try some spelling errors
            return rubric_items[get_standard_rubric_key(standard, grade.value.replace("radable", "radeable"))]
        except KeyError: # this should never occur but just in case
            try: # try some spelling errors
                return rubric_items[get_standard_rubric_key(standard, grade.value.replace("grad", "Grad"))]
            except KeyError:
                raise KeyError(f"Failed in 'try_extract_rubric_score'\nFailed to get gradescope score for standard '{standard}' and score '{grade}'. Please check spelling and formatting in gradescope!")


def add_rubric_scores_old(grades_and_evals):
    for student in grades_and_evals:
        student["rubric score"] = {}  # add new dictionary key for scores
        for key in list(student["questions"].keys()):
            # Im doing this dumb. Ill outline a better way to do this
            # for each question check the keys and see if "L? Rubric Score" exists and if so
            # us that to determine the standard. This will help limit the way the gradescope outline is created
            # and only require correct formatting in the "L? Rubric Score" group
            if re.match(r"\d{1,2}\.?\d?: \w\d{1,2} .*", key):
                standard = key.split(" ")[1]  # possible point of failure. need the questions to be labeled in a very specific way!
                score = default_rubric_eval  # think about changing this. Its very bad if this is used
                for rub_score in RubricScore:
                    if try_extract_rubric_score(student["questions"][key]["rubric_items"],standard, rub_score):
                        score = rub_score.value
                student["rubric score"][standard] = score.split(" (")[0]


def add_rubric_scores(grades_and_evals, email_str=None):
    for student in grades_and_evals:
        student["rubric score"] = {}  # add new dictionary key for scores
        for key in list(student["questions"].keys()):
            stds = []
            for rubric_score_item in list(student["questions"][key]['rubric_items'].keys()):
                # Omg this is hacky but needs to be done.
                if re.match(f"\\w\\d{{1,2}}{get_standard_rubric_key()}.*", rubric_score_item):
                    stds.append(rubric_score_item.split(" ")[0])
            stds = list(set(stds))

            if len(stds) == 0:
                print(f"Student: {student['First Name']+ ' '+ student['Last Name']}(Section: {student['Sections'].split('-')[-1]}), has no Rubric Score Group for problem {key}")
                
            for standard in stds:
                rubric_with_data =0
                score = default_rubric_eval  # think about changing this. Its very bad if this is used
                for rub_score in RubricScore:
                    if try_extract_rubric_score(student["questions"][key]["rubric_items"],standard, rub_score):
                        score = rub_score.value
                        rubric_with_data += 1
                if rubric_with_data != 1:
                    if email_str is not None:
                        email_str.append(f"Student: {student['First Name']+ ' '+ student['Last Name']}(Section: {student['Sections'].split('-')[-1]}), Standard:{standard} has {rubric_with_data} rubric scores selected")
                    else:
                        print(f"Student: {student['First Name']+ ' '+ student['Last Name']}(Section: {student['Sections'].split('-')[-1]}), Standard:{standard} has {rubric_with_data} rubric scores selected")
                student["rubric score"][standard] = score.split(" (")[0]  # can do just score.


def save_assignment_to_csv(assignment_name, canvas_df, sections):
    from datetime import date
    today = date.today()
    canvas_df.to_csv(f"{OUTPUT_DIR}{assignment_name.replace(':', '').replace(' ', '-')}-results-{today.strftime('%m-%d')}-{"-".join(sections)}.csv", index=False)


def get_gradescope_data_for_versd_assignment(course_num, assignment_nums_dict, sections_keys=[], canvas_usable=True, canvas_roster=None, email_str=None):
    evals = []
    
    if len(sections_keys) == 0:
        sections_keys = list(assignment_nums_dict.keys())

    for assignment_num_key in sections_keys:
        assert assignment_num_key in assignment_nums_dict, f"'{assignment_num_key}' not found. The known sections are: {assignment_nums_dict.keys()}"
        evals_ver = gradescope.get_assignment_evaluations(course_num, assignment_nums_dict[assignment_num_key])
        evals += [eval for eval in evals_ver if eval["Status"] == "Graded"]
    add_rubric_scores(evals, email_str)

    if canvas_usable and canvas_roster is not None and len(evals) > 0:
        canvas_df = pd.read_csv(open(canvas_roster, 'rb'), usecols=["Student Name", "Student SIS ID"])
        canvas_id_dict = {row["Student SIS ID"]: row["Student Name"] for _, row in canvas_df.iterrows()}
        assignment_stds = list(evals[ 0]["rubric score"].keys())
        columns = ["Student Name", "Student ID"] + [f"Rating: {standard}" for standard in assignment_stds]

        rubric_scores = []
        for student in evals:  # skip test student
            if student["SID"] == "123456789":
                continue
            elif student["SID"] == "":
                print("\nYikes, it appears that a quiz was not matched to a student. Please check gradescope to unlock this mystery student!\n")
            else:
                if int(student["SID"]) in canvas_id_dict:
                    rubric_scores.append([canvas_id_dict[int(student["SID"])], student["SID"]] + 
                                            [student["rubric score"][std] for std in assignment_stds])
                else:
                    print(f"\nStudent {student['First Name']} {student['Last Name']}(SID: {student['SID']}) not found in Canvas Roster. Skipping")
        the_frame = pd.DataFrame(rubric_scores, columns=columns)
        return the_frame
    else:
        return evals

# probably wont work lol
def get_gradescope_data_for_assignment(course_num, assignment_num, canvas_usable=True, canvas_roster=None):
    evals = gradescope.get_assignment_evaluations(course_num, assignment_num)
    evals = [eval for eval in evals if eval["Status"] != "Missing"]
    add_rubric_scores(evals)
    if canvas_usable and canvas_roster is not None:
        canvas_df = pd.read_csv(open(canvas_roster, 'rb'), usecols=["Student Name", "Student SIS ID"])
        canvas_id_dict = {row["Student SIS ID"]: row["Student Name"] for _, row in canvas_df.iterrows()}
        assignment_stds = list(evals[0]["rubric score"].keys())
        columns = ["Student Name", "Student ID"] + [f"Rating: {standard}" for standard in assignment_stds]

        rubric_scores = []
        for student in evals:  # skip test student
            if student["SID"] == "123456789":
                continue
            else:
                rubric_scores.append([canvas_id_dict[int(student["SID"])], student["SID"]] + 
                                        [student["rubric score"][std] for std in assignment_stds])
        
        the_frame = pd.DataFrame(rubric_scores, columns=columns)
        return the_frame
    else:
        return evals

def get_all_assignments(abbrs=KEY_ABBREVIATIONS):
    # NOTE: remove "/assignments" for only active assignments?
    result = gradescope.api.request(endpoint="courses/{}/assignments".format(GRADESCOPE_COURSE_NUMBER))
    soup = bs4.BeautifulSoup(result.content.decode(), features="html.parser")

    assignments_table = json.loads(soup.find("div", attrs={"data-react-class":"AssignmentsTable"}).attrs['data-react-props'].replace("'", "\""))["table_data"]
    
    assignments = {}
    for assignment in assignments_table:
        if assignment['type'] == 'assignment': # Ignore the assignment groups
            assign_match =re.match(r"Mod(?:ule)* ([0-9]*): ([A-z]+) *([Ss]ection)? *([0-9,a-z]*)", assignment['title'])
            # group 1: module #
            # group 2: Quiz/Exam/Reass etc
            # group 3: "Section " or blank
            # group 4: section # or "alts"
            assert assign_match is not None, f"Assignment {assignment['title']} did not fit expected regex pattern: 'Module ([0-9]*): ([A-z])* (Section )*([0-9,a-z]*)'"
            
            assignment_group_name = assignment['title'][0:assign_match.regs[2][1]]
            for word in abbrs.keys():
                assignment_group_name = assignment_group_name.replace(word, abbrs[word])

            #section_num = assign_match.group(4) if len(assign_match.group(4)) > 0 else "all"
            if not assignment_group_name in assignments.keys():
                assignments[assignment_group_name] = {assign_match.group(4): int(assignment['id'].split("_")[-1])}
            else:
                assignments[assignment_group_name][assign_match.group(4)] = int(assignment['id'].split("_")[-1])
    return assignments

if not bool(BIG_LOOK_UP_TABLE):
    BIG_LOOK_UP_TABLE = get_all_assignments()

if DRAFT_EMAILS:
    email_str = []
else:
    email_str = None

if ONE_FILE_EACH:
    if len(SECTIONS) == 0:
        assert ASSIGNMENT_NAME in BIG_LOOK_UP_TABLE, f"{ASSIGNMENT_NAME} not found. The known assignments are: {BIG_LOOK_UP_TABLE.keys()}"
        SECTIONS = list(BIG_LOOK_UP_TABLE[ASSIGNMENT_NAME].keys())

    for section in SECTIONS:
        assert section in BIG_LOOK_UP_TABLE[ASSIGNMENT_NAME], f"{ASSIGNMENT_NAME} not found. The known sections are: {BIG_LOOK_UP_TABLE[ASSIGNMENT_NAME].keys()}"
        evals = get_gradescope_data_for_versd_assignment(GRADESCOPE_COURSE_NUMBER, 
                                                        BIG_LOOK_UP_TABLE[ASSIGNMENT_NAME], [section], 
                                                        True, CANVAS_ROSTER,
                                                        email_str)
        print(f"{len(evals)} students exported for section {section}")
        if len(evals) > 0:
            save_assignment_to_csv(ASSIGNMENT_NAME, evals, [section])
else:
    evals = get_gradescope_data_for_versd_assignment(GRADESCOPE_COURSE_NUMBER, 
                                                    BIG_LOOK_UP_TABLE[ASSIGNMENT_NAME], SECTIONS, 
                                                    True, CANVAS_ROSTER,
                                                    email_str)
    print(f"{len(evals)} students exported for sections: {SECTIONS}")
    if len(evals) > 0:
        save_assignment_to_csv(ASSIGNMENT_NAME, evals, SECTIONS)

if DRAFT_EMAILS:
    for section in list(BIG_LOOK_UP_TABLE[ASSIGNMENT_NAME].keys()):
        print_str = ""
        for student_str in email_str:
            if bool(re.search(r'\d'+f'{section[1:]}', student_str)):
                print_str += student_str + "\n"

        if len(print_str) > 0:
            print("""\nHey,\nWhen running my code to extract the rubric score from gradescope for """ + ASSIGNMENT_NAME + """, my code found the following mistakes. Can you fix them in gradescope.\n\n""" + print_str + """\nIf you can update the rubric scores for these students before the coordinator meeting on Tuesday that would be great. If you can't, just let me know when you update them so I can publish the most up to date scores to canvas.\n\nThanks,\nIan Jorquera\n\n\n""")
        
