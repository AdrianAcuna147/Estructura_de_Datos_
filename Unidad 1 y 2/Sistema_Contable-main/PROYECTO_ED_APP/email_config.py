# Configuración de Email para Recuperación de Contraseña
# IMPORTANTE: Reemplaza estas credenciales con las tuyas

EMAIL_CONFIG = {
    # INSTRUCCIONES PARA GMAIL (Recomendado):
    # 1. Abre: https://myaccount.google.com/apppasswords
    # 2. Selecciona: Mail y Windows (o tu dispositivo)
    # 3. Genera una contraseña de aplicación de 16 caracteres
    # 4. Copia la contraseña aquí en 'sender_password'
    # 5. Tu email va en 'sender_email' (ej: tu_email@gmail.com)
    
    "smtp_server": "smtp.gmail.com",  # Para Gmail
    "smtp_port": 587,  # 587 para TLS (recomendado), 465 para SSL
    "sender_email": "adrianyamauitz@gmail.com",  # CAMBIA ESTO: Tu email de Gmail
    "sender_password": "gzpj ffyu hmze ggac",  # CAMBIA ESTO: Tu contraseña de aplicación Gmail
    "sender_name": "StakFlow - Recuperación de Contraseña"
}

# ALTERNATIVA: Si tienes otro servidor SMTP (Office 365, Outlook, etc):
# - Office 365: smtp.office365.com, puerto 587
# - Outlook: smtp-mail.outlook.com, puerto 587
# 
# Para obtener contraseña de aplicación:
# Gmail: https://myaccount.google.com/apppasswords
# Office/Outlook: Usa tu contraseña normal de la cuenta
#
# NOTAS IMPORTANTES:
# - NO uses caracteres especiales en contraseña o email
# - Si falla, verifica que la contraseña de app sea de 16 caracteres sin espacios
# - Gmail requiere verificación en dos factores: https://myaccount.google.com/security

