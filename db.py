import sqlite3

#database class
class Database:
    def __init__(self, db_file):
        self.connetion = sqlite3.connect(db_file)
        self.cursor = self.connetion.cursor()
    
    def user_exists(self, user_id):
        with self.connetion:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id):
        with self.connetion:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def set_active(self, user_id, active):
        with self.connetion:
            return self.connetion.execute("UPDATE `users` SET `active` = ? WHERE `user_id` = ?", (active, user_id,))

    def get_users(self):
        with self.connetion:
            return self.cursor.execute("SELECT `user_id`, `active` FROM `users`").fetchall()
    
    def get_user_count(self):
        with self.connetion:
            return self.cursor.execute("SELECT COUNT(*) FROM `users`").fetchmany(1)
    
    def get__active_user_count(self):
        with self.connetion:
            return self.cursor.execute("SELECT COUNT(*) FROM `users` WHERE `active` = ?", (1,)).fetchmany(1)

    def get_admins(self, admin_id):
        with self.connetion:
            result = self.cursor.execute("SELECT * FROM `admins` WHERE `admin_id` = ?", (admin_id,)).fetchmany(1)
            return bool(len(result))

    def add_admin(self, user_id):
        with self.connetion:
            return self.cursor.execute("INSERT INTO `admins` (`admin_id`) VALUES (?)", (user_id,))