# $======================$
# ||BACKEND DEL SISTEMA ||
# $======================$

# Importamos reflex porque es importante
import reflex as rx 
import json #para crear el archivo .json
import os # permite manipular archivos, gestionar directorios, controlar procesos y acceder a variables de entorno
from datetime import datetime #Para el registro de las fechas


class ContableState(rx.State):
    # ======================
    # VARIABLES A UTILIZAR
    # ======================
    # Variables de los datos
    saldo_inicial: float = 0.0

    facturas_clientes: dict[str, float] = {}
    facturas_proveedores: dict[str, float] = {}

    numero_factura: str = ""
    nombre_producto: str = ""
    monto_factura: float = 0.0

    # Login variables
    nombre_cliente: str = ""
    nombre_proveedor: str = ""
    correo_cliente: str = ""
    correo_proveedor: str = ""

    # Modal variables
    mostrar_modal: bool = False
    tipo_modal: str = " "

    # Errores variables
    error_nombre: str = ""
    error_correo: str = ""
    error_general: str = ""

    # Historial variable
    historial: list[dict] = []

    # pestaña actual
    pestana_actual: str = "dashboard"

    # Base de datos
    archivo_db = "historial.json"

    #Busqueda
    texto_busqueda: str = ""

    #Variables de inventario
    productos: list[dict] = []

    nombre_producto_nuevo: str = ""
    stock_inicial: int = 0
    precio_compra: float = 0.0
    precio_venta: float = 0.0

    # variable delarchivo json inventario
    archivo_inventario = "inventario.json"

    # variable del buscador inventario 
    texto_busqueda_producto: str = ""


