import random
import string
from faker import Faker

courses_data = [
    {'CourseID': 1, 'CourseCode': 'COMP2140', 'CourseName': 'Introduction to Computer Science'},
    {'CourseID': 2, 'CourseCode': 'MATH1250', 'CourseName': 'Calculus I'},
    {'CourseID': 3, 'CourseCode': 'PHYS2320', 'CourseName': 'Physics for Engineers'},
    {'CourseID': 4, 'CourseCode': 'ENGL1100', 'CourseName': 'English Composition'},
    {'CourseID': 5, 'CourseCode': 'PSYC1500', 'CourseName': 'Principles of Psychology'},
    {'CourseID': 6, 'CourseCode': 'HIST1101', 'CourseName': 'World History: Ancient Civilizations'},
    {'CourseID': 7, 'CourseCode': 'CHEM2010', 'CourseName': 'General Chemistry'},
    {'CourseID': 8, 'CourseCode': 'ART1100', 'CourseName': 'Introduction to Drawing'},
    {'CourseID': 9, 'CourseCode': 'BIOL1200', 'CourseName': 'Introduction to Biology'},
    {'CourseID': 10, 'CourseCode': 'ECON2010', 'CourseName': 'Principles of Microeconomics'},
    {'CourseID': 11, 'CourseCode': 'SOC1010', 'CourseName': 'Introduction to Sociology'},
    {'CourseID': 12, 'CourseCode': 'ENGL2200', 'CourseName': 'British Literature'},
    {'CourseID': 13, 'CourseCode': 'COMP2520', 'CourseName': 'Data Structures and Algorithms'},
    {'CourseID': 14, 'CourseCode': 'MATH2350', 'CourseName': 'Differential Equations'},
    {'CourseID': 15, 'CourseCode': 'PHYS2420', 'CourseName': 'Modern Physics'},
    {'CourseID': 16, 'CourseCode': 'ENGL3300', 'CourseName': 'Shakespearean Tragedies'},
    {'CourseID': 17, 'CourseCode': 'PSYC2200', 'CourseName': 'Cognitive Psychology'},
    {'CourseID': 18, 'CourseCode': 'HIST2101', 'CourseName': 'World History: Medieval to Early Modern'},
    {'CourseID': 19, 'CourseCode': 'CHEM3010', 'CourseName': 'Organic Chemistry'},
    {'CourseID': 20, 'CourseCode': 'ART1200', 'CourseName': 'Painting Techniques'},
    {'CourseID': 21, 'CourseCode': 'BIOL2300', 'CourseName': 'Genetics'},
    {'CourseID': 22, 'CourseCode': 'ECON2020', 'CourseName': 'Macroeconomics'},
    {'CourseID': 23, 'CourseCode': 'SOC2010', 'CourseName': 'Social Problems'},
    {'CourseID': 24, 'CourseCode': 'ENGL2400', 'CourseName': 'American Literature'},
    {'CourseID': 25, 'CourseCode': 'COMP3120', 'CourseName': 'Computer Architecture'},
    {'CourseID': 26, 'CourseCode': 'MATH2250', 'CourseName': 'Linear Algebra'},
    {'CourseID': 27, 'CourseCode': 'PHYS3320', 'CourseName': 'Quantum Mechanics'},
    {'CourseID': 28, 'CourseCode': 'ENGL2500', 'CourseName': 'Creative Writing'},
    {'CourseID': 29, 'CourseCode': 'PSYC3200', 'CourseName': 'Abnormal Psychology'},
    {'CourseID': 30, 'CourseCode': 'HIST2201', 'CourseName': 'World History: Enlightenment to Present'},
    {'CourseID': 31, 'CourseCode': 'CHEM3510', 'CourseName': 'Physical Chemistry'},
    {'CourseID': 32, 'CourseCode': 'ART1300', 'CourseName': 'Sculpture'},
    {'CourseID': 33, 'CourseCode': 'BIOL2400', 'CourseName': 'Cell Biology'},
    {'CourseID': 34, 'CourseCode': 'ECON3010', 'CourseName': 'International Economics'},
    {'CourseID': 35, 'CourseCode': 'SOC3010', 'CourseName': 'Criminology'},
    {'CourseID': 36, 'CourseCode': 'ENGL2600', 'CourseName': 'African American Literature'},
    {'CourseID': 37, 'CourseCode': 'COMP3220', 'CourseName': 'Database Systems'},
    {'CourseID': 38, 'CourseCode': 'MATH2450', 'CourseName': 'Probability and Statistics'},
    {'CourseID': 39, 'CourseCode': 'PHYS3420', 'CourseName': 'Electromagnetism'},
    {'CourseID': 40, 'CourseCode': 'ENGL2700', 'CourseName': 'Poetry Workshop'},
    {'CourseID': 41, 'CourseCode': 'PSYC3100', 'CourseName': 'Developmental Psychology'},
    {'CourseID': 42, 'CourseCode': 'HIST2301', 'CourseName': 'American History: Colonial Period'},
    {'CourseID': 43, 'CourseCode': 'CHEM3610', 'CourseName': 'Biochemistry'},
    {'CourseID': 44, 'CourseCode': 'ART1400', 'CourseName': 'Printmaking'},
    {'CourseID': 45, 'CourseCode': 'BIOL2500', 'CourseName': 'Ecology'},
    {'CourseID': 46, 'CourseCode': 'ECON3020', 'CourseName': 'Labor Economics'},
    {'CourseID': 47, 'CourseCode': 'SOC3020', 'CourseName': 'Sociology of Gender'},
    {'CourseID': 48, 'CourseCode': 'ENGL2800', 'CourseName': 'Contemporary Literature'},
    {'CourseID': 49, 'CourseCode': 'COMP3320', 'CourseName': 'Operating Systems'},
    {'CourseID': 50, 'CourseCode': 'MATH2550', 'CourseName': 'Numerical Analysis'},
    {'CourseID': 51, 'CourseCode': 'PHYS3520', 'CourseName': 'Optics'},
    {'CourseID': 52, 'CourseCode': 'ENGL2900', 'CourseName': 'Fiction Writing'},
    {'CourseID': 53, 'CourseCode': 'PSYC3300', 'CourseName': 'Health Psychology'},
    {'CourseID': 54, 'CourseCode': 'HIST2401', 'CourseName': 'American History: Revolutionary War'},
    {'CourseID': 55, 'CourseCode': 'CHEM3710', 'CourseName': 'Analytical Chemistry'},
    {'CourseID': 56, 'CourseCode': 'ART1500', 'CourseName': 'Ceramics'},
    {'CourseID': 57, 'CourseCode': 'BIOL2600', 'CourseName': 'Marine Biology'},
    {'CourseID': 58, 'CourseCode': 'ECON3030', 'CourseName': 'Environmental Economics'},
    {'CourseID': 59, 'CourseCode': 'SOC3030', 'CourseName': 'Sociology of Deviance'},
    {'CourseID': 60, 'CourseCode': 'ENGL3000', 'CourseName': 'Postcolonial Literature'},
    {'CourseID': 61, 'CourseCode': 'COMP3420', 'CourseName': 'Software Engineering'},
    {'CourseID': 62, 'CourseCode': 'MATH2650', 'CourseName': 'Discrete Mathematics'},
    {'CourseID': 63, 'CourseCode': 'PHYS3620', 'CourseName': 'Thermodynamics'},
    {'CourseID': 64, 'CourseCode': 'ENGL3100', 'CourseName': 'Screenwriting'},
    {'CourseID': 65, 'CourseCode': 'PSYC3400', 'CourseName': 'Social Psychology'},
    {'CourseID': 66, 'CourseCode': 'HIST2501', 'CourseName': 'American History: Civil War'},
    {'CourseID': 67, 'CourseCode': 'CHEM3810', 'CourseName': 'Inorganic Chemistry'},
    {'CourseID': 68, 'CourseCode': 'ART1600', 'CourseName': 'Photography'},
    {'CourseID': 69, 'CourseCode': 'BIOL2700', 'CourseName': 'Zoology'},
    {'CourseID': 70, 'CourseCode': 'ECON3040', 'CourseName': 'Public Finance'},
    {'CourseID': 71, 'CourseCode': 'SOC3040', 'CourseName': 'Sociology of Religion'},
    {'CourseID': 72, 'CourseCode': 'ENGL3200', 'CourseName': 'Contemporary Poetry'},
    {'CourseID': 73, 'CourseCode': 'COMP3520', 'CourseName': 'Artificial Intelligence'},
    {'CourseID': 74, 'CourseCode': 'MATH2750', 'CourseName': 'Real Analysis'},
    {'CourseID': 75, 'CourseCode': 'PHYS3720', 'CourseName': 'Nuclear Physics'},
    {'CourseID': 76, 'CourseCode': 'ENGL3300', 'CourseName': 'Playwriting'},
    {'CourseID': 77, 'CourseCode': 'PSYC3500', 'CourseName': 'Industrial/Organizational Psychology'},
    {'CourseID': 78, 'CourseCode': 'HIST2601', 'CourseName': 'American History: Reconstruction Era'},
    {'CourseID': 79, 'CourseCode': 'CHEM3910', 'CourseName': 'Physical Organic Chemistry'},
    {'CourseID': 80, 'CourseCode': 'ART1700', 'CourseName': 'Digital Art'},
    {'CourseID': 81, 'CourseCode': 'BIOL2800', 'CourseName': 'Botany'},
    {'CourseID': 82, 'CourseCode': 'ECON3050', 'CourseName': 'International Trade'},
    {'CourseID': 83, 'CourseCode': 'SOC3050', 'CourseName': 'Urban Sociology'},
    {'CourseID': 84, 'CourseCode': 'ENGL3400', 'CourseName': 'Modern Drama'},
    {'CourseID': 85, 'CourseCode': 'COMP3620', 'CourseName': 'Machine Learning'},
    {'CourseID': 86, 'CourseCode': 'MATH2850', 'CourseName': 'Complex Analysis'},
    {'CourseID': 87, 'CourseCode': 'PHYS3820', 'CourseName': 'Particle Physics'},
    {'CourseID': 88, 'CourseCode': 'ENGL3500', 'CourseName': 'Literary Theory'},
    {'CourseID': 89, 'CourseCode': 'PSYC3600', 'CourseName': 'Clinical Psychology'},
    {'CourseID': 90, 'CourseCode': 'HIST2701', 'CourseName': 'American History: Gilded Age'},
    {'CourseID': 91, 'CourseCode': 'CHEM4010', 'CourseName': 'Environmental Chemistry'},
    {'CourseID': 92, 'CourseCode': 'ART1800', 'CourseName': 'Art History'},
    {'CourseID': 93, 'CourseCode': 'BIOL2900', 'CourseName': 'Microbiology'},
    {'CourseID': 94, 'CourseCode': 'ECON3060', 'CourseName': 'Economic Development'},
    {'CourseID': 95, 'CourseCode': 'SOC3060', 'CourseName': 'Sociology of Health and Illness'},
    {'CourseID': 96, 'CourseCode': 'ENGL3600', 'CourseName': 'Contemporary Fiction'},
    {'CourseID': 97, 'CourseCode': 'COMP3720', 'CourseName': 'Natural Language Processing'},
    {'CourseID': 98, 'CourseCode': 'MATH2950', 'CourseName': 'Topology'},
    {'CourseID': 99, 'CourseCode': 'PHYS3920', 'CourseName': 'Condensed Matter Physics'},
    {'CourseID': 100, 'CourseCode': 'ENGL3700', 'CourseName': 'Film Studies'},
    {'CourseID': 101, 'CourseCode': 'PSYC3700', 'CourseName': 'Forensic Psychology'},
    {'CourseID': 102, 'CourseCode': 'HIST2801', 'CourseName': 'American History: Progressive Era'},
    {'CourseID': 103, 'CourseCode': 'CHEM4110', 'CourseName': 'Physical Biochemistry'},
    {'CourseID': 104, 'CourseCode': 'ART1900', 'CourseName': 'Graphic Design'},
    {'CourseID': 105, 'CourseCode': 'BIOL3000', 'CourseName': 'Immunology'},
    {'CourseID': 106, 'CourseCode': 'ECON3070', 'CourseName': 'Economic Policy'},
    {'CourseID': 107, 'CourseCode': 'SOC3070', 'CourseName': 'Criminological Theory'},
    {'CourseID': 108, 'CourseCode': 'ENGL3800', 'CourseName': 'Science Fiction Literature'},
    {'CourseID': 109, 'CourseCode': 'COMP3820', 'CourseName': 'Computer Graphics'},
    {'CourseID': 110, 'CourseCode': 'MATH3050', 'CourseName': 'Number Theory'},
    {'CourseID': 111, 'CourseCode': 'PHYS4020', 'CourseName': 'Astrophysics'},
    {'CourseID': 112, 'CourseCode': 'ENGL3900', 'CourseName': 'Gender Studies'},
    {'CourseID': 113, 'CourseCode': 'PSYC3800', 'CourseName': 'Counseling Psychology'},
    {'CourseID': 114, 'CourseCode': 'HIST2901', 'CourseName': 'American History: Jazz Age'},
    {'CourseID': 115, 'CourseCode': 'CHEM4210', 'CourseName': 'Medicinal Chemistry'},
    {'CourseID': 116, 'CourseCode': 'ART2000', 'CourseName': 'Typography'},
    {'CourseID': 117, 'CourseCode': 'BIOL3100', 'CourseName': 'Genetics and Society'},
    {'CourseID': 118, 'CourseCode': 'ECON3080', 'CourseName': 'International Finance'},
    {'CourseID': 119, 'CourseCode': 'SOC3080', 'CourseName': 'Social Stratification'},
    {'CourseID': 120, 'CourseCode': 'ENGL4000', 'CourseName': 'Gothic Literature'},
    {'CourseID': 121, 'CourseCode': 'COMP3920', 'CourseName': 'Data Mining'},
    {'CourseID': 122, 'CourseCode': 'MATH3150', 'CourseName': 'Abstract Algebra'},
    {'CourseID': 123, 'CourseCode': 'PHYS4120', 'CourseName': 'Cosmology'},
    {'CourseID': 124, 'CourseCode': 'ENGL4100', 'CourseName': 'Postmodern Literature'},
    {'CourseID': 125, 'CourseCode': 'PSYC3900', 'CourseName': 'Health Psychology'},
    {'CourseID': 126, 'CourseCode': 'HIST3001', 'CourseName': 'American History: Great Depression'},
    {'CourseID': 127, 'CourseCode': 'CHEM4310', 'CourseName': 'Organic Synthesis'},
    {'CourseID': 128, 'CourseCode': 'ART2100', 'CourseName': 'Illustration'},
    {'CourseID': 129, 'CourseCode': 'BIOL3200', 'CourseName': 'Evolutionary Biology'},
    {'CourseID': 130, 'CourseCode': 'ECON3090', 'CourseName': 'Behavioral Economics'},
    {'CourseID': 131, 'CourseCode': 'SOC3090', 'CourseName': 'Sociology of the Family'},
    {'CourseID': 132, 'CourseCode': 'ENGL4200', 'CourseName': 'Renaissance Literature'},
    {'CourseID': 133, 'CourseCode': 'COMP4020', 'CourseName': 'Human-Computer Interaction'},
    {'CourseID': 134, 'CourseCode': 'MATH3250', 'CourseName': 'Partial Differential Equations'},
    {'CourseID': 135, 'CourseCode': 'PHYS4220', 'CourseName': 'Quantum Field Theory'},
    {'CourseID': 136, 'CourseCode': 'ENGL4300', 'CourseName': 'Critical Theory'},
    {'CourseID': 137, 'CourseCode': 'PSYC4000', 'CourseName': 'Sport Psychology'},
    {'CourseID': 138, 'CourseCode': 'HIST3101', 'CourseName': 'American History: World War II'},
    {'CourseID': 139, 'CourseCode': 'CHEM4410', 'CourseName': 'Physical Inorganic Chemistry'},
    {'CourseID': 140, 'CourseCode': 'ART2200', 'CourseName': 'Digital Photography'},
    {'CourseID': 141, 'CourseCode': 'BIOL3300', 'CourseName': 'Ecology and Conservation Biology'},
    {'CourseID': 142, 'CourseCode': 'ECON3100', 'CourseName': 'International Trade Law'},
    {'CourseID': 143, 'CourseCode': 'SOC3100', 'CourseName': 'Sociology of Education'},
    {'CourseID': 144, 'CourseCode': 'ENGL4400', 'CourseName': 'Victorian Literature'},
    {'CourseID': 145, 'CourseCode': 'COMP4120', 'CourseName': 'Natural Language Understanding'},
    {'CourseID': 146, 'CourseCode': 'MATH3350', 'CourseName': 'Algebraic Topology'},
    {'CourseID': 147, 'CourseCode': 'PHYS4320', 'CourseName': 'General Relativity'},
    {'CourseID': 148, 'CourseCode': 'ENGL4500', 'CourseName': 'Postcolonial Theory'},
    {'CourseID': 149, 'CourseCode': 'PSYC4100', 'CourseName': 'Clinical Neuropsychology'},
    {'CourseID': 150, 'CourseCode': 'HIST3201', 'CourseName': 'American History: Cold War Era'},
    {'CourseID': 151, 'CourseCode': 'CHEM4510', 'CourseName': 'Bioinorganic Chemistry'},
    {'CourseID': 152, 'CourseCode': 'ART2300', 'CourseName': 'Digital Painting'},
    {'CourseID': 153, 'CourseCode': 'BIOL3400', 'CourseName': 'Ecology and Evolutionary Biology'},
    {'CourseID': 154, 'CourseCode': 'ECON3110', 'CourseName': 'International Business'},
    {'CourseID': 155, 'CourseCode': 'SOC3110', 'CourseName': 'Sociology of Work'},
    {'CourseID': 156, 'CourseCode': 'ENGL4600', 'CourseName': 'Modernist Literature'},
    {'CourseID': 157, 'CourseCode': 'COMP4220', 'CourseName': 'Cryptography'},
    {'CourseID': 158, 'CourseCode': 'MATH3450', 'CourseName': 'Number Theory'},
    {'CourseID': 159, 'CourseCode': 'PHYS4420', 'CourseName': 'String Theory'},
    {'CourseID': 160, 'CourseCode': 'ENGL4700', 'CourseName': 'Contemporary Literary Criticism'},
    {'CourseID': 161, 'CourseCode': 'PSYC4200', 'CourseName': 'Clinical Psychology'},
    {'CourseID': 162, 'CourseCode': 'HIST3301', 'CourseName': 'American History: Civil Rights Movement'},
    {'CourseID': 163, 'CourseCode': 'CHEM4610', 'CourseName': 'Physical Analytical Chemistry'},
    {'CourseID': 164, 'CourseCode': 'ART2400', 'CourseName': 'Mixed Media'},
    {'CourseID': 165, 'CourseCode': 'BIOL3500', 'CourseName': 'Marine Ecology'},
    {'CourseID': 166, 'CourseCode': 'ECON3120', 'CourseName': 'Globalization'},
    {'CourseID': 167, 'CourseCode': 'SOC3120', 'CourseName': 'Sociology of Media'},
    {'CourseID': 168, 'CourseCode': 'ENGL4800', 'CourseName': 'Postcolonial Literature and Film'},
    {'CourseID': 169, 'CourseCode': 'COMP4320', 'CourseName': 'Data Science'},
    {'CourseID': 170, 'CourseCode': 'MATH3550', 'CourseName': 'Algebraic Topology'},
    {'CourseID': 171, 'CourseCode': 'PHYS4520', 'CourseName': 'Quantum Computing'},
    {'CourseID': 172, 'CourseCode': 'ENGL4900', 'CourseName': 'Literary Journalism'},
    {'CourseID': 173, 'CourseCode': 'PSYC4300', 'CourseName': 'Health Psychology'},
    {'CourseID': 174, 'CourseCode': 'HIST3401', 'CourseName': 'American History: Vietnam War Era'},
    {'CourseID': 175, 'CourseCode': 'CHEM4710', 'CourseName': 'Supramolecular Chemistry'},
    {'CourseID': 176, 'CourseCode': 'ART2500', 'CourseName': 'Fashion Design'},
    {'CourseID': 177, 'CourseCode': 'BIOL3600', 'CourseName': 'Conservation Biology'},
    {'CourseID': 178, 'CourseCode': 'ECON3130', 'CourseName': 'Development Economics'},
    {'CourseID': 179, 'CourseCode': 'SOC3130', 'CourseName': 'Sociology of Religion'},
    {'CourseID': 180, 'CourseCode': 'ENGL5000', 'CourseName': 'American Literature: 20th Century'},
    {'CourseID': 181, 'CourseCode': 'COMP4420', 'CourseName': 'Artificial Neural Networks'},
    {'CourseID': 182, 'CourseCode': 'MATH3650', 'CourseName': 'Differential Geometry'},
    {'CourseID': 183, 'CourseCode': 'PHYS4620', 'CourseName': 'Black Holes'},
    {'CourseID': 184, 'CourseCode': 'ENGL5100', 'CourseName': 'Postcolonial Cinema'},
    {'CourseID': 185, 'CourseCode': 'PSYC4400', 'CourseName': 'Counseling and Psychotherapy'},
    {'CourseID': 186, 'CourseCode': 'HIST3501', 'CourseName': 'American History: Contemporary America'},
    {'CourseID': 187, 'CourseCode': 'CHEM4810', 'CourseName': 'Organometallic Chemistry'},
    {'CourseID': 188, 'CourseCode': 'ART2600', 'CourseName': 'Interior Design'},
    {'CourseID': 189, 'CourseCode': 'BIOL3700', 'CourseName': 'Plant Ecology'},
    {'CourseID': 190, 'CourseCode': 'ECON31 40', 'CourseName': 'Economic Geography'},
    {'CourseID': 191, 'CourseCode': 'SOC3140', 'CourseName': 'Sociology of Immigration'},
    {'CourseID': 192, 'CourseCode': 'ENGL5200', 'CourseName': 'Shakespearean Comedy'},
    {'CourseID': 193, 'CourseCode': 'COMP4520', 'CourseName': 'Machine Vision'},
    {'CourseID': 194, 'CourseCode': 'MATH3750', 'CourseName': 'Algebraic Number Theory'},
    {'CourseID': 195, 'CourseCode': 'PHYS4720', 'CourseName': 'Quantum Gravity'},
    {'CourseID': 196, 'CourseCode': 'ENGL5300', 'CourseName': 'Science Fiction Film'},
    {'CourseID': 197, 'CourseCode': 'PSYC4500', 'CourseName': 'Neuropsychology'},
    {'CourseID': 198, 'CourseCode': 'HIST3601', 'CourseName': 'American History: Post-9/11 Era'},
    {'CourseID': 199, 'CourseCode': 'CHEM4910', 'CourseName': 'Green Chemistry'},
    {'CourseID': 200, 'CourseCode': 'ART2700', 'CourseName': 'Sculpture Installation'}
]
fake = Faker()

