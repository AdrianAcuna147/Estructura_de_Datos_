#!/usr/bin/env python3
"""Script para agregar la columna recovery_code a la tabla usuario en la BD"""

from sqlalchemy import create_engine, text

# Configuración de la BD
db_url = "postgresql://postgres.huzlrdruzspfdbclgzhk:proyecto_123@aws-1-us-east-1.pooler.supabase.com:6543/postgres"

try:
    engine = create_engine(db_url)
    
    with engine.connect() as connection:
        # Verificar si la columna ya existe
        result = connection.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='usuario' AND column_name='recovery_code'
        """))
        
        if result.fetchone() is None:
            # La columna no existe, crearla
            print("Agregando columna recovery_code a la tabla usuario...")
            connection.execute(text("""
                ALTER TABLE usuario 
                ADD COLUMN recovery_code VARCHAR NULL
            """))
            connection.commit()
            print("✓ Columna recovery_code agregada exitosamente")
        else:
            print("✓ La columna recovery_code ya existe")
            
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
