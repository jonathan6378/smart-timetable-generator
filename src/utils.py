import csv, sqlite3

def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f: return list(csv.DictReader(f))

def initialize_database(path):
    con = sqlite3.connect(path)
    con.execute("""CREATE TABLE IF NOT EXISTS schedules(
        id INTEGER PRIMARY KEY AUTOINCREMENT, course_id TEXT, course_name TEXT,
        teacher TEXT, day TEXT, time TEXT, room TEXT, fitness REAL)""")
    con.commit()
    return con

def save_schedule(con, rows, fitness):
    con.execute("DELETE FROM schedules")
    con.executemany("INSERT INTO schedules(course_id,course_name,teacher,day,time,room,fitness) VALUES(?,?,?,?,?,?,?)",
        [(r["course_id"],r["course_name"],r["teacher"],r["day"],r["time"],r["room"],fitness) for r in rows])
    con.commit()
