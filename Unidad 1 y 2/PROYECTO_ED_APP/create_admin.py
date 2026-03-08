import sqlite3
import bcrypt

# Connect to DB
conn = sqlite3.connect('stakflow.db')
cursor = conn.cursor()

# Hash password with bcrypt
password = 'admin123'
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Insert admin user
cursor.execute('''
    INSERT INTO usuario (nombre, apellidos, correo, contrasena_hash, rol, activo, domicilio, edad, recovery_code)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', ('Admin', 'User', 'admin@example.com', hashed, 'admin', True, 'StakFlow HQ', 25, ''))

conn.commit()
print('✅ Admin user created with bcrypt hash')
print('   Username: Admin')
print('   Password: admin123')
conn.close()
