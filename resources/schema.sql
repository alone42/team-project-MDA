DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS configurations;
DROP TABLE IF EXISTS assignees;

CREATE TABLE IF NOT EXISTS configurations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type BOOLEAN NOT NULL,
    path TEXT NOT NULL,
    begin_time TEXT,
    end_time TEXT
);

CREATE TABLE IF NOT EXISTS assignees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    configuration_id INTEGER,
    task_id INTEGER,
    order_number INTEGER,
    FOREIGN KEY(configuration_id) REFERENCES configurations(id),
    FOREIGN KEY(task_id) REFERENCES tasks(id)
);