# ================================
# DATOS PARA GRAFICA FINANCIERA
# ================================
    grafica_financiera: list[dict] = [
    {"mes": "Enero", "ingresos": 12000, "egresos": 8000},
    {"mes": "Febrero", "ingresos": 15000, "egresos": 9000},
    {"mes": "Marzo", "ingresos": 10000, "egresos": 7000},
    ]


    # ======================
    # SETTERS
    # ======================
    #Setters de datos
    def set_saldo_inicial(self, value):
        self.saldo_inicial = float(value)

    def set_numero_factura(self, value):
        self.numero_factura = value

    def set_nombre_producto(self, value):
        self.nombre_producto = value

    def set_monto_factura(self, value):
        self.monto_factura = float(value)

    #Setters del login
    def set_nombre_cliente(self, value):
        self.nombre_cliente = str(value)

    def set_nombre_proovedor(self, value):
        self.nombre_proveedor = str(value)

    def set_correo_cliente(self, value):
        self.correo_cliente = str(value)

    def set_correo_proovedor(self, value):
        self.correo_proveedor = str(value)
    
    #Setter de busqueda
    def set_texto_busqueda(self, value):
        self.texto_busqueda = value

    #Setter buscador inventario
    def set_texto_busqueda_producto(self, value):
        self.texto_busqueda_producto = value


    # ======================
    # PESTAÑAS
    # Lleva a las pestañas cuandao presionas unn boton
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


    # ======================
    # INVENTARIO SETTERS   ||
    # ======================
    def set_nombre_producto_nuevo(self, value):
        self.nombre_producto_nuevo = value

    def set_stock_inicial(self, value):
        self.stock_inicial = int(value) if value else 0

    def set_precio_compra(self, value):
        self.precio_compra = float(value) if value else 0.0

    def set_precio_venta(self, value):
        self.precio_venta = float(value) if value else 0.0


    # ======================
    # MODAL (Ventana que se abre al presionar "ingresar cliente" o "ingresar proveedor")
    # ======================
    def abrir_modal_cliente(self):
        self.tipo_modal = "cliente"
        self._limpiar_datos_modal()
        self._limpiar_errores()
        self.mostrar_modal = True

    def abrir_modal_proveedor(self):
        self.tipo_modal = "proveedor"
        self._limpiar_datos_modal()
        self._limpiar_errores()
        self.mostrar_modal = True

    def cerrar_modal(self):
        self.mostrar_modal = False

    def _limpiar_errores(self):
        self.error_nombre = ""
        self.error_correo = ""
        self.error_general = ""

    def _limpiar_datos_modal(self):
        self.nombre_cliente = ""
        self.correo_cliente = ""
        self.nombre_proveedor = ""
        self.correo_proveedor = ""


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


    # ======================
    # JSON BASE DE DATOS
    # ======================
    def cargar_historial(self):
        if os.path.exists(self.archivo_db):
            with open(self.archivo_db, "r", encoding="utf-8") as f:
                self.historial = json.load(f)

    def guardar_historial(self):
        with open(self.archivo_db, "w", encoding="utf-8") as f:
            json.dump(self.historial, f, indent=4, ensure_ascii=False)


    # =====================
    # INVENTARIO JSON
    # =====================
    def cargar_inventario(self):
        if os.path.exists(self.archivo_inventario):
            with open(self.archivo_inventario, "r", encoding="utf-8") as f:
                self.productos = json.load(f)

    def guardar_inventario(self):
        with open(self.archivo_inventario, "w", encoding="utf-8") as f:
            json.dump(self.productos, f, indent=4, ensure_ascii=False)

    def generar_id_producto(self):
        if not self.productos:
            return 1
        return max(p["id"] for p in self.productos) + 1

    def on_load(self):
        self.cargar_historial()
        self.cargar_inventario()


    # =====================
    # INVENTARIO
    # =====================
    def agregar_producto(self):

        if self.nombre_producto_nuevo.strip() == "":
            return

        for p in self.productos:
            if p["nombre"].lower() == self.nombre_producto_nuevo.lower():
                return

        nuevo = {
            "id": self.generar_id_producto(),
            "nombre": self.nombre_producto_nuevo,
            "stock": self.stock_inicial,
            "precio_compra": self.precio_compra,
            "precio_venta": self.precio_venta,
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.productos.append(nuevo)
        self.guardar_inventario()

        self.nombre_producto_nuevo = ""
        self.stock_inicial = 0
        self.precio_compra = 0
        self.precio_venta = 0

    def obtener_producto(self, nombre):
        for p in self.productos:
            if p["nombre"] == nombre:
                return p
        return None


    # ======================
    # CONFIRMAR MODAL 
    # ======================
    def confirmar_modal(self):
        self._limpiar_errores()
        hay_error = False

        producto = self.obtener_producto(self.nombre_producto)

        #Verifica si el producto fue previamente registrado en el inventario
        if not producto:
            self.error_general = "El producto no existe en inventario"
            return

        if self.tipo_modal == "cliente":

            # Si el producto aun se mantiene en el inventario
            if producto["stock"] <= 0:
                self.error_general = "Sin stock disponible"
                return

            #Verifica si el campo del nombre del cliente  no esta lleno
            if not self.nombre_cliente.strip():
                self.error_nombre = "El nombre del cliente es obligatorio"
                hay_error = True

            #Verifica si el campo del correo del cliente  no esta lleno
            if not self.correo_cliente.strip():
                self.error_correo = "El correo del cliente es obligatorio"
                hay_error = True
            
            #Verifica si el campo del numero de factura del cliente  no esta lleno
            if not self.numero_factura:
                self.error_general = "Debe ingresar número de factura"
                hay_error = True

            if hay_error:
                return
            
            #Resta un stock cuando el producto el movimiento ya ha sido registrado por el cliente
            producto["stock"] -= 1
            self.guardar_inventario()

            self.agregar_factura_cliente()

            # Agrega un registro en el .json
            self.historial.append({
                "tipo": "Cliente",
                "nombre": self.nombre_cliente,
                "correo": self.correo_cliente,
                "numero_factura": self.numero_factura,
                "producto": self.nombre_producto,
                "monto": self.monto_factura,
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            })

        elif self.tipo_modal == "proveedor":
            
            #Verifica si el campo del nombre del proveedor  no esta lleno
            if not self.nombre_proveedor.strip():
                self.error_nombre = "El nombre del proveedor es obligatorio"
                hay_error = True

            #Verifica si el campo del correo del proveedor  no esta lleno
            if not self.correo_proveedor.strip():
                self.error_correo = "El correo del proveedor es obligatorio"
                hay_error = True
            
            #Verifica si el numero de la factura no esta lleno
            if not self.numero_factura:
                self.error_general = "Debe ingresar número de factura"
                hay_error = True

            if hay_error:
                return

            ##Suma un stock cuando el producto el movimiento ya ha sido registrado por el proveedor
            producto["stock"] += 1
            self.guardar_inventario()

            self.agregar_factura_proveedor()

            # Agrega un registro "proveedor" en el .json
            self.historial.append({
                "tipo": "Proveedor",
                "nombre": self.nombre_proveedor,
                "correo": self.correo_proveedor,
                "numero_factura": self.numero_factura,
                "producto": self.nombre_producto,
                "monto": self.monto_factura,
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            })

        self.guardar_historial()
        self._limpiar_datos_modal()
        self._limpiar()
        self.cerrar_modal()


    # ======================
    # VARIABLES COMPUTADAS FINANCIERAS
    # ======================

    #Suma los ingresos registrados
    @rx.var
    def total_ingresos(self) -> float:
        return sum(self.facturas_clientes.values())

    #Suma el total de ingresos registrados
    @rx.var
    def total_egresos(self) -> float:
        return sum(self.facturas_proveedores.values())
    
    #Resta del saldo inicial cuando se registra un egreso
    @rx.var
    def saldo_total(self) -> float:
        return self.saldo_inicial + self.total_ingresos - self.total_egresos


    # ======================
    # MÉTRICAS DASHBOARD
    # ======================
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
        return [p for p in self.productos if p["stock"] <= 5]


    # ======================
    # DATOS PARA GRÁFICA DASHBOARD
    # ======================
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
                resumen[mes] = {
                    "mes": mes,
                    "ingresos": 0,
                    "egresos": 0,
                }

            if tipo == "Cliente":
                resumen[mes]["ingresos"] += monto
            elif tipo == "Proveedor":
                resumen[mes]["egresos"] += monto

        resultado = []
        for mes in sorted(resumen.keys()):
            ingresos = resumen[mes]["ingresos"]
            egresos = resumen[mes]["egresos"]
            resultado.append({
                "mes": mes,
                "ingresos": ingresos,
                "egresos": egresos,
                "balance": ingresos - egresos
            })

        return resultado


    # ======================
    # BUSQUEDA ROBUSTA
    # ======================
    @rx.var
    def historial_filtrado(self) -> list[dict]:

        if not self.texto_busqueda.strip():
            return self.historial

        texto = self.texto_busqueda.strip().lower()
        resultados = []

        for r in self.historial:
            nombre = str(r.get("nombre", "")).lower()
            factura = str(r.get("numero_factura", "")).lower()
            fecha = str(r.get("fecha", "")).lower()

            if texto in nombre or texto in factura or texto in fecha:
                resultados.append(r)

        return resultados


    # ======================
    # BUSQUEDA INVENTARIO
    # ======================
    @rx.var
    def productos_filtrados(self) -> list[dict]:

        if not self.texto_busqueda_producto:
            return self.productos

        texto = self.texto_busqueda_producto.lower()

        return [
            p for p in self.productos
            if texto in p["nombre"].lower()
            or texto == str(p["id"])
        ]
