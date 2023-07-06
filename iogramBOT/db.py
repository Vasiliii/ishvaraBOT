import sqlite3
import time

class DataBase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        
    def user_exists(self, user_id):
        with self.conn:
            result = self.cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))
        
    def add_user(self, user_id, name):
        with self.conn:
            return self.conn.execute("INSERT INTO users (user_id, name) VALUES (?, ?)", (user_id, name,))
        
    def mute(self, user_id):
        with self.conn:
            user = self.cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return int(user[3]) >= int(time.time())  
        
    def add_mute(self, user_id, mute_time):
        with self.conn:
            return self.conn.execute("UPDATE users SET mute = ? WHERE user_id =?", (int(time.time()) +  mute_time * 60 *60, user_id,))
        
    def unmute(self, user_name):
        with self.conn:
            return self.conn.execute("UPDATE users SET mute = 0 WHERE name =?", ( user_name,))
    
    def warning(self, user_id):
        with self.conn:
            return self.conn.execute("UPDATE users SET warning = warning + 1 WHERE user_id =?",(user_id,))
    
    def check_warning(self, user_id):
        with self.conn:
            user =  self.cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return int(user[2]) >= 2  
        
    def add_log(self, user_id , login):
        with self.conn:
            return self.conn.execute("UPDATE users SET login = ? WHERE user_id = ?  ", (login, user_id,))
        
    def check_log(self, login):
        with self.conn:
            result = self.cur.execute("SELECT * FROM users WHERE login = ?", (login,)).fetchall()
            return bool(len(result)) 
    
    def add_pass(self, user_id , password):
        with self.conn:
            return self.conn.execute("UPDATE users SET pass = ? WHERE user_id = ?  ", (password, user_id,))
    
    def check_pass(self, password):
        with self.conn:
            result = self.cur.execute("SELECT * FROM users WHERE pass = ?", (password,)).fetchall()
            return bool(len(result)) 
        
    def add_nights(self, mute_time ):
        with self.conn:
            return self.conn.execute("UPDATE nights SET mute = ? WHERE id = ?", (int(time.time()) +  mute_time * 60 * 60, 1,))
        
    def nights(self):
        with self.conn:
            nights = self.cur.execute("SELECT * FROM nights WHERE id = 1").fetchone()
            return int(nights[0]) >= int(time.time())