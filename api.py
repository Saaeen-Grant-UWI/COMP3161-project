# Group 21

from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

def connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="OurVle_DB"
    )
    return conn



@app.route('/', methods=['GET'])
def welcome():
    response = {'message': 'OurVle API'}
    return jsonify(response), 201

# Register User
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        userid = data['user_id']
        password = data['password']
        try:
            conn = connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute('SELECT * FROM Users WHERE UserID = %s AND Password = %s', (userid, password))
            user = cursor.fetchone()
            if user:

                if user['Active'] == 1:
                    conn.close()
                    response = {'message': 'User account is already active'}
                    return jsonify(response), 200

                cursor.execute('UPDATE Users SET Active = 1 WHERE UserID = %s', (userid,))
                conn.commit()
                
                cursor.execute('SELECT UserType FROM UserTypes WHERE UserTypeID = %s', (user['Type'],))
                user_type = cursor.fetchone()['UserType']
                
                conn.close()
                response = [{'message': 'User has been registered. Account is now active.'}, {'user_type': user_type}]
                return jsonify(response), 200
            else:
                conn.close()
                response = {'message': 'User does not exist'}
                return jsonify(response), 404
        except Exception as e:
            response = {'error': str(e)}
            return jsonify(response), 500

# User Login
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        userid = data['user_id']
        password = data['password']
        try:
            conn = connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM Users WHERE UserID = %s AND Password = %s',
                                (userid, password))
            user = cursor.fetchone()
            conn.close()
            if user:
                response = [user, {'message': 'Login successful'}]
                return jsonify(response), 200
            else:
                response = {'error': 'Invalid credentials'}
                return jsonify(response), 401
        except Exception as e:
            response = {'error': str(e)}
            return jsonify(response), 500

# Courses
# Create Course
@app.route('/create_course', methods=['POST'])
def create_course():
    if request.method == 'POST':
        data = request.get_json()
        user_type = data['user_type']
        course_code = data['course_code']
        course_name = data['course_name']
        
        if user_type == 1:
            try:
                conn = connection()
                cursor = conn.cursor()
                
                # Check if course already exists
                cursor.execute('SELECT * FROM Courses WHERE CourseCode = %s', (course_code,))
                existing_course = cursor.fetchone()
                if existing_course:
                    conn.close()
                    response = {'error': 'Course already exists'}
                    return jsonify(response), 400
                
                # If course doesn't exist, create it
                cursor.execute('INSERT INTO Courses (CourseCode, CourseName) VALUES (%s, %s)',
                               (course_code, course_name))
                conn.commit()
                conn.close()
                response = {'message': 'Course created successfully'}
                return jsonify(response), 201
            except Exception as e:
                response = {'error': str(e)}
                return jsonify(response), 500
        else:
            response = {'message': 'User not an admin, access denied'}
            return jsonify(response), 401


# Retrieve Courses
@app.route('/courses', methods=['GET'])
def courses():
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM Courses')
        courses = cursor.fetchall()
        conn.close()
        # courses_list = [{'CourseCode': course[0], 'CourseName': course[1]} for course in courses]
        return jsonify(courses), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Retrieve Student Courses
@app.route('/courses/student/<int:student_id>', methods=['GET'])
def student_courses(student_id): 
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT Courses.* FROM Enrolled JOIN Courses ON Enrolled.CourseID = Courses.CourseID WHERE Enrolled.StudentID = %s',
                               (student_id,))
        courses = cursor.fetchall()
        conn.close()
        # courses_list = [{'CourseCode': course[0], 'CourseName': course[1]} for course in courses]
        return jsonify(courses), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500
    
# Retrieve Lecturer Courses
@app.route('/courses/lecturer/<int:lecturer_id>', methods=['GET'])
def teacher_courses(lecturer_id): 
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT Courses.* FROM Teaches JOIN Courses ON Teaches.CourseID = Courses.CourseID WHERE Teaches.LecturerID = %s',
                               (lecturer_id,))
        courses = cursor.fetchall()
        conn.close()
        # courses_list = [{'CourseCode': course[0], 'CourseName': course[1]} for course in courses]
        return jsonify(courses), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500