# Function to generate a random password excluding specific characters
def generate_password():
    characters = string.ascii_letters + string.digits
    special_chars = "!@#$%&()[]{}?"
    char_string = ''.join(random.choice(characters) for _ in range(7)) + random.choice(special_chars)  # Ensure one special character in the password
    char_list = list(char_string)
    random.shuffle(char_list)
    return ''.join(char_list)

def generate_full_name(lecturer_mode=False):
    genders = ["F", "M"]
    title = []

    gender = random.choice(genders)

    if gender == "M":
        title = ["Mr."]
        first_name = fake.first_name_male()
        middle_name = fake.first_name_male()
    elif gender == 'F':
        title = ["Mrs.", "Ms."]
        first_name = fake.first_name_female()
        middle_name = fake.first_name_female()

    last_name = fake.last_name()

    if lecturer_mode:
        title.append('Dr.')

    return {"title": random.choice(title), "first_name": first_name, "middle_name": middle_name,
            "last_name": last_name, "gender": gender}

num_users_type_1 = 1000
num_users_type_2 = 50
num_users_type_3 = 100000

# Starting user ID
start_user_id = 100000000

# Initialize lists to hold the course assignments for each teacher and administrators for each course
teachers_courses = {}
course_admins = {}

# Generate course assignments for each teacher
for i in range(num_users_type_2):
    teacher_id = start_user_id + num_users_type_1 + i
    courses = random.sample(courses_data, 4)  # Select 4 random courses for each teacher
    teachers_courses[teacher_id] = [course['CourseID'] for course in courses]

