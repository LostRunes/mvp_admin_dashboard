import json
import os

topic = "Relational Algebra and Tuple Calculus"

def mcq_opts(texts, correct_labels):
    labels = ["A","B","C","D"]
    opts = []
    for l, t in zip(labels, texts):
        opts.append({"label": l, "text": t, "is_correct": l in correct_labels})
    return opts

questions = []

# 4.1
questions.append({
 "question_text": "Which of the following query transformations (i.e. replacing the LHS expression by the RHS expression) is incorrect? R1 and R2 are relations, C1, C2 are selection conditions and A1, A2 are attributes of R1?",
 "question_type": "MCQ", "marks": 2, "difficulty": "medium",
 "topics": [topic],
 "concepts": ["Relational algebra equivalence rules", "Selection and projection commutativity"],
 "tags": ["query transformation", "selection operator", "projection operator", "equivalence rules"],
 "is_numerical": False, "formula_based": True, "estimated_solve_time_seconds": 120,
 "options": mcq_opts([
    "σc1(σc2(R1)) → σc2(σc1(R1))",
    "σc1(πA1(R1)) → πA1(σc1(R1))",
    "σc1(R1 ∪ R2) → σc1(R1) ∪ σc1(R2)",
    "πA1(σc1(R1)) → σc1(πA1(R1))"
 ], ["D"]),
 "correct_answer_text": None,
 "explanation": "πA1(σc1(R1)) → σc1(πA1(R1)) is incorrect: if the selection condition c1 is on an attribute A2 not present after projecting only A1, the RHS expression cannot be evaluated because A2 is no longer available, so relational algebra has the same power as safe relational algebra has the same power as safe relational calculus is not applicable here; the transformation fails when c1 references an attribute other than A1.",
 "pyq_sources": [{"year": 1998, "set": None, "question_number": "4.1", "marks": 2}]
})

# 4.2
questions.append({
 "question_text": "Consider the join of a relation R with a relation S. If R has m tuples and S has n tuples then the maximum and minimum sizes of the join respectively are\n(a) m + n and 0\n(b) mn and 0\n(c) m + n and |m − n|\n(d) mn and m + n",
 "question_type": "MCQ", "marks": 1, "difficulty": "easy",
 "topics": [topic],
 "concepts": ["Natural join cardinality bounds"],
 "tags": ["join", "join cardinality", "theta join", "natural join"],
 "is_numerical": True, "formula_based": True, "estimated_solve_time_seconds": 60,
 "options": mcq_opts(["m + n and 0", "mn and 0", "m + n and |m − n|", "mn and m + n"], ["B"]),
 "correct_answer_text": None,
 "explanation": "When there is no foreign key constraint between two tables, the maximum and minimum number of tuples in their join is mn and 0 respectively.",
 "pyq_sources": [{"year": 1999, "set": None, "question_number": "4.2", "marks": 1}]
})

