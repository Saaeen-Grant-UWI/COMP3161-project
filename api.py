from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('OurVle_DB')
    conn.row_factory = sqlite3.Row
    return conn

# Register User
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    userid = data['userid']
    password = data['password']
    user_type = data['type']
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO Users (UserID, Password, Type) VALUES (?, ?, ?)',
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
def user_login():
    data = request.get_json()
    userid = data['userid']
    password = data['password']
    try:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE UserID = ? AND Password = ?',
                            (userid, password)).fetchone()
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
        conn = get_db_connection()
        conn.execute('INSERT INTO Courses (CourseCode, CourseName) VALUES (?, ?)',
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
def get_courses():
    try:
        conn = get_db_connection()
        courses = conn.execute('SELECT * FROM Courses').fetchall()
        conn.close()
        courses_list = [{'CourseCode': course['CourseCode'], 'CourseName': course['CourseName']} for course in courses]
        return jsonify(courses_list), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Register for Course
@app.route('/register_course', methods=['POST'])
def register_for_course():
    data = request.get_json()
    student_id = data['student_id']
    course_id = data['course_id']
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO Enrolled (StudentID, CourseID) VALUES (?, ?)',
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
def get_course_members(course_id):
    try:
        conn = get_db_connection()
        members = conn.execute('SELECT u.UserID, u.Type FROM Users u JOIN Enrolled e ON u.UserID = e.StudentID WHERE e.CourseID = ?',
                               (course_id,)).fetchall()
        conn.close()
        members_list = [{'UserID': member['UserID'], 'Type': member['Type']} for member in members]
        return jsonify(members_list), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Retrieve Calendar Events
@app.route('/calendar_events/<int:course_id>', methods=['GET'])
def get_calendar_events(course_id):
    try:
        conn = get_db_connection()
        events = conn.execute('SELECT * FROM CalendarEvents WHERE SectionID IN (SELECT SectionID FROM Sections WHERE CourseID = ?)',
                              (course_id,)).fetchall()
        conn.close()
        events_list = [{'CalendarEventID': event['CalendarEventID'], 'StartDate': event['StartDate'], 'EndDate': event['EndDate']} for event in events]
        return jsonify(events_list), 200
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
        conn = get_db_connection()
        conn.execute('INSERT INTO CalendarEvents (SectionID, StartDate, EndDate) VALUES (?, ?, ?)',
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
@app.route('/forums/<int:course_id>', methods=['GET'])
def get_course_forums(course_id):
    try:
        conn = get_db_connection()
        forums = conn.execute('SELECT * FROM DiscussionForums WHERE SectionID IN (SELECT SectionID FROM Sections WHERE CourseID = ?)',
                              (course_id,)).fetchall()
        conn.close()
        forums_list = [{'DiscussionForum': forum['DiscussionForum'], 'DiscussionForumTitle': forum['DiscussionForumTitle']} for forum in forums]
        return jsonify(forums_list), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Create Forum
@app.route('/create_forum', methods=['POST'])
def create_forum():
    data = request.get_json()
    course_id = data['course_id']
    forum_title = data['forum_title']
    forum_desc = data['forum_desc']
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO DiscussionForums (SectionID, DiscussionForumTitle, DiscussionForumDescription) VALUES (?, ?, ?)',
                     (course_id, forum_title, forum_desc))
        conn.commit()
        conn.close()
        response = {'message': 'Forum created successfully'}
        return jsonify(response), 201
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Discussion Threads
# Retrieve Threads
@app.route('/threads/<int:forum_id>', methods=['GET'])
def get_forum_threads(forum_id):
    try:
        conn = get_db_connection()
        threads = conn.execute('SELECT * FROM DiscussionThreads WHERE ForumID = ?',
                               (forum_id,)).fetchall()
        conn.close()
        threads_list = [{'ThreadID': thread['ThreadID'], 'ThreadTitle': thread['ThreadTitle'], 'Post': thread['Post']} for thread in threads]
        return jsonify(threads_list), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Add Thread
@app.route('/add_thread', methods=['POST'])
def add_thread():
    data = request.get_json()
    forum_id = data['forum_id']
    thread_title = data['thread_title']
    post = data['post']
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO DiscussionThreads (ForumID, ThreadTitle, Post) VALUES (?, ?, ?)',
                     (forum_id, thread_title, post))
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
    reply = data['reply']
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO Replies (ThreadID, Reply) VALUES (?, ?)',
                     (thread_id, reply))
        conn.commit()
        conn.close()
        response = {'message': 'Reply added successfully'}
        return jsonify(response), 201
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Course Content
# Retrieve Course Content
@app.route('/course_content/<int:course_id>', methods=['GET'])
def get_course_content(course_id):
    try:
        conn = get_db_connection()
        content = conn.execute('SELECT * FROM CourseContent WHERE SectionID IN (SELECT SectionID FROM Sections WHERE CourseID = ?)',
                               (course_id,)).fetchall()
        conn.close()
        content_list = [{'ContentID': item['ContentID'], 'Content': item['Content']} for item in content]
        return jsonify(content_list), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# Assignments
