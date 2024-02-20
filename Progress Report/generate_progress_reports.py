import os
import pandas as pd
import re
import glob
import math
os.chdir(os.path.dirname(__file__))

OUTPUT_DIR = "output/"

canvas_roster = r"../canvas_roster.csv"

# maybe make dict to have number of times needed to get mastery
# Maybe save this to file and load in. FOr now i Wont touc
STANDARDS_dict = {"T1":3,"T2":3,
             "L1":3,"L2":2,"L3":3,"L4":3,"L5":3,"L6":2,"L7":2,
             "D1":2,"D2":2,"D3":3,"D4":3,"D5":2,"D6":2,"D7":3,"D8":3,"D9":3,"D10":2,"D11":3,
             "I1":2,"I2":2,"I3":2,"I4":2,"I5":2}



from enum import Enum
class RubricScore(Enum):
    Satisfactory = "Satisfactory"
    RevisionNeeded = "Minor Revision"
    NotYet = "Not Yet"
    NotGradable = "Not gradable"

STANDARDS = list(STANDARDS_dict.keys())


def read_n_combine(rubrics_dir):
    # If only i knew how to use data frames this would have been a single line! and 100x faster. But what ever
    rubrics = glob.glob(f"{rubrics_dir}/*.csv")
    #combined_df = pd.DataFrame(columns=["Student Name","Student ID"]+STANDARDS)
    combined_dict = {}
    
    canvas_df = pd.read_csv(open(canvas_roster, 'rb'), usecols=["Student SIS ID", "Section Name"])
    canvas_id_dict = {row["Student SIS ID"]: row["Section Name"] for _, row in canvas_df.iterrows()}

    # structure here is {student name + student id: {standard: count}}
    for r in rubrics:
        rubric_df = pd.read_csv(r)
        stds_assessed = rubric_df.columns[4:]
        for _, row in rubric_df.iterrows():
            if row["Student Name"] == "Test Student":
                continue
            posted_score = row["Posted Score"]
            if (row["Student Name"], int(row["Student ID"])) not in combined_dict.keys():  # and combined_df['Student ID'] == row['Student ID']) & (df['B'] == 3)).any():
                combined_dict[(row["Student Name"], int(row["Student ID"]))]= {standard:0 for standard in STANDARDS}
                combined_dict[(row["Student Name"], int(row["Student ID"]))]["Section"]=canvas_id_dict[int(row["Student ID"])]
            for standard_key in stds_assessed:
                standard = standard_key.split(": ")[-1]
                # idk do a check with posted score or something
                if posted_score == 1 and row[standard_key] not in [rub_score.value for rub_score in RubricScore]:
                    print(f'Student: {row["Student Name"]} received no rubric score on {standard} in {r}. But their posted score is 1 (Complete)!')
                if row[standard_key] == "Satisfactory":
                    combined_dict[(row["Student Name"], int(row["Student ID"]))][standard] += 1
    rubric_totals = []
    for student, id in list(combined_dict.keys()):  # skip test student
        if id == "123456789":
            continue
        else:
            rubric_totals.append([student, int(id)] + [combined_dict[(student, id)]["Section"]] + [combined_dict[(student, id)][std] for std in STANDARDS])
        
    the_dframe = pd.DataFrame(rubric_totals, columns=["Student Name", "Student ID", "Section"]+STANDARDS)
    return the_dframe


def from_combine_get_completed_stds(combined_df):
    totals_arr = []
    for _, row in combined_df.iterrows():
        student_info = [row["Student Name"], row["Student ID"], row["Section"]]
        offset = len(student_info)
        completed_stds = student_info+[0]*len(STANDARDS)
        for ind, standard in enumerate(STANDARDS):
            if row[standard] >= STANDARDS_dict[standard]:
                completed_stds[ind+offset] = 1
            else:
                completed_stds[ind+offset] = 0
        totals_arr.append(completed_stds)
    the_dframe = pd.DataFrame(totals_arr, columns=["Student Name", "Student ID", "Section"]+STANDARDS)
    return the_dframe
            

def save_assignment_to_csv(canvas_df, save_name="Grade Report"):
    from datetime import date
    today = date.today()
    canvas_df.to_csv(f"{OUTPUT_DIR}{save_name}-{today.strftime('%m-%d')}.csv", index=False)



combined_scores = read_n_combine("Rubric Scores")
save_assignment_to_csv(combined_scores)
totals = from_combine_get_completed_stds(combined_scores)
save_assignment_to_csv(totals,"Completed Standards")
print("Done!")
