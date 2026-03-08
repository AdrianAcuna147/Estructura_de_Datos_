import sqlite3

conn = sqlite3.connect('stakflow.db')
cursor = conn.cursor()
cursor.execute('DELETE FROM usuario')
conn.commit()
conn.close()
print('✅ Database cleaned')
