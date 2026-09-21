-- =========================================================
-- database/schema.sql
--
-- Full MySQL schema for FitTrack, matching the SQLAlchemy models in
-- backend/models/ exactly. You normally do NOT need to run this file
-- by hand -- `python -m backend.database.init_db` creates the
-- database and every table for you from the models. This file exists
-- as a readable, portable reference (and a manual fallback if you
-- ever need to stand up the schema without going through Python).
--
-- Run manually with:
--   mysql -u root -p < database/schema.sql
-- =========================================================

CREATE DATABASE IF NOT EXISTS fittrack
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE fittrack;

-- ---------------------------------------------------------
-- 1. users -- one login account per person (admin/trainer/member)
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50)  NOT NULL,
    email           VARCHAR(120) NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    role            ENUM('ADMIN', 'TRAINER', 'MEMBER') NOT NULL DEFAULT 'MEMBER',
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_users_username (username),
    UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- 2. members -- gym-member profile, 1-to-1 with users
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS members (
    id                          INT AUTO_INCREMENT PRIMARY KEY,
    user_id                     INT NOT NULL,
    first_name                  VARCHAR(50)  NOT NULL,
    last_name                   VARCHAR(50)  NOT NULL,
    phone                       VARCHAR(20)  NULL,
    date_of_birth               DATE         NULL,
    gender                      ENUM('MALE', 'FEMALE', 'OTHER', 'PREFER_NOT_TO_SAY') NULL,
    address                     VARCHAR(255) NULL,
    emergency_contact_name      VARCHAR(100) NULL,
    emergency_contact_phone     VARCHAR(20)  NULL,
    join_date                   DATE NOT NULL,
    created_at                  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at                  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_members_user_id (user_id),
    CONSTRAINT fk_members_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- 3. trainers -- trainer profile, 1-to-1 with users
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS trainers (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    first_name      VARCHAR(50)  NOT NULL,
    last_name       VARCHAR(50)  NOT NULL,
    phone           VARCHAR(20)  NULL,
    specialization  VARCHAR(100) NULL,
    bio             TEXT         NULL,
    hire_date       DATE NOT NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_trainers_user_id (user_id),
    CONSTRAINT fk_trainers_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- 4. memberships -- one row per membership period a member buys
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS memberships (
    id                 INT AUTO_INCREMENT PRIMARY KEY,
    member_id          INT NOT NULL,
    membership_type    ENUM('BASIC', 'STANDARD', 'PREMIUM', 'VIP') NOT NULL,
    status             ENUM('ACTIVE', 'EXPIRED', 'CANCELLED', 'PENDING') NOT NULL DEFAULT 'PENDING',
    start_date         DATE NOT NULL,
    end_date           DATE NOT NULL,
    fee                DECIMAL(8, 2) NOT NULL,
    created_at         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY ix_memberships_member_id (member_id),
    CONSTRAINT fk_memberships_member
        FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- 5. exercises -- shared exercise catalog
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS exercises (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    name                VARCHAR(100) NOT NULL,
    description         TEXT NULL,
    category            ENUM('CARDIO', 'STRENGTH', 'FLEXIBILITY', 'BALANCE', 'HIIT', 'SPORTS', 'OTHER') NOT NULL,
    muscle_group        VARCHAR(100) NULL,
    equipment_needed    VARCHAR(150) NULL,
    difficulty_level    ENUM('BEGINNER', 'INTERMEDIATE', 'ADVANCED') NOT NULL DEFAULT 'BEGINNER',
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_exercises_name (name)
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- 6. workout_plans -- named programs authored by a trainer
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS workout_plans (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    trainer_id          INT NULL,
    name                VARCHAR(150) NOT NULL,
    description         TEXT NULL,
    difficulty_level    ENUM('BEGINNER', 'INTERMEDIATE', 'ADVANCED') NOT NULL DEFAULT 'BEGINNER',
    duration_weeks      INT NULL,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY ix_workout_plans_trainer_id (trainer_id),
    CONSTRAINT fk_workout_plans_trainer
        FOREIGN KEY (trainer_id) REFERENCES trainers(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- 7. workout_exercises -- join: exercises inside a workout plan
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS workout_exercises (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    workout_plan_id     INT NOT NULL,
    exercise_id         INT NOT NULL,
    order_index         INT NOT NULL DEFAULT 1,
    sets                INT NULL,
    reps                INT NULL,
    duration_seconds    INT NULL,
    rest_seconds        INT NULL,
    notes               TEXT NULL,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_plan_exercise_order (workout_plan_id, exercise_id, order_index),
    KEY ix_workout_exercises_exercise_id (exercise_id),
    CONSTRAINT fk_workout_exercises_plan
        FOREIGN KEY (workout_plan_id) REFERENCES workout_plans(id) ON DELETE CASCADE,
    CONSTRAINT fk_workout_exercises_exercise
        FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- 8. member_workouts -- join: a workout plan assigned to a member
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS member_workouts (
    id                          INT AUTO_INCREMENT PRIMARY KEY,
    member_id                   INT NOT NULL,
    workout_plan_id             INT NOT NULL,
    assigned_by_trainer_id      INT NULL,
    status                      ENUM('ACTIVE', 'COMPLETED', 'PAUSED', 'CANCELLED') NOT NULL DEFAULT 'ACTIVE',
    start_date                  DATE NOT NULL,
    end_date                    DATE NULL,
    created_at                  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at                  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY ix_member_workouts_member_id (member_id),
    KEY ix_member_workouts_plan_id (workout_plan_id),
    KEY ix_member_workouts_trainer_id (assigned_by_trainer_id),
    CONSTRAINT fk_member_workouts_member
        FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
    CONSTRAINT fk_member_workouts_plan
        FOREIGN KEY (workout_plan_id) REFERENCES workout_plans(id) ON DELETE CASCADE,
    CONSTRAINT fk_member_workouts_trainer
        FOREIGN KEY (assigned_by_trainer_id) REFERENCES trainers(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- 9. workout_logs -- exercises a member actually completed
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS workout_logs (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    member_id           INT NOT NULL,
    exercise_id         INT NOT NULL,
    member_workout_id   INT NULL,
    log_date            DATE NOT NULL,
    sets_completed      INT NULL,
    reps_completed      INT NULL,
    weight_used_kg      DECIMAL(6, 2) NULL,
    duration_seconds    INT NULL,
    calories_burned     DECIMAL(6, 2) NULL,
    notes               TEXT NULL,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY ix_workout_logs_member_id (member_id),
    KEY ix_workout_logs_exercise_id (exercise_id),
    KEY ix_workout_logs_member_workout_id (member_workout_id),
    KEY ix_workout_logs_log_date (log_date),
    CONSTRAINT fk_workout_logs_member
        FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
    CONSTRAINT fk_workout_logs_exercise
        FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE RESTRICT,
    CONSTRAINT fk_workout_logs_member_workout
        FOREIGN KEY (member_workout_id) REFERENCES member_workouts(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- 10. attendance -- one row per gym visit (check-in/check-out)
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS attendance (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    member_id           INT NOT NULL,
    attendance_date     DATE NOT NULL,
    check_in_time       DATETIME NOT NULL,
    check_out_time      DATETIME NULL,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY ix_attendance_member_id (member_id),
    KEY ix_attendance_member_date (member_id, attendance_date),
    CONSTRAINT fk_attendance_member
        FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- 11. payments -- money a member has paid, usually for a membership
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS payments (
    id                      INT AUTO_INCREMENT PRIMARY KEY,
    member_id               INT NOT NULL,
    membership_id           INT NULL,
    amount                  DECIMAL(8, 2) NOT NULL,
    payment_date            DATE NOT NULL,
    payment_method          ENUM('CASH', 'CARD', 'BANK_TRANSFER', 'ONLINE') NOT NULL,
    status                  ENUM('PENDING', 'COMPLETED', 'FAILED', 'REFUNDED') NOT NULL DEFAULT 'PENDING',
    transaction_reference   VARCHAR(100) NULL,
    created_at              DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_payments_transaction_reference (transaction_reference),
    KEY ix_payments_member_id (member_id),
    KEY ix_payments_membership_id (membership_id),
    CONSTRAINT fk_payments_member
        FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
    CONSTRAINT fk_payments_membership
        FOREIGN KEY (membership_id) REFERENCES memberships(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- 12. announcements -- gym-wide or role-targeted posts
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS announcements (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    created_by          INT NULL,
    title               VARCHAR(150) NOT NULL,
    content             TEXT NOT NULL,
    target_audience     ENUM('ALL', 'MEMBER', 'TRAINER') NOT NULL DEFAULT 'ALL',
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    published_at        DATETIME NULL,
    expires_at          DATETIME NULL,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY ix_announcements_created_by (created_by),
    CONSTRAINT fk_announcements_user
        FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- 13. notifications -- in-app notifications delivered to one user
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS notifications (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    user_id             INT NOT NULL,
    title               VARCHAR(150) NOT NULL,
    message             TEXT NOT NULL,
    notification_type   ENUM('INFO', 'WARNING', 'SUCCESS', 'PAYMENT', 'WORKOUT', 'ANNOUNCEMENT', 'ATTENDANCE') NOT NULL DEFAULT 'INFO',
    is_read             BOOLEAN NOT NULL DEFAULT FALSE,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY ix_notifications_user_id (user_id),
    CONSTRAINT fk_notifications_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- 14. progress_records -- periodic body-measurement snapshots
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS progress_records (
    id                          INT AUTO_INCREMENT PRIMARY KEY,
    member_id                   INT NOT NULL,
    recorded_by_trainer_id      INT NULL,
    record_date                 DATE NOT NULL,
    weight_kg                   DECIMAL(5, 2) NULL,
    body_fat_percentage         DECIMAL(4, 2) NULL,
    muscle_mass_kg              DECIMAL(5, 2) NULL,
    chest_cm                    DECIMAL(5, 2) NULL,
    waist_cm                    DECIMAL(5, 2) NULL,
    hips_cm                     DECIMAL(5, 2) NULL,
    notes                       TEXT NULL,
    created_at                  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at                  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY ix_progress_records_member_id (member_id),
    KEY ix_progress_records_trainer_id (recorded_by_trainer_id),
    KEY ix_progress_records_record_date (record_date),
    CONSTRAINT fk_progress_records_member
        FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
    CONSTRAINT fk_progress_records_trainer
        FOREIGN KEY (recorded_by_trainer_id) REFERENCES trainers(id) ON DELETE SET NULL
) ENGINE=InnoDB;