# Register for Course
@app.route('/register_course', methods=['POST'])
def register_course():
    if request.method == 'POST':
        data = request.get_json()
        user_type = data['user_type']
        student_id = data['student_id']
        course_code = data['course_code']

        
        if user_type == 3:
            try:
                conn = connection()
                cursor = conn.cursor(dictionary=True)

                cursor.execute('SELECT CourseID FROM Courses WHERE CourseCode = %s', (course_code,))
                course_id = cursor.fetchone()['CourseID']

                # Check if student is already enrolled in the course
                cursor.execute('SELECT * FROM Enrolled WHERE StudentID = %s AND CourseID = %s',
                               (student_id, course_id))
                existing_enrollment = cursor.fetchone()
                if existing_enrollment:
                    conn.close()
                    response = {'error': 'Student is already enrolled in the course'}
                    return jsonify(response), 400
                
                # If student is not already enrolled, register them for the course
                cursor.execute('INSERT INTO Enrolled (StudentID, CourseID) VALUES (%s, %s)',
                               (student_id, course_id))
                conn.commit()
                conn.close()
                response = {'message': 'Registered for course successfully'}
                return jsonify(response), 201
            except Exception as e:
                response = {'error': str(e)+" or course may not exist"}
                return jsonify(response), 500
        else:
            response = {'message': 'Not a student: cannot register for courses'}
            return jsonify(response), 401
    
@app.route('/assign_course', methods=['POST'])
def assign_course():
    if request.method == 'POST':
        data = request.get_json()
        user_type = data['user_type']
        lecturer_id = data['lecturer_id']
        course_code = data['course_code']

        if user_type == 2 :
            try:
                conn = connection()
                cursor = conn.cursor(dictionary=True)

                cursor.execute('SELECT CourseID FROM Courses WHERE CourseCode = %s', (course_code,))
                course_id = cursor.fetchone()['CourseID']

                cursor.execute('SELECT * FROM Teaches WHERE LecturerID = %s AND CourseID = %s',
                               (lecturer_id, course_id))
                existing_assignment = cursor.fetchone()
                if existing_assignment:
                    conn.close()
                    response = {'error': 'Lecturer is already assigned to the course'}
                    return jsonify(response), 400

                cursor.execute('INSERT INTO Teaches (LecturerID, CourseID) VALUES (%s, %s)',
                            (lecturer_id, course_id))
                conn.commit()
                conn.close()
                response = {'message': 'Assigned to course successfully'}
                return jsonify(response), 201
            except Exception as e:
                response = {'error': str(e)+" or course may not exist"}
                return jsonify(response), 500
        else:
            response = {'message': 'Not a lecturer : connot be assigned to courses'}
            return jsonify(response), 401

# Retrieve Members
@app.route('/members/<string:course_code>', methods=['GET'])
def members(course_code):
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT CourseID FROM Courses WHERE CourseCode = %s', (course_code,))
        course_id = cursor.fetchone()['CourseID']

        cursor.execute('SELECT Users.UserID, Users.Title, Users.FirstName, Users.MiddleName, Users.LastName, Users.Gender, Users.Type FROM Users INNER JOIN Administrates ON Users.UserID = Administrates.AdminID WHERE Administrates.CourseID = %s UNION SELECT Users.UserID, Users.Title, Users.FirstName, Users.MiddleName, Users.LastName, Users.Gender, Users.Type FROM Users INNER JOIN Teaches ON Users.UserID = Teaches.LecturerID WHERE Teaches.CourseID = %s',
                               (course_id,course_id,))
        members = cursor.fetchall() 
        conn.close()
        # members_list = [{'UserID': member[0], 'Type': member[1]} for member in members]
        return jsonify(members), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

@app.route('/create_section/', methods=['POST'])
def create_section():
    try:
        data = request.get_json()
        user_type = data['user_type']
        course_code = data['course_code']
        title = data['title']
        description = data['description']

        conn = connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT CourseID FROM Courses WHERE CourseCode = %s', (course_code,))
        course_id = cursor.fetchone()['CourseID']


        cursor.execute('INSERT INTO Sections (CourseID, SectionTitle, SectionDescription) VALUES (%s, %s, %s)',
                                (course_id, title, description))
        
        conn.commit()
        conn.close()
        response = {'message': 'Section to course successfully'}
        return jsonify(response), 201
    except Exception as e:
            response = {'error': str(e)}
            return jsonify(response), 500