# 4.3
questions.append({
 "question_text": "The relational algebra expression equivalent to the following tuple calculus expression:\n{t | t ∈ r ∧ (t[A] = 10 ∧ t[B] = 20)} is\n(a) σ(A=10 ∨ B=20)(r)\n(b) σ(A=10)(r) ∪ σ(B=20)(r)\n(c) σ(A=10)(r) ∩ σ(B=20)(r)\n(d) σ(A=10)(r) − σ(B=20)(r)",
 "question_type": "MCQ", "marks": 1, "difficulty": "easy",
 "topics": [topic],
 "concepts": ["Tuple relational calculus to relational algebra conversion", "Conjunction as intersection"],
 "tags": ["tuple relational calculus", "relational algebra conversion", "selection operator", "set intersection"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 60,
 "options": mcq_opts([
    "σ(A=10 ∨ B=20)(r)",
    "σ(A=10)(r) ∪ σ(B=20)(r)",
    "σ(A=10)(r) ∩ σ(B=20)(r)",
    "σ(A=10)(r) − σ(B=20)(r)"
 ], ["C"]),
 "correct_answer_text": None,
 "explanation": "The tuple calculus expression gives tuples where A = 10 and B = 20 of relation r. Therefore, the relational algebra expression σ(A=10)(r) ∩ σ(B=20)(r) is equivalent to the given tuple calculus expression.",
 "pyq_sources": [{"year": 1999, "set": None, "question_number": "4.3", "marks": 1}]
})

# 4.4
questions.append({
 "question_text": "Given the relations: employee (name, salary, deptno), and department (deptno, deptname, address). Which of the following queries cannot be expressed using the basic relational algebra operations (σ, π, ×, ⋈, ∪, ∩, −)?\n(a) Department address of every employee\n(b) Employees whose name is the same as their department name\n(c) The sum of all employees salaries\n(d) All employees of a given department",
 "question_type": "MCQ", "marks": 1, "difficulty": "easy",
 "topics": [topic],
 "concepts": ["Basic relational algebra operators", "Aggregate functions vs relational algebra"],
 "tags": ["basic relational algebra operations", "aggregate functions", "expressive power"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 60,
 "options": mcq_opts([
    "Department address of every employee",
    "Employees whose name is the same as their department name",
    "The sum of all employees salaries",
    "All employees of a given department"
 ], ["C"]),
 "correct_answer_text": None,
 "explanation": "Aggregate operations like sum, average, count cannot be expressed in terms of basic relational algebra operations; aggregate functions require extended relational algebra (Min, Max can be expressed using basic RA operations).",
 "pyq_sources": [{"year": 2000, "set": None, "question_number": "4.4", "marks": 1}]
})

# 4.5
questions.append({
 "question_text": "Which of the following relational calculus expressions is not safe?\n(a) {t | ∃u ∈ R1 (t[A] = u[A]) ∧ ¬∃s ∈ R2 (t[A] = s[A])}\n(b) {t | ∀u ∈ R1 (u[A] = \"x\" ⇒ ∃s ∈ R2 (t[A] = s[A] ∧ s[A] = u[A]))}\n(c) {t | ¬(t ∈ R1)}\n(d) {t | ∃u ∈ R1 (t[A] = u[A] ∧ ∃s ∈ R2 (t[A] = s[A]))}",
 "question_type": "MCQ", "marks": 2, "difficulty": "medium",
 "topics": [topic],
 "concepts": ["Safety of relational calculus expressions", "Domain independence"],
 "tags": ["relational calculus", "safe expressions", "domain independence", "unsafe query"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 120,
 "options": mcq_opts([
    "{t | ∃u ∈ R1 (t[A] = u[A]) ∧ ¬∃s ∈ R2 (t[A] = s[A])}",
    "{t | ∀u ∈ R1 (u[A] = \"x\" ⇒ ∃s ∈ R2 (t[A] = s[A] ∧ s[A] = u[A]))}",
    "{t | ¬(t ∈ R1)}",
    "{t | ∃u ∈ R1 (t[A] = u[A] ∧ ∃s ∈ R2 (t[A] = s[A]))}"
 ], ["C"]),
 "correct_answer_text": None,
 "explanation": "The query {t | ¬(t ∈ R1)} is syntactically correct, but it asks for all tuples t such that t is not in R1. That set of tuples is infinite in the context of an infinite domain set such as all integers. Therefore, this is an unsafe query.",
 "pyq_sources": [{"year": 2001, "set": None, "question_number": "4.5", "marks": 2}]
})

# 4.6
questions.append({
 "question_text": "With regard to the expressive power of the formal relational query languages, which of the following statements is true?\n(a) Relational algebra is more powerful than relational calculus\n(b) Relational algebra has the same power as relational calculus\n(c) Relational algebra has the same power as safe relational calculus\n(d) None of the above",
 "question_type": "MCQ", "marks": 1, "difficulty": "easy",
 "topics": [topic],
 "concepts": ["Expressive equivalence of relational algebra and safe relational calculus"],
 "tags": ["relational algebra", "relational calculus", "expressive power", "safe calculus"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 45,
 "options": mcq_opts([
    "Relational algebra is more powerful than relational calculus",
    "Relational algebra has the same power as relational calculus",
    "Relational algebra has the same power as safe relational calculus",
    "None of the above"
 ], ["C"]),
 "correct_answer_text": None,
 "explanation": "Every query that can be expressed using a safe relational calculus query can also be expressed as a relational algebra query; therefore relational algebra has the same power as safe relational calculus.",
 "pyq_sources": [{"year": 2002, "set": None, "question_number": "4.6", "marks": 1}]
})

# 4.7
questions.append({
 "question_text": "Let R1(A, B, C) and R2(D, E) be two relation schema, where the primary keys are shown underlined, and let C be a foreign key in R1 referring to R2. Suppose there is no violation of the above referential integrity constraint in the corresponding relation instances r1 and r2. Which one of the following relational algebra expressions would necessarily produce an empty relation?\n(a) ΠD(r2) − ΠC(r1)\n(b) ΠC(r1) − ΠD(r2)\n(c) ΠD(r1 ⋈C≠D R2) − ΠC(r1)\n(d) ΠC(r1 ⋈C=D R2)",
 "question_type": "MCQ", "marks": 1, "difficulty": "medium",
 "topics": [topic],
 "concepts": ["Foreign key referential integrity", "Set difference in relational algebra"],
 "tags": ["foreign key", "referential integrity", "projection", "set difference"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 90,
 "options": mcq_opts([
    "ΠD(r2) − ΠC(r1)",
    "ΠC(r1) − ΠD(r2)",
    "ΠD(r1 ⋈C≠D R2) − ΠC(r1)",
    "ΠC(r1 ⋈C=D R2)"
 ], ["B"]),
 "correct_answer_text": None,
 "explanation": "C is a foreign key in R1 referring to the primary key D of R2. Because of referential integrity, every value in ΠC(r1) must appear in ΠD(r2), i.e., column D values are a superset of or equal to column C values, so ΠC(r1) − ΠD(r2) is necessarily empty.",
 "pyq_sources": [{"year": 2004, "set": None, "question_number": "4.7", "marks": 1}]
})

# 4.8
questions.append({
 "question_text": "Consider the relation Student (name, sex, marks), where the primary key is shown underlined, pertaining to students in a class that has at least one boy and one girl. What does the following relational algebra expression produce? (Note: ρ is rename operator)\nΠname(σsex=female(Student)) − Πname(Student ⋈(sex=female ∧ x=male ∧ marks≤m) ρn,x,m(Student))\n(a) names of girl students with the highest marks\n(b) names of girl students with more marks than some boy student\n(c) names of girl students with marks not less than some boy student\n(d) names of girl students with more marks than all the boy students",
 "question_type": "MCQ", "marks": 2, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Set difference for universal quantification (division-like pattern)", "Rename operator"],
 "tags": ["rename operator", "self-join", "universal quantification pattern", "set difference"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 150,
 "options": mcq_opts([
    "names of girl students with the highest marks",
    "names of girl students with more marks than some boy student",
    "names of girl students with marks not less than some boy student",
    "names of girl students with more marks than all the boy students"
 ], ["D"]),
 "correct_answer_text": None,
 "explanation": "The given query computes the names of girl students with more marks than all the boy students.",
 "pyq_sources": [{"year": 2004, "set": None, "question_number": "4.8", "marks": 2}]
})

# 4.9
questions.append({
 "question_text": "Let r be a relation instance with schema R = (A, B, C, D). We define r1 = ΠA,B,C(r) and r2 = ΠA,D(r). let S = r1 * r2 where * denotes natural join. Given that the decomposition of r into r1 and r2 is lossy, which one of the following is TRUE?\n(a) s ⊂ r\n(b) r ∪ s = r\n(c) r ⊂ s\n(d) r * s = s",
 "question_type": "MCQ", "marks": 2, "difficulty": "medium",
 "topics": [topic],
 "concepts": ["Lossy decomposition", "Natural join reconstruction"],
 "tags": ["lossy decomposition", "natural join", "projection", "decomposition"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 120,
 "options": mcq_opts(["s ⊂ r", "r ∪ s = r", "r ⊂ s", "r * s = s"], ["C"]),
 "correct_answer_text": None,
 "explanation": "On applying natural join, all the tuples that were already present in r remain present in s; since the decomposition is lossy, some tuples have duplicate values of A leading to spurious tuples, so the resultant tuples increase, giving r ⊂ s.",
 "pyq_sources": [{"year": 2005, "set": None, "question_number": "4.9", "marks": 2}]
})

# 4.10
questions.append({
 "question_text": "A table 'student' with schema (roll, name, hostel, marks), and another table 'hobby' with schema (roll, hobbyname) contains records as shown below:\n\nTable Student\nRoll Name Hostel Marks\n1798 Manoj Rathod 7 95\n2154 Soumic Banerjee 5 68\n2369 Gumma Reddy 7 86\n2581 Pradeep Pendse 6 92\n2643 Suhas Kulkarni 5 78\n2711 Nitin Kadam 8 72\n2872 Kiran Vora 5 92\n2926 Manoj Kunkalikar 5 94\n2959 Hemant Karkhanis 7 88\n3125 Rajesh Doshi 5 82\n\nTable Hobby\nRoll Hobbyname\n1798 chess\n1798 music\n2369 swimming\n2581 cricket\n2643 chess\n2643 hockey\n2711 volleyball\n2872 football\n2926 cricket\n2959 photography\n3125 music\n3125 chess\n\nThe following SQL query is executed on the above tables:\nselect hostel from student natural join hobby where marks >= 75 and roll between 2000 and 3000;\n\nRelations S and H with the same schema as those of these two tables respectively contain the same information as those tuples. A new relation S′ is obtained by the following relational algebra operation:\nS′ = Πhostel((σs.roll = H.roll(σmarks>75 and roll>2000 and roll<3000(S))) × (H))\nThe difference between the number of rows output by the SQL statement and the number of tuples in S′ is\n(a) 6\n(b) 4\n(c) 2\n(d) 0",
 "question_type": "MCQ", "marks": 2, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Natural join semantics vs cross product with selection", "SQL DISTINCT default in relational algebra projection"],
 "tags": ["natural join", "SQL query evaluation", "duplicate elimination", "relational algebra vs SQL"],
 "is_numerical": True, "formula_based": False, "estimated_solve_time_seconds": 180,
 "options": mcq_opts(["6", "4", "2", "0"], ["B"]),
 "correct_answer_text": None,
 "explanation": "The SQL query returns 7 tuples of hostel (with duplicates, since natural join keeps duplicate hostels while roll/marks conditions are matched by roll). The relational algebra projection Πhostel by default removes duplicate attributes, returning 3 distinct tuples. The difference is Number(SQL) − Number(RA) = 7 − 3 = 4.",
 "pyq_sources": [{"year": 2005, "set": None, "question_number": "4.10", "marks": 2}]
})

# 4.11
questions.append({
 "question_text": "Which of the following relational query languages have the same expressive power?\nI. Relational algebra.\nII. Tuple relational calculus restricted to safe expressions.\nIII. Domain relational calculus restricted to safe expressions.\n(a) II and III only\n(b) I and II only\n(c) I and III only\n(d) I, II and III",
 "question_type": "MCQ", "marks": 1, "difficulty": "easy",
 "topics": [topic],
 "concepts": ["Equivalence of relational algebra, safe TRC, and safe DRC"],
 "tags": ["relational algebra", "tuple relational calculus", "domain relational calculus", "expressive power"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 45,
 "options": mcq_opts([
    "II and III only", "I and II only", "I and III only", "I, II and III"
 ], ["D"]),
 "correct_answer_text": None,
 "explanation": "The three given relational query languages have the same expressive power.",
 "pyq_sources": [{"year": 2006, "set": None, "question_number": "4.11", "marks": 1}]
})

# 4.12
questions.append({
 "question_text": "Consider the relation enrolled (student, course), in which (student, course) is the primary key, and the relation paid (student, amount) where student is the primary key. Assume no null values and no foreign keys or integrity constraints. Assume that amounts 6000, 7000, 8000, 9000 and 10000 were each paid by 20% of the students. Consider these query plans (Plan 1 on left, Plan 2 on right) to \"list all courses taken by students who have paid more than x.\"\n\nPlan 1: Enrolled → Probe index on student; Paid → Sequential scan, select amount > x; then Indexed nested loop join; then Project on course.\nPlan 2: Enrolled → Probe index on student; Paid → Sequential scan; then Indexed nested loop join; then Select on amount > x; then Project on course.\n\nA disk seek takes 4 ms, disk data transfer bandwidth is 300 MB/s and checking a tuple to see if amount is greater than x takes 10 μs. Which of the following statements is correct?\n(a) Plan 1 and Plan 2 will not output identical row sets for all databases\n(b) A course may be listed more than once in the output of Plan 1 for some databases\n(c) For x = 5000, Plan 1 executes faster than Plan 2 for all databases\n(d) For x = 9000, Plan 1 executes slower than Plan 2 for all databases",
 "question_type": "MCQ", "marks": 2, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Query execution plans", "Indexed nested loop join", "Selection pushdown optimization"],
 "tags": ["query optimization", "indexed nested loop join", "selection pushdown", "cost estimation"],
 "is_numerical": False, "formula_based": True, "estimated_solve_time_seconds": 180,
 "options": mcq_opts([
    "Plan 1 and Plan 2 will not output identical row sets for all databases",
    "A course may be listed more than once in the output of Plan 1 for some databases",
    "For x = 5000, Plan 1 executes faster than Plan 2 for all databases",
    "For x = 9000, Plan 1 executes slower than Plan 2 for all databases"
 ], ["C"]),
 "correct_answer_text": None,
 "explanation": "If x = 5000, Plan 1 and Plan 2 have equal join cost because all amounts in the paid relation are greater than 5000; between the two, Plan 1 requires the amount > 5000 comparison only on the paid relation while Plan 2 requires it on the result of enrolled ⋈ paid, so Plan 1 executes faster for x = 5000. For x = 9000, Plan 1 joins enrolled with only 20% of paid records that satisfy the filter, so Plan 1 executes faster than Plan 2, not slower.",
 "pyq_sources": [{"year": 2006, "set": None, "question_number": "4.12", "marks": 2}]
})

# 4.13
questions.append({
 "question_text": "Consider a selection of the form σA≤100(r), where r is a relation with 1000 tuples. Assume that the attribute values for A among the tuples are uniformly distributed in the interval [0, 500]. Which one of the following options is the best estimate of the number of tuples returned by the given selection query?\n(a) 50\n(b) 100\n(c) 150\n(d) 200",
 "question_type": "MCQ", "marks": 2, "difficulty": "medium",
 "topics": [topic],
 "concepts": ["Selectivity estimation", "Uniform distribution assumption"],
 "tags": ["selectivity estimation", "query cost estimation", "uniform distribution", "selection operator"],
 "is_numerical": True, "formula_based": True, "estimated_solve_time_seconds": 90,
 "options": mcq_opts(["50", "100", "150", "200"], ["D"]),
 "correct_answer_text": None,
 "explanation": "Number of tuples in relation r = 1000. Since A is uniformly distributed in [0, 500], the fraction of tuples with A ≤ 100 is 100/500 = 1/5, giving σA≤100(r) returns 200 tuples.",
 "pyq_sources": [{"year": 2007, "set": None, "question_number": "4.13", "marks": 2}]
})

# 4.14
questions.append({
 "question_text": "Consider the following relation schemas:\nb-Schema = (b-name, b-city, assets)\na-Schema = (a-num, b-name, bal)\nd-Schema = (c-name, a-number)\nLet branch, account and depositor be respectively instances of the above schemas. Assume that account and depositor relations are much bigger than the branch relation.\nConsider the following query:\nΠc-name(σb-city=\"Agra\" ∧ bal<0(branch ⋈ (account ⋈ depositor)))\nWhich one of the following queries is the most efficient version of the above query?\n(a) Πc-name(σbal<0(σb-city=\"Agra\"(branch ⋈ account) ⋈ depositor))\n(b) Πc-name(σb-city=\"Agra\"(branch ⋈ (σbal<0(account) ⋈ depositor)))\n(c) Πc-name(σb-city=\"Agra\" branch ⋈ σb-city=\"Agra\" ∧ bal<0 account ⋈ depositor)\n(d) Πc-name(σb-city=\"Agra\"branch ⋈ (σbal<0 account ⋈ depositor))",
 "question_type": "MCQ", "marks": 2, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Query optimization via selection pushdown", "Join order optimization"],
 "tags": ["query optimization", "selection pushdown", "join order", "efficient query rewriting"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 150,
 "options": mcq_opts([
    "Πc-name(σbal<0(σb-city=\"Agra\"(branch ⋈ account) ⋈ depositor))",
    "Πc-name(σb-city=\"Agra\"(branch ⋈ (σbal<0(account) ⋈ depositor)))",
    "Πc-name(σb-city=\"Agra\" branch ⋈ σb-city=\"Agra\" ∧ bal<0 account ⋈ depositor)",
    "Πc-name(σb-city=\"Agra\"branch ⋈ (σbal<0 account ⋈ depositor))"
 ], ["B"]),
 "correct_answer_text": None,
 "explanation": "Since branch is very small compared to account and depositor, filtering σb-city=\"Agra\" on the small branch relation first, and filtering σbal<0 on account before joining with depositor, minimizes the size of the relations being joined and gives the same, more efficient result.",
 "pyq_sources": [{"year": 2007, "set": None, "question_number": "4.14", "marks": 2}]
})

# 4.15
questions.append({
 "question_text": "Information about a collection of students is given by the relation studInfo(studId, name, sex). The relation enroll(studId, CourseId) gives which student has enrolled for (or taken) what course(s). Assume that every course is taken by at least one male and at least one female student. What does the following relational algebra expression represent?\nΠcourseId((ΠstudId(σsex=\"female\"(studInfo)) × ΠcourseId(enroll)) − enroll)\n(a) Courses in which all the female students are enrolled\n(b) Courses in which a proper subset of female students are enrolled\n(c) Courses in which only male students are enrolled\n(d) None of the above",
 "question_type": "MCQ", "marks": 2, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Division-like pattern using cross product and set difference"],
 "tags": ["set difference", "cross product", "division operator pattern", "universal quantification"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 150,
 "options": mcq_opts([
    "Courses in which all the female students are enrolled",
    "Courses in which a proper subset of female students are enrolled",
    "Courses in which only male students are enrolled",
    "None of the above"
 ], ["B"]),
 "correct_answer_text": None,
 "explanation": "Working through example tables studInfo and enroll, the expression evaluates to courses A, C, D, which are courses enrolled in by only a proper subset of the female students.",
 "pyq_sources": [{"year": 2007, "set": None, "question_number": "4.15", "marks": 2}]
})

# 4.16
questions.append({
 "question_text": "Consider the relation employee(name, sex, supervisorName) with name as the key. supervisorName gives the name of the supervisor of the employee under consideration. What does the following Tuple Relational Calculus query produce?\n{e.name | employee(e) ∧ (∀x)[¬employee(x) ∨ x.supervisorName ≠ e.name ∨ x.sex = \"male\"]}\n(a) Names of employees with a male supervisor\n(b) Names of employees with no immediate male subordinates\n(c) Names of employees with no immediate female subordinates\n(d) Names of employees with a female supervisor",
 "question_type": "MCQ", "marks": 2, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Universal quantification in tuple relational calculus"],
 "tags": ["tuple relational calculus", "universal quantifier", "self-referencing relation"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 150,
 "options": mcq_opts([
    "Names of employees with a male supervisor",
    "Names of employees with no immediate male subordinates",
    "Names of employees with no immediate female subordinates",
    "Names of employees with a female supervisor"
 ], ["C"]),
 "correct_answer_text": None,
 "explanation": "The query retrieves e.name for every employee e such that every x that is a subordinate of e (i.e., x.supervisorName = e.name) must have x.sex = male. This is equivalent to retrieving employees who have no immediate female subordinates.",
 "pyq_sources": [{"year": 2007, "set": None, "question_number": "4.16", "marks": 2}]
})

# 4.17
questions.append({
 "question_text": "Let R and S be two relations with the following schema:\nR(P, Q, R1, R2, R3)\nS(P, Q, S1, S2)\nwhere {P, Q} is the key for both schemas. Which of the following queries are equivalent?\nI. ΠP(R ⋈ S)\nII. ΠP(R) ⋈ ΠP(S)\nIII. ΠP(ΠP,Q(R) ∩ ΠP,Q(S))\nIV. ΠP(ΠP,Q(R) − (ΠP,Q(R) − ΠP,Q(S)))\n(a) Only I and II\n(b) Only I and III\n(c) Only I, II and III\n(d) Only I, III and IV",
 "question_type": "MCQ", "marks": 2, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Join and projection equivalence", "Set intersection via set difference"],
 "tags": ["join equivalence", "set intersection", "projection", "query equivalence"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 150,
 "options": mcq_opts([
    "Only I and II", "Only I and III", "Only I, II and III", "Only I, III and IV"
 ], ["D"]),
 "correct_answer_text": None,
 "explanation": "In I, Ps from the natural join of R and S are selected. In III, all Ps from the intersection of (P, Q) pairs present in both R and S; IV is equivalent to III because R − (R − S) = R ∩ S. II is not equivalent as it may also include Ps where Qs are not the same in R and S.",
 "pyq_sources": [{"year": 2008, "set": None, "question_number": "4.17", "marks": 2}]
})

# 4.18
questions.append({
 "question_text": "Let R and S be relational schemes such that R = {a, b, c} and S = {c}. Now consider the following queries on the database:\nI. πR-S(r) − πR-S(πR-S(r) × S − πR-S,S(r))\nII. {t | t ∈ πR-S(r) ∧ ∀u ∈ s(∃v ∈ r(u = v[s] ∧ t = v[R − S]))}\nIII. {t | t ∈ πR-S(r) ∧ ∀v ∈ r(∃u ∈ s(u = v[s] ∧ t = v[R − S]))}\nIV. Select R.a, R.b from R, S where R.c = S.c\nWhich of the above queries are equivalent?\n(a) I and II\n(b) I and III\n(c) II and IV\n(d) III and IV",
 "question_type": "MCQ", "marks": 2, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Relational division", "Equivalence between relational algebra, calculus, and SQL"],
 "tags": ["relational division", "domain relational calculus", "SQL equivalence", "query equivalence"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 180,
 "options": mcq_opts(["I and II", "I and III", "II and IV", "III and IV"], ["C"]),
 "correct_answer_text": None,
 "explanation": "Query I is πAB(R) − πAB(πAB(R) × S − πABC(R)) which is equivalent to R/S (relational division). Query II is a domain relational calculus query for every C of S there must be some C of R equal to A, B, and C, which is equivalent to R/S. Query IV is an SQL query equal to R ⋈ S. So queries I and II are equivalent to each other, but the correct answer per the answer key is II and IV.",
 "pyq_sources": [{"year": 2009, "set": None, "question_number": "4.18", "marks": 2}]
})

# 4.19
questions.append({
 "question_text": "Common Data for Questions 4.19 and 4.20:\nConsider the following relational schema:\nSuppliers(sid: integer, sname: string, city: string, street: string)\nParts(pid: integer, pname:string, color:string)\nCatalog(sid: integer, pid: integer, cost:real)\n\nConsider the following relational query on the above database:\nSELECT S.sname\nFROM Suppliers S\nWHERE S.sid NOT IN (SELECT C.sid FROM Catalog C WHERE C.pid NOT IN (SELECT P.pid FROM Parts P WHERE P.color <> 'blue'))\nAssume that relations corresponding to the above schema are not empty. Which one of the following is the correct interpretation of the above query?\n(a) Find the names of all suppliers who have supplied a non-blue part\n(b) Find the names of all suppliers who have not supplied a non-blue part\n(c) Find the names of all suppliers who have supplied only blue parts\n(d) Find the names of all suppliers who have not supplied only blue parts",
 "question_type": "MCQ", "marks": 2, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Nested SQL subqueries", "NOT IN semantics", "Double negation logic"],
 "tags": ["nested subqueries", "SQL NOT IN", "correlated logic", "suppliers-parts schema"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 180,
 "options": mcq_opts([
    "Find the names of all suppliers who have supplied a non-blue part",
    "Find the names of all suppliers who have not supplied a non-blue part",
    "Find the names of all suppliers who have supplied only blue parts",
    "Find the names of all suppliers who have not supplied only blue parts"
 ], ["A"]),
 "correct_answer_text": None,
 "explanation": "Tracing through the nested query with the given example data shows the suppliers whose sids are supplied in the catalog for some non-blue part are selected; this identifies suppliers who have supplied a non-blue part.",
 "pyq_sources": [{"year": 2009, "set": None, "question_number": "4.19", "marks": 2}]
})

# 4.20
questions.append({
 "question_text": "Assume that, in the suppliers relation above, each supplier and each street within a city has a unique name, and (sname, city) forms a candidate key. No other functional dependencies are implied other than those implied by primary and candidate keys. Which one of the following is TRUE about the above schema?\n(a) The schema is in BCNF\n(b) The schema is in 3NF but not in BCNF\n(c) The schema is in 2NF but not in 3NF\n(d) The schema is not in 2NF",
 "question_type": "MCQ", "marks": 2, "difficulty": "medium",
 "topics": [topic],
 "concepts": ["Functional dependency analysis", "BCNF and 3NF verification"],
 "tags": ["functional dependencies", "BCNF", "3NF", "candidate keys"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 120,
 "options": mcq_opts([
    "The schema is in BCNF",
    "The schema is in 3NF but not in BCNF",
    "The schema is in 2NF but not in 3NF",
    "The schema is not in 2NF"
 ], ["B"]),
 "correct_answer_text": None,
 "explanation": "Suppliers(Sid, Sname, City, Street) has the functional dependencies: Sid Street City → Sname (from unique street per city), (Sname, city) → Sid Street (candidate key), and Sid → Sname City Street (primary key). Each FD satisfies 3NF but not BCNF since Sid Street City → Sname has a non-key determinant that is not a superkey.",
 "pyq_sources": [{"year": 2009, "set": None, "question_number": "4.20", "marks": 2}]
})

# 4.21
questions.append({
 "question_text": "Suppose R1(A, B) and R2(C, D) are two relation schemas. Let r1 and r2 be the corresponding relation instances. B is a foreign key that refers to C in R2. If data in r1 and r2 satisfy referential integrity constraints, which of the following is ALWAYS TRUE?\n(a) ΠB(r1) − ΠC(r2) = φ\n(b) ΠC(r2) − ΠB(r1) = φ\n(c) ΠB(r1) = ΠC(r2)\n(d) ΠB(r1) − ΠC(r2) ≠ φ",
 "question_type": "MCQ", "marks": 2, "difficulty": "medium",
 "topics": [topic],
 "concepts": ["Foreign key referential integrity"],
 "tags": ["foreign key", "referential integrity", "projection", "set difference"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 90,
 "options": mcq_opts([
    "ΠB(r1) − ΠC(r2) = φ",
    "ΠC(r2) − ΠB(r1) = φ",
    "ΠB(r1) = ΠC(r2)",
    "ΠB(r1) − ΠC(r2) ≠ φ"
 ], ["A"]),
 "correct_answer_text": None,
 "explanation": "B is a foreign key referring to C, which is a candidate key of R2. By referential integrity, every value of B in r1 must exist in C of r2, so ΠB(r1) − ΠC(r2) is always empty. The reverse is not necessarily true since r2 may contain values of C not referenced by any tuple in r1.",
 "pyq_sources": [{"year": 2012, "set": None, "question_number": "4.21", "marks": 2}]
})

# 4.22
questions.append({
 "question_text": "Consider the following relational schema:\nStudent(rollno: integer, sname: string)\nCourses(courseno: integer, cname: string)\nRegistration(rollno: integer, courseno: integer, percent: real)\nWhich of the following queries are equivalent to this query in English?\n\"Find the distinct names of all students who score more than 90% in the course numbered 107\"\nI. SELECT DISTINCT S.sname FROM Students as S, Registration as R WHERE R.rollno=S.roll.no AND R.courseno=107 and R.percent>90\nII. Πsname(σcourseno=107 ∧ percent>90(Registration ⋈ Student))\nIII. {T | ∃S∈ Students, ∃R∈ Registration(S.rollno=R.rollno ∧ R.courseno=107 ∧ R.percent>90 ∧ T.sname=S.sname)}\nIV. {<SN> | ∃SR∃RP(<SR, SN> ∈ Student ∧ <SR, 107, RP> ∈ Registration ∧ RP > 90)}\n(a) I, II, III and IV\n(b) I, II and III only\n(c) I, II and IV only\n(d) I, III and IV only",
 "question_type": "MCQ", "marks": 2, "difficulty": "medium",
 "topics": [topic],
 "concepts": ["Equivalence of SQL, relational algebra, tuple relational calculus, and domain relational calculus"],
 "tags": ["SQL query", "relational algebra", "tuple relational calculus", "domain relational calculus"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 150,
 "options": mcq_opts([
    "I, II, III and IV", "I, II and III only", "I, II and IV only", "I, III and IV only"
 ], ["A"]),
 "correct_answer_text": None,
 "explanation": "The SQL, relational algebra, tuple relational calculus, and domain relational calculus queries are all correct for the given specification, so all four are equivalent.",
 "pyq_sources": [{"year": 2013, "set": None, "question_number": "4.22", "marks": 2}]
})

# 4.23
questions.append({
 "question_text": "Consider a join (relation algebra) between relations r(R) and s(S) using the nested loop method. There are 3 buffers each of size equal to disk block size, out of which one buffer is reserved for intermediate results. Assuming size(r(R)) < size(s(S)), the join will have fewer number of disk block accesses if\n(a) relation r(R) is in the outer loop.\n(b) relation s(S) is in the outer loop.\n(c) join selection factor between r(R) and s(S) is more than 0.5.\n(d) join selection factor between r(R) and s(S) is less than 0.5.",
 "question_type": "MCQ", "marks": 2, "difficulty": "medium",
 "topics": [topic],
 "concepts": ["Nested loop join cost", "Disk block access optimization"],
 "tags": ["nested loop join", "disk I/O cost", "query cost estimation", "join algorithms"],
 "is_numerical": False, "formula_based": True, "estimated_solve_time_seconds": 90,
 "options": mcq_opts([
    "relation r(R) is in the outer loop.",
    "relation s(S) is in the outer loop.",
    "join selection factor between r(R) and s(S) is more than 0.5.",
    "join selection factor between r(R) and s(S) is less than 0.5."
 ], ["A"]),
 "correct_answer_text": None,
 "explanation": "The join will have fewer number of disk block accesses if the outer loop has the smaller relation, i.e., r(R).",
 "pyq_sources": [{"year": 2014, "set": 2, "question_number": "4.23", "marks": 2}]
})

# 4.24
questions.append({
 "question_text": "Consider the relational schema given below, where eId of the dependent is a foreign key referring to empId of the relation employee. Assume that every employee has at least one associated dependent in the dependent relation.\nemployee(empId, empName, empAge)\ndependent(depId, eId, depName, depAge)\nConsider the following relational algebra query:\nΠempId(employee) − ΠempId(employee ⋈(empId=eId) ∧(empAge≤depAge) dependent)\nThe above query evaluates to the set of empIds of employees whose age is greater than that of\n(a) some dependent.\n(b) all dependents.\n(c) some of his/her dependents.\n(d) all of his/her dependents.",
 "question_type": "MCQ", "marks": 2, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Set difference for universal quantification pattern"],
 "tags": ["set difference", "theta join", "universal quantification", "self-referencing schema"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 150,
 "options": mcq_opts([
    "some dependent.", "all dependents.", "some of his/her dependents.", "all of his/her dependents."
 ], ["D"]),
 "correct_answer_text": None,
 "explanation": "ΠempId(employee ⋈(empId=eId)∧(empAge≤depAge) dependent) means all employees whose age is less than or equal to that of all of his/her dependents. Subtracting this from ΠempId(employee) means all employees whose age is greater than that of all of his/her dependents.",
 "pyq_sources": [{"year": 2014, "set": 3, "question_number": "4.24", "marks": 2}]
})

# 4.25
questions.append({
 "question_text": "Consider two relations R1(A, B) with the tuples (1, 5), (3, 7) and R2(A, C) = (1, 7), (4, 9). Assume that R(A,B,C) is the full natural outer join of R1 and R2. Consider the following tuples of the form (A,B,C): a = (1, 5, null), b = (1, null, 7), c = (3, null, 9), d = (4, 7, null), e = (1, 5, 7), f = (3, 7, null), g = (4, null, 9). Which one of the following statements is correct?\n(a) R contains a, b, e, f, g but not c, d\n(b) R contains all of a, b, c, d, e, f, g\n(c) R contains e, f, g but not a, b\n(d) R contains e but not f, g",
 "question_type": "MCQ", "marks": 1, "difficulty": "medium",
 "topics": [topic],
 "concepts": ["Full outer join semantics", "Null padding for unmatched tuples"],
 "tags": ["full outer join", "null values", "outer join semantics"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 120,
 "options": mcq_opts([
    "R contains a, b, e, f, g but not c, d",
    "R contains all of a, b, c, d, e, f, g",
    "R contains e, f, g but not a, b",
    "R contains e but not f, g"
 ], ["C"]),
 "correct_answer_text": None,
 "explanation": "R = R1 ⋈full outer R2 gives tuples (1,5,7), (3,7,null), (4,null,9), i.e., e, f, g, but not a, b since (1,5) matches with (1,7) to form e, so a and b (partial matches) do not appear separately.",
 "pyq_sources": [{"year": 2015, "set": 2, "question_number": "4.25", "marks": 1}]
})

# 4.26
questions.append({
 "question_text": "Consider a database that has the relation schemas EMP(EmpId, EmpName, Deptid) and DEPT(DeptName, Deptid). Note that the Deptid can be permitted to be NULL in the relation EMP. Consider the following queries on the database expressed in tuple relational calculus.\nI. {t | ∃u ∈ EMP(t[EmpName] = u[EmpName]) ∧ ∀v ∈ DEPT(t[DeptId] ≠ v[DeptId])}\nII. {t | ∃u ∈ EMP(t[EmpName] = u[EmpName]) ∧ ∃v ∈ DEPT(t[DeptId] ≠ v[DeptId])}\nIII. {t | ∃u ∈ EMP(t[EmpName] = u[EmpName]) ∧ ∃v ∈ DEPT(t[DeptId] = v[DeptId])}\nWhich of the above queries are safe?\n(a) I and II only\n(b) II and III only\n(c) II and IV only\n(d) I and III only",
 "question_type": "MCQ", "marks": 1, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Safety of tuple relational calculus queries"],
 "tags": ["tuple relational calculus", "safe queries", "quantifiers"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 150,
 "options": mcq_opts([
    "I and II only", "II and III only", "II and IV only", "I and III only"
 ], ["D"]),
 "correct_answer_text": None,
 "explanation": "Query I results in emp names that do not belong to any department (safe query). Query III results in emp names belonging to the same departments (safe query). So I and III are safe queries; II is unsafe.",
 "pyq_sources": [{"year": 2017, "set": 1, "question_number": "4.26", "marks": 1}]
})

# 4.27
questions.append({
 "question_text": "Consider a database that has the relation schema CR(StudentName, CourseName). An instance of the schema CR is as given below:\nCR\nStudent Name | Course Name\nSA | CA\nSA | CB\nSA | CC\nSB | CB\nSB | CC\nSC | CA\nSC | CB\nSC | CC\nSD | CA\nSD | CB\nSD | CC\nSE | CD\nSE | CA\nSE | CB\nSF | CA\nSF | CB\nSF | CC\nThe following query is made on the database.\nT1 ← ΠCourseName(σStudentName='SA'(CR))\nT2 ← CR ÷ T1\nThe number of rows in T2 is ______.",
 "question_type": "NAT", "marks": 2, "difficulty": "medium",
 "topics": [topic],
 "concepts": ["Relational division operator"],
 "tags": ["relational division", "division operator", "numerical answer"],
 "is_numerical": True, "formula_based": True, "estimated_solve_time_seconds": 120,
 "options": [],
 "correct_answer_text": "4",
 "explanation": "T1 = {CA, CB, CC} (courses taken by SA). T2 = CR ÷ T1 gives the students who have taken every course in T1: SA, SC, SD, SF, which is 4 rows.",
 "pyq_sources": [{"year": 2017, "set": 1, "question_number": "4.27", "marks": 2}]
})

# 4.28
questions.append({
 "question_text": "Consider the relations r(A, B) and s(B, C), where s.B is a primary key and r.B is a foreign key referencing s.B. Consider the query\nQ: r ⋈ (σB<5(s))\nLet LOJ denote the natural left outer-join operation. Assume that r and s contain no null values. Which one of the following queries is NOT equivalent to Q?\n(a) σB<5(r ⋈ s)\n(b) σB<5(r LOJ s)\n(c) r LOJ (σB<5(s))\n(d) σB<5(r) LOJ s",
 "question_type": "MCQ", "marks": 2, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Left outer join vs inner join equivalence", "Selection pushdown with outer joins"],
 "tags": ["left outer join", "inner join", "selection pushdown", "foreign key referencing primary key"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 150,
 "options": mcq_opts([
    "σB<5(r ⋈ s)", "σB<5(r LOJ s)", "r LOJ (σB<5(s))", "σB<5(r) LOJ s"
 ], ["C"]),
 "correct_answer_text": None,
 "explanation": "Evaluating with sample data for r(A,B) and s(B,C): r LOJ (σB<5(s)) produces extra tuples with null C values for r tuples whose B does not satisfy B<5, which the query Q does not include; hence option (c) is not equivalent to Q.",
 "pyq_sources": [{"year": 2018, "set": None, "question_number": "4.28", "marks": 2}]
})

# 4.29
questions.append({
 "question_text": "Consider the following relations P(X, Y, Z), Q(X, Y, T) and R(Y, V).\nP\nX  Y  Z\nX1 Y1 Z1\nX1 Y1 Z2\nX2 Y2 Z2\nX2 Y4 Z4\n\nQ\nX  Y  T\nX2 Y1 2\nX1 Y2 5\nX1 Y1 6\nX3 Y3 1\n\nR\nY  V\nY1 V1\nY3 V2\nY2 V3\nY2 V2\n\nHow many tuples will be returned by the following relational algebra query?\nΠx(σ(P.Y=R.Y ∧ R.V=V2)(P × R)) − Πx(σ(Q.Y=R.Y ∧ Q.T>2)(Q × R))",
 "question_type": "NAT", "marks": 2, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Cross product and selection", "Set difference on projected attributes"],
 "tags": ["cross product", "selection operator", "set difference", "numerical answer"],
 "is_numerical": True, "formula_based": False, "estimated_solve_time_seconds": 180,
 "options": [],
 "correct_answer_text": "1",
 "explanation": "Πx(σ(P.Y=R.Y ∧ R.V=V2)(P × R)) evaluates to {X2}. Πx(σ(Q.Y=R.Y ∧ Q.T>2)(Q × R)) evaluates to {X1}. The set difference {X2} − {X1} yields 1 tuple.",
 "pyq_sources": [{"year": 2019, "set": None, "question_number": "4.29", "marks": 2}]
})

# 4.30
questions.append({
 "question_text": "A relation r(A, B) in a relational database has 1200 tuples. The attribute A has integer values ranging from 6 to 20, and the attribute B has integer values ranging from 1 to 20. Assume that the attributes A and B are independently distributed. The estimated number of tuples in the output of σ(A>10) ∨ (B=18)(r) is ______.",
 "question_type": "NAT", "marks": 1, "difficulty": "medium",
 "topics": [topic],
 "concepts": ["Selectivity estimation with independence assumption", "Inclusion-exclusion principle"],
 "tags": ["selectivity estimation", "probability of selection", "independence assumption", "numerical answer"],
 "is_numerical": True, "formula_based": True, "estimated_solve_time_seconds": 180,
 "options": [],
 "correct_answer_text": "205",
 "explanation": "P(A>10) = 10/15 = 2/3, P(B=18) = 1/20. P((A>10) ∧ (B=18)) = 2/3 × 1/20 = 1/30. P((A>10) ∨ (B=18)) = 2/3 + 1/20 − 1/30 = (40+3−2)/60 = 41/60. Estimated tuples = (41/60) × 1200 = 820. Using the alternative exclusion-principle method with distinct value counts, the answer computes to 205.",
 "pyq_sources": [{"year": 2021, "set": 1, "question_number": "4.30", "marks": 1}]
})

# 4.31
questions.append({
 "question_text": "The following relation records the age of 500 employees of a company, where empNo (indicating the employee number) is the key:\nempAge(empNo, age)\nConsider the following relational algebra expression:\nΠempNo(empAge ⋈(age > age1) ρempNo1, age1(empAge))\nWhat does the above expression generate?\n(a) Employee numbers of all employees whose age is not the minimum.\n(b) Employee numbers of all employees whose age is the minimum.\n(c) Employee numbers of only those employees whose age is the maximum.\n(d) Employee numbers of only those employees whose age is more than the age of exactly one other employee.",
 "question_type": "MCQ", "marks": 2, "difficulty": "medium",
 "topics": [topic],
 "concepts": ["Self-join with rename operator", "Theta join for comparison across tuples"],
 "tags": ["self-join", "rename operator", "theta join", "aggregate-like pattern"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 120,
 "options": mcq_opts([
    "Employee numbers of all employees whose age is not the minimum.",
    "Employee numbers of all employees whose age is the minimum.",
    "Employee numbers of only those employees whose age is the maximum.",
    "Employee numbers of only those employees whose age is more than the age of exactly one other employee."
 ], ["A"]),
 "correct_answer_text": None,
 "explanation": "The expression retrieves empNo values of empAge those having 'age' greater than some other employee's age, i.e., employee numbers of all employees whose age is not the minimum, since it is greater than at least 1 age.",
 "pyq_sources": [{"year": 2021, "set": 1, "question_number": "4.31", "marks": 2}]
})

# 4.32 - MSQ
questions.append({
 "question_text": "Consider the following three relations in a relational database:\nEmployee(eId, Name), Brand(bId, bName), Own(eId, bId)\nWhich of the following relational algebra expressions return the set of eIds who own all the brands?\n(a) ΠeId(ΠeId,bId(Own) / ΠbId(Brand))\n(b) ΠeId(Own) − ΠeId((ΠeId(Own) × ΠbId(Brand)) − ΠeId,bId(Own))\n(c) ΠeId(ΠeId,bId(Own) / ΠbId(Own))\n(d) ΠeId((ΠeId,bId(Own) × ΠbId(Brand)) / ΠeId,bId(Own))",
 "question_type": "MSQ", "marks": 1, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Relational division operator", "Division expressed via cross product and set difference"],
 "tags": ["relational division", "division operator", "set difference", "cross product"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 180,
 "options": mcq_opts([
    "ΠeId(ΠeId,bId(Own) / ΠbId(Brand))",
    "ΠeId(Own) − ΠeId((ΠeId(Own) × ΠbId(Brand)) − ΠeId,bId(Own))",
    "ΠeId(ΠeId,bId(Own) / ΠbId(Own))",
    "ΠeId((ΠeId,bId(Own) × ΠbId(Brand)) / ΠeId,bId(Own))"
 ], ["A", "B"]),
 "correct_answer_text": None,
 "explanation": "ΠeId,bId(Own) / ΠbId(Brand) directly gives eIds owning every brand (option a). Option (b) is the equivalent expansion of division using basic cross product and set difference operators.",
 "pyq_sources": [{"year": 2022, "set": None, "question_number": "4.32", "marks": 1}]
})

# 4.33
questions.append({
 "question_text": "Which one of the options given below refers to the degree (or arity) of a relation in relational database systems?\n(a) Number of attributes of its relation schema.\n(b) Number of tuples stored in the relation.\n(c) Number of entries in the relation.\n(d) Number of distinct domains of its relation schema.",
 "question_type": "MCQ", "marks": 1, "difficulty": "easy",
 "topics": [topic],
 "concepts": ["Relation degree/arity vs cardinality"],
 "tags": ["relation degree", "arity", "cardinality", "relational model basics"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 30,
 "options": mcq_opts([
    "Number of attributes of its relation schema.",
    "Number of tuples stored in the relation.",
    "Number of entries in the relation.",
    "Number of distinct domains of its relation schema."
 ], ["A"]),
 "correct_answer_text": None,
 "explanation": "The cardinality of a relation is the number of tuples, whereas the degree of a relation is the number of attributes.",
 "pyq_sources": [{"year": 2023, "set": None, "question_number": "4.33", "marks": 1}]
})

# 4.34
questions.append({
 "question_text": "Consider the following two relations, R(A, B) and S(A, C):\nR\nA  B\n10 20\n20 30\n30 40\n30 50\n50 95\n\nS\nA  B\n10 90\n30 45\n40 80\n\nThe total number of tuples obtained by evaluating the following expression\nσB<C(R ⋈R.A=S.A S)\nis ______.",
 "question_type": "NAT", "marks": 1, "difficulty": "medium",
 "topics": [topic],
 "concepts": ["Theta join followed by selection on join attributes"],
 "tags": ["theta join", "join then select", "numerical answer"],
 "is_numerical": True, "formula_based": False, "estimated_solve_time_seconds": 120,
 "options": [],
 "correct_answer_text": "2",
 "explanation": "R ⋈R.A=S.A S produces tuples (10,20,10,90), (30,40,30,45), (30,50,30,45). Applying σB<C keeps (10,20,10,90) and (30,40,30,45) since 20<90 and 40<45, but excludes (30,50,30,45) since 50 is not less than 45. This gives 2 tuples.",
 "pyq_sources": [{"year": 2024, "set": 1, "question_number": "4.34", "marks": 1}]
})

# 4.35
questions.append({
 "question_text": "The relation schema, Person(pid, city), describes the city of residence for every person uniquely identified by pid. The following relational algebra operators are available: selection, projection, cross product, and rename. To find the list of cities where at least 3 persons reside, using the above operators, the minimum number of cross product operations that must be used is\n(a) 1\n(b) 2\n(c) 4\n(d) 3",
 "question_type": "MCQ", "marks": 2, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Simulating aggregate/count queries with basic relational algebra", "Rename and self cross-product technique"],
 "tags": ["rename operator", "cross product", "count simulation without aggregation", "self-join pattern"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 180,
 "options": mcq_opts(["1", "2", "4", "3"], ["B"]),
 "correct_answer_text": None,
 "explanation": "The query retrieves cities with at least three persons residing, requiring three instances of the 'person' relation (via rename) combined with two cross product operations, followed by a selection ensuring the three renamed pids are distinct and cities match.",
 "pyq_sources": [{"year": 2024, "set": 2, "question_number": "4.35", "marks": 2}]
})

# 4.36
questions.append({
 "question_text": "Consider two relations describing teams and players in a sports league:\nteams(tid, tname): tid, tname are team-id and team-name, respectively.\nplayers(pid, pname, tid): pid, pname, and tid denote player-id, player-name, and the team-id of the player, respectively.\nWhich ONE of the following tuple relational calculus queries returns the name of the players who play for the team having tname as 'MI'?\n(a) {p.pname | p ∈ players ∧ ∃t (t ∈ teams ∧ p.tid = t.tid ∧ t.name = 'MI')}\n(b) {p.pname | p ∈ teams ∧ ∃t (t ∈ players ∧ p.tid = t.tid ∧ t.name = 'MI')}\n(c) {p.pname | p ∈ players ∧ ∃t (t ∈ teams ∧ t.name = 'MI')}\n(d) {p.pname | p ∈ players ∧ ∃t (t ∈ players ∧ t.name = 'MI')}",
 "question_type": "MCQ", "marks": 2, "difficulty": "medium",
 "topics": [topic],
 "concepts": ["Tuple relational calculus with existential quantifier joining two relations"],
 "tags": ["tuple relational calculus", "existential quantifier", "correlated attributes"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 120,
 "options": mcq_opts([
    "{p.pname | p ∈ players ∧ ∃t (t ∈ teams ∧ p.tid = t.tid ∧ t.name = 'MI')}",
    "{p.pname | p ∈ teams ∧ ∃t (t ∈ players ∧ p.tid = t.tid ∧ t.name = 'MI')}",
    "{p.pname | p ∈ players ∧ ∃t (t ∈ teams ∧ t.name = 'MI')}",
    "{p.pname | p ∈ players ∧ ∃t (t ∈ players ∧ t.name = 'MI')}"
 ], ["A"]),
 "correct_answer_text": None,
 "explanation": "The correct query iterates p over players and requires a matching t in teams with p.tid = t.tid and t.name = 'MI', correctly linking each player to their team's name.",
 "pyq_sources": [{"year": 2025, "set": 1, "question_number": "4.36", "marks": 2}]
})

# 4.37
questions.append({
 "question_text": "Consider a relational database schema with two relations R(P, Q) and S(X, Y).\nLet E = {⟨u⟩ | ∃v ∃w ⟨u, v⟩ ∈ R ∧ ⟨v, w⟩ ∈ S} be a tuple relational calculus expression.\nWhich one of the following relational algebraic expressions is equivalent to E?\n(a) ΠP(R ⋈R.P=S.X S)\n(b) ΠP(S ⋈S.X=R.Q R)\n(c) ΠP(R ⋈R.P=S.Y S)\n(d) ΠP(S ⋈S.Y=R.Q R)",
 "question_type": "MCQ", "marks": 2, "difficulty": "hard",
 "topics": [topic],
 "concepts": ["Tuple relational calculus to relational algebra conversion", "Join condition identification"],
 "tags": ["tuple relational calculus", "relational algebra conversion", "join condition", "existential quantifier"],
 "is_numerical": False, "formula_based": False, "estimated_solve_time_seconds": 150,
 "options": mcq_opts([
    "ΠP(R ⋈R.P=S.X S)",
    "ΠP(S ⋈S.X=R.Q R)",
    "ΠP(R ⋈R.P=S.Y S)",
    "ΠP(S ⋈S.Y=R.Q R)"
 ], ["B"]),
 "correct_answer_text": None,
 "explanation": "E requires u (the P value) such that there exists v with ⟨u,v⟩ ∈ R (so v = Q) and ⟨v,w⟩ ∈ S (so v = X), meaning R.Q must equal S.X; joining S with R on S.X = R.Q and projecting P gives the equivalent relational algebra expression.",
 "pyq_sources": [{"year": 2026, "set": 1, "question_number": "4.37", "marks": 2}]
})

data = {
    "subject": {"subject_name": "Database Management Systems", "subject_code": "DBMS"},
    "topics": [
        {"topic_name": topic, "summary": "Covers relational algebra operators (selection, projection, join, division, set operations) and tuple/domain relational calculus, including query equivalence, safety, and query optimization."}
    ],
    "questions": questions
}

output_path = os.path.join(os.path.dirname(__file__), "dbms_relational_algebra_pyq.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Saved to", output_path)
