CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dob TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    user_role TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    gender TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    passcode TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id TEXT NOT NULL,
    is_occupied BOOLEAN DEFAULT false,
    is_enabled BOOLEAN DEFAULT true
);

CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id TEXT NOT NULL,
    patient_id TEXT NOT NULL,
    room_id TEXT NULL,
    approved BOOLEAN DEFAULT false,
    date TEXT NOT NULL,
    date_admitted TEXT NULL,
    date_dischared TEXT NULL,
    status TEXT DEFAULT 'PENDING',
    progress INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    note TEXT NOT NULL,
    date TEXT NOT NULL
);