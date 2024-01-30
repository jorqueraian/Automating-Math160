### DO NOT MODIFY THIS FILE UNLESS YOU ARE CONFIDENT IN THE CHANGES
### MOST MODIFICATIONS SHOULD BE DONE IN THE GradescopeConfig.py FILE
### including selecting what assignment to export


# Im going to try this: https://pypi.org/project/gradescope/
# but really im using this https://github.com/mooey5775/gradescope/tree/master which used the above

from GradescopeConfig import *
import re
import pandas as pd

def try_extract_rubric_score(rubric_items, standard, grade):
    # super sloppy fix but for now its fine
    try:
        return rubric_items[get_standard_rubric_key(standard, grade)]
    except KeyError:
        return rubric_items[get_standard_rubric_key_old(standard, grade)]

def get_standard_rubric_key_old(standard, grade): # possible point of failure. need the rubrics to be labeled in a very specific way!
    return f"**{standard}**: Rubric Score: {RubricScoreMod1[grade.name].value}"


def add_rubric_scores(grades_and_evals):
    for student in grades_and_evals:
        student["rubric score"] = {}  # add new dictionary key for scores
        for key in list(student["questions"].keys()):
            if re.match(r"\d{1,2}: \w\d{1,2} .*", key):
                standard = key.split(" ")[1]  # possible point of failure. need the questions to be labeled in a very specific way!
                score = default_rubric_eval
                for rub_score in RubricScore:
                    if try_extract_rubric_score(student["questions"][key]["rubric_items"],standard, rub_score):
                        score = rub_score.value
                student["rubric score"][standard] = score.split(" (")[0]


def save_assignment_to_csv(assignment_name, canvas_df):
    canvas_df.to_csv(f"{assignment_name.replace(':', '').replace(' ', '-')}-results.csv", index=False)


def get_gradescope_data_for_versd_assignment(course_num, assignment_nums, canvas_usable=True, canvas_roster=None):
    evals = []
    for assignment_num in assignment_nums:
        evals_ver = gradescope.get_assignment_evaluations(course_num, assignment_num)
        evals += [eval for eval in evals_ver if eval["Status"] == "Graded"]
    add_rubric_scores(evals)

    if canvas_usable and canvas_roster is not None:
        canvas_df = pd.read_csv(open(canvas_roster, 'rb'), usecols=["Full name", "SIS Id"])
        canvas_id_dict = {row["SIS Id"]: row["Full name"] for _, row in canvas_df.iterrows()}
        assignment_stds = list(evals[ 0]["rubric score"].keys())
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


def get_gradescope_data_for_assignment(course_num, assignment_num, canvas_usable=True, canvas_roster=None):
    evals = gradescope.get_assignment_evaluations(course_num, assignment_num)
    evals = [eval for eval in evals if eval["Status"] != "Missing"]
    add_rubric_scores(evals)
    if canvas_usable and canvas_roster is not None:
        canvas_df = pd.read_csv(open(canvas_roster, 'rb'), usecols=["Full name", "SIS Id"])
        canvas_id_dict = {row["SIS Id"]: row["Full name"] for _, row in canvas_df.iterrows()}
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


evals = get_gradescope_data_for_versd_assignment(GRADESCOPE_COURSE_NUMBER, 
                                                BIG_LOOK_UP_TABLE[ASSIGNMENT_NAME], 
                                                True, CANVAS_ROSTER)
save_assignment_to_csv(ASSIGNMENT_NAME, evals)
