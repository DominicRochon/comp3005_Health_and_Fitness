DROP TABLE IF EXISTS "Users" CASCADE;
DROP TABLE IF EXISTS "Admins" CASCADE;
DROP TABLE IF EXISTS "Trainers" CASCADE;
DROP TABLE IF EXISTS "TrainerDetails" CASCADE;
DROP TABLE IF EXISTS "Members" CASCADE;
DROP TABLE IF EXISTS "MemberDetails" CASCADE;
DROP TABLE IF EXISTS "Rooms" CASCADE;
DROP TABLE IF EXISTS "Session" CASCADE;
DROP TABLE IF EXISTS "SessionDetails" CASCADE;
DROP TABLE IF EXISTS "MemberGroupEvent" CASCADE;
DROP TABLE IF EXISTS "GroupEvents" CASCADE;

CREATE TABLE "Users" (
 "user_id" SERIAL PRIMARY KEY,
 "username" TEXT NOT NULL UNIQUE,
 "password" TEXT NOT NULL,
 "email" TEXT NOT NULL UNIQUE,
 "user_type" TEXT NOT NULL
);

CREATE TABLE "Admins" (
 "user_id" integer,
 "admin_id" SERIAL PRIMARY KEY
);

CREATE TABLE "Trainers" (
 "user_id" integer,
 "trainer_id" SERIAL PRIMARY KEY
);

CREATE TABLE "TrainerDetails" (
 "trainer_id" integer,
 "training_schedule" TEXT,
 "progress_notes" TEXT
);

CREATE TABLE "Members" (
 "user_id" integer,
 "member_id" SERIAL PRIMARY KEY
);

CREATE TABLE "MemberDetails" (
 "member_id" integer,
 "fitness_goals" TEXT,
 "health_metrics" TEXT,
 "exercise_routine" TEXT,
 "fitness_achievements" TEXT,
 "billingInfo" TEXT,
 "loyalty_points" integer
);

CREATE TABLE "Rooms" (
 "room_id" SERIAL PRIMARY KEY,
 "name" TEXT,
 "equipment_status" TEXT
);

CREATE TABLE "Session" (
 "session_id" SERIAL PRIMARY KEY,
 "member_id" integer,
 "trainer_id" integer,
 "room_id" integer
);

CREATE TABLE "SessionDetails" (
 "session_id" integer,
 "session_date" TEXT,
 "session_time" TEXT,
 "session_status" TEXT
);

CREATE TABLE "MemberGroupEvent" (
  "member_id" integer,
  "event_id" integer,
  UNIQUE ("member_id", "event_id")
);

CREATE TABLE "GroupEvents" (
 "event_id" SERIAL PRIMARY KEY,
 "event_name" TEXT,
 "event_date" TEXT,
 "event_description" TEXT,
 "trainer_id" integer,
 "room_id" integer
);

ALTER TABLE "Admins" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("user_id");

ALTER TABLE "Trainers" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("user_id");

ALTER TABLE "TrainerDetails" ADD FOREIGN KEY ("trainer_id") REFERENCES "Trainers" ("trainer_id");

ALTER TABLE "Members" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("user_id");

ALTER TABLE "MemberDetails" ADD FOREIGN KEY ("member_id") REFERENCES "Members" ("member_id");

ALTER TABLE "Session" ADD FOREIGN KEY ("member_id") REFERENCES "Members" ("member_id");

ALTER TABLE "Session" ADD FOREIGN KEY ("trainer_id") REFERENCES "Trainers" ("trainer_id");

ALTER TABLE "Session" ADD FOREIGN KEY ("room_id") REFERENCES "Rooms" ("room_id");

ALTER TABLE "SessionDetails" ADD FOREIGN KEY ("session_id") REFERENCES "Session" ("session_id");

ALTER TABLE "MemberGroupEvent" ADD FOREIGN KEY ("member_id") REFERENCES "Members" ("member_id");

ALTER TABLE "MemberGroupEvent" ADD FOREIGN KEY ("event_id") REFERENCES "GroupEvents" ("event_id");

ALTER TABLE "GroupEvents" ADD FOREIGN KEY ("trainer_id") REFERENCES "Trainers" ("trainer_id");

ALTER TABLE "GroupEvents" ADD FOREIGN KEY ("room_id") REFERENCES "Rooms" ("room_id");
