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

# Register User
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    userid = data['userid']
    password = data['password']
    user_type = data['type']
    try:
        conn = connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Users (UserID, Password, Type) VALUES (%s, %s, %s)',
                     (userid, password, user_type))
        conn.commit()
        conn.close()
        response = {'message': 'User registered successfully'}
        return jsonify(response), 201
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    userid = data['userid']
    password = data['password']
    try:
        conn = connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE UserID = %s AND Password = %s',
                            (userid, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            response = {'message': 'Login successful'}
            return jsonify(response), 200
        else:
            response = {'error': 'Invalid credentials'}
            return jsonify(response), 401
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Create Course
@app.route('/create_course', methods=['POST'])
def create_course():
    data = request.get_json()
    course_code = data['course_code']
    course_name = data['course_name']
    try:
        conn = connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Courses (CourseCode, CourseName) VALUES (%s, %s)',
                     (course_code, course_name))
        conn.commit()
        conn.close()
        response = {'message': 'Course created successfully'}
        return jsonify(response), 201
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

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

# Register for Course
@app.route('/register_course', methods=['POST'])
def register_course():
    data = request.get_json()
    student_id = data['student_id']
    course_id = data['course_id']
    try:
        conn = connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Enrolled (StudentID, CourseID) VALUES (%s, %s)',
                     (student_id, course_id))
        conn.commit()
        conn.close()
        response = {'message': 'Registered for course successfully'}
        return jsonify(response), 201
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Retrieve Members
@app.route('/members/<int:course_id>', methods=['GET'])
def members(course_id):
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT Users.UserID, Users.Title, Users.FirstName, Users.MiddleName, Users.LastName, Users.Gender, Users.Type FROM Users INNER JOIN Administrates ON Users.UserID = Administrates.AdminID WHERE Administrates.CourseID = %s UNION SELECT Users.UserID, Users.Title, Users.FirstName, Users.MiddleName, Users.LastName, Users.Gender, Users.Type FROM Users INNER JOIN Teaches ON Users.UserID = Teaches.LecturerID WHERE Teaches.CourseID = %s',
                               (course_id,course_id,))
        members = cursor.fetchall()
        conn.close()
        # members_list = [{'UserID': member[0], 'Type': member[1]} for member in members]
        return jsonify(members), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Retrieve Calendar Events
@app.route('/calendar_events/<int:calendar_event_id>', methods=['GET'])
def calendar_events(calendar_event_id):
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM CalendarEvents WHERE CalendarEventID = %s',
                              (calendar_event_id,))
        events = cursor.fetchall()
        conn.close()
        # events_list = [{'CalendarEventID': event[0], 'StartDate': event[1], 'EndDate': event[2]} for event in events]
        return jsonify(events), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Create Calendar Event
@app.route('/create_calendar_event', methods=['POST'])
def create_calendar_event():
    data = request.get_json()
    course_id = data['course_id']
    start_date = data['start_date']
    end_date = data['end_date']
    try:
        conn = connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO CalendarEvents (SectionID, StartDate, EndDate) VALUES (%s, %s, %s)',
                     (course_id, start_date, end_date))
        conn.commit()
        conn.close()
        response = {'message': 'Calendar event created successfully'}
        return jsonify(response), 201
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Forums
# Retrieve Forums
@app.route('/forums/<int:forum_id>', methods=['GET'])
def forums(forum_id):
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM DiscussionForums WHERE DiscussionForumID = %s',
                              (forum_id,))
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
    data = request.get_json()
    section_id = data['course_id']
    forum_title = data['forum_title']
    created_on = data['created_on']
    created_by = data['created_by']
    forum_description = data['forum_description']
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

# Discussion Threads
# Retrieve Threads
@app.route('/threads/<int:forum_thread_id>', methods=['GET'])
def threads(forum_thread_id):
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM DiscussionThreads WHERE DiscussionThreadID = %s',
                               (forum_thread_id,))
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
    data = request.get_json()
    forum_id = data['forum_id']
    created_on = data['created_on']
    created_by = data['created_by']
    thread_title = data['thread_title']
    thread_description = data['thread_description']
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

# Replies
# Add Reply
@app.route('/add_reply', methods=['POST'])
def add_reply():
    data = request.get_json()
    thread_id = data['thread_id']
    created_on = data['created_on']
    created_by = data['created_by']
    reply_title = data['reply_title']
    reply_content = data['reply_content']
    reply_to_reply = data.get('reply_to_reply', None)  # handling if 'ReplyToReply' is not provided in the request
    try:
        conn = connection()
        cursor = conn.cursor()
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
@app.route('/course_content/<int:course_content_id>', methods=['GET'])
def course_content(course_content_id):
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM CourseContent WHERE CourseContentID = %s)',
                               (course_content_id,))
        content = cursor.fetchall()
        conn.close()
        # content_list = [{'CourseContentID': item[0], 'Content': item[1]} for item in content]
        return jsonify(content), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Assignments
# Submit Assignment
@app.route('/submit_assignment', methods=['POST'])
def submit_assignment():
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
    data = request.get_json()
    student_id = data['student_id']
    assignment_id = data['assignment_id']
    grade = data['grade']
    try:
        conn = connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE Grades SET Grade = %s WHERE StudentID = %s AND AssignmentID = %s',
                     (grade, student_id, assignment_id))
        conn.commit()
        conn.close()
        response = {'message': 'Assignment graded successfully'}
        return jsonify(response), 200
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
        cursor.execute('SELECT CourseID, COUNT(StudentID) AS StudentCount FROM Enrolled GROUP BY CourseID HAVING StudentCount >= 50')
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
        cursor.execute('SELECT StudentID, COUNT(CourseID) AS CourseCount FROM Enrolled GROUP BY StudentID HAVING CourseCount >= 5')
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
        cursor.execute('SELECT LecturerID, COUNT(CourseID) AS CourseCount FROM Teaches GROUP BY LecturerID HAVING CourseCount >= 3')
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
        cursor.execute('SELECT CourseID, COUNT(StudentID) AS StudentCount FROM Enrolled GROUP BY CourseID ORDER BY StudentCount DESC LIMIT 10')
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
        cursor.execute('SELECT StudentID, AVG(Grade) AS AverageGrade FROM Grades GROUP BY StudentID ORDER BY AverageGrade DESC LIMIT 10')
        students = cursor.fetchall()
        conn.close()
        # students_list = [{'StudentID': student[0], 'AverageGrade': student[1]} for student in students]
        return jsonify(students), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=True)