# Submit Assignment
@app.route('/submit_assignment', methods=['POST'])
def submit_assignment():
    data = request.get_json()
    student_id = data['student_id']
    course_id = data['course_id']
    assignment_id = data['assignment_id']
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO Assignments (StudentID, CourseID, AssignmentID) VALUES (?, ?, ?)',
                     (student_id, course_id, assignment_id))
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
    course_id = data['course_id']
    assignment_id = data['assignment_id']
    grade = data['grade']
    try:
        conn = get_db_connection()
        conn.execute('UPDATE Assignments SET Grade = ? WHERE StudentID = ? AND CourseID = ? AND AssignmentID = ?',
                     (grade, student_id, course_id, assignment_id))
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
def get_courses_with_50_or_more_students():
    try:
        conn = get_db_connection()
        courses = conn.execute('SELECT CourseID, COUNT(StudentID) AS StudentCount FROM Enrolled GROUP BY CourseID HAVING StudentCount >= 50').fetchall()
        conn.close()
        courses_list = [{'CourseID': course['CourseID'], 'StudentCount': course['StudentCount']} for course in courses]
        return jsonify(courses_list), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# All students that do 5 or more courses
@app.route('/students_with_5_or_more_courses', methods=['GET'])
def get_students_with_5_or_more_courses():
    try:
        conn = get_db_connection()
        students = conn.execute('SELECT StudentID, COUNT(CourseID) AS CourseCount FROM Enrolled GROUP BY StudentID HAVING CourseCount >= 5').fetchall()
        conn.close()
        students_list = [{'StudentID': student['StudentID'], 'CourseCount': student['CourseCount']} for student in students]
        return jsonify(students_list), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# All lecturers that teach 3 or more courses
@app.route('/lecturers_with_3_or_more_courses', methods=['GET'])
def get_lecturers_with_3_or_more_courses():
    try:
        conn = get_db_connection()
        lecturers = conn.execute('SELECT UserID, COUNT(CourseID) AS CourseCount FROM Courses GROUP BY UserID HAVING CourseCount >= 3').fetchall()
        conn.close()
        lecturers_list = [{'UserID': lecturer['UserID'], 'CourseCount': lecturer['CourseCount']} for lecturer in lecturers]
        return jsonify(lecturers_list), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# The 10 most enrolled courses
@app.route('/top_10_enrolled_courses', methods=['GET'])
def get_top_10_enrolled_courses():
    try:
        conn = get_db_connection()
        courses = conn.execute('SELECT CourseID, COUNT(StudentID) AS StudentCount FROM Enrolled GROUP BY CourseID ORDER BY StudentCount DESC LIMIT 10').fetchall()
        conn.close()
        courses_list = [{'CourseID': course['CourseID'], 'StudentCount': course['StudentCount']} for course in courses]
        return jsonify(courses_list), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

# The top 10 students with the highest overall averages
@app.route('/top_10_students_highest_averages', methods=['GET'])
def get_top_10_students_highest_averages():
    try:
        conn = get_db_connection()
        students = conn.execute('SELECT StudentID, AVG(Grade) AS AverageGrade FROM Assignments GROUP BY StudentID ORDER BY AverageGrade DESC LIMIT 10').fetchall()
        conn.close()
        students_list = [{'StudentID': student['StudentID'], 'AverageGrade': student['AverageGrade']} for student in students]
        return jsonify(students_list), 200
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=True)