# Retrieve Calendar Events
@app.route('/calendar_events/<string:course_code>', methods=['GET'])
def calendar_events(course_code):
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT ce.CalendarEventID, ce.StartDate, ce.EndDate FROM CalendarEvents ce JOIN Sections s ON ce.SectionID = s.SectionID WHERE s.CourseID = (SELECT CourseID FROM Courses WHERE CourseCode = %s)',
                              (course_code,))
        events = cursor.fetchall()
        conn.close()
        # events_list = [{'CalendarEventID': event[0], 'StartDate': event[1], 'EndDate': event[2]} for event in events]
        return jsonify(events), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500
    
@app.route('/student_calendar_events/<int:student_id>', methods=['GET'])
def student_calendar_events(student_id):
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        events = []

        cursor.execute('SELECT Courses.* FROM Enrolled JOIN Courses ON Enrolled.CourseID = Courses.CourseID WHERE Enrolled.StudentID = %s',
                               (student_id,))
        courses = cursor.fetchall()

        for course in courses :
            cursor.execute('SELECT ce.CalendarEventID, ce.StartDate, ce.EndDate FROM CalendarEvents ce JOIN Sections s ON ce.SectionID = s.SectionID WHERE s.CourseID = (SELECT CourseID FROM Courses WHERE CourseCode = %s)',
                                (course['CourseCode'],))
            events.extend(cursor.fetchall())

        conn.close()
        # events_list = [{'CalendarEventID': event[0], 'StartDate': event[1], 'EndDate': event[2]} for event in events]
        return jsonify(events), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Create Calendar Event
@app.route('/create_calendar_event', methods=['POST'])
def create_calendar_event():
    if request.method == 'POST':
        data = request.get_json()
        user_type = data['user_type']
        section_id = data['section_id']
        start_date = data['start_date']
        end_date = data['end_date']

        if user_type != 3 :
            try:
                conn = connection()
                cursor = conn.cursor(dictionary=True)


                cursor.execute('INSERT INTO CalendarEvents (SectionID, StartDate, EndDate) VALUES (%s, %s, %s)',
                            (section_id, start_date, end_date))
                conn.commit()
                conn.close()
                response = {'message': 'Calendar event created successfully'}
                return jsonify(response), 201
            except Exception as e:
                response = {'error': str(e)}
                return jsonify(response), 500
        else:
            response = {'message': 'Students connot create calendar events'}
            return jsonify(response), 401


# Forums
# Retrieve Forums
@app.route('/forums/<string:course_code>', methods=['GET'])
def forums(course_code):
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT DF.* FROM DiscussionForums DF JOIN Sections S ON DF.SectionID = S.SectionID WHERE S.CourseID = (SELECT CourseID FROM Courses WHERE CourseCode = %s)',
                              (course_code,))
        forums = cursor.fetchall()
        conn.close()
        # forums_list = [{'DiscussionForum': forum[0], 'DiscussionForumTitle': forum[1]} for forum in forums]
        return jsonify(forums), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Create Forum
@app.route('/create_forum', methods=['POST'])
def create_forum():
    if request.method == 'POST':
        data = request.get_json()
        user_type = data['user_type']
        section_id = data['section_id']
        forum_title = data['forum_title']
        created_on = data['created_on']
        created_by = data['created_by']
        forum_description = data['forum_description']

        if user_type != 3 :
            try:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO DiscussionForums (SectionID, CreatedOn, CreatedBy, DiscussionForumTitle, DiscussionForumDescription) VALUES (%s, %s, %s, %s, %s)',
                            (section_id, created_on, created_by, forum_title, forum_description))
                conn.commit()
                conn.close()
                response = {'message': 'Forum created successfully'}
                return jsonify(response), 201
            except Exception as e:
                response = {'error': str(e)}
                return jsonify(response), 500
        else:
            response = {'message': 'Students connot create discussion forums'}
            return jsonify(response), 401

    
# Discussion Threads
# Retrieve Threads
@app.route('/threads/<int:forum_id>', methods=['GET'])
def threads(forum_id):
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM DiscussionThreads WHERE DiscussionForumID = %s',
                               (forum_id,))
        threads = cursor.fetchall()
        conn.close()
        # threads_list = [{'ThreadID': thread[0], 'ThreadTitle': thread[1], 'Post': thread[2]} for thread in threads]
        return jsonify(threads), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Add Thread
