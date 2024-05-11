

DROP TABLE IF EXISTS `Administrates`;

CREATE TABLE `Administrates` (
  `AdminID` int NOT NULL,
  `CourseID` int NOT NULL,
  PRIMARY KEY (`AdminID`,`CourseID`)
); 


DROP TABLE IF EXISTS `Assignments`;

CREATE TABLE `Assignments` (
  `AssignmentID` int NOT NULL AUTO_INCREMENT,
  `SectionID` int NOT NULL,
  `AssignmentTitle` varchar(255) NOT NULL,
  `AssignmentDescription` text NOT NULL,
  PRIMARY KEY (`AssignmentID`)
);


DROP TABLE IF EXISTS `CalendarEvents`;

CREATE TABLE `CalendarEvents` (
  `CalendarEventID` int NOT NULL AUTO_INCREMENT,
  `SectionID` int NOT NULL,
  `StartDate` date NOT NULL,
  `EndDate` date NOT NULL,
  PRIMARY KEY (`CalendarEventID`)
);


DROP TABLE IF EXISTS `CourseContent`;

CREATE TABLE `CourseContent` (
  `CourseContentID` int NOT NULL AUTO_INCREMENT,
  `SectionID` int NOT NULL,
  `Content` text NOT NULL,
  `ContentType` int NOT NULL,
  PRIMARY KEY (`CourseContentID`)
);


DROP TABLE IF EXISTS `CourseContentTypes`;

CREATE TABLE `CourseContentTypes` (
  `CourseContentTypeID` int NOT NULL AUTO_INCREMENT,
  `CourseContentType` varchar(64) NOT NULL,
  PRIMARY KEY (`CourseContentTypeID`)
);

INSERT INTO `CourseContentTypes` VALUES (1,'Link'),(2,'File'),(3,'Slides');



DROP TABLE IF EXISTS `Courses`;

CREATE TABLE `Courses` (
  `CourseID` int NOT NULL AUTO_INCREMENT,
  `CourseCode` varchar(10) NOT NULL,
  `CourseName` varchar(255) NOT NULL,
  PRIMARY KEY (`CourseID`)
); 


DROP TABLE IF EXISTS `DiscussionForums`;

CREATE TABLE `DiscussionForums` (
  `DiscussionForumID` int NOT NULL AUTO_INCREMENT,
  `SectionID` int NOT NULL,
  `CreatedOn` date NOT NULL,
  `CreatedBy` int NOT NULL,
  `DiscussionForumTitle` varchar(100) NOT NULL,
  `DiscussionForumDescription` varchar(255) NOT NULL,
  PRIMARY KEY (`DiscussionForumID`)
); 

DROP TABLE IF EXISTS `DiscussionReplies`;

CREATE TABLE `DiscussionReplies` (
  `DiscussionReplyID` int NOT NULL AUTO_INCREMENT,
  `DiscussionThreadID` int NOT NULL,
  `CreatedOn` date NOT NULL,
  `CreatedBy` int NOT NULL,
  `DiscussionReplyTitle` varchar(45) NOT NULL,
  `DiscussionReplyContent` text NOT NULL,
  `ReplyToReply` int DEFAULT '0',
  PRIMARY KEY (`DiscussionReplyID`)
);


DROP TABLE IF EXISTS `DiscussionThreads`;

CREATE TABLE `DiscussionThreads` (
  `DiscussionThreadID` int NOT NULL AUTO_INCREMENT,
  `DiscussionForumID` int NOT NULL,
  `CreatedOn` datetime NOT NULL,
  `CreatedBy` int NOT NULL,
  `DiscussionForumTitle` varchar(255) NOT NULL,
  `DiscussionForumDescription` text NOT NULL,
  PRIMARY KEY (`DiscussionThreadID`)
);

DROP TABLE IF EXISTS `Enrolled`;

CREATE TABLE `Enrolled` (
  `StudentID` int NOT NULL,
  `CourseID` int NOT NULL,
  PRIMARY KEY (`StudentID`,`CourseID`)
);


DROP TABLE IF EXISTS `Grades`;

CREATE TABLE `Grades` (
  `StudentID` int NOT NULL,
  `AssignmentID` int NOT NULL,
  `Grade` int NOT NULL,
  PRIMARY KEY (`AssignmentID`,`StudentID`)
);

DROP TABLE IF EXISTS `Sections`;

CREATE TABLE `Sections` (
  `SectionID` int NOT NULL AUTO_INCREMENT,
  `CourseID` int NOT NULL,
  `SectionTitle` varchar(255) NOT NULL,
  `SectionDescription` text NOT NULL,
  PRIMARY KEY (`SectionID`)
);



DROP TABLE IF EXISTS `Submissions`;

CREATE TABLE `Submissions` (
  `StudentID` int NOT NULL,
  `AssignmentID` int NOT NULL,
  `Submission` text NOT NULL,
  PRIMARY KEY (`StudentID`,`AssignmentID`)
); 

DROP TABLE IF EXISTS `Teaches`;

CREATE TABLE `Teaches` (
  `LecturerID` int NOT NULL,
  `CourseID` int NOT NULL,
  PRIMARY KEY (`LecturerID`,`CourseID`)
);

DROP TABLE IF EXISTS `UserTypes`;

CREATE TABLE `UserTypes` (
  `UserTypeID` int NOT NULL AUTO_INCREMENT,
  `UserType` varchar(45) NOT NULL,
  PRIMARY KEY (`UserTypeID`)
); 


INSERT INTO `UserTypes` VALUES (1,'Admin'),(2,'Lecturer'),(3,'Student');


DROP TABLE IF EXISTS `Users`;

CREATE TABLE `Users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Title` varchar(5) NOT NULL,
  `FirstName` varchar(255) NOT NULL,
  `MiddleName` varchar(255) NOT NULL,
  `LastName` varchar(255) NOT NULL,
  `Gender` char(1) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Type` int NOT NULL,
  `Active` int DEFAULT '0',
  PRIMARY KEY (`UserID`)
);

CREATE OR REPLACE VIEW courses_with_50_or_more_students AS
SELECT CourseID, COUNT(StudentID) AS StudentCount FROM Enrolled GROUP BY CourseID HAVING StudentCount >= 50;

CREATE OR REPLACE VIEW students_with_5_or_more_courses AS
SELECT StudentID, COUNT(CourseID) AS CourseCount FROM Enrolled GROUP BY StudentID HAVING CourseCount >= 5;

CREATE OR REPLACE VIEW lecturers_with_3_or_more_courses AS
SELECT LecturerID, COUNT(CourseID) AS CourseCount FROM Teaches GROUP BY LecturerID HAVING CourseCount >= 3;

CREATE OR REPLACE VIEW top_10_enrolled_courses AS
SELECT CourseID, COUNT(StudentID) AS StudentCount FROM Enrolled GROUP BY CourseID ORDER BY StudentCount DESC LIMIT 10;

CREATE OR REPLACE VIEW top_10_students_highest_averages AS
SELECT StudentID, AVG(Grade) AS AverageGrade FROM Grades GROUP BY StudentID ORDER BY AverageGrade DESC LIMIT 10;
