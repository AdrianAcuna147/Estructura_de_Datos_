# Reporte de Desarrollo - StakFlow

## 📋 Descripción General de la Aplicación

**StakFlow** es una aplicación de gestión contable desarrollada para facilitar los procesos financieros de empresas. La app comenzó como un simple programa en línea de comandos y evolucionó a una aplicación web con interfaz gráfica intuitiva que permite a los usuarios realizar operaciones contables de manera sencilla y eficiente.

---

## 🛠️ Tecnologías Utilizadas

### **Backend**
- **Lenguaje**: Python
  - Elegido por su facilidad de programación y versatilidad
  - Excelente soporte para librerías de gestión de datos y autenticación

### **Framework Web**
- **Reflex**: Framework web Python reactivo que genera automáticamente plantillas web
  - Permite separar la lógica de negocio (backend) de la interfaz gráfica (frontend)
  - Proporciona componentes UI listos para usar
  - Facilita la comunicación entre cliente y servidor

### **Base de Datos**
- **Fase 1**: Archivos JSON (almacenamiento temporal)
  - Utilizado inicialmente para simular una base de datos
  - Permitió prototipado rápido
  
- **Fase 2**: Supabase con PostgreSQL (implementación actual)
  - Base de datos relacional robusta
  - Mejor organización de datos en tablas
  - Gestión segura de credenciales de usuarios
  - Escalabilidad para crecer con la empresa

### **Autenticación y Seguridad**
- **bcrypt**: Hashing seguro de contraseñas
- **Variables de entorno**: Protección de credenciales sensibles
- **python-dotenv**: Manejo de configuración segura

---

## 🏗️ Arquitectura de la Aplicación

```
Frontend (Interfaz Gráfica)
        ↓
    Reflex Framework
        ↓
Backend (Lógica de Negocio)
        ↓
Supabase PostgreSQL Database
```

**Separación de responsabilidades:**
- **Frontend**: Componentes visuales e interfaz de usuario
- **Backend**: Lógica contable, procesamiento de datos, autenticación
- **Base de datos**: Almacenamiento persistente y relaciones entre entidades

---

## 💰 Sistema Contable Implementado

### **Componentes Principales**

1. **Saldo/Presupuesto**
   - Representa el capital actual de la empresa
   - Solo administradores pueden editar directamente
   - Se actualiza automáticamente con movimientos contables

2. **Ingresos (Ganancias)**
   - Registrados mediante ventas de productos
   - Se suman automáticamente al saldo total
   - Visible en reportes en tiempo real

3. **Egresos (Gastos)**
   - Registrados mediante compras a proveedores
   - Se restan automáticamente del saldo total
   - Trazable para auditoría

4. **Movimientos Contables**
   - Cada transacción es registrada con detalles completos
   - Historial completo de cambios
   - Facilita reconciliación y auditoría

---

## 📊 Características Principales de StakFlow

### **Módulos Implementados**

| Módulo | Descripción | Acceso |
|--------|-------------|--------|
| **Dashboard** | Panel en tiempo real con ganancias/pérdidas, métricas clave y estado actual | Todos los usuarios |
| **Inventario** | Gestión de productos, agregar/editar/eliminar artículos, ver stock disponible | Administradores y Gerentes |
| **Historial de Movimientos** | Registro detallado de todos los ingresos y egresos | Todos los usuarios (lectura) |
| **Historial de Registros** | Log de cambios en el sistema, quién hizo qué y cuándo | Administradores |
| **Gestión de Cuenta** | Perfil personal, cambio de contraseña, datos de usuario | Todos los usuarios |
| **Gestión de Usuarios** | Crear, editar, eliminar usuarios del sistema, asignar roles | Solo Administradores |
| **Cuentas Contables** | Visualización y gestión de diferentes cuentas contables | Administradores |
| **Buscador Integrado** | Búsqueda rápida en toda la aplicación | Todos los usuarios |

---

## 🔒 Medidas de Seguridad Implementadas

### 1. **Variables de entorno (.env)** 🔑 CRÍTICO
La base de datos y credenciales están protegidas en un archivo `.env` que nunca se sube a GitHub.

**¿Qué hacer?**
1. Abre el archivo `.env` en la raíz del proyecto
2. Reemplaza los valores con tus credenciales reales:
   - `DATABASE_URL`: Tu cadena de conexión a Supabase
   - `EMAIL_PASSWORD`: Tu app password de Gmail
   - `SECRET_KEY`: Genera una clave aleatoria (usa: `python -c "import secrets; print(secrets.token_hex(32))"`)

**¿Por qué?**
- El archivo `.env` está en `.gitignore` → Nunca se sube a GitHub
- Las credenciales están separadas del código
- Cada developer puede tener sus propias credenciales

---

### 2. **Hashing de contraseñas con bcrypt**  IMPLEMENTADO
Las contraseñas ahora usan **bcrypt** en lugar de SHA-256 simple.

**Ventajas:**
-  Mucho más seguro contra ataques de fuerza bruta
-  Salt automático (cada hash es único)
-  Resistente a rainbow tables
-  Adaptable (se puede aumentar factor de trabajo)