@app.route('/add_thread', methods=['POST'])
def add_thread():
    if request.method == 'POST':
        data = request.get_json()
        user_type = data['user_type']
        forum_id = data['forum_id']
        created_on = data['created_on']
        created_by = data['created_by']
        thread_title = data['thread_title']
        thread_description = data['thread_description']

        if user_type != 3 :
            try:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO DiscussionThreads (DiscussionForumID, CreatedOn, CreatedBy, DiscussionForumTitle, DiscussionForumDescription) VALUES (%s, %s, %s, %s, %s)',
                            (forum_id, created_on, created_by, thread_title, thread_description))
                conn.commit()
                conn.close()
                response = {'message': 'Thread added successfully'}
                return jsonify(response), 201
            except Exception as e:
                response = {'error': str(e)}
                return jsonify(response), 500
        else:
            response = {'message': 'Students connot create discussion threads'}
            return jsonify(response), 401

# Replies
# Add Reply
@app.route('/add_reply', methods=['POST'])
def add_reply():
    if request.method == 'POST':
        data = request.get_json()
        thread_id = data['thread_id']
        created_on = data['created_on']
        created_by = data['created_by']
        reply_title = data['reply_title']
        reply_content = data['reply_content']
        reply_to_reply = data.get('reply_to_reply')
        try:
            conn = connection()
            cursor = conn.cursor()

            cursor.execute('SELECT DiscussionForumID FROM DiscussionThreads WHERE DiscussionThreadID = %s', (thread_id,))
            discussion_forum_id = cursor.fetchone()[0]

            cursor.execute('SELECT SectionID FROM DiscussionForums WHERE DiscussionForumID = %s', (discussion_forum_id,))
            section_id = cursor.fetchone()[0]

            cursor.execute('SELECT CourseID FROM Sections WHERE SectionID = %s', (section_id,))
            course_id = cursor.fetchone()[0]

            cursor.execute('SELECT StudentID FROM Enrolled WHERE CourseID = %s', (course_id,))
            enrolled = cursor.fetchone()[0]

            if not enrolled:
                response = {'message': 'Student not enrolled in course'}
                return jsonify(response), 401






            cursor.execute('INSERT INTO DiscussionReplies (DiscussionThreadID, CreatedOn, CreatedBy, DiscussionReplyTitle, DiscussionReplyContent, ReplyToReply) VALUES (%s, %s, %s, %s, %s, %s)',
                        (thread_id, created_on, created_by, reply_title, reply_content, reply_to_reply))
            conn.commit()
            conn.close()
            response = {'message': 'Reply added successfully'}
            return jsonify(response), 201
        except Exception as e:
            response = {'error': str(e)}
            return jsonify(response), 500


# Course Content
# Retrieve Course Content
@app.route('/course_content/<string:course_code>', methods=['GET'])
def course_content(course_code):
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT cc.CourseContentID, cc.Content, cc.ContentType FROM CourseContent cc JOIN Sections s ON cc.SectionID = s.SectionID WHERE s.CourseID = (SELECT CourseID FROM Courses WHERE CourseCode = %s)',
                               (course_code,))
        content = cursor.fetchall()
        conn.close()
        # content_list = [{'CourseContentID': item[0], 'Content': item[1]} for item in content]
        return jsonify(content), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Add Course Content
@app.route('/add_course_content', methods=['POST'])
def add_course_content():
    if request.method == 'POST':
        data = request.get_json()
        user_type = data['user_type']
        section_id = data['section_id']
        content = data['content']
        content_type = data['content_type']

        if user_type == 2 :
            try:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO CourseContent (SectionID, Content, ContentType) VALUES (%s, %s, %s)',
                            (section_id, content, content_type))
                conn.commit()
                conn.close()
                response = {'message': 'Course Content added successfully'}
                return jsonify(response), 201
            except Exception as e:
                response = {'error': str(e)}
                return jsonify(response), 500
        else:
            response = {'message': 'Not a lecturer : connot be add course content'}
            return jsonify(response), 401
    
# Assignments

