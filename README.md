# Math160-Automation
Making things ffaster!

## Bonus Quizzes How to
This code is used to generate personalized quizzes for each students from a problem bank of problems for each standard.
1) At the bottom of the file `create_quiz.py` there are setting to set the directory of the problem bank and the output directory. For example you may set `PROBLEM_BANK = r"C:/Users/jorqu/OneDrive - Colostate/..../Module 15 Reassessment/problembank/FA24/"`. Make sure the directory string ends with a `/` and not that in windows you may need to switch all the `\` to `/` even when using the python raw string.
2) Add a tex file in the problem bank directory for each standard you wish to have, including any images. Each file should named as the standard, for example, the standard L2 would have the file `L2.tex`. Each file should be partial tex file starting with `\item`. an example is show below:
```latex
\item\label{std:L3} {\em L3: I can algebraically evaluate the limit of a function at a point.}\\
  Let $g(x)= \begin{cases} 3x+2 & x< 2 \\ 2 & x=2 \\ (x-1)^2+A & x > 2 \\ \end{cases} $.\\
\begin{enumerate}
    \item Compute $\displaystyle{\lim_{x\rightarrow 2^{-}}g(x)}$.
    \vskip 2in
    \item Compute $\displaystyle{\lim_{x\rightarrow 2^{+}}g(x)}$.
    \vskip 2in
    \item Find a value for $A$ so that $\displaystyle{\lim_{x\rightarrow 2}g(x)}$ exists.
\end{enumerate}
``` 
3) Modify the `standards.csv` file if needed. This file is used to create the header page of the quizzes.
4) Change the variable `student_csv_file` to be the location of the csv file with quizzes to create. This file should have no header row. Each row should be `Student Name,Instructor Name,Standard 1, Standard 2, .....` and there is no limit to how many standards each student can have.
5) Once each variable and setting has been modified accordingly, run the file. You will see the Latex outputs in the terminal.

## Gradescope to Canvas How to
This code is used to export the rubric scores from canvas to a usable csv file that can be uploaded using tamper monkey.
1. There is a lot of points of failure in these scripts. So before running update all necessary files from canvas: 
* re-download `canvas_roster.csv` from [canvas](https://teacherscollege.screenstepslive.com/a/1286286-download-a-student-roster-in-canvas) (For the time being this file should be saved in the parent directory and not the `Gradescope` directory), 
* re-sync Canvas roster on Gradescope. 
* Update `config.yaml` (DO NOT COMMIT THIS UPDATED FILE TO GITHIB) This file should be saved in the `Gradescope` directory.
2) This code is split into two files, `GradescopeConfig.py` and  `ExportFromGradescope.py`. All setting can be changed in the `GradescopeConfig.py` file. This file will also walk you through all other set up instructions.
* When setting the `ASSIGNMENT_NAME` variable, it should match the names in gradescope. For example in Gradescope if you have assignments of the form `Module 13: Quiz Section 001` you should set `ASSIGNMENT_NAME="Module 13: Quiz"`. If you are doing a Homework, you should abbreviate Homework as HW, so for example `ASSIGNMENT_NAME="Module 11: HW"`. Or you can modify `KEY_ABBREVIATIONS`
3) You can run either the `GradescopeConfig.py` or the `ExportFromGradescope.py` files. The script may give outputs relating to mistakes in the rubric scores. Please double check the the output has all the standards you think it should. Most issue will be caught by the code, but sometimes entire standards may be left out. This is almost always due to an issue on the gradescope side, often a missing or misspelled rubric score group.
4) output files will be save in the specified output directory, defaults to `Gradescope/output/`
5) To import to scores to canvas use the tamper monkey script `import_rubric_scores` found [here](https://github.com/UCBoulder/canvas-userscripts?tab=readme-ov-file). Your best bet here it to create a new script in tamper monkey and then just copy and paste the code.

## Makeup Quizzes
This code is used to speed up the process of creating pre-calc makeup quiz forms and make printing make up quizzes a bit easier.
1) Update `MAKEUP_QUIZ_EXCEL`, `MAKEUP_QUIZ_EXCEL_SHEET`, and `QUIZZES_LOCATIONS` variable in `save_makeup_quizzes.py` file as needed. The code will read each row of `MAKEUP_QUIZ_EXCEL` to determine the students names, the instructors name, the date for the quiz(which can be omitted, and the date of running the code will be used). All of which go onto the pre-calc makeup quiz form.
* The variable `QUIZZES_LOCATIONS` should be a list of all the available quizzes. Please note that it is not the name of the quiz file that matters here but the directory it is in. For example for the Mod 2 Quiz, It should be saved in a directory named something like `Module 2 Quiz`, the actual quiz can be named what ever. The code will do its best to autodetect the correct quiz for the possibilities and will give a warning if a quiz cant be found.
* If you want to use this code for the personalized reassessments you can but it is often very finicky. Alternatively you can print only the cover pages by setting `print_only_covers=True`. When trying to match the reassessments, you should add the `QUIZZES_LOCATIONS` something like `r"C:/Users/jorqu.../Module 11 Applied Optimization/Mod11Reassessment/ReassessmentQuizzes` which is the path to the output directory of the bonus quiz code, without `/` at the end. The code will then try and match the instructor name and student name to a personalized quiz. You should also set the variable `default_quiz_override` to a copy of the entire quiz, in case no personalized quiz is found.
2) Close the Excel file before running(I always get an access denied error if i don't) and then run the code.
3) Update Excel file indicating which files have been printed.


## Progress Report
This code is intended to use the canvas rubric data to aggregate standard data for every student.
1) Export rubric scores from canvas using Tamper Monkey for each assignment you wish to be included, and put these in `Progress Report/Rubric Scores` directory. Us `export_rubric_scores` from [here](https://github.com/UCBoulder/canvas-userscripts?tab=readme-ov-file).
2) (Re-)download `canvas_roster.csv` from [canvas](https://teacherscollege.screenstepslive.com/a/1286286-download-a-student-roster-in-canvas) This file should be saved in the parent directory and not the `Progress Report` directory.
3) Update the `STANDARDS_dict` variable as needed, to indicate how many standards are needed for completion in the `generate_progress_reports.py` file.
4) run file, the progress report files will be saved in the provided output directory.

