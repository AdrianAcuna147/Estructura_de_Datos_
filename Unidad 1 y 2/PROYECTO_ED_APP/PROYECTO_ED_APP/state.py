# $======================$
# ||BACKEND DEL SISTEMA ||
# $======================$

##### AVISO ######
# Solo Dios y yo (Adrian Yama) sabemos que hace este codigo, sino sabe pregunte

#LIBRERIAS

import reflex as rx
import re
from datetime import datetime
from sqlmodel import select
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
from typing import Optional
import bcrypt # Mas seguro

try:
    import dns.resolver
    DNS_DISPONIBLE = True
except ImportError:
    DNS_DISPONIBLE = False

try:
    from .email_config import EMAIL_CONFIG
except ImportError:
    try:
        from email_config import EMAIL_CONFIG
    except ImportError:
        EMAIL_CONFIG = None


# ======================
# MODELOS DE BASE DE DATOS
# ======================
class Producto(rx.Model, table=True):
    nombre: str
    marca: str = ""
    modelo: str = ""
    numero_serie: str = ""
    stock: int = 0
    precio_compra: float = 0.0
    precio_venta: float = 0.0
    fecha_creacion: str = ""


class Transaccion(rx.Model, table=True):
    tipo: str
    nombre: str
    correo: str
    numero_factura: str
    producto: str
    monto: float
    fecha: str
    usuario: str = ""


class Movimiento(rx.Model, table=True):
    tipo: str
    descripcion: str
    fecha: str
    usuario: str = ""


class Usuario(rx.Model, table=True):
    nombre: str
    apellidos: str
    correo: str
    contrasena_hash: str
    rol: str
    activo: bool = True
    domicilio: str = ""
    edad: int = 0
    recovery_code: str = None


class Deuda(rx.Model, table=True):
    proveedor: str
    correo_proveedor: str = ""
    producto: str
    marca: str = ""
    modelo: str = ""
    stock_pendiente: int = 0
    monto_total: float = 0.0
    fecha: str
    pagada: bool = False


# ============================================================
# FIX: _hash_password usa SHA-256 (compatible con BD existente)
#      _verificar_password soporta SHA-256 Y bcrypt como fallback
# ============================================================
def _hash_password(password: str) -> str:
    """Hash con SHA-256 — compatible con la BD existente."""
    return hashlib.sha256(password.encode()).hexdigest()


def _verificar_password(password: str, hash_guardado: str) -> bool:
    """Verifica contraseña. Soporta SHA-256 (actual) y bcrypt (legado).
    
    El problema con bcrypt es que genera un hash diferente cada vez
    (incluye salt aleatorio), por lo que NO se puede comparar en SQL.
    Esta función maneja ambos formatos correctamente.
    """
    # SHA-256 primero (formato estándar de la BD)
    if hashlib.sha256(password.encode()).hexdigest() == hash_guardado:
        return True
    # Fallback bcrypt por si hay hashes viejos en la BD
    try:
        return bcrypt.checkpw(password.encode(), hash_guardado.encode())
    except Exception:
        return False