# Generate administrators for each course
for course in courses_data:
    course_id = course['CourseID']
    admins = random.sample(range(start_user_id, start_user_id + num_users_type_1), 5)  # Select 5 random admins for each course
    course_admins[course_id] = admins

# Write SQL queries to insert users, teachers, and their course assignments into the database
with open("insert_queries.sql", "w") as sql_file:
    # SQL query to insert users
    sql_query_users = "TRUNCATE TABLE Users;\nTRUNCATE TABLE Teaches;\nTRUNCATE TABLE Administrates;\nTRUNCATE TABLE Enrolled;\n" + "INSERT INTO Users (UserID, Title, FirstName, MiddleName, LastName, Gender, Password, Type) VALUES\n"

    # SQL query to insert course assignments for teachers
    sql_query_teaches = "INSERT INTO Teaches (LecturerID, CourseID) VALUES\n"

    # SQL query to insert administrators for each course
    sql_query_administrates = "INSERT INTO Administrates (AdminID, CourseID) VALUES\n"

    # Generating queries for type 1 users
    for i in range(num_users_type_1):
        user_id = start_user_id + i
        name = generate_full_name()
        password = generate_password()
        sql_query_users += f"({user_id}, '{name['title']}', '{name['first_name']}', '{name['middle_name']}', '{name['last_name']}', '{name['gender']}', '{password}', 1),\n"

    # Generating queries for type 2 users (teachers)
    for i in range(num_users_type_2):
        user_id = start_user_id + num_users_type_1 + i
        name = generate_full_name(lecturer_mode=True)
        password = generate_password()
        sql_query_users += f"({user_id}, '{name['title']}', '{name['first_name']}', '{name['middle_name']}', '{name['last_name']}', '{name['gender']}', '{password}', 2),\n"
        # Insert course assignments for this teacher
        for course_id in teachers_courses[user_id]:
            sql_query_teaches += f"({user_id}, {course_id}),\n"

    # Generating queries for type 3 users
    for i in range(num_users_type_3):
        user_id = start_user_id + num_users_type_1 + num_users_type_2 + i
        name = generate_full_name()
        password = generate_password()
        sql_query_users += f"({user_id}, '{name['title']}', '{name['first_name']}', '{name['middle_name']}', '{name['last_name']}', '{name['gender']}', '{password}', 3),\n"

    # SQL query to insert users into the Enrolled table
    sql_query_enrolled = "TRUNCATE TABLE Enrolled;\nINSERT INTO Enrolled (StudentID, CourseID) VALUES\n"

    # Generate enrollments for each student
    for i in range(num_users_type_3):
        student_id = start_user_id + num_users_type_1 + num_users_type_2 + i
        num_enrollments = random.randint(3, 6)  # Randomly select between 3 to 6 courses for each student
        enrolled_courses = random.sample(courses_data, num_enrollments)
        for course in enrolled_courses:
            course_id = course['CourseID']
            sql_query_enrolled += f"({student_id}, {course_id}),\n"

    sql_query_users = sql_query_users.rstrip(",\n") + ";\n"
    sql_query_teaches = sql_query_teaches.rstrip(",\n") + ";\n"
    sql_query_enrolled = sql_query_enrolled.rstrip(",\n") + ";\n"

    # Generating queries for inserting administrators for each course
    for course_id, admins in course_admins.items():
        for admin_id in admins:
            sql_query_administrates += f"({admin_id}, {course_id}),\n"

    sql_query_administrates = sql_query_administrates.rstrip(",\n") + ";\n"

    # Write the queries to the SQL file
    sql_file.write(sql_query_users)
    sql_file.write(sql_query_teaches)
    sql_file.write(sql_query_administrates)
    sql_file.write(sql_query_enrolled)

print("SQL file 'insert_queries.sql' created.")