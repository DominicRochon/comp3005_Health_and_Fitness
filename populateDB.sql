/* The purpose of the populateDB.sql file is to have some values already present for testing purposes */


-- Adding some members
INSERT INTO "Users" ("username", "password", "email", "user_type")
VALUES 
('jpen', 'pass', 'JustinePenny@gmail.com', 'member'),
('XPlaneX', 'g0wter', 'planexo@gmail.com', 'member'),
('HowardBerns', 'burnsH0t', 'BernsH@gmail.com', 'member');

INSERT INTO "Members" ("user_id")
VALUES 
(1),
(2),
(3);

INSERT INTO "MemberDetails" ("member_id", "fitness_goals", "health_metrics", "exercise_routine", "fitness_achievements", "billingInfo", "loyalty_points")
VALUES 
(1, 'Run a half-marathon', 'Normal blood pressure, 150lbs, 5foot 7inches', '30 min treadmill', 'ran 5k', 'all fees paid', 14),
(2, 'Bench 150lbs', '160lbs, 5foot 10inches', 'routine2', 'achievement2', 'owes 40$ from group session', 5),
(3, 'Lose 15 pounds', 'High blood pressure, 190lbs, 5foot 9inches', 'routine3', 'achievement3', 'billing3', 228);


-- Adding some trainers
INSERT INTO "Users" ("username", "password", "email", "user_type")
VALUES 
('ChaseyU', 'chuntrain', 'chunder@gmail.com', 'trainer'),
('EmilyCarp10', 'p@ssc0de', 'emCarp@gmail.com', 'trainer');

INSERT INTO "Trainers" ("user_id")
VALUES 
(4),
(5);

INSERT INTO "TrainerDetails" ("trainer_id", "training_schedule", "progress_notes")
VALUES 
(1, 'Monday spin class, weightlifting on tuesday private', 'Howard is showing progress'),
(2, 'Wednesday pilates class, Thursday Yoga workshop', 'Class did well with downwards dog last week');


-- Adding an admin
INSERT INTO "Users" ("username", "password", "email", "user_type")
VALUES 
('admin', 'adminpass', 'morganChu@gmail.com', 'admin');

INSERT INTO "Admins" ("user_id")
VALUES
(6);

-- Adding rooms
INSERT INTO "Rooms" ("name", "equipment_status")
VALUES 
('Suite 1', 'All equipment good'),
('Suite 2', '15lbs dumbbell missing'),
('Gym', 'Broken butterfly machine');

-- Adding an event
INSERT INTO "GroupEvents" ("event_name", "event_date", "event_description", "trainer_id", "room_id")
VALUES 
('Yoga', 'Tuesday', 'A yoga class with a trainer', 1, 2);

-- Add sessions
INSERT INTO "Session" ("member_id", "trainer_id", "room_id")
VALUES 
(1, 2, 3);

INSERT INTO "SessionDetails" ("session_id", "session_date", "session_time", "session_status")
VALUES 
(1, 'Friday', '2pm', 'Scheduled');


INSERT INTO "Session" ("member_id", "trainer_id", "room_id")
VALUES 
(1, 1, 1);

INSERT INTO "SessionDetails" ("session_id", "session_date", "session_time", "session_status")
VALUES 
(2, 'Saturday', '10am', 'Cancelled');