**¿Cómo funciona?**
```python
# Guardar contraseña (usa bcrypt automáticamente)
usuario.contrasena_hash = _hash_password("micontraseña123")

# Verificar contraseña en login
if _verificar_password("micontraseña123", usuario.contrasena_hash):
    print("Login exitoso")
```

**IMPORTANTE:** Las contraseñas antiguas en la BD (SHA-256) no funcionarán con bcrypt.
Solución: Fuerza a todos los usuarios a cambiar contraseña en el primer login.

---

### 3. **Protección de rutas** VERIFICADO
El sistema verifica que estés logueado antes de permitir acceso a páginas protegidas.

**Ejemplo:**
```python
def on_load(self):
    if not self.usuario_logueado:
        return rx.redirect("/login")
```

---

### 4. **.gitignore** CONFIGURADO
El archivo `.gitignore` protege información sensible:
```
.env              # Variables de entorno
.env.local        # Configuración local
email_config.py   # Credenciales de email
__pycache__/      # Archivos compilados
*.pyc             # Bytecode Python
```

---

## Checklist de seguridad

- [ ] Llenar el archivo `.env` con credenciales reales
- [ ] Cambiar la contraseña del admin (Admin / admin123)
- [ ] Generar una `SECRET_KEY` de verdad
- [ ] Verificar que `.gitignore` está actualizado
- [ ] No compartir el archivo `.env` con nadie
- [ ] Hacer el primer push sin `.env` en el historio
- [ ] Cambiar todas las contraseñas SHA-256 a bcrypt (o forzar cambio de contraseña)

---

## 🛡️ Protecciones Automáticas del Framework

- **SQL Injection**: Ya protegido por SQLModel (ORM) - evita inyección SQL
- **XSS (Cross-Site Scripting)**: Reflex HTML-encoda automáticamente todos los valores
- **CORS**: Configurado para aceptar solo solicitudes autorizadas

---

## 🔴 SI NECESITAS RESETEAR EL SISTEMA

Si necesitas resetear las contraseñas (porque cambiaste de SHA-256 a bcrypt):

```python
# En state.py, función inicializar_admin():
admin.contrasena_hash = _hash_password("nueva_contraseña_temporal")
```

Luego fuerza a los usuarios a cambiar contraseña desde la app.

---

## 🎯 Desafíos Encontrados en el Desarrollo

1. **Migración de almacenamiento**: Pasar de JSON a PostgreSQL requirió restructuración de la lógica de datos
2. **Integración Reflex + Backend**: Coordinar la comunicación reactiva entre frontend y backend
3. **Autenticación segura**: Implementar bcrypt y manejo seguro de contraseñas
4. **Manejo de roles y permisos**: Gestionar diferentes niveles de acceso (Administrador, Gerente, Usuario)
5. **Consistencia de datos contables**: Asegurar que las operaciones financieras sean precisas y auditables

---

## 🚀 Mejoras Implementadas Recientemente

✅ Migración a Supabase PostgreSQL  
✅ Implementación de bcrypt para contraseñas  
✅ Sistema de roles y permisos basado en administradores  
✅ Dashboard en tiempo real  
✅ Historial completo de movimientos  
✅ Variables de entorno para credenciales  

---

## 📈 Próximas Mejoras Planeadas para Mayor Seguridad y Funcionalidad

### Corto Plazo (Próximas iteraciones)
1. **Rate limiting**: Limitar intentos de login fallidos
2. **Auditoría mejorada**: Logs más detallados de cambios sensibles
3. **Validación de datos**: Validación más estricta en formularios frontend

### Mediano Plazo
1. **2FA (Two-Factor Authentication)**: SMS o Google Authenticator para mayor seguridad
2. **Exportación de reportes**: PDF, Excel con historial contable
3. **Multicurrency**: Soporte para diferentes monedas

### Largo Plazo
1. **HTTPS y certificados SSL/TLS**: Para producción
2. **CSRF Protection avanzada**: Tokens anti-CSRF en todos los formularios
3. **Encriptación de datos sensibles**: Para campos especialmente críticos
4. **Sistema de permisos granular**: Control más fino sobre qué puede hacer cada rol
5. **Backup automático**: Respaldos programados en la nube
6. **API REST externa**: Para integración con otros sistemas

---

## 📝 Conclusión

StakFlow se ha desarrollado como una solución integral para la gestión contable de empresas. El proceso evolucionó desde un prototipo simple en línea de comandos a una aplicación web robusta con:

- ✅ **Interfaz intuitiva** para facilitar procesos contables
- ✅ **Base de datos relacional** para datos organizados y seguros
- ✅ **Sistema contable automático** que calcula ganancias y pérdidas en tiempo real
- ✅ **Control de acceso** mediante roles de usuario
- ✅ **Medidas de seguridad** implementadas desde el diseño
- ✅ **Separación frontend/backend** para mantenibilidad

El proyecto demuestra las mejores prácticas en desarrollo web seguro y es escalable para futuras expansiones.

---

## Referencias

- **bcrypt**: https://github.com/pyca/bcrypt
- **python-dotenv**: https://github.com/theskumar/python-dotenv
- **OWASP Password Storage**: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