class ContableState(rx.State):
    saldo_inicial: float = 0.0
    facturas_clientes: dict[str, float] = {}
    facturas_proveedores: dict[str, float] = {}
    numero_factura: str = ""
    nombre_producto: str = ""
    monto_factura: float = 0.0
    nombre_cliente: str = ""
    nombre_proveedor: str = ""
    correo_cliente: str = ""
    correo_proveedor: str = ""
    mostrar_modal: bool = False
    tipo_modal: str = " "
    error_nombre: str = ""
    error_correo: str = ""
    error_general: str = ""
    error_inventario: str = ""
    historial: list[dict] = []
    movimientos: list[dict] = []
    pestana_actual: str = "dashboard"
    texto_busqueda: str = ""
    productos: list[dict] = []
    nombre_producto_nuevo: str = ""
    marca_producto_nuevo: str = ""
    modelo_producto_nuevo: str = ""
    numero_serie_producto_nuevo: str = ""
    stock_inicial: int = 0
    precio_compra: float = 0.0
    precio_venta: float = 0.0
    texto_busqueda_producto: str = ""

    edit_id: int = 0
    edit_nombre: str = ""
    edit_marca: str = ""
    edit_modelo: str = ""
    edit_numero_serie: str = ""
    edit_stock: int = 0
    edit_precio_compra: float = 0.0
    edit_precio_venta: float = 0.0
    mostrar_modal_editar: bool = False
    productos_desplegable_abierto: bool = False
    mostrar_modal_eliminar: bool = False
    eliminar_id: int = 0
    eliminar_nombre: str = ""
    stock_minimo_alerta: int = 5

    # RECEPCIÓN
    items_recepcion: list[dict] = []
    item_producto_sel: str = ""
    item_cantidad: int = 1
    item_precio_iva: float = 0.0
    mostrar_modal_proveedor_recepcion: bool = False
    texto_busqueda_recepcion: str = ""
    item_marca_sel: str = ""
    item_modelo_sel: str = ""
    # Aliases compatibles con contable.py
    item_marca_recepcion: str = ""
    item_modelo_recepcion: str = ""
    cantidad_venta: int = 1

    # CLIENTE
    marca_seleccionada: str = ""
    modelo_seleccionado: str = ""

    # AUTENTICACIÓN
    usuario_logueado: bool = False
    usuario_nombre: str = ""
    usuario_rol: str = ""
    usuario_correo: str = ""
    usuario_domicilio: str = ""
    usuario_edad: int = 0
    usuario_apellidos: str = ""
    usuario_id: int = 0
    login_nombre: str = ""
    login_password: str = ""
    login_error: str = ""
    login_mostrar_password: bool = False
    reg_nombre: str = ""
    reg_apellidos: str = ""
    reg_correo: str = ""
    reg_password: str = ""
    reg_domicilio: str = ""
    reg_edad: int = 0
    reg_rol: str = "empleado"
    reg_error: str = ""
    reg_exito: str = ""
    mostrar_modal_registro: bool = False
    usuarios_lista: list[dict] = []
    usuarios_pagina_actual: int = 1
    usuarios_items_por_pagina: int = 10
    usuarios_texto_busqueda: str = ""

    # PERFIL
    mostrar_modal_perfil: bool = False
    editar_perfil_nombre: str = ""
    editar_perfil_apellidos: str = ""
    editar_perfil_domicilio: str = ""
    editar_perfil_edad: int = 0
    editar_perfil_correo: str = ""
    editar_perfil_error: str = ""
    editar_perfil_exito: str = ""

    # HISTORIAL
    filtro_tipo_historial: str = ""
    filtro_usuario_historial: str = ""
    filtro_fecha_inicio: str = ""
    filtro_fecha_fin: str = ""
    pagina_actual: int = 1
    items_por_pagina: int = 20

    # EDICIÓN TRANSACCIÓN
    mostrar_modal_editar_transaccion: bool = False
    editar_trans_id: int = 0
    editar_trans_numero: str = ""
    editar_trans_monto: float = 0.0
    editar_trans_producto: str = ""
    editar_trans_nombre: str = ""
    editar_trans_correo: str = ""

    # DEUDAS
    deudas: list[dict] = []
    error_deuda: str = ""

    # MI CUENTA
    cuenta_pass_actual: str = ""
    cuenta_pass_nueva: str = ""
    cuenta_pass_confirmar: str = ""
    cuenta_error: str = ""
    cuenta_exito: str = ""

    grafica_financiera: list[dict] = [
        {"mes": "Enero",   "ingresos": 12000, "egresos": 8000},
        {"mes": "Febrero", "ingresos": 15000, "egresos": 9000},
        {"mes": "Marzo",   "ingresos": 10000, "egresos": 7000},
    ]

    # RECUPERACIÓN
    mostrar_modal_recuperacion: bool = False
    recuperacion_correo: str = ""
    recuperacion_error: str = ""
    recuperacion_exito: str = ""
    recuperacion_paso: int = 1
    recuperacion_codigo: str = ""
    _recuperacion_codigo_real: str = ""
    recuperacion_password_nueva: str = ""

    # ======================
    # SETTERS BÁSICOS
    # ======================
    def set_saldo_inicial(self, value):
        try:
            self.saldo_inicial = float(value) if value.strip() else 0.0
        except (ValueError, AttributeError):
            self.saldo_inicial = 0.0

    def set_numero_factura(self, value): self.numero_factura = value
    def set_nombre_producto(self, value):
        self.nombre_producto = value
        self.error_general = ""

    def set_monto_factura(self, value):
        try:
            self.monto_factura = float(value) if value.strip() else 0.0
        except (ValueError, AttributeError):
            self.monto_factura = 0.0

    def set_nombre_cliente(self, value): self.nombre_cliente = str(value)
    def set_nombre_proovedor(self, value): self.nombre_proveedor = str(value)
    def set_correo_cliente(self, value): self.correo_cliente = str(value)
    def set_correo_proovedor(self, value): self.correo_proveedor = str(value)
    def set_texto_busqueda(self, value): self.texto_busqueda = value
    def set_texto_busqueda_producto(self, value): self.texto_busqueda_producto = value

    def set_item_producto_sel(self, value: str):
        """Seleccionar producto — limpia marca y modelo (cascada Producto→Marca→Modelo)."""
        self.item_producto_sel = value
        self.item_marca_sel = ""
        self.item_marca_recepcion = ""
        self.item_modelo_sel = ""
        self.item_modelo_recepcion = ""
        self.item_precio_iva = 0.0
        for p in self.productos:
            if p["nombre"] == value:
                self.item_precio_iva = p["precio_compra"]
                break

    def set_item_cantidad(self, value):
        try:
            self.item_cantidad = int(value) if value else 1
        except (ValueError, AttributeError):
            self.item_cantidad = 1

    def set_item_precio_iva(self, value):
        try:
            self.item_precio_iva = float(value) if value else 0.0
        except (ValueError, AttributeError):
            self.item_precio_iva = 0.0

    def set_marca_seleccionada(self, value: str): self.marca_seleccionada = value
    def set_modelo_seleccionado(self, value: str): self.modelo_seleccionado = value

    def set_stock_minimo_alerta(self, value):
        try:
            v = int(value) if value else 5
            self.stock_minimo_alerta = max(0, v)
        except (ValueError, AttributeError):
            self.stock_minimo_alerta = 5

    def set_texto_busqueda_recepcion(self, value: str): self.texto_busqueda_recepcion = value

    def set_item_marca_sel(self, value: str):
        """Al cambiar marca, limpia solo modelo (mantiene producto)."""
        self.item_marca_sel = value
        self.item_marca_recepcion = value
        self.item_modelo_sel = ""
        self.item_modelo_recepcion = ""
        self.item_precio_iva = 0.0

    def set_item_marca_recepcion(self, value: str):
        """Alias para compatibilidad con contable.py."""
        self.set_item_marca_sel(value)

    def set_item_modelo_sel(self, value: str):
        """Al cambiar modelo, mantiene producto y marca."""
        self.item_modelo_sel = value
        self.item_modelo_recepcion = value

    def set_item_modelo_recepcion(self, value: str):
        """Alias para compatibilidad con contable.py."""
        self.set_item_modelo_sel(value)

    def set_cantidad_venta(self, value):
        try:
            self.cantidad_venta = max(1, int(value)) if value else 1
        except (ValueError, AttributeError):
            self.cantidad_venta = 1

    # SETTERS HISTORIAL
    def set_filtro_tipo_historial(self, value: str):
        self.filtro_tipo_historial = value
        self.pagina_actual = 1

    def set_filtro_usuario_historial(self, value: str):
        self.filtro_usuario_historial = value
        self.pagina_actual = 1

    def set_filtro_fecha_inicio(self, value: str):
        self.filtro_fecha_inicio = value
        self.pagina_actual = 1

    def set_filtro_fecha_fin(self, value: str):
        self.filtro_fecha_fin = value
        self.pagina_actual = 1

    def set_pagina_actual(self, value: int):
        total = self.total_paginas_historial
        self.pagina_actual = max(1, min(int(value), total))

    def limpiar_filtros_historial(self):
        self.filtro_tipo_historial = ""
        self.filtro_usuario_historial = ""
        self.filtro_fecha_inicio = ""
        self.filtro_fecha_fin = ""
        self.texto_busqueda = ""
        self.pagina_actual = 1

    # ================================
    # SETTERS PARA USUARIOS
    # ================================
    def set_usuarios_texto_busqueda(self, value: str):
        self.usuarios_texto_busqueda = value
        self.usuarios_pagina_actual = 1

    def set_usuarios_pagina_actual(self, value: int):
        total = self.total_paginas_usuarios
        self.usuarios_pagina_actual = max(1, min(int(value), total))

    def usuarios_pagina_anterior(self):
        self.usuarios_pagina_actual = max(1, self.usuarios_pagina_actual - 1)

    def usuarios_pagina_siguiente(self):
        total = self.total_paginas_usuarios
        self.usuarios_pagina_actual = min(self.usuarios_pagina_actual + 1, total)

    # EDICIÓN/ANULACIÓN TRANSACCIONES
    def set_editar_trans_numero(self, value): self.editar_trans_numero = value
    def set_editar_trans_monto(self, value):
        try:
            self.editar_trans_monto = float(value) if value else 0.0
        except (ValueError, AttributeError):
            self.editar_trans_monto = 0.0
    def set_editar_trans_producto(self, value): self.editar_trans_producto = value
    def set_editar_trans_nombre(self, value): self.editar_trans_nombre = value
    def set_editar_trans_correo(self, value): self.editar_trans_correo = value

    def abrir_modal_editar_transaccion(self, trans_id: int):
        for t in self.historial:
            if t.get("id") == trans_id:
                self.editar_trans_id = trans_id
                self.editar_trans_numero = t.get("numero_factura", "")
                self.editar_trans_monto = float(t.get("monto", 0))
                self.editar_trans_producto = t.get("producto", "")
                self.editar_trans_nombre = t.get("nombre", "")
                self.editar_trans_correo = t.get("correo", "")
                break
        self.mostrar_modal_editar_transaccion = True

    def cerrar_modal_editar_transaccion(self):
        self.mostrar_modal_editar_transaccion = False

    def guardar_edicion_transaccion(self):
        if not self.editar_trans_id:
            return
        with rx.session() as session:
            t = session.get(Transaccion, self.editar_trans_id)
            if t:
                t.numero_factura = self.editar_trans_numero
                t.monto = self.editar_trans_monto
                t.producto = self.editar_trans_producto
                t.nombre = self.editar_trans_nombre
                t.correo = self.editar_trans_correo
                session.add(t)
                session.commit()
        self.cargar_historial()
        self.mostrar_modal_editar_transaccion = False
        self._registrar_movimiento(
            "Transacción editada",
            f"Se editó transacción #{self.editar_trans_id} — Factura: {self.editar_trans_numero} — ${self.editar_trans_monto}"
        )

    def cancelar_transaccion(self, trans_id: int):
        with rx.session() as session:
            t = session.get(Transaccion, trans_id)
            if t:
                desc = f"Transacción anulada — {t.tipo} — {t.nombre} — Factura: {t.numero_factura} — ${t.monto}"
                session.delete(t)
                session.commit()
                self._registrar_movimiento("Transacción anulada", desc)
        self.cargar_historial()

    # SETTERS MI CUENTA
    def set_cuenta_pass_actual(self, value):
        self.cuenta_pass_actual = value
        self.cuenta_error = ""
        self.cuenta_exito = ""

    def set_cuenta_pass_nueva(self, value):
        self.cuenta_pass_nueva = value
        self.cuenta_error = ""
        self.cuenta_exito = ""

    def set_cuenta_pass_confirmar(self, value):
        self.cuenta_pass_confirmar = value
        self.cuenta_error = ""
        self.cuenta_exito = ""

    # AUTOCOMPLETE PROVEEDOR
    def set_nombre_proveedor_busqueda(self, value: str):
        self.nombre_proveedor = str(value)
        self.error_nombre = ""

    def seleccionar_proveedor_sugerido(self, nombre: str):
        self.nombre_proveedor = nombre
        for t in reversed(self.historial):
            if t.get("nombre", "").lower() == nombre.lower() and t.get("tipo") == "Proveedor":
                self.correo_proveedor = t.get("correo", "")
                break

    # PESTAÑAS
    def ir_contable(self): self.pestana_actual = "contable"
    def ir_historial(self): self.pestana_actual = "historial"
    def ir_buscador(self): self.pestana_actual = "buscador"
    def ir_inventario(self): self.pestana_actual = "inventario"
    def ir_dashboard(self): self.pestana_actual = "dashboard"

    def ir_usuarios(self):
        self.pestana_actual = "usuarios"
        self.cargar_usuarios()

    def ir_cuenta(self):
        self.pestana_actual = "cuenta"
        self.cuenta_pass_actual = ""
        self.cuenta_pass_nueva = ""
        self.cuenta_pass_confirmar = ""
        self.cuenta_error = ""
        self.cuenta_exito = ""

    # INVENTARIO SETTERS
    def set_nombre_producto_nuevo(self, value):
        self.nombre_producto_nuevo = value
        self.error_inventario = ""

    def set_marca_producto_nuevo(self, value): self.marca_producto_nuevo = value
    def set_modelo_producto_nuevo(self, value): self.modelo_producto_nuevo = value

    def set_numero_serie_producto_nuevo(self, value):
        self.numero_serie_producto_nuevo = value
        self.error_inventario = ""

    def set_stock_inicial(self, value):
        try:
            self.stock_inicial = int(value) if value else 0
        except (ValueError, AttributeError):
            self.stock_inicial = 0

    def set_precio_compra(self, value):
        try:
            self.precio_compra = float(value) if value else 0.0
        except (ValueError, AttributeError):
            self.precio_compra = 0.0

    def set_precio_venta(self, value):
        try:
            self.precio_venta = float(value) if value else 0.0
        except (ValueError, AttributeError):
            self.precio_venta = 0.0

    # SETTERS EDICIÓN PRODUCTO
    def set_edit_nombre(self, value): self.edit_nombre = value
    def set_edit_marca(self, value): self.edit_marca = value
    def set_edit_modelo(self, value): self.edit_modelo = value
    def set_edit_numero_serie(self, value): self.edit_numero_serie = value

    def set_edit_stock(self, value):
        try:
            self.edit_stock = int(value) if value else 0
        except (ValueError, AttributeError):
            self.edit_stock = 0

    def set_edit_precio_compra(self, value):
        try:
            self.edit_precio_compra = float(value) if value else 0.0
        except (ValueError, AttributeError):
            self.edit_precio_compra = 0.0

    def set_edit_precio_venta(self, value):
        try:
            self.edit_precio_venta = float(value) if value else 0.0
        except (ValueError, AttributeError):
            self.edit_precio_venta = 0.0

    # MODAL
    def cerrar_modal(self): self.mostrar_modal = False

    def _limpiar_errores(self):
        self.error_nombre = ""
        self.error_correo = ""
        self.error_general = ""
        self.error_deuda = ""

    def _limpiar_datos_modal(self):
        self.nombre_cliente = ""
        self.correo_cliente = ""
        self.nombre_proveedor = ""
        self.correo_proveedor = ""

    # MOVIMIENTOS
    def _registrar_movimiento(self, tipo: str, descripcion: str):
        with rx.session() as session:
            mov = Movimiento(
                tipo=tipo,
                descripcion=descripcion,
                fecha=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                usuario=self.usuario_nombre,
            )
            session.add(mov)
            session.commit()
        self.cargar_movimientos()

    def cargar_movimientos(self):
        with rx.session() as session:
            movs = session.exec(select(Movimiento)).all()
            self.movimientos = [
                {"tipo": m.tipo, "descripcion": m.descripcion, "fecha": m.fecha, "usuario": m.usuario}
                for m in movs
            ]

    # DEUDAS
    def cargar_deudas(self):
        with rx.session() as session:
            deudas_db = session.exec(select(Deuda)).all()
            self.deudas = [
                {
                    "id": d.id, "proveedor": d.proveedor,
                    "correo_proveedor": d.correo_proveedor, "producto": d.producto,
                    "marca": d.marca, "modelo": d.modelo,
                    "stock_pendiente": d.stock_pendiente, "monto_total": d.monto_total,
                    "fecha": d.fecha, "pagada": d.pagada,
                }
                for d in deudas_db
            ]

    def marcar_deuda_pagada(self, deuda_id: int):
        self.error_deuda = ""
        deuda_info = None
        for d in self.deudas:
            if d["id"] == deuda_id:
                deuda_info = d
                break
        if not deuda_info:
            return
        monto = deuda_info["monto_total"]
        saldo_disponible = (
            self.saldo_inicial
            + sum(self.facturas_clientes.values())
            - sum(self.facturas_proveedores.values())
        )
        if saldo_disponible <= 0 or saldo_disponible < monto:
            self.error_deuda = (
                f"Saldo insuficiente — necesitas ${monto:.2f} "
                f"pero tienes ${max(0.0, saldo_disponible):.2f}"
            )
            return
        folio_pago = f"PAGO-DEUDA-{deuda_id}"
        with rx.session() as session:
            pago = Transaccion(
                tipo="Pago deuda", nombre=deuda_info["proveedor"],
                correo=deuda_info["correo_proveedor"], numero_factura=folio_pago,
                producto=deuda_info["producto"], monto=monto,
                fecha=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                usuario=self.usuario_nombre,
            )
            session.add(pago)
            session.commit()
        with rx.session() as session:
            deuda = session.get(Deuda, deuda_id)
            if deuda:
                deuda.pagada = True
                session.add(deuda)
                session.commit()
        self.cargar_historial()
        self.cargar_deudas()
        self._registrar_movimiento(
            "Pago de deuda",
            f"Se pagó deuda con {deuda_info['proveedor']} — Producto: {deuda_info['producto']} — ${monto:.2f}"
        )

    # RECEPCIÓN
    def abrir_modal_proveedor(self):
        self._limpiar_datos_modal()
        self._limpiar_errores()
        self.items_recepcion = []
        self.item_producto_sel = ""
        self.item_cantidad = 1
        self.item_precio_iva = 0.0
        self.numero_factura = ""
        self.texto_busqueda_recepcion = ""
        self.item_marca_sel = ""
        self.item_marca_recepcion = ""
        self.item_modelo_sel = ""
        self.item_modelo_recepcion = ""
        self.mostrar_modal_proveedor_recepcion = True

    def cerrar_modal_proveedor_recepcion(self):
        self.mostrar_modal_proveedor_recepcion = False
        self.items_recepcion = []
        self.texto_busqueda_recepcion = ""
        self.item_marca_sel = ""
        self.item_marca_recepcion = ""
        self.item_modelo_sel = ""
        self.item_modelo_recepcion = ""
        self._limpiar_errores()

    def agregar_item_recepcion(self):
        if not self.item_producto_sel:
            return
        for item in self.items_recepcion:
            if item["nombre"] == self.item_producto_sel:
                item["cantidad"] += self.item_cantidad
                item["precio_iva"] = self.item_precio_iva
                item["subtotal"] = item["cantidad"] * item["precio_iva"]
                self.items_recepcion = list(self.items_recepcion)
                self.item_producto_sel = ""
                self.item_cantidad = 1
                self.item_precio_iva = 0.0
                self.texto_busqueda_recepcion = ""
                return
        stock_actual = 0
        numero_serie = ""
        for p in self.productos:
            if p["nombre"] == self.item_producto_sel:
                stock_actual = p["stock"]
                numero_serie = p.get("numero_serie", "")
                break
        self.items_recepcion = self.items_recepcion + [{
            "nombre": self.item_producto_sel,
            "numero_serie": numero_serie,
            "cantidad": self.item_cantidad,
            "precio_iva": self.item_precio_iva,
            "stock_actual": stock_actual,
            "subtotal": self.item_cantidad * self.item_precio_iva,
        }]
        self.item_producto_sel = ""
        self.item_cantidad = 1
        self.item_precio_iva = 0.0
        self.texto_busqueda_recepcion = ""

    def quitar_item_recepcion(self, nombre: str):
        self.items_recepcion = [i for i in self.items_recepcion if i["nombre"] != nombre]

    def confirmar_recepcion(self):
        self._limpiar_errores()
        if not self.nombre_proveedor.strip():
            self.error_nombre = "El nombre del proveedor es obligatorio"
            return
        if not self.correo_proveedor.strip():
            self.error_correo = "El correo del proveedor es obligatorio"
            return
        if not self._validar_formato_correo(self.correo_proveedor):
            self.error_correo = "El correo no tiene un formato válido"
            return
        if not self._verificar_dominio_correo(self.correo_proveedor):
            self.error_correo = "El dominio del correo no existe"
            return
        if not self.numero_factura.strip():
            self.error_general = "Debe ingresar número de factura / folio"
            return
        if not self.items_recepcion:
            self.error_general = "Debe agregar al menos un producto"
            return
        total = sum(i["subtotal"] for i in self.items_recepcion)
        items_snap = list(self.items_recepcion)
        proveedor_snap = self.nombre_proveedor
        correo_snap = self.correo_proveedor
        folio_snap = self.numero_factura
        saldo_disponible = (
            self.saldo_inicial
            + sum(self.facturas_clientes.values())
            - sum(self.facturas_proveedores.values())
        )
        monto_deuda = max(0.0, total - saldo_disponible)
        with rx.session() as session:
            for item in self.items_recepcion:
                prod_db = session.exec(select(Producto).where(Producto.nombre == item["nombre"])).first()
                if prod_db:
                    prod_db.stock += item["cantidad"]
                    session.add(prod_db)
            session.commit()
        with rx.session() as session:
            transaccion = Transaccion(
                tipo="Proveedor", nombre=self.nombre_proveedor, correo=self.correo_proveedor,
                numero_factura=self.numero_factura,
                producto=", ".join(i["nombre"] for i in self.items_recepcion),
                monto=total, fecha=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                usuario=self.usuario_nombre,
            )
            session.add(transaccion)
            session.commit()
        self.facturas_proveedores[self.numero_factura] = total
        if monto_deuda > 0:
            with rx.session() as session:
                for item in items_snap:
                    proporcion = (item["subtotal"] / total) if total > 0 else (1.0 / len(items_snap))
                    monto_item = round(monto_deuda * proporcion, 2)
                    prod = next((p for p in self.productos if p["nombre"] == item["nombre"]), {})
                    deuda = Deuda(
                        proveedor=proveedor_snap, correo_proveedor=correo_snap,
                        producto=item["nombre"], marca=prod.get("marca", ""),
                        modelo=prod.get("modelo", ""), stock_pendiente=item["cantidad"],
                        monto_total=monto_item,
                        fecha=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pagada=False,
                    )
                    session.add(deuda)
                session.commit()
            self.cargar_deudas()
        self.cargar_historial()
        self.cargar_inventario()
        self._limpiar_datos_modal()
        self._limpiar()
        self.items_recepcion = []
        self.texto_busqueda_recepcion = ""
        self.mostrar_modal_proveedor_recepcion = False
        self._registrar_movimiento(
            "Recepción",
            f"Recepción de {proveedor_snap} — Folio: {folio_snap} — "
            f"Productos: {', '.join(i['nombre'] for i in items_snap)} — Total: ${total}"
        )

    # VALIDACIÓN CORREO
    def _validar_formato_correo(self, correo: str) -> bool:
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron, correo))

    def _verificar_dominio_correo(self, correo: str) -> bool:
        if not DNS_DISPONIBLE:
            return True
        try:
            dominio = correo.split("@")[1]
            dns.resolver.resolve(dominio, "MX")
            return True
        except Exception:
            return False

    def validar_correo_cliente_live(self, value):
        self.correo_cliente = str(value)
        if value.strip() and not self._validar_formato_correo(value):
            self.error_correo = "El correo no tiene un formato válido (ejemplo@dominio.com)"
        else:
            self.error_correo = ""

    def validar_correo_proveedor_live(self, value):
        self.correo_proveedor = str(value)
        if value.strip() and not self._validar_formato_correo(value):
            self.error_correo = "El correo no tiene un formato válido (ejemplo@dominio.com)"
        else:
            self.error_correo = ""

    # ACCIONES
    def agregar_factura_cliente(self):
        if self.numero_factura and self.numero_factura not in self.facturas_clientes:
            self.facturas_clientes[self.numero_factura] = self.monto_factura

    def agregar_factura_proveedor(self):
        if self.numero_factura and self.numero_factura not in self.facturas_proveedores:
            self.facturas_proveedores[self.numero_factura] = self.monto_factura

    def _limpiar(self):
        self.numero_factura = ""
        self.monto_factura = 0.0
        self.nombre_producto = ""
        self.error_general = ""

    def seleccionar_producto(self, nombre: str):
        self.nombre_producto = nombre
        self.error_general = ""
        # Buscar el producto y obtener su marca y modelo automáticamente
        for p in self.productos:
            if p["nombre"] == nombre:
                self.monto_factura = p["precio_venta"]
                self.marca_seleccionada = p.get("marca", "")
                self.modelo_seleccionado = p.get("modelo", "")
                break

    # CARGA DE DATOS
    def cargar_historial(self):
        try:
            with rx.session() as session:
                transacciones = session.exec(select(Transaccion)).all()
                self.historial = [
                    {
                        "id": t.id, "tipo": t.tipo, "nombre": t.nombre, "correo": t.correo,
                        "numero_factura": t.numero_factura, "producto": t.producto,
                        "monto": t.monto, "fecha": t.fecha, "usuario": t.usuario,
                    }
                    for t in transacciones
                ]
                self.facturas_clientes = {}
                self.facturas_proveedores = {}
                for t in transacciones:
                    if t.tipo == "Cliente":
                        self.facturas_clientes[t.numero_factura] = t.monto
                    elif t.tipo in ("Proveedor", "Pago deuda"):
                        self.facturas_proveedores[t.numero_factura] = t.monto
        except Exception as e:
            print(f"Error en cargar_historial: {e}")
            self.historial = []
            self.facturas_clientes = {}
            self.facturas_proveedores = {}

    def cargar_inventario(self):
        with rx.session() as session:
            productos_db = session.exec(select(Producto)).all()
            self.productos = [
                {
                    "id": p.id, "nombre": p.nombre, "marca": p.marca,
                    "modelo": p.modelo, "numero_serie": p.numero_serie,
                    "stock": p.stock, "precio_compra": p.precio_compra,
                    "precio_venta": p.precio_venta, "fecha_creacion": p.fecha_creacion,
                }
                for p in productos_db
            ]

    # INVENTARIO ACCIONES
    def agregar_producto(self):
        self.error_inventario = ""
        if self.nombre_producto_nuevo.strip() == "":
            self.error_inventario = "El nombre del producto es obligatorio"
            return
        if len(self.numero_serie_producto_nuevo.strip()) < 6:
            self.error_inventario = "El N° de serie debe tener al menos 6 caracteres"
            return
        for p in self.productos:
            if p["numero_serie"] == self.numero_serie_producto_nuevo.strip():
                self.error_inventario = "Ya existe un producto con ese N° de serie"
                return
        for p in self.productos:
            if p["nombre"].lower() == self.nombre_producto_nuevo.lower():
                self.error_inventario = "Ya existe un producto con ese nombre"
                return
        with rx.session() as session:
            nuevo = Producto(
                nombre=self.nombre_producto_nuevo, marca=self.marca_producto_nuevo,
                modelo=self.modelo_producto_nuevo, numero_serie=self.numero_serie_producto_nuevo,
                stock=self.stock_inicial, precio_compra=self.precio_compra,
                precio_venta=self.precio_venta,
                fecha_creacion=datetime.now().strftime("%Y-%m-%d %H:%M"),
            )
            session.add(nuevo)
            session.commit()
        nombre_snap = self.nombre_producto_nuevo
        stock_snap = self.stock_inicial
        self.cargar_inventario()
        self.nombre_producto_nuevo = ""
        self.marca_producto_nuevo = ""
        self.modelo_producto_nuevo = ""
        self.numero_serie_producto_nuevo = ""
        self.stock_inicial = 0
        self.precio_compra = 0
        self.precio_venta = 0
        self._registrar_movimiento("Producto creado", f"Se creó el producto '{nombre_snap}' con stock inicial {stock_snap}")

    def obtener_producto(self, nombre):
        for p in self.productos:
            if p["nombre"] == nombre:
                return p
        return None

    def abrir_modal_editar(self, producto_id: int):
        for p in self.productos:
            if p["id"] == producto_id:
                self.edit_id = producto_id
                self.edit_nombre = p["nombre"]
                self.edit_marca = p.get("marca", "")
                self.edit_modelo = p.get("modelo", "")
                self.edit_numero_serie = p.get("numero_serie", "")
                self.edit_stock = p["stock"]
                self.edit_precio_compra = p["precio_compra"]
                self.edit_precio_venta = p["precio_venta"]
                break
        self.mostrar_modal_editar = True

    def cerrar_modal_editar(self): self.mostrar_modal_editar = False

    def guardar_edicion(self):
        if not self.edit_nombre.strip():
            return
        with rx.session() as session:
            producto = session.get(Producto, self.edit_id)
            if producto:
                producto.nombre = self.edit_nombre
                producto.marca = self.edit_marca
                producto.modelo = self.edit_modelo
                producto.numero_serie = self.edit_numero_serie
                producto.stock = self.edit_stock
                producto.precio_compra = self.edit_precio_compra
                producto.precio_venta = self.edit_precio_venta
                session.add(producto)
                session.commit()
        self.cargar_inventario()
        self.mostrar_modal_editar = False
        self._registrar_movimiento(
            "Producto editado",
            f"Se editó '{self.edit_nombre}' — Marca: {self.edit_marca} — Modelo: {self.edit_modelo} — "
            f"Serie: {self.edit_numero_serie} — Stock: {self.edit_stock} — "
            f"P.Compra: ${self.edit_precio_compra} — P.Venta: ${self.edit_precio_venta}"
        )

    def abrir_modal_eliminar(self, producto_id: int):
        for p in self.productos:
            if p["id"] == producto_id:
                self.eliminar_id = producto_id
                self.eliminar_nombre = p["nombre"]
                break
        self.mostrar_modal_eliminar = True

    def confirmar_eliminar(self, producto_id: int):
        self.eliminar_id = producto_id
        self.mostrar_modal_eliminar = True

    def cancelar_eliminar(self):
        self.eliminar_id = 0
        self.mostrar_modal_eliminar = False

    def eliminar_producto(self):
        nombre_snap = self.eliminar_nombre
        with rx.session() as session:
            producto = session.get(Producto, self.eliminar_id)
            if producto:
                session.delete(producto)
                session.commit()
        self.cargar_inventario()
        self.eliminar_id = 0
        self.mostrar_modal_eliminar = False
        self._registrar_movimiento("Producto eliminado", f"Se eliminó el producto '{nombre_snap}'")

    # CONFIRMAR VENTA CLIENTE
    def confirmar_modal(self):
        self._limpiar_errores()
        hay_error = False
        producto = self.obtener_producto(self.nombre_producto)
        if not producto:
            self.error_general = "Selecciona un producto del inventario"
            return
        if producto["stock"] <= 0:
            self.error_general = "Sin stock disponible"
            return
        if producto["stock"] < self.cantidad_venta:
            self.error_general = f"Stock insuficiente — solo hay {producto['stock']} unidades"
            return
        if not self.nombre_cliente.strip():
            self.error_nombre = "El nombre del cliente es obligatorio"
            hay_error = True
        if not self.correo_cliente.strip():
            self.error_correo = "El correo del cliente es obligatorio"
            hay_error = True
        elif not self._validar_formato_correo(self.correo_cliente):
            self.error_correo = "El correo no tiene un formato válido"
            hay_error = True
        elif not self._verificar_dominio_correo(self.correo_cliente):
            self.error_correo = "El dominio del correo no existe"
            hay_error = True
        if not self.numero_factura:
            self.error_general = "Debe ingresar número de factura"
            hay_error = True
        if hay_error:
            return
        cliente_snap = self.nombre_cliente
        producto_snap = self.nombre_producto
        factura_snap = self.numero_factura
        monto_total = self.monto_total_venta
        with rx.session() as session:
            prod_db = session.get(Producto, producto["id"])
            if prod_db:
                prod_db.stock -= self.cantidad_venta
                session.add(prod_db)
                session.commit()
        self.facturas_clientes[self.numero_factura] = monto_total
        with rx.session() as session:
            transaccion = Transaccion(
                tipo="Cliente", nombre=self.nombre_cliente, correo=self.correo_cliente,
                numero_factura=self.numero_factura, producto=self.nombre_producto,
                monto=monto_total, fecha=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                usuario=self.usuario_nombre,
            )
            session.add(transaccion)
            session.commit()
        self.cargar_historial()
        self.cargar_inventario()
        self._limpiar_datos_modal()
        self._limpiar()
        self.cantidad_venta = 1
        self.marca_seleccionada = ""
        self.modelo_seleccionado = ""
        self._registrar_movimiento(
            "Venta",
            f"Venta a {cliente_snap} — Producto: {producto_snap} x{self.cantidad_venta} — "
            f"Factura: {factura_snap} — ${monto_total}"
        )

    # AUTENTICACIÓN
    def set_login_nombre(self, value): self.login_nombre = value
    def set_login_password(self, value): self.login_password = value
    def toggle_login_password(self): self.login_mostrar_password = not self.login_mostrar_password
    def set_reg_nombre(self, value): self.reg_nombre = value
    def set_reg_apellidos(self, value): self.reg_apellidos = value
    def set_reg_correo(self, value): self.reg_correo = value
    def set_reg_password(self, value): self.reg_password = value
    def set_reg_domicilio(self, value): self.reg_domicilio = value
    def set_reg_edad(self, value): self.reg_edad = int(value) if value else 0
    def set_reg_rol(self, value): self.reg_rol = value

    # SETTERS EDITAR PERFIL
    def set_editar_perfil_nombre(self, value): self.editar_perfil_nombre = value
    def set_editar_perfil_apellidos(self, value): self.editar_perfil_apellidos = value
    def set_editar_perfil_domicilio(self, value): self.editar_perfil_domicilio = value
    def set_editar_perfil_edad(self, value): self.editar_perfil_edad = int(value) if value else 0
    def set_editar_perfil_correo(self, value): self.editar_perfil_correo = value

    def abrir_modal_perfil(self):
        if self.usuario_logueado:
            self.editar_perfil_nombre = self.usuario_nombre
            self.editar_perfil_apellidos = self.usuario_apellidos
            self.editar_perfil_domicilio = self.usuario_domicilio
            self.editar_perfil_edad = self.usuario_edad
            self.editar_perfil_correo = self.usuario_correo
            self.editar_perfil_error = ""
            self.editar_perfil_exito = ""
            self.mostrar_modal_perfil = True

    def cerrar_modal_perfil(self):
        self.mostrar_modal_perfil = False
        self.editar_perfil_error = ""
        self.editar_perfil_exito = ""

    def guardar_cambios_perfil(self):
        self.editar_perfil_error = ""
        self.editar_perfil_exito = ""
        if not self.editar_perfil_nombre.strip():
            self.editar_perfil_error = "El nombre no puede estar vacío"
            return
        if not self.editar_perfil_apellidos.strip():
            self.editar_perfil_error = "Los apellidos no pueden estar vacíos"
            return
        if self.editar_perfil_edad < 0 or self.editar_perfil_edad > 60:
            self.editar_perfil_error = "Edad inválida (0-60)"
            return
        with rx.session() as session:
            usuario = session.exec(select(Usuario).where(Usuario.id == self.usuario_id)).first()
            if not usuario:
                self.editar_perfil_error = "Usuario no encontrado"
                return
            usuario.nombre = self.editar_perfil_nombre
            usuario.apellidos = self.editar_perfil_apellidos
            usuario.domicilio = self.editar_perfil_domicilio
            usuario.edad = self.editar_perfil_edad
            session.add(usuario)
            session.commit()
        self.usuario_nombre = self.editar_perfil_nombre
        self.usuario_apellidos = self.editar_perfil_apellidos
        self.usuario_domicilio = self.editar_perfil_domicilio
        self.usuario_edad = self.editar_perfil_edad
        self.editar_perfil_exito = "Datos actualizados exitosamente"

    def inicializar_admin(self):
        try:
            with rx.session() as session:
                admin = session.exec(select(Usuario).where(Usuario.correo == "admin@dominio.com")).first()
                if not admin:
                    admin = Usuario(
                        nombre="Admin", apellidos="Uno", correo="admin@dominio.com",
                        contrasena_hash=_hash_password("admin123"),
                        rol="administrador", activo=True,
                    )
                    session.add(admin)
                    session.commit()
        except Exception as e:
            print(f"Error inicializando admin: {e}")

    def login(self):
        self.login_error = ""
        if not self.login_nombre.strip() or not self.login_password.strip():
            self.login_error = "Ingresa tu nombre y contraseña"
            return
        with rx.session() as session:
            # FIX: Buscar SOLO por nombre+activo, verificar contraseña aparte
            # (bcrypt genera hash distinto cada vez, no se puede comparar en SQL)
            usuario = session.exec(
                select(Usuario).where(
                    Usuario.nombre == self.login_nombre,
                    Usuario.activo == True,
                )
            ).first()
            if not usuario or not _verificar_password(self.login_password, usuario.contrasena_hash):
                self.login_error = "Nombre o contraseña incorrectos"
                return
            self.usuario_logueado = True
            self.usuario_id = usuario.id
            self.usuario_nombre = usuario.nombre
            self.usuario_apellidos = usuario.apellidos
            self.usuario_rol = usuario.rol
            self.usuario_correo = usuario.correo
            self.usuario_domicilio = usuario.domicilio
            self.usuario_edad = usuario.edad
            self.login_nombre = ""
            self.login_password = ""
        self.cargar_historial()
        self.cargar_inventario()
        self.cargar_movimientos()
        self.cargar_deudas()

    def logout(self):
        self.usuario_logueado = False
        self.usuario_id = 0
        self.usuario_nombre = ""
        self.usuario_apellidos = ""
        self.usuario_rol = ""
        self.usuario_correo = ""
        self.usuario_domicilio = ""
        self.usuario_edad = 0
        self.login_nombre = ""
        self.login_password = ""
        self.login_error = ""
        self.login_mostrar_password = False

    def abrir_modal_registro(self):
        self.reg_nombre = ""
        self.reg_apellidos = ""
        self.reg_correo = ""
        self.reg_password = ""
        self.reg_domicilio = ""
        self.reg_edad = 0
        self.reg_rol = "empleado"
        self.reg_error = ""
        self.reg_exito = ""
        self.mostrar_modal_registro = True

    def cerrar_modal_registro(self): self.mostrar_modal_registro = False

    def registrar_usuario(self):
        self.reg_error = ""
        self.reg_exito = ""
        if not self.reg_nombre.strip():
            self.reg_error = "El nombre es obligatorio"
            return
        if not self.reg_apellidos.strip():
            self.reg_error = "Los apellidos son obligatorios"
            return
        if not self._validar_formato_correo(self.reg_correo):
            self.reg_error = "El correo no tiene un formato válido"
            return
        if not self._verificar_dominio_correo(self.reg_correo):
            self.reg_error = "El dominio del correo no existe"
            return
        if len(self.reg_password) < 6:
            self.reg_error = "La contraseña debe tener al menos 6 caracteres"
            return
        with rx.session() as session:
            existente = session.exec(select(Usuario).where(Usuario.nombre == self.reg_nombre)).first()
            if existente:
                self.reg_error = "Ya existe un usuario con ese nombre"
                return
            nuevo = Usuario(
                nombre=self.reg_nombre, apellidos=self.reg_apellidos, correo=self.reg_correo,
                contrasena_hash=_hash_password(self.reg_password), rol=self.reg_rol, activo=True,
                domicilio=self.reg_domicilio, edad=self.reg_edad,
            )
            session.add(nuevo)
            session.commit()
        self.reg_exito = f"Usuario '{self.reg_nombre}' creado como {self.reg_rol}"
        self.reg_nombre = ""
        self.reg_apellidos = ""
        self.reg_correo = ""
        self.reg_password = ""
        self.reg_domicilio = ""
        self.reg_edad = 0
        self.cargar_usuarios()

    def cargar_usuarios(self):
        with rx.session() as session:
            usuarios = session.exec(select(Usuario)).all()
            self.usuarios_lista = [
                {"id": u.id, "nombre": u.nombre, "apellidos": u.apellidos,
                 "correo": u.correo, "rol": u.rol, "activo": u.activo}
                for u in usuarios
            ]

    @rx.var
    def usuarios_filtrados(self) -> list[dict]:
        if not self.usuarios_texto_busqueda.strip():
            return self.usuarios_lista
        texto = self.usuarios_texto_busqueda.strip().lower()
        return [
            u for u in self.usuarios_lista
            if texto in u["nombre"].lower() or
               texto in u["apellidos"].lower() or
               texto in u["correo"].lower()
        ]

    @rx.var
    def usuarios_paginados(self) -> list[dict]:
        start = (self.usuarios_pagina_actual - 1) * self.usuarios_items_por_pagina
        end = start + self.usuarios_items_por_pagina
        return self.usuarios_filtrados[start:end]

    @rx.var
    def total_usuarios_filtradores(self) -> int:
        return len(self.usuarios_filtrados)

    @rx.var
    def total_paginas_usuarios(self) -> int:
        total = self.total_usuarios_filtradores
        paginas = (total + self.usuarios_items_por_pagina - 1) // self.usuarios_items_por_pagina
        return max(1, paginas)

    def desactivar_usuario(self, usuario_id: int):
        with rx.session() as session:
            usuario = session.get(Usuario, usuario_id)
            if usuario and usuario.correo != "admin@dominio.com":
                usuario.activo = not usuario.activo
                session.add(usuario)
                session.commit()
        self.cargar_usuarios()

    # CAMBIAR CONTRASEÑA
    def cambiar_contrasena(self):
        self.cuenta_error = ""
        self.cuenta_exito = ""
        if not self.cuenta_pass_actual.strip():
            self.cuenta_error = "Ingresa tu contraseña actual"
            return
        if not self.cuenta_pass_nueva.strip():
            self.cuenta_error = "Ingresa la nueva contraseña"
            return
        if len(self.cuenta_pass_nueva) < 6:
            self.cuenta_error = "La nueva contraseña debe tener al menos 6 caracteres"
            return
        if self.cuenta_pass_nueva != self.cuenta_pass_confirmar:
            self.cuenta_error = "Las contraseñas nuevas no coinciden"
            return
        if self.cuenta_pass_actual == self.cuenta_pass_nueva:
            self.cuenta_error = "La nueva contraseña debe ser diferente a la actual"
            return
        try:
            with rx.session() as session:
                usuario = session.exec(select(Usuario).where(Usuario.nombre == self.usuario_nombre)).first()
                if not usuario:
                    self.cuenta_error = "Usuario no encontrado"
                    return
                # FIX: usar _verificar_password en lugar de comparar hashes
                if not _verificar_password(self.cuenta_pass_actual, usuario.contrasena_hash):
                    self.cuenta_error = "La contraseña actual es incorrecta"
                    return
                usuario.contrasena_hash = _hash_password(self.cuenta_pass_nueva)
                session.add(usuario)
                session.commit()
            self.cuenta_pass_actual = ""
            self.cuenta_pass_nueva = ""
            self.cuenta_pass_confirmar = ""
            self.cuenta_exito = "Contraseña actualizada correctamente"
            self._registrar_movimiento("Cambio de contraseña", f"{self.usuario_nombre} actualizó su contraseña")
        except Exception as e:
            self.cuenta_error = f"Error al cambiar contraseña: {str(e)}"
            return

    # ON LOAD
    def on_load(self):
        try:
            self.inicializar_admin()
        except Exception as e:
            print(f"Error en inicializar_admin: {e}")
        try:
            self.cargar_historial()
        except Exception as e:
            print(f"Error cargando historial: {e}")
        try:
            self.cargar_inventario()
        except Exception as e:
            print(f"Error cargando inventario: {e}")
        try:
            self.cargar_movimientos()
        except Exception as e:
            print(f"Error cargando movimientos: {e}")
        try:
            self.cargar_deudas()
        except Exception as e:
            print(f"Error cargando deudas: {e}")

    # ======================
    # VARIABLES COMPUTADAS
    # ======================
    @rx.var
    def total_ingresos(self) -> float:
        return sum(self.facturas_clientes.values())

    @rx.var
    def total_egresos(self) -> float:
        return sum(self.facturas_proveedores.values())

    @rx.var
    def balance_real(self) -> float:
        return self.saldo_inicial + self.total_ingresos - self.total_egresos

    @rx.var
    def saldo_total(self) -> float:
        return max(0.0, self.balance_real)

    @rx.var
    def saldo_insuficiente(self) -> bool:
        return self.balance_real < 0

    @rx.var
    def deuda_total_acumulada(self) -> float:
        return abs(self.balance_real) if self.balance_real < 0 else 0.0

    @rx.var
    def precio_producto_seleccionado(self) -> float:
        for p in self.productos:
            if p["nombre"] == self.nombre_producto:
                return p["precio_venta"]
        return 0.0

    @rx.var
    def monto_total_venta(self) -> float:
        return round(self.precio_producto_seleccionado * self.cantidad_venta, 2)

    @rx.var
    def stock_producto_seleccionado(self) -> int:
        for p in self.productos:
            if p["nombre"] == self.nombre_producto:
                return p["stock"]
        return 0

    @rx.var
    def stock_disponible_producto(self) -> int:
        for p in self.productos:
            if p["nombre"] == self.nombre_producto:
                return p["stock"]
        return 0

    @rx.var
    def total_productos(self) -> int:
        return len(self.productos)

    @rx.var
    def total_clientes(self) -> int:
        return len({r["nombre"] for r in self.historial if r["tipo"] == "Cliente"})

    @rx.var
    def total_proveedores(self) -> int:
        return len({r["nombre"] for r in self.historial if r["tipo"] == "Proveedor"})

    @rx.var
    def productos_stock_bajo(self) -> list[dict]:
        return [p for p in self.productos if p["stock"] <= self.stock_minimo_alerta]

    @rx.var
    def datos_grafica_mensual(self) -> list[dict]:
        resumen = {}
        for r in self.historial:
            fecha_str = r.get("fecha", "")
            monto = float(r.get("monto", 0))
            tipo = r.get("tipo", "")
            try:
                fecha = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M:%S")
                mes = fecha.strftime("%Y-%m")
            except:
                continue
            if mes not in resumen:
                resumen[mes] = {"mes": mes, "ingresos": 0, "egresos": 0}
            if tipo == "Cliente":
                resumen[mes]["ingresos"] += monto
            elif tipo in ("Proveedor", "Pago deuda"):
                resumen[mes]["egresos"] += monto
        resultado = []
        for mes in sorted(resumen.keys()):
            ingresos = resumen[mes]["ingresos"]
            egresos = resumen[mes]["egresos"]
            resultado.append({"mes": mes, "ingresos": ingresos, "egresos": egresos, "balance": ingresos - egresos})
        return resultado

    @rx.var
    def historial_filtrado(self) -> list[dict]:
        if not self.texto_busqueda.strip():
            return self.historial
        texto = self.texto_busqueda.strip().lower()
        return [
            r for r in self.historial
            if texto in str(r.get("nombre", "")).lower()
            or texto in str(r.get("numero_factura", "")).lower()
            or texto in str(r.get("fecha", "")).lower()
        ]

    @rx.var
    def productos_filtrados(self) -> list[dict]:
        umbral = self.stock_minimo_alerta
        if not self.texto_busqueda_producto:
            lista = self.productos
        else:
            texto = self.texto_busqueda_producto.lower()
            lista = [p for p in self.productos if texto in p["nombre"].lower() or texto == str(p["id"])]
        return [{**p, "stock_bajo": p["stock"] <= umbral} for p in lista]

    @rx.var
    def nombres_productos_con_stock(self) -> list[str]:
        return [p["nombre"] for p in self.productos if p["stock"] > 0]

    @rx.var
    def nombres_todos_productos(self) -> list[str]:
        return [p["nombre"] for p in self.productos]

    @rx.var
    def nombres_productos_recepcion(self) -> list[str]:
        if not self.texto_busqueda_recepcion.strip():
            return [p["nombre"] for p in self.productos]
        texto = self.texto_busqueda_recepcion.strip().lower()
        return [
            p["nombre"] for p in self.productos
            if texto in p["nombre"].lower()
            or texto in p.get("marca", "").lower()
            or texto in p.get("modelo", "").lower()
        ]

    @rx.var
    def productos_con_stock_filtrados(self) -> list[dict]:
        if not self.nombre_producto.strip():
            return []
        texto = self.nombre_producto.strip().lower()
        return [p for p in self.productos if texto in p["nombre"].lower() and p["stock"] > 0]

    @rx.var
    def marcas_disponibles(self) -> list[str]:
        return sorted(list({p["marca"] for p in self.productos if p["stock"] > 0 and p["marca"]}))

    @rx.var
    def modelos_por_marca(self) -> list[str]:
        return sorted(list({p["modelo"] for p in self.productos if p["marca"] == self.marca_seleccionada and p["stock"] > 0 and p["modelo"]}))

    @rx.var
    def productos_por_modelo(self) -> list[str]:
        if not self.marca_seleccionada or not self.modelo_seleccionado:
            return []
        return [
            p["nombre"] for p in self.productos
            if p["marca"] == self.marca_seleccionada
            and p["modelo"] == self.modelo_seleccionado
            and p["stock"] > 0
        ]

    @rx.var
    def nombres_productos_filtrados_por_modelo(self) -> list[str]:
        return [p["nombre"] for p in self.productos if p["marca"] == self.marca_seleccionada and p["modelo"] == self.modelo_seleccionado and p["stock"] > 0]

    @rx.var
    def total_recepcion(self) -> float:
        return sum(i["subtotal"] for i in self.items_recepcion)

    @rx.var
    def total_piezas_recepcion(self) -> int:
        return sum(i["cantidad"] for i in self.items_recepcion)

    @rx.var
    def precio_compra_producto_sel(self) -> float:
        for p in self.productos:
            if p["nombre"] == self.item_producto_sel:
                return p["precio_compra"]
        return 0.0

    @rx.var
    def historial_completo(self) -> list[dict]:
        resultado = []
        for t in self.historial:
            resultado.append({
                "id": t.get("id", 0),
                "tipo": t["tipo"],
                "descripcion": f"{t['nombre']} — {t['producto']} — Factura: {t['numero_factura']} — ${t['monto']}",
                "fecha": t["fecha"],
                "usuario": t.get("usuario", ""),
            })
        for m in self.movimientos:
            resultado.append({
                "id": 0,
                "tipo": m["tipo"], "descripcion": m["descripcion"],
                "fecha": m["fecha"], "usuario": m.get("usuario", ""),
            })
        return sorted(resultado, key=lambda x: x["fecha"], reverse=True)

    @rx.var
    def sugerencias_proveedor(self) -> list[dict]:
        texto = self.nombre_proveedor.strip().lower()
        if not texto:
            return []
        vistos = set()
        resultado = []
        for t in self.historial:
            if t.get("tipo") != "Proveedor":
                continue
            nombre = t.get("nombre", "")
            if nombre.lower() in vistos:
                continue
            if texto in nombre.lower():
                vistos.add(nombre.lower())
                resultado.append({"nombre": nombre, "correo": t.get("correo", "")})
        return resultado

    # VARS DEUDAS
    @rx.var
    def deudas_pendientes(self) -> list[dict]:
        return [d for d in self.deudas if not d["pagada"]]

    @rx.var
    def total_deuda(self) -> float:
        return sum(d["monto_total"] for d in self.deudas if not d["pagada"])

    @rx.var
    def hay_deuda_activa(self) -> bool:
        return any(not d["pagada"] for d in self.deudas)

    @rx.var
    def deuda_recepcion_actual(self) -> float:
        diferencia = self.balance_real - self.total_recepcion
        return abs(diferencia) if diferencia < 0 else 0.0

    @rx.var
    def recepcion_genera_deuda(self) -> bool:
        return self.total_recepcion > self.balance_real and self.total_recepcion > 0

    # ================================
    # VARS CASCADA RECEPCIÓN: Producto → Marca → Modelo
    # ================================
    @rx.var
    def productos_recepcion_filtrados(self) -> list[str]:
        """Todos los productos disponibles — se muestran desde el inicio."""
        return [p["nombre"] for p in self.productos]

    @rx.var
    def marcas_recepcion(self) -> list[str]:
        """Marcas del producto seleccionado (aparece tras elegir producto)."""
        if not self.item_producto_sel:
            return []
        return sorted(list({
            p["marca"] for p in self.productos
            if p["nombre"] == self.item_producto_sel and p["marca"]
        }))

    @rx.var
    def modelos_recepcion(self) -> list[str]:
        """Modelos del producto+marca seleccionados (aparece tras elegir marca)."""
        if not self.item_producto_sel or not self.item_marca_sel:
            return []
        return sorted(list({
            p["modelo"] for p in self.productos
            if p["nombre"] == self.item_producto_sel
            and p["marca"] == self.item_marca_sel
            and p["modelo"]
        }))

    @rx.var
    def productos_recepcion(self) -> list[str]:
        """Alias legacy."""
        return self.productos_recepcion_filtrados

    # VARS HISTORIAL
    @rx.var
    def tipos_disponibles_historial(self) -> list[str]:
        return sorted(list({r["tipo"] for r in self.historial if r.get("tipo")}))

    @rx.var
    def usuarios_disponibles_historial(self) -> list[str]:
        return sorted(list({r.get("usuario", "") for r in self.historial if r.get("usuario")}))

    @rx.var
    def historial_completo_filtrado(self) -> list[dict]:
        resultado = self.historial_completo
        if self.filtro_tipo_historial:
            resultado = [r for r in resultado if r.get("tipo") == self.filtro_tipo_historial]
        if self.filtro_usuario_historial:
            resultado = [r for r in resultado if r.get("usuario") == self.filtro_usuario_historial]
        if self.texto_busqueda.strip():
            texto = self.texto_busqueda.strip().lower()
            resultado = [
                r for r in resultado
                if texto in r.get("descripcion", "").lower()
                or texto in r.get("tipo", "").lower()
                or texto in r.get("usuario", "").lower()
                or texto in r.get("fecha", "").lower()
            ]
        if self.filtro_fecha_inicio:
            try:
                desde = datetime.strptime(self.filtro_fecha_inicio, "%Y-%m-%d")
                resultado = [r for r in resultado if datetime.strptime(r["fecha"], "%d/%m/%Y %H:%M:%S") >= desde]
            except Exception:
                pass
        if self.filtro_fecha_fin:
            try:
                hasta = datetime.strptime(self.filtro_fecha_fin, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
                resultado = [r for r in resultado if datetime.strptime(r["fecha"], "%d/%m/%Y %H:%M:%S") <= hasta]
            except Exception:
                pass
        return resultado

    @rx.var
    def total_paginas_historial(self) -> int:
        total = len(self.historial_completo_filtrado)
        paginas = (total + self.items_por_pagina - 1) // self.items_por_pagina
        return max(1, paginas)

    @rx.var
    def historial_filtrado_y_paginado(self) -> list[dict]:
        inicio = (self.pagina_actual - 1) * self.items_por_pagina
        fin = inicio + self.items_por_pagina
        return self.historial_completo_filtrado[inicio:fin]

    # ================================
    # RECUPERACIÓN DE CONTRASEÑA (3 pasos)
    # ================================
    def abrir_modal_recuperacion(self):
        self.mostrar_modal_recuperacion = True
        self.recuperacion_paso = 1
        self.recuperacion_correo = ""
        self.recuperacion_codigo = ""
        self._recuperacion_codigo_real = ""
        self.recuperacion_password_nueva = ""
        self.recuperacion_error = ""
        self.recuperacion_exito = ""

    def cerrar_modal_recuperacion(self):
        self.mostrar_modal_recuperacion = False
        self.recuperacion_paso = 1

    def set_recuperacion_correo(self, value: str):
        self.recuperacion_correo = value
        self.recuperacion_error = ""

    def set_recuperacion_codigo(self, value: str):
        self.recuperacion_codigo = value
        self.recuperacion_error = ""

    def set_recuperacion_password_nueva(self, value: str):
        self.recuperacion_password_nueva = value
        self.recuperacion_error = ""

    def set_recuperacion_paso(self, value: int):
        self.recuperacion_paso = int(value)
        self.recuperacion_error = ""

    def _enviar_correo_recuperacion(self, correo_destino: str, codigo: str, nombre_usuario: str) -> bool:
        """Envía el código de recuperación por email."""
        if not EMAIL_CONFIG:
            print("⚠️ EMAIL_CONFIG no configurada. Email no enviado.")
            return False
        try:
            mensaje = MIMEMultipart('alternative')
            mensaje['Subject'] = "Código de Recuperación de Contraseña - StakFlow"
            mensaje['From'] = EMAIL_CONFIG.get('sender_name', 'StakFlow')
            mensaje['To'] = correo_destino
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                    <div style="max-width: 500px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <h2 style="color: #3182CE; text-align: center;">StakFlow</h2>
                        <h3 style="color: #1a202c; margin-bottom: 20px;">Recuperación de Contraseña</h3>
                        <p style="color: #4a5568; font-size: 16px;">Hola <strong>{nombre_usuario}</strong>,</p>
                        <p style="color: #4a5568; font-size: 14px;">Recibimos una solicitud para recuperar tu contraseña. 
                        Usa el siguiente código en la aplicación:</p>
                        <div style="background-color: #edf2f7; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0;">
                            <p style="font-size: 32px; font-weight: bold; color: #3182CE; letter-spacing: 5px; margin: 0;">
                                {codigo}
                            </p>
                        </div>
                        <p style="color: #4a5568; font-size: 14px;">Este código expira en 15 minutos.</p>
                        <p style="color: #a0aec0; font-size: 12px; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 20px;">
                            Si no solicitaste esta recuperación, puedes ignorar este mensaje.
                        </p>
                    </div>
                </body>
            </html>
            """
            texto = f"Código de recuperación: {codigo}\n\nEste código expira en 15 minutos."
            mensaje.attach(MIMEText(texto, 'plain'))
            mensaje.attach(MIMEText(html, 'html'))
            smtp_server = EMAIL_CONFIG.get('smtp_server')
            smtp_port = EMAIL_CONFIG.get('smtp_port', 587)
            sender_email = EMAIL_CONFIG.get('sender_email')
            sender_password = EMAIL_CONFIG.get('sender_password')
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(mensaje)
            print(f"✓ Email enviado a {correo_destino}")
            return True
        except Exception as e:
            print(f"✗ Error enviando email: {e}")
            import traceback
            traceback.print_exc()
            return False

    def solicitar_recuperacion_contrasena(self):
        """Paso 1: verifica correo y envía código."""
        self.recuperacion_error = ""
        self.recuperacion_exito = ""
        if not self.recuperacion_correo.strip():
            self.recuperacion_error = "Ingresa tu correo"
            return
        nombre_usuario = ""
        codigo = ""
        try:
            with rx.session() as session:
                usuario = session.exec(
                    select(Usuario).where(Usuario.correo == self.recuperacion_correo.strip())
                ).first()
                if not usuario:
                    self.recuperacion_error = "No existe una cuenta con ese correo"
                    return
                nombre_usuario = usuario.nombre
                codigo = str(random.randint(100000, 999999))
                usuario.recovery_code = codigo
                session.add(usuario)
                session.commit()
            self._recuperacion_codigo_real = codigo
            exito = self._enviar_correo_recuperacion(
                correo_destino=self.recuperacion_correo.strip(),
                codigo=codigo,
                nombre_usuario=nombre_usuario
            )
            if exito:
                self.recuperacion_exito = f"Código enviado a {self.recuperacion_correo}"
                self.recuperacion_paso = 2
                self.recuperacion_codigo = ""
                self.recuperacion_password_nueva = ""
            else:
                self.recuperacion_error = "Error enviando email. Contactate con soporte."
                self._recuperacion_codigo_real = ""
        except Exception as e:
            self.recuperacion_error = f"Error: {str(e)}"
            self._recuperacion_codigo_real = ""
            return
        self.recuperacion_paso = 2

    def validar_y_cambiar_contrasena_recuperacion(self):
        """Paso 2: valida código y cambia contraseña."""
        self.recuperacion_error = ""
        if not self._recuperacion_codigo_real:
            self.recuperacion_error = "Por favor solicita un código primero"
            return
        if self.recuperacion_codigo.strip() != self._recuperacion_codigo_real:
            self.recuperacion_error = "Código incorrecto"
            return
        if not self.recuperacion_password_nueva.strip():
            self.recuperacion_error = "Ingresa una nueva contraseña"
            return
        if len(self.recuperacion_password_nueva) < 6:
            self.recuperacion_error = "La contraseña debe tener al menos 6 caracteres"
            return
        try:
            with rx.session() as session:
                usuario = session.exec(
                    select(Usuario).where(Usuario.correo == self.recuperacion_correo.strip())
                ).first()
                if not usuario:
                    self.recuperacion_error = "Usuario no encontrado"
                    return
                usuario.contrasena_hash = _hash_password(self.recuperacion_password_nueva)
                usuario.recovery_code = None
                session.add(usuario)
                session.commit()
            self._registrar_movimiento(
                "Recuperación de contraseña",
                f"Se cambió la contraseña de la cuenta {self.recuperacion_correo}"
            )
            self.recuperacion_exito = "Contraseña actualizada correctamente"
            self.recuperacion_paso = 3
            self.recuperacion_correo = ""
            self.recuperacion_codigo = ""
            self.recuperacion_password_nueva = ""
            self._recuperacion_codigo_real = ""
        except Exception as e:
            self.recuperacion_error = f"Error al cambiar contraseña: {str(e)}"
            return