# Create Assignment
@app.route('/create_assignment', methods=['POST'])
def create_assignment():
    if request.method == 'POST':
        data = request.get_json()
        user_type = data['user_type']
        section_id = data['section_id']
        title = data['title']
        description = data['description']

        if user_type == 2 :
            try:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO Assignments (SectionID, AssignmentTitle, AssignmentDescription) VALUES (%s, %s, %s)',
                            (section_id, title, description))
                conn.commit()
                conn.close()
                response = {'message': 'Assignment created successfully'}
                return jsonify(response), 201
            except Exception as e:
                response = {'error': str(e)}
                return jsonify(response), 500
        else:
            response = {'message': 'Not a lecturer : connot be create assignment'}
            return jsonify(response), 401

# Submit Assignment
@app.route('/submit_assignment', methods=['POST'])
def submit_assignment():
    if request.method == 'POST':
        data = request.get_json()
        student_id = data['student_id']
        assignment_id = data['assignment_id']
        submission = data['submission']
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Submissions (StudentID, AssignmentID, Submission) VALUES (%s, %s, %s)',
                        (student_id, assignment_id, submission))
            conn.commit()
            conn.close()
            response = {'message': 'Assignment submitted successfully'}
            return jsonify(response), 201
        except Exception as e:
            response = {'error': str(e)}
            return jsonify(response), 500
    


# Grade Assignment
@app.route('/grade_assignment', methods=['POST'])
def grade_assignment():
    if request.method == 'POST':
        data = request.get_json()
        user_type = data['user_type']
        student_id = data['student_id']
        assignment_id = data['assignment_id']
        grade = data['grade']

        if user_type == 2 :
            try:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO Grades (StudentID, AssignmentID, Grade) VALUES (%s, %s, %s)',
                            (student_id, assignment_id, grade))
                conn.commit()
                conn.close()
                response = {'message': 'Assignment graded successfully'}
                return jsonify(response), 200
            except Exception as e:
                response = {'error': str(e)}
                return jsonify(response), 500
        else:
            response = {'message': 'Not a lecturer : connot be add grade'}
            return jsonify(response), 401
        
@app.route('/students_average/<int:student_id>', methods=['GET'])
def students_average(student_id):
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT StudentID, AVG(Grade) AS AverageGrade FROM Grades WHERE StudentID = %s', (student_id,))
        students = cursor.fetchall()
        conn.close()
        # students_list = [{'StudentID': student[0], 'AverageGrade': student[1]} for student in students]
        return jsonify(students), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Reports
# All courses that have 50 or more students
@app.route('/courses_with_50_or_more_students', methods=['GET'])
def courses_with_50_or_more_students():
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM courses_with_50_or_more_students')
        courses = cursor.fetchall()
        conn.close()
        # courses_list = [{'CourseID': course[0], 'StudentCount': course[1]} for course in courses]
        return jsonify(courses), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# All students that do 5 or more courses
@app.route('/students_with_5_or_more_courses', methods=['GET'])
def students_with_5_or_more_courses():
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM students_with_5_or_more_courses')
        students = cursor.fetchall()
        conn.close()
        # students_list = [{'StudentID': student[0], 'CourseCount': student[1]} for student in students]
        return jsonify(students), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# All lecturers that teach 3 or more courses
@app.route('/lecturers_with_3_or_more_courses', methods=['GET'])
def lecturers_with_3_or_more_courses():
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM lecturers_with_3_or_more_courses')
        lecturers = cursor.fetchall()
        conn.close()
        # lecturers_list = [{'UserID': lecturer[0], 'CourseCount': lecturer[1]} for lecturer in lecturers]
        return jsonify(lecturers), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# The 10 most enrolled courses
@app.route('/top_10_enrolled_courses', methods=['GET'])
def top_10_enrolled_courses():
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM top_10_enrolled_courses')
        courses = cursor.fetchall()
        conn.close()
        # courses_list = [{'CourseID': course[0], 'StudentCount': course[1]} for course in courses]
        return jsonify(courses), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# The top 10 students with the highest overall averages
@app.route('/top_10_students_highest_averages', methods=['GET'])
def top_10_students_highest_averages():
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM top_10_students_highest_averages')
        students = cursor.fetchall()
        conn.close()
        # students_list = [{'StudentID': student[0], 'AverageGrade': student[1]} for student in students]
        return jsonify(students), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=True)

