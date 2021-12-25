import sqlite3

from sqlite3 import Error


class ConfigurationSettings:
    def __init__(self):
        database = r"resources/database.db"
        self.conn = self.create_connection(database)

    def create_connection(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return self.conn

    def close_connection(self):
        if self.conn:
            self.conn.close()

    def recreate_columns(self):
        if self.conn is not None:
            with open("resources/schema.sql") as f:
                self.conn.executescript(f.read())

    def create_table(self, create_table_sql):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute(create_table_sql)
            except Error as e:
                print(e)

    def add_new_task(self, task):
        if self.conn is not None:
            sql = ''' INSERT INTO tasks(name, type, path, begin_time, end_time)
                      VALUES(?,?,?,?,?) '''
            cur = self.conn.cursor()
            cur.execute(sql, task)
            self.conn.commit()

    def add_new_configuration(self, configuration):
        if self.conn is not None:
            sql = ''' INSERT INTO configurations(title)
                      VALUES(?) '''
            cur = self.conn.cursor()
            cur.execute(sql, (configuration,))
            self.conn.commit()
            return cur.lastrowid

    def create_assignee(self, assignee):
        if self.conn is not None:
            sql = ''' INSERT INTO assignees(configuration_id, task_id, order_number)
                      VALUES(?, ?, ?) '''
            cur = self.conn.cursor()
            cur.execute(sql, assignee)
            self.conn.commit()
            return cur.lastrowid

    def update_task(self, task):
        if self.conn is not None:
            sql = ''' UPDATE tasks
                  SET name = ? , begin_time = ? , end_time = ?
                  WHERE path = ?'''
            cur = self.conn.cursor()
            cur.execute(sql, task)
            self.conn.commit()

    def delete_task(self, task_id):
        if self.conn is not None:
            sql = 'DELETE FROM tasks WHERE id=?'
            cur = self.conn.cursor()
            cur.execute(sql, (task_id,))
            self.conn.commit()
        self.delete_assignee(task_id)

    def delete_assignee(self, task_id):
        if self.conn is not None:
            sql = 'DELETE FROM assignees WHERE task_id=?'
            cur = self.conn.cursor()
            cur.execute(sql, (task_id,))
            self.conn.commit()

    def delete_all_tasks(self, stimuli_type):
        if self.conn is not None:
            sql = 'DELETE FROM tasks WHERE type=?'
            cur = self.conn.cursor()
            cur.execute(sql, (stimuli_type,))
            self.conn.commit()
        self.delete_all_assignees()

    # ADD DELETE BY STIMULI TYPE
    def delete_all_assignees(self):
        if self.conn is not None:
            sql = 'DELETE FROM assignees'
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()

    def delete_task_from_configuration(self, task_id):
        if self.conn is not None:
            sql = 'DELETE FROM assignees WHERE task_id=?'
            cur = self.conn.cursor()
            cur.execute(sql, (task_id,))
            self.conn.commit()

    def delete_configuration(self, title):
        if self.conn is not None:
            sql = 'DELETE FROM configurations WHERE title=?'
            cur = self.conn.cursor()
            cur.execute(sql, (title,))
            self.conn.commit()

    def select_tasks_by_type(self, stimuli_type):
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute('SELECT id, name, path, begin_time, end_time FROM tasks WHERE type=?', (stimuli_type,))
            rows = cur.fetchall()
            return rows

    def select_available_configurations(self):
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute("SELECT id, title FROM configurations")
            rows = cur.fetchall()
            return rows
        return ''

    def select_data_by_selected_configuration(self, title):
        if self.conn is not None:
            sql = 'SELECT * FROM tasks ' \
                    'INNER JOIN assignees ON tasks.id = assignees.task_id ' \
                    'INNER JOIN configurations ON assignees.configuration_id = configurations.id ' \
                    'WHERE configurations.title = ? ORDER BY assignees.order_number'
            cur = self.conn.cursor()
            cur.execute(sql, (title,))
            rows = cur.fetchall()
            return rows
        return ''

    def select_data_by_selected_configuration_and_type(self, title, stimuli_type):
        if self.conn is not None:
            sql = 'SELECT task_id FROM assignees ' \
                    'INNER JOIN tasks ON assignees.task_id = tasks.id ' \
                    'INNER JOIN configurations ON assignees.configuration_id = configurations.id ' \
                    'WHERE configurations.title = ? AND tasks.type=? ORDER BY assignees.task_id'
            cur = self.conn.cursor()
            cur.execute(sql, (title, stimuli_type))
            rows = cur.fetchall()
            return rows
        return ''

    def get_tasks_order(self, title):
        if self.conn is not None:
            sql = 'SELECT tasks.id, order_number FROM assignees ' \
                  'INNER JOIN tasks ON tasks.id = assignees.task_id ' \
                  'INNER JOIN configurations ON assignees.configuration_id = configurations.id ' \
                  'WHERE configurations.title = ? ORDER BY assignees.order_number'
            cur = self.conn.cursor()
            cur.execute(sql, (title,))
            rows = cur.fetchall()
            return rows
        return ''

    def update_task_order(self, task_id, order):
        if self.conn is not None:
            sql = ''' UPDATE assignees
                  SET order_number = ?
                  WHERE task_id = ?'''
            cur = self.conn.cursor()
            cur.execute(sql, (order, task_id))
            self.conn.commit()
