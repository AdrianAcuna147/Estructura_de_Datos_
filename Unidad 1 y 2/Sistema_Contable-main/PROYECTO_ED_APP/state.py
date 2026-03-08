# $======================$
# ||BACKEND DEL SISTEMA ||
# $======================$

##### AVISO ######
# Solo Dios y yo (Adrian Yama) sabemos que hace este codigo, sino sabe pregunte

import reflex as rx
import re
from datetime import datetime
from sqlmodel import select
from typing import Optional
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

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
    recovery_code: Optional[str] = None  # Código de recuperación, opcional


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


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class ContableState(rx.State):
    # ======================
    # VARIABLES A UTILIZAR
    # ======================
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
    # ================================
    # FILTROS Y PAGINACIÓN DE HISTORIAL
    # ================================
    filtro_tipo_historial: str = ""
    filtro_usuario_historial: str = ""
    filtro_fecha_inicio: str = ""
    filtro_fecha_fin: str = ""
    pagina_actual: int = 1
    items_por_pagina: int = 10
    productos: list[dict] = []
    nombre_producto_nuevo: str = ""
    marca_producto_nuevo: str = ""
    modelo_producto_nuevo: str = ""
    numero_serie_producto_nuevo: str = ""
    stock_inicial: int = 0
    precio_compra: float = 0.0
    precio_venta: float = 0.0
    texto_busqueda_producto: str = ""

    # EDICIÓN
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

    # =============================
    # EDICIÓN DE TRANSACCIONES (UI)
    # =============================
    editar_trans_id: int = 0
    editar_trans_numero: str = ""
    editar_trans_monto: float = 0.0
    editar_trans_nombre: str = ""
    editar_trans_correo: str = ""
    editar_trans_producto: str = ""
    editar_trans_tipo: str = ""
    mostrar_modal_editar_transaccion: bool = False

    stock_minimo_alerta: int = 5

    # ================================
    # VARIABLES RECEPCIÓN DE MERCANCÍA
    # Cascada: marca → modelo → producto
    # ================================
    items_recepcion: list[dict] = []
    item_marca_recepcion: str = ""     # NUEVO
    item_modelo_recepcion: str = ""    # NUEVO
    item_producto_sel: str = ""
    item_cantidad: int = 1
    item_precio_iva: float = 0.0
    mostrar_modal_proveedor_recepcion: bool = False
    texto_busqueda_recepcion: str = ""

    # ================================
    # VARIABLES FILTRO CLIENTE
    # Cascada: marca → modelo → producto
    # ================================
    marca_seleccionada: str = ""
    modelo_seleccionado: str = ""
    cantidad_venta: int = 1  # NUEVO

    # ================================
    # VARIABLES DE AUTENTICACIÓN
    # ================================
    usuario_logueado: bool = False
    usuario_nombre: str = ""
    usuario_rol: str = ""
    usuario_correo: str = ""
    login_nombre: str = ""
    login_password: str = ""
    login_error: str = ""
    login_mostrar_password: bool = False
    recuperacion_correo: str = ""
    recuperacion_codigo: str = ""
    recuperacion_password_nueva: str = ""
    recuperacion_error: str = ""
    recuperacion_exito: str = ""
    recuperacion_paso: int = 1
    mostrar_modal_recuperacion: bool = False
    reg_nombre: str = ""
    reg_apellidos: str = ""
    reg_correo: str = ""
    reg_password: str = ""
    reg_rol: str = "empleado"
    reg_error: str = ""
    reg_exito: str = ""
    mostrar_modal_registro: bool = False
    usuarios_lista: list[dict] = []

    # ================================
    # VARIABLES DEUDAS
    # ================================
    deudas: list[dict] = []
    error_deuda: str = ""

    # ================================
    # VARIABLES MI CUENTA
    # ================================
    cuenta_pass_actual: str = ""
    cuenta_pass_nueva: str = ""
    cuenta_pass_confirmar: str = ""
    cuenta_error: str = ""
    cuenta_exito: str = ""

    # ================================
    # DATOS PARA GRAFICA FINANCIERA
    # ================================
    grafica_financiera: list[dict] = [
        {"mes": "Enero",   "ingresos": 12000, "egresos": 8000},
        {"mes": "Febrero", "ingresos": 15000, "egresos": 9000},
        {"mes": "Marzo",   "ingresos": 10000, "egresos": 7000},
    ]

    # ======================
    # SETTERS GENERALES
    # ======================
    def set_saldo_inicial(self, value):
        try:
            self.saldo_inicial = float(value) if value.strip() else 0.0
        except (ValueError, AttributeError):
            self.saldo_inicial = 0.0

    def set_numero_factura(self, value):
        self.numero_factura = value

    def set_nombre_producto(self, value):
        self.nombre_producto = value
        self.error_general = ""

    def set_monto_factura(self, value):
        try:
            self.monto_factura = float(value) if value.strip() else 0.0
        except (ValueError, AttributeError):
            self.monto_factura = 0.0

    def set_nombre_cliente(self, value):
        self.nombre_cliente = str(value)

    def set_nombre_proovedor(self, value):
        self.nombre_proveedor = str(value)

    def set_correo_cliente(self, value):
        self.correo_cliente = str(value)

    def set_correo_proovedor(self, value):
        self.correo_proveedor = str(value)

    def set_texto_busqueda(self, value):
        self.texto_busqueda = value
        self.pagina_actual = 1

    def set_texto_busqueda_producto(self, value):
        self.texto_busqueda_producto = value

    # Setters de filtros historial
    def set_filtro_tipo_historial(self, value):
        self.filtro_tipo_historial = str(value)
        self.pagina_actual = 1

    def set_filtro_usuario_historial(self, value):
        self.filtro_usuario_historial = str(value)
        self.pagina_actual = 1

    def set_filtro_fecha_inicio(self, value):
        self.filtro_fecha_inicio = str(value)
        self.pagina_actual = 1

    def set_filtro_fecha_fin(self, value):
        self.filtro_fecha_fin = str(value)
        self.pagina_actual = 1

    def set_pagina_actual(self, value):
        try:
            p = int(value) if value else 1
            self.pagina_actual = max(1, p)
        except (ValueError, TypeError):
            self.pagina_actual = 1

    def limpiar_filtros_historial(self):
        self.texto_busqueda = ""
        self.filtro_tipo_historial = ""
        self.filtro_usuario_historial = ""
        self.filtro_fecha_inicio = ""
        self.filtro_fecha_fin = ""
        self.pagina_actual = 1

    def set_recuperacion_correo(self, value):
        self.recuperacion_correo = str(value)
        self.recuperacion_error = ""
        self.recuperacion_exito = ""

    def set_recuperacion_codigo(self, value):
        self.recuperacion_codigo = str(value)
        self.recuperacion_error = ""

    def set_recuperacion_password_nueva(self, value):
        self.recuperacion_password_nueva = str(value)
        self.recuperacion_error = ""

    # ================================
    # SETTERS CASCADA RECEPCIÓN (NUEVO)
    # ================================
    def set_item_marca_recepcion(self, value: str):
        """Cambia marca → resetea modelo y producto."""
        self.item_marca_recepcion = value
        self.item_modelo_recepcion = ""
        self.item_producto_sel = ""
        self.item_precio_iva = 0.0

    def set_item_modelo_recepcion(self, value: str):
        """Cambia modelo → resetea producto y auto-selecciona si hay uno solo."""
        self.item_modelo_recepcion = value
        self.item_producto_sel = ""
        self.item_precio_iva = 0.0
        candidatos = [
            p for p in self.productos
            if p["marca"] == self.item_marca_recepcion and p["modelo"] == value
        ]
        if len(candidatos) == 1:
            self.item_producto_sel = candidatos[0]["nombre"]
            self.item_precio_iva = candidatos[0]["precio_compra"]

    def set_item_producto_sel(self, value: str):
        self.item_producto_sel = value
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

    def set_texto_busqueda_recepcion(self, value: str):
        self.texto_busqueda_recepcion = value

    # Setters para edición de transacción (modal)
    def set_editar_trans_numero(self, value):
        self.editar_trans_numero = str(value)

    def set_editar_trans_monto(self, value):
        try:
            self.editar_trans_monto = float(value) if value is not None else 0.0
        except (ValueError, TypeError):
            self.editar_trans_monto = 0.0

    def set_editar_trans_nombre(self, value):
        self.editar_trans_nombre = str(value)

    def set_editar_trans_correo(self, value):
        self.editar_trans_correo = str(value)

    def set_editar_trans_producto(self, value):
        self.editar_trans_producto = str(value)

    def set_editar_trans_tipo(self, value):
        self.editar_trans_tipo = str(value)

    def abrir_modal_editar_transaccion(self, transaccion_id: int):
        with rx.session() as session:
            trans = session.get(Transaccion, transaccion_id)
            if not trans:
                return
            self.editar_trans_id = transaccion_id
            self.editar_trans_numero = trans.numero_factura
            self.editar_trans_monto = trans.monto
            self.editar_trans_nombre = trans.nombre
            self.editar_trans_correo = trans.correo
            self.editar_trans_producto = trans.producto
            self.editar_trans_tipo = trans.tipo
            self.mostrar_modal_editar_transaccion = True

    def cerrar_modal_editar_transaccion(self):
        self.mostrar_modal_editar_transaccion = False
        self.editar_trans_id = 0
        self.editar_trans_numero = ""
        self.editar_trans_monto = 0.0
        self.editar_trans_nombre = ""
        self.editar_trans_correo = ""
        self.editar_trans_producto = ""
        self.editar_trans_tipo = ""

    def guardar_edicion_transaccion(self):
        if not self.editar_trans_id:
            self.error_general = "ID de transacción inválido"
            return
        self.editar_transaccion(
            self.editar_trans_id,
            tipo=self.editar_trans_tipo,
            nombre=self.editar_trans_nombre,
            correo=self.editar_trans_correo,
            numero_factura=self.editar_trans_numero,
            producto=self.editar_trans_producto,
            monto=self.editar_trans_monto,
        )
        self.cerrar_modal_editar_transaccion()

    # ================================
    # SETTERS CASCADA CLIENTE (NUEVO)
    # ================================
    def set_marca_seleccionada(self, value: str):
        """Cambia marca → resetea modelo y producto."""
        self.marca_seleccionada = value
        self.modelo_seleccionado = ""
        self.nombre_producto = ""
        self.monto_factura = 0.0

    def set_modelo_seleccionado(self, value: str):
        """Cambia modelo → resetea producto."""
        self.modelo_seleccionado = value
        self.nombre_producto = ""
        self.monto_factura = 0.0

    def set_cantidad_venta(self, value):
        """Actualiza cantidad y recalcula monto en tiempo real."""
        try:
            v = int(value) if value else 1
            self.cantidad_venta = max(1, v)
        except (ValueError, AttributeError):
            self.cantidad_venta = 1
        for p in self.productos:
            if p["nombre"] == self.nombre_producto:
                self.monto_factura = p["precio_venta"] * self.cantidad_venta
                break

    def set_stock_minimo_alerta(self, value):
        try:
            v = int(value) if value else 5
            self.stock_minimo_alerta = max(0, v)
        except (ValueError, AttributeError):
            self.stock_minimo_alerta = 5

    # ================================
    # SETTERS MI CUENTA
    # ================================
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

    # ================================
    # SETTER AUTOCOMPLETE PROVEEDOR
    # ================================
    def set_nombre_proveedor_busqueda(self, value: str):
        self.nombre_proveedor = str(value)
        self.error_nombre = ""

    def seleccionar_proveedor_sugerido(self, nombre: str):
        self.nombre_proveedor = nombre
        for t in reversed(self.historial):
            if t.get("nombre", "").lower() == nombre.lower() and t.get("tipo") == "Proveedor":
                self.correo_proveedor = t.get("correo", "")
                break

    # ======================
    # PESTAÑAS
    # ======================
    def ir_contable(self):
        self.pestana_actual = "contable"

    def ir_historial(self):
        self.pestana_actual = "historial"

    def ir_buscador(self):
        self.pestana_actual = "buscador"

    def ir_inventario(self):
        self.pestana_actual = "inventario"

    def ir_dashboard(self):
        self.pestana_actual = "dashboard"

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

    # ======================
    # INVENTARIO SETTERS
    # ======================
    def set_nombre_producto_nuevo(self, value):
        self.nombre_producto_nuevo = value
        self.error_inventario = ""

    def set_marca_producto_nuevo(self, value):
        self.marca_producto_nuevo = value

    def set_modelo_producto_nuevo(self, value):
        self.modelo_producto_nuevo = value

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

    # ======================
    # SETTERS EDICIÓN
    # ======================
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

    # ======================
    # MODAL
    # ======================
    def cerrar_modal(self):
        self.mostrar_modal = False

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

    # ======================
    # REGISTRO DE MOVIMIENTOS
    # ======================
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

    # ======================
    # DEUDAS
    # ======================
    def cargar_deudas(self):
        with rx.session() as session:
            deudas_db = session.exec(select(Deuda)).all()
            self.deudas = [
                {
                    "id": d.id,
                    "proveedor": d.proveedor,
                    "correo_proveedor": d.correo_proveedor,
                    "producto": d.producto,
                    "marca": d.marca,
                    "modelo": d.modelo,
                    "stock_pendiente": d.stock_pendiente,
                    "monto_total": d.monto_total,
                    "fecha": d.fecha,
                    "pagada": d.pagada,
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
        # Asegurar unicidad del folio generado
        try:
            if not self._validar_numero_factura_unico(folio_pago):
                folio_pago = f"{folio_pago}-{int(datetime.now().timestamp())}"
        except Exception:
            # Si por alguna razón no podemos validar (p.ej. antes de que exista la función), añadimos timestamp
            folio_pago = f"{folio_pago}-{int(datetime.now().timestamp())}"
        with rx.session() as session:
            pago = Transaccion(
                tipo="Pago deuda",
                nombre=deuda_info["proveedor"],
                correo=deuda_info["correo_proveedor"],
                numero_factura=folio_pago,
                producto=deuda_info["producto"],
                monto=monto,
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

    # ================================
    # MODAL RECEPCIÓN DE MERCANCÍA
    # ================================
    def abrir_modal_proveedor(self):
        self._limpiar_datos_modal()
        self._limpiar_errores()
        self.items_recepcion = []
        self.item_marca_recepcion = ""
        self.item_modelo_recepcion = ""
        self.item_producto_sel = ""
        self.item_cantidad = 1
        self.item_precio_iva = 0.0
        self.numero_factura = ""
        self.texto_busqueda_recepcion = ""
        self.mostrar_modal_proveedor_recepcion = True

    def cerrar_modal_proveedor_recepcion(self):
        self.mostrar_modal_proveedor_recepcion = False
        self.items_recepcion = []
        self.item_marca_recepcion = ""
        self.item_modelo_recepcion = ""
        self.item_producto_sel = ""
        self.texto_busqueda_recepcion = ""
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
                self.item_marca_recepcion = ""
                self.item_modelo_recepcion = ""
                self.item_producto_sel = ""
                self.item_cantidad = 1
                self.item_precio_iva = 0.0
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
        self.item_marca_recepcion = ""
        self.item_modelo_recepcion = ""
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
        # Validar que el número de factura sea único antes de aplicar cambios en inventario/transacción
        if not self._validar_numero_factura_unico(self.numero_factura):
            self.error_general = "El número de factura ya existe"
            return

        with rx.session() as session:
            for item in self.items_recepcion:
                prod_db = session.exec(select(Producto).where(Producto.nombre == item["nombre"])).first()
                if prod_db:
                    prod_db.stock += item["cantidad"]
                    session.add(prod_db)
            session.commit()

        with rx.session() as session:
            transaccion = Transaccion(
                tipo="Proveedor",
                nombre=self.nombre_proveedor,
                correo=self.correo_proveedor,
                numero_factura=self.numero_factura,
                producto=", ".join(i["nombre"] for i in self.items_recepcion),
                monto=total,
                fecha=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
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
                        proveedor=proveedor_snap,
                        correo_proveedor=correo_snap,
                        producto=item["nombre"],
                        marca=prod.get("marca", ""),
                        modelo=prod.get("modelo", ""),
                        stock_pendiente=item["cantidad"],
                        monto_total=monto_item,
                        fecha=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        pagada=False,
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
            f"Recepción de {proveedor_snap} — Folio: {folio_snap} — Productos: {', '.join(i['nombre'] for i in items_snap)} — Total: ${total}"
        )

    # ======================
    # VALIDACIÓN DE CORREO
    # ======================
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

    # ======================
    # ACCIONES
    # ======================
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
        self.marca_seleccionada = ""
        self.modelo_seleccionado = ""
        self.cantidad_venta = 1

    def seleccionar_producto(self, nombre: str):
        self.nombre_producto = nombre
        self.error_general = ""
        for p in self.productos:
            if p["nombre"] == nombre:
                self.monto_factura = p["precio_venta"] * self.cantidad_venta
                break

    # ======================
    # CARGA DE DATOS
    # ======================
    def cargar_historial(self):
        with rx.session() as session:
            transacciones = session.exec(select(Transaccion)).all()
            self.historial = [
                {
                    "id": t.id,
                    "tipo": t.tipo, "nombre": t.nombre, "correo": t.correo,
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

    # =====================
    # INVENTARIO ACCIONES
    # =====================
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

    def cerrar_modal_editar(self):
        self.mostrar_modal_editar = False

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

    # ======================
    # CONFIRMAR VENTA CLIENTE (con cantidad)
    # ======================
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
            self.error_general = f"Stock insuficiente — solo hay {producto['stock']} unidades disponibles"
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

        monto_total = producto["precio_venta"] * self.cantidad_venta
        self.monto_factura = monto_total

        cliente_snap = self.nombre_cliente
        producto_snap = self.nombre_producto
        factura_snap = self.numero_factura
        cantidad_snap = self.cantidad_venta
        # Validar que el número de factura sea único antes de registrar la venta
        if not self._validar_numero_factura_unico(self.numero_factura):
            self.error_general = "El número de factura ya existe"
            return

        with rx.session() as session:
            prod_db = session.get(Producto, producto["id"])
            if prod_db:
                prod_db.stock -= self.cantidad_venta
                session.add(prod_db)
                session.commit()

        self.agregar_factura_cliente()

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
        self._registrar_movimiento(
            "Venta",
            f"Venta a {cliente_snap} — Producto: {producto_snap} x{cantidad_snap} — Factura: {factura_snap} — ${monto_total}"
        )

    # ======================
    # AUTENTICACIÓN
    # ======================
    def set_login_nombre(self, value): self.login_nombre = value
    def set_login_password(self, value): self.login_password = value
    def toggle_login_password(self): self.login_mostrar_password = not self.login_mostrar_password
    def abrir_modal_recuperacion(self):
        self.mostrar_modal_recuperacion = True
        self.recuperacion_paso = 1
        self.recuperacion_correo = ""
        self.recuperacion_codigo = ""
        self.recuperacion_password_nueva = ""
        self.recuperacion_error = ""
        self.recuperacion_exito = ""

    def cerrar_modal_recuperacion(self):
        self.mostrar_modal_recuperacion = False
        self.recuperacion_paso = 1
        self.recuperacion_correo = ""
        self.recuperacion_codigo = ""
        self.recuperacion_password_nueva = ""
        self.recuperacion_error = ""
        self.recuperacion_exito = ""
    def set_reg_nombre(self, value): self.reg_nombre = value
    def set_reg_apellidos(self, value): self.reg_apellidos = value
    def set_reg_correo(self, value): self.reg_correo = value
    def set_reg_password(self, value): self.reg_password = value
    def set_reg_rol(self, value): self.reg_rol = value

    def inicializar_admin(self):
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

    def login(self):
        self.login_error = ""
        if not self.login_nombre.strip() or not self.login_password.strip():
            self.login_error = "Ingresa tu nombre y contraseña"
            return
        hash_pw = _hash_password(self.login_password)
        with rx.session() as session:
            usuario = session.exec(
                select(Usuario).where(
                    Usuario.nombre == self.login_nombre,
                    Usuario.contrasena_hash == hash_pw,
                    Usuario.activo == True,
                )
            ).first()
            if not usuario:
                self.login_error = "Nombre o contraseña incorrectos"
                return
            self.usuario_logueado = True
            self.usuario_nombre = usuario.nombre
            self.usuario_rol = usuario.rol
            self.usuario_correo = usuario.correo
            self.login_nombre = ""
            self.login_password = ""
        self.cargar_historial()
        self.cargar_inventario()
        self.cargar_movimientos()
        self.cargar_deudas()

    def logout(self):
        self.usuario_logueado = False
        self.usuario_nombre = ""
        self.usuario_rol = ""
        self.usuario_correo = ""
        self.login_nombre = ""
        self.login_password = ""
        self.login_error = ""
        self.login_mostrar_password = False

    # ================================
    # RECUPERACIÓN DE CONTRASEÑA
    # ================================
    def _enviar_correo_recuperacion(self, correo_destino: str, codigo: str, nombre_usuario: str) -> bool:
        """Envía el código de recuperación por email.
        
        Returns:
            bool: True si se envió correctamente, False si falló
        """
        if not EMAIL_CONFIG:
            print("⚠️ EMAIL_CONFIG no configurada. Email no enviado.")
            return False
        
        try:
            # Crear mensaje
            mensaje = MIMEMultipart('alternative')
            mensaje['Subject'] = "Código de Recuperación de Contraseña - StakFlow"
            mensaje['From'] = EMAIL_CONFIG.get('sender_name', 'StakFlow')
            mensaje['To'] = correo_destino
            
            # Contenido HTML del email
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
                            Si no solicitaste this recuperación, puedes ignorar este mensaje.
                        </p>
                    </div>
                </body>
            </html>
            """
            
            # Agregar versión texto
            texto = f"Código de recuperación: {codigo}\n\nEste código expira en 15 minutos."
            
            parte_texto = MIMEText(texto, 'plain')
            parte_html = MIMEText(html, 'html')
            
            mensaje.attach(parte_texto)
            mensaje.attach(parte_html)
            
            # Enviar email
            smtp_server = EMAIL_CONFIG.get('smtp_server')
            smtp_port = EMAIL_CONFIG.get('smtp_port', 587)
            sender_email = EMAIL_CONFIG.get('sender_email')
            sender_password = EMAIL_CONFIG.get('sender_password')
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Usar TLS
                server.login(sender_email, sender_password)
                server.send_message(mensaje)
            
            print(f"✓ Email enviado a {correo_destino}")
            return True
            
        except Exception as e:
            print(f"✗ Error enviando email: {e}")
            return False

    def solicitar_recuperacion_contrasena(self):
        """Genera código de recuperación y lo envía por email."""
        self.recuperacion_error = ""
        self.recuperacion_exito = ""
        if not self.recuperacion_correo.strip():
            self.recuperacion_error = "Ingresa tu correo"
            return
        
        nombre_usuario = ""
        codigo = ""
        
        with rx.session() as session:
            usuario = session.exec(select(Usuario).where(Usuario.correo == self.recuperacion_correo)).first()
            if not usuario:
                self.recuperacion_error = "No existe usuario con ese correo"
                return
            
            # Extraer datos DENTRO de la sesión
            nombre_usuario = usuario.nombre
            
            # Generar código
            codigo = ''.join(random.choices(string.digits, k=6))
            usuario.recovery_code = codigo
            session.add(usuario)
            session.commit()
        
        # Enviar email (FUERA de la sesión)
        exito = self._enviar_correo_recuperacion(
            correo_destino=self.recuperacion_correo,
            codigo=codigo,
            nombre_usuario=nombre_usuario
        )
        
        if exito:
            self.recuperacion_exito = f"Código enviado a {self.recuperacion_correo}"
        else:
            self.recuperacion_error = "Error enviando email. Contactate con soporte."
            return
        
        self.recuperacion_paso = 2

    def validar_y_cambiar_contrasena_recuperacion(self):
        """Valida código y cambia contraseña (segunda llamada desde paso 2)."""
        self.recuperacion_error = ""
        self.recuperacion_exito = ""
        if not self.recuperacion_codigo.strip() or not self.recuperacion_password_nueva.strip():
            self.recuperacion_error = "Completa código y nueva contraseña"
            return
        if len(self.recuperacion_password_nueva) < 6:
            self.recuperacion_error = "Contraseña mínimo 6 caracteres"
            return
        with rx.session() as session:
            usuario = session.exec(select(Usuario).where(Usuario.correo == self.recuperacion_correo)).first()
            if not usuario:
                self.recuperacion_error = "Usuario no encontrado"
                return
            if usuario.recovery_code != self.recuperacion_codigo:
                self.recuperacion_error = "Código incorrecto"
                return
            usuario.contrasena_hash = _hash_password(self.recuperacion_password_nueva)
            usuario.recovery_code = ""
            session.add(usuario)
            session.commit()
        self.recuperacion_exito = "Contraseña actualizada. Ya puedes iniciar sesión."
        self.recuperacion_paso = 3  # Paso confirmación

    def abrir_modal_registro(self):
        self.reg_nombre = ""
        self.reg_apellidos = ""
        self.reg_correo = ""
        self.reg_password = ""
        self.reg_rol = "empleado"
        self.reg_error = ""
        self.reg_exito = ""
        self.mostrar_modal_registro = True

    def cerrar_modal_registro(self):
        self.mostrar_modal_registro = False

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
            )
            session.add(nuevo)
            session.commit()
        self.reg_exito = f"Usuario '{self.reg_nombre}' creado como {self.reg_rol}"
        self.reg_nombre = ""
        self.reg_apellidos = ""
        self.reg_correo = ""
        self.reg_password = ""
        self.cargar_usuarios()

    def cargar_usuarios(self):
        with rx.session() as session:
            usuarios = session.exec(select(Usuario)).all()
            self.usuarios_lista = [
                {"id": u.id, "nombre": u.nombre, "apellidos": u.apellidos,
                 "correo": u.correo, "rol": u.rol, "activo": u.activo}
                for u in usuarios
            ]

    def desactivar_usuario(self, usuario_id: int):
        with rx.session() as session:
            usuario = session.get(Usuario, usuario_id)
            if usuario and usuario.correo != "admin@dominio.com":
                usuario.activo = not usuario.activo
                session.add(usuario)
                session.commit()
        self.cargar_usuarios()

    # ================================
    # CAMBIAR CONTRASEÑA
    # ================================
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
        hash_actual = _hash_password(self.cuenta_pass_actual)
        with rx.session() as session:
            usuario = session.exec(select(Usuario).where(Usuario.nombre == self.usuario_nombre)).first()
            if not usuario:
                self.cuenta_error = "Usuario no encontrado"
                return
            if usuario.contrasena_hash != hash_actual:
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

    # =============================
    # VALIDACIÓN Y EDICIÓN DE TRANSACCIONES
    # =============================
    def _validar_numero_factura_unico(self, numero_factura: str) -> bool:
        """Devuelve True si no existe una transacción con ese número de factura."""
        if not numero_factura or not str(numero_factura).strip():
            return False
        try:
            with rx.session() as session:
                existente = session.exec(select(Transaccion).where(Transaccion.numero_factura == numero_factura)).first()
                return existente is None
        except Exception:
            # Si no se puede comprobar (por ejemplo en estado inconsistente), conservadoramente False
            return False

    def editar_transaccion(self, transaccion_id: int, *, tipo: str = None, nombre: str = None,
                           correo: str = None, numero_factura: str = None,
                           producto: str = None, monto: float = None):
        """Editar una transacción. Si se cambia el número de factura valida unicidad."""
        self.error_general = ""
        with rx.session() as session:
            trans = session.get(Transaccion, transaccion_id)
            if not trans:
                self.error_general = "Transacción no encontrada"
                return
            if numero_factura and numero_factura != trans.numero_factura:
                if not self._validar_numero_factura_unico(numero_factura):
                    self.error_general = "El número de factura ya existe"
                    return
                trans.numero_factura = numero_factura
            if tipo is not None:
                trans.tipo = tipo
            if nombre is not None:
                trans.nombre = nombre
            if correo is not None:
                trans.correo = correo
            if producto is not None:
                trans.producto = producto
            if monto is not None:
                try:
                    trans.monto = float(monto)
                except (ValueError, TypeError):
                    pass
            trans.fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            session.add(trans)
            session.commit()

        self.cargar_historial()
        self._registrar_movimiento("Transacción editada", f"ID {transaccion_id} editada por {self.usuario_nombre}")

    def cancelar_transaccion(self, transaccion_id: int):
        """Anula (elimina) una transacción. Intenta revertir efectos simples como restituir stock en ventas."""
        self.error_general = ""
        with rx.session() as session:
            trans = session.get(Transaccion, transaccion_id)
            if not trans:
                self.error_general = "Transacción no encontrada"
                return
            # Revertir efectos simples: venta -> devolver stock
            if trans.tipo == "Cliente":
                try:
                    prod = session.exec(select(Producto).where(Producto.nombre == trans.producto)).first()
                    if prod:
                        prod.stock += 1
                        session.add(prod)
                except Exception:
                    pass
            # Eliminar referencias en mapas de facturas si existen
            try:
                if trans.tipo == "Cliente" and trans.numero_factura in self.facturas_clientes:
                    del self.facturas_clientes[trans.numero_factura]
                if trans.tipo in ("Proveedor", "Pago deuda") and trans.numero_factura in self.facturas_proveedores:
                    del self.facturas_proveedores[trans.numero_factura]
            except Exception:
                pass
            session.delete(trans)
            session.commit()

        self.cargar_historial()
        self.cargar_inventario()
        self._registrar_movimiento("Transacción anulada", f"ID {transaccion_id} anulada por {self.usuario_nombre}")

    # ======================
    # ON LOAD
    # ======================
    def on_load(self):
        self.inicializar_admin()
        self.cargar_historial()
        self.cargar_inventario()
        self.cargar_movimientos()
        self.cargar_deudas()

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
        """Total = precio × cantidad, se actualiza en tiempo real."""
        return self.precio_producto_seleccionado * self.cantidad_venta

    @rx.var
    def stock_producto_seleccionado(self) -> int:
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
        if not self.texto_busqueda_producto:
            return self.productos
        texto = self.texto_busqueda_producto.lower()
        return [
            p for p in self.productos
            if texto in p["nombre"].lower() or texto == str(p["id"])
        ]

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

    # ================================
    # VARS CASCADA CLIENTE
    # ================================
    @rx.var
    def marcas_disponibles(self) -> list[str]:
        return sorted(list({p["marca"] for p in self.productos if p["stock"] > 0 and p["marca"]}))

    @rx.var
    def modelos_por_marca(self) -> list[str]:
        return sorted(list({
            p["modelo"] for p in self.productos
            if p["marca"] == self.marca_seleccionada and p["stock"] > 0 and p["modelo"]
        }))

    @rx.var
    def nombres_productos_filtrados_por_modelo(self) -> list[str]:
        return [
            p["nombre"] for p in self.productos
            if p["marca"] == self.marca_seleccionada
            and p["modelo"] == self.modelo_seleccionado
            and p["stock"] > 0
        ]

    # ================================
    # VARS CASCADA RECEPCIÓN
    # ================================
    @rx.var
    def marcas_recepcion(self) -> list[str]:
        return sorted(list({p["marca"] for p in self.productos if p["marca"]}))

    @rx.var
    def modelos_recepcion(self) -> list[str]:
        return sorted(list({
            p["modelo"] for p in self.productos
            if p["marca"] == self.item_marca_recepcion and p["modelo"]
        }))

    @rx.var
    def productos_recepcion_filtrados(self) -> list[str]:
        return [
            p["nombre"] for p in self.productos
            if p["marca"] == self.item_marca_recepcion
            and p["modelo"] == self.item_modelo_recepcion
        ]

    @rx.var
    def productos_con_stock_filtrados(self) -> list[dict]:
        if not self.nombre_producto.strip():
            return []
        texto = self.nombre_producto.strip().lower()
        return [p for p in self.productos if texto in p["nombre"].lower() and p["stock"] > 0]

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
    def historial_filtrado_completo(self) -> list[dict]:
        resultado = []
        for t in self.historial:
            resultado.append({
                "id": t.get("id", 0),
                "tipo": t["tipo"],
                "nombre": t.get("nombre", ""),
                "correo": t.get("correo", ""),
                "numero_factura": t.get("numero_factura", ""),
                "producto": t.get("producto", ""),
                "monto": t.get("monto", 0),
                "descripcion": f"{t.get('nombre','')} — {t.get('producto','')} — Factura: {t.get('numero_factura','')} — ${t.get('monto',0)}",
                "fecha": t["fecha"],
                "usuario": t.get("usuario", ""),
            })
        for m in self.movimientos:
            resultado.append({
                "tipo": m["tipo"], "descripcion": m["descripcion"],
                "fecha": m["fecha"], "usuario": m.get("usuario", ""),
            })
        return sorted(resultado, key=lambda x: x["fecha"], reverse=True)

    @rx.var
    def historial_filtrado_y_paginado(self) -> list[dict]:
        """Aplica filtros de texto, fecha, tipo y usuario, luego pagina."""
        filtrados = self.historial_filtrado_completo
        if self.filtro_tipo_historial.strip():
            filtrados = [h for h in filtrados if h.get("tipo", "").lower() == self.filtro_tipo_historial.lower()]
        if self.filtro_usuario_historial.strip():
            filtrados = [h for h in filtrados if h.get("usuario", "").lower() == self.filtro_usuario_historial.lower()]
        if self.filtro_fecha_inicio.strip():
            try:
                fecha_inicio = datetime.strptime(self.filtro_fecha_inicio, "%Y-%m-%d").date()
                filtrados = [h for h in filtrados if datetime.strptime(h.get("fecha", "01/01/2000 00:00:00"), "%d/%m/%Y %H:%M:%S").date() >= fecha_inicio]
            except:
                pass
        if self.filtro_fecha_fin.strip():
            try:
                fecha_fin = datetime.strptime(self.filtro_fecha_fin, "%Y-%m-%d").date()
                filtrados = [h for h in filtrados if datetime.strptime(h.get("fecha", "31/12/2099 23:59:59"), "%d/%m/%Y %H:%M:%S").date() <= fecha_fin]
            except:
                pass
        total_paginas = max(1, (len(filtrados) + self.items_por_pagina - 1) // self.items_por_pagina)
        if self.pagina_actual > total_paginas:
            self.pagina_actual = total_paginas
        inicio = (self.pagina_actual - 1) * self.items_por_pagina
        fin = inicio + self.items_por_pagina
        return filtrados[inicio:fin]

    @rx.var
    def total_paginas_historial(self) -> int:
        """Calcula total de páginas."""
        filtrados = self.historial_filtrado_completo
        if self.filtro_tipo_historial.strip():
            filtrados = [h for h in filtrados if h.get("tipo", "").lower() == self.filtro_tipo_historial.lower()]
        if self.filtro_usuario_historial.strip():
            filtrados = [h for h in filtrados if h.get("usuario", "").lower() == self.filtro_usuario_historial.lower()]
        if self.filtro_fecha_inicio.strip():
            try:
                fecha_inicio = datetime.strptime(self.filtro_fecha_inicio, "%Y-%m-%d").date()
                filtrados = [h for h in filtrados if datetime.strptime(h.get("fecha", "01/01/2000 00:00:00"), "%d/%m/%Y %H:%M:%S").date() >= fecha_inicio]
            except:
                pass
        if self.filtro_fecha_fin.strip():
            try:
                fecha_fin = datetime.strptime(self.filtro_fecha_fin, "%Y-%m-%d").date()
                filtrados = [h for h in filtrados if datetime.strptime(h.get("fecha", "31/12/2099 23:59:59"), "%d/%m/%Y %H:%M:%S").date() <= fecha_fin]
            except:
                pass
        return max(1, (len(filtrados) + self.items_por_pagina - 1) // self.items_por_pagina)

    @rx.var
    def tipos_disponibles_historial(self) -> list[str]:
        return sorted(list({h.get("tipo", "") for h in self.historial_filtrado_completo if h.get("tipo", "")}))

    @rx.var
    def usuarios_disponibles_historial(self) -> list[str]:
        return sorted(list({h.get("usuario", "") for h in self.historial_filtrado_completo if h.get("usuario", "")}))

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

    # ================================
    # VARS DEUDAS
    # ================================
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