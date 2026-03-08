import reflex as rx
from PROYECTO_ED_APP.state import ContableState
from PROYECTO_ED_APP.componentes.tabla_productos_y_stock import tabla_productos_stock
from PROYECTO_ED_APP.componentes.sidebar import sidebar

def vista_contable() -> rx.Component:
    return rx.box(
        sidebar(),

        rx.box(
            rx.center(
                rx.hstack(
                    # COLUMNA IZQUIERDA
                    rx.vstack(
                        rx.heading(
                            "Sistema Contable",
                            size="9",
                            weight="bold",
                            margin_bottom="0.5em",
                            color="#FFFFFF"
                        ),

                        rx.tabs.root(
                            # TABS HEADER
                            rx.tabs.list(
                                rx.tabs.trigger(
                                    rx.hstack(
                                        rx.icon(tag="wallet", size=14),
                                        rx.text("Saldo", size="2"),
                                        spacing="1",
                                        align="center",
                                    ),
                                    value="saldo",
                                    style={
                                        "cursor": "pointer",
                                        "padding": "0.5em 1.2em",
                                        "border_radius": "lg",
                                        "color": "#A0AEC0",
                                        "_selected": {
                                            "color": "#FFFFFF",
                                            "bg": "#2D3748",
                                        },
                                    },
                                ),
                                rx.tabs.trigger(
                                    rx.hstack(
                                        rx.icon(tag="user", size=14),
                                        rx.text("Cliente", size="2"),
                                        spacing="1",
                                        align="center",
                                    ),
                                    value="cliente",
                                    style={
                                        "cursor": "pointer",
                                        "padding": "0.5em 1.2em",
                                        "border_radius": "lg",
                                        "color": "#A0AEC0",
                                        "_selected": {
                                            "color": "#FFFFFF",
                                            "bg": "#2D3748",
                                        },
                                    },
                                ),
                                rx.tabs.trigger(
                                    rx.hstack(
                                        rx.icon(tag="truck", size=14),
                                        rx.text("Proveedor", size="2"),
                                        spacing="1",
                                        align="center",
                                    ),
                                    value="proveedor",
                                    style={
                                        "cursor": "pointer",
                                        "padding": "0.5em 1.2em",
                                        "border_radius": "lg",
                                        "color": "#A0AEC0",
                                        "_selected": {
                                            "color": "#FFFFFF",
                                            "bg": "#2D3748",
                                        },
                                    },
                                ),
                                bg="#1A202C",
                                border="1px solid #2D3748",
                                border_radius="xl",
                                padding="0.3em",
                                width="100%",
                            ),

                            # ==================
                            # TAB: SALDO
                            # ==================
                            rx.tabs.content(
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.icon(tag="wallet", size=18, color="#A0AEC0"),
                                            rx.text("Saldo Inicial", weight="bold", color="#E2E8F0"),
                                            spacing="2",
                                        ),
                                        rx.input(
                                            placeholder="0",
                                            type="number",
                                            on_change=ContableState.set_saldo_inicial,
                                            width="100%",
                                            variant="surface",
                                            bg="#2D3748",
                                            color="#FFFFFF",
                                            border="none",
                                            style={"_hover": {"bg": "#1A202C"}},
                                        ),
                                        rx.divider(color_scheme="gray", opacity="0.2"),
                                        rx.grid(
                                            rx.vstack(
                                                rx.text("Ingresos", size="2", color="#A0AEC0"),
                                                rx.text(
                                                    f"${ContableState.total_ingresos}",
                                                    color="#48BB78", weight="bold", size="4"
                                                ),
                                                align_items="center",
                                            ),
                                            rx.vstack(
                                                rx.text("Egresos", size="2", color="#A0AEC0"),
                                                rx.text(
                                                    f"${ContableState.total_egresos}",
                                                    color="#F56565", weight="bold", size="4"
                                                ),
                                                align_items="center",
                                            ),
                                            rx.vstack(
                                                rx.text("Saldo Total", size="2", color="#A0AEC0"),
                                                rx.text(
                                                    f"${ContableState.saldo_total}",
                                                    color="#FFFFFF", weight="bold", size="4",
                                                ),
                                                align_items="center",
                                            ),
                                            columns="3",
                                            width="100%",
                                            padding_top="0.5em",
                                        ),
                                        align="start",
                                        width="100%",
                                        spacing="4",
                                    ),
                                    padding="1.5em",
                                    bg="#1A202C",
                                    border_radius="xl",
                                    border="1px solid #2D3748",
                                    width="100%",
                                ),
                                value="saldo",
                                width="100%",
                            ),

                            # ==================
                            # TAB: CLIENTE
                            # ==================
                            rx.tabs.content(
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.icon(tag="file-text", size=18, color="#A0AEC0"),
                                            rx.text("Factura de Cliente", weight="bold", color="#E2E8F0"),
                                            spacing="2",
                                        ),
                                        rx.input(
                                            placeholder="Número de factura",
                                            value=ContableState.numero_factura,
                                            on_change=ContableState.set_numero_factura,
                                            width="100%",
                                            bg="#2D3748",
                                            color="#FFFFFF",
                                            border="none",
                                            style={"_hover": {"bg": "#1A202C"}},
                                        ),

                                        # Seleccionar Producto
                                        rx.select(
                                            ContableState.nombres_productos_con_stock,
                                            placeholder="Seleccionar producto...",
                                            on_change=ContableState.seleccionar_producto,
                                            value=ContableState.nombre_producto,
                                            bg="#2D3748",
                                            color="#FFFFFF",
                                            border="none",
                                            width="100%",
                                            style={"_hover": {"bg": "#1A202C"}},
                                        ),

                                        # Seleccionar Marca
                                        rx.select(
                                            ContableState.marcas_disponibles,
                                            placeholder="Seleccionar marca...",
                                            on_change=ContableState.set_marca_seleccionada,
                                            value=ContableState.marca_seleccionada,
                                            bg="#2D3748",
                                            color="#FFFFFF",
                                            border="none",
                                            width="100%",
                                            style={"_hover": {"bg": "#1A202C"}},
                                        ),

                                        # Seleccionar Modelo
                                        rx.select(
                                            ContableState.modelos_por_marca,
                                            placeholder="Seleccionar modelo...",
                                            on_change=ContableState.set_modelo_seleccionado,
                                            value=ContableState.modelo_seleccionado,
                                            bg="#2D3748",
                                            color="#FFFFFF",
                                            border="none",
                                            width="100%",
                                            style={"_hover": {"bg": "#1A202C"}},
                                        ),

                                        # PRECIO AUTOMÁTICO
                                        rx.cond(
                                            ContableState.nombre_producto != "",
                                            rx.box(
                                                rx.hstack(
                                                    rx.icon(tag="tag", size=14, color="#48BB78"),
                                                    rx.text("Precio de venta:", color="#A0AEC0", size="2"),
                                                    rx.text(
                                                        f"${ContableState.precio_producto_seleccionado}",
                                                        color="#48BB78",
                                                        weight="bold",
                                                        size="3",
                                                    ),
                                                    spacing="2",
                                                    align="center",
                                                ),
                                                padding="0.6em 1em",
                                                bg="#1A3A2A",
                                                border="1px solid #2F855A",
                                                border_radius="lg",
                                                width="100%",
                                            ),
                                            rx.box(
                                                rx.hstack(
                                                    rx.icon(tag="tag", size=14, color="#4A5568"),
                                                    rx.text(
                                                        "Selecciona un producto para ver el precio",
                                                        color="#4A5568",
                                                        size="2",
                                                    ),
                                                    spacing="2",
                                                    align="center",
                                                ),
                                                padding="0.6em 1em",
                                                bg="#1A202C",
                                                border="1px solid #2D3748",
                                                border_radius="lg",
                                                width="100%",
                                            ),
                                        ),

                                        rx.divider(color_scheme="gray", opacity="0.2"),
                                        rx.text("Datos del Cliente", weight="bold", color="#A0AEC0", size="2"),
                                        rx.input(
                                            placeholder="Nombre del cliente",
                                            value=ContableState.nombre_cliente,
                                            on_change=ContableState.set_nombre_cliente,
                                            width="100%",
                                            bg="#2D3748",
                                            color="#FFFFFF",
                                            border=rx.cond(
                                                ContableState.error_nombre != "",
                                                "1px solid #F56565", "none"
                                            ),
                                            style={"_hover": {"bg": "#1A202C"}},
                                        ),
                                        rx.cond(
                                            ContableState.error_nombre != "",
                                            rx.hstack(
                                                rx.icon(tag="circle-alert", size=12, color="#F56565"),
                                                rx.text(ContableState.error_nombre, color="#F56565", size="1"),
                                                spacing="1",
                                            ),
                                        ),
                                        rx.input(
                                            placeholder="Correo (ejemplo@dominio.com)",
                                            value=ContableState.correo_cliente,
                                            on_change=ContableState.validar_correo_cliente_live,
                                            on_blur=ContableState.validar_correo_cliente_live,
                                            width="100%",
                                            bg="#2D3748",
                                            color="#FFFFFF",
                                            border=rx.cond(
                                                ContableState.error_correo != "",
                                                "1px solid #F56565", "none"
                                            ),
                                            style={"_hover": {"bg": "#1A202C"}},
                                        ),
                                        rx.cond(
                                            ContableState.error_correo != "",
                                            rx.hstack(
                                                rx.icon(tag="circle-alert", size=12, color="#F56565"),
                                                rx.text(ContableState.error_correo, color="#F56565", size="1"),
                                                spacing="1",
                                            ),
                                        ),
                                        rx.cond(
                                            ContableState.error_general != "",
                                            rx.hstack(
                                                rx.icon(tag="circle-alert", size=12, color="#F56565"),
                                                rx.text(
                                                    ContableState.error_general,
                                                    color="#F56565", size="2", weight="bold",
                                                ),
                                                spacing="1",
                                            ),
                                        ),
                                        rx.button(
                                            rx.icon(tag="user-check", size=16),
                                            "Confirmar Venta",
                                            on_click=ContableState.confirmar_modal,
                                            bg="#38A169",
                                            color="#FFFFFF",
                                            width="100%",
                                            _hover={
                                                "transform": "translateY(-3px)",
                                                "transition": "all 0.2s ease-in-out",
                                                "box_shadow": "0 8px 20px #38A16944",
                                                "bg": "#2F855A",
                                            },
                                        ),
                                        spacing="3",
                                        width="100%",
                                    ),
                                    padding="1.5em",
                                    bg="#1A202C",
                                    border_radius="xl",
                                    border="1px solid #2D3748",
                                    width="100%",
                                ),
                                value="cliente",
                                width="100%",
                            ),

                            # ==================
                            # TAB: PROVEEDOR
                            # ==================
                            rx.tabs.content(
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.icon(tag="truck", size=18, color="#A0AEC0"),
                                            rx.text("Recepción de Mercancía", weight="bold", color="#E2E8F0"),
                                            spacing="2",
                                        ),
                                        rx.text(
                                            "Registra la entrada de productos de un proveedor.",
                                            color="#718096",
                                            size="2",
                                        ),
                                        rx.button(
                                            rx.icon(tag="truck", size=16),
                                            "Abrir Recepción de Mercancía",
                                            on_click=ContableState.abrir_modal_proveedor,
                                            bg="#E53E3E",
                                            color="#FFFFFF",
                                            width="100%",
                                            size="3",
                                            _hover={
                                                "transform": "translateY(-3px)",
                                                "transition": "all 0.2s ease-in-out",
                                                "box_shadow": "0 8px 20px #E53E3E44",
                                                "bg": "#C53030",
                                            },
                                        ),
                                        spacing="4",
                                        width="100%",
                                    ),
                                    padding="1.5em",
                                    bg="#1A202C",
                                    border_radius="xl",
                                    border="1px solid #2D3748",
                                    width="100%",
                                ),
                                value="proveedor",
                                width="100%",
                            ),

                            default_value="saldo",
                            width="100%",
                        ),

                        width="420px",
                        spacing="4",
                        align_items="stretch",
                    ),

                    # COLUMNA DERECHA: TABLA
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.icon(tag="package", size=22, color="#A0AEC0"),
                                rx.heading("Inventario y Stock", size="5", color="#E2E8F0"),
                                spacing="3",
                            ),
                            rx.divider(color_scheme="gray", opacity="0.2"),
                            rx.box(
                                tabla_productos_stock(),
                                width="100%",
                                overflow_x="auto"
                            ),
                            width="100%",
                            spacing="4",
                        ),
                        padding="2em",
                        bg="#1A202C",
                        border_radius="20px",
                        border="1px solid #2D3748",
                        width="480px",
                        height="fit-content",
                        margin_top="7em",
                    ),
                    spacing="9",
                    align_items="start",
                    justify="center",
                    width="100%",
                    max_width="1100px",
                ),
            ),
            padding_left="250px",
            width="100%",
        ),

        # ================================
        # MODAL RECEPCIÓN DE MERCANCÍA
        # ================================
        rx.cond(
            ContableState.mostrar_modal_proveedor_recepcion,
            rx.center(
                rx.box(
                    rx.vstack(

                        # HEADER
                        rx.hstack(
                            rx.hstack(
                                rx.icon(tag="truck", size=22, color="#48BB78"),
                                rx.heading("Recepción de Mercancía", size="5", color="#FFFFFF"),
                                spacing="2",
                                align="center",
                            ),
                            rx.spacer(),
                            rx.button(
                                rx.icon(tag="x", size=16),
                                on_click=ContableState.cerrar_modal_proveedor_recepcion,
                                variant="ghost",
                                color="#718096",
                                _hover={"color": "#FFFFFF"},
                                size="1",
                            ),
                            width="100%",
                            align="center",
                            padding_bottom="1em",
                            border_bottom="1px solid #2D3748",
                        ),

                        # DATOS DEL PROVEEDOR
                        rx.box(
                            rx.vstack(
                                rx.text("Datos del Proveedor", weight="bold", color="#A0AEC0", size="2"),
                                rx.hstack(
                                    rx.vstack(
                                        rx.text("Nombre", color="#718096", size="1"),
                                        rx.input(
                                            placeholder="Nombre del proveedor",
                                            value=ContableState.nombre_proveedor,
                                            on_change=ContableState.set_nombre_proovedor,
                                            bg="#2D3748", color="#FFFFFF",
                                            border=rx.cond(
                                                ContableState.error_nombre != "",
                                                "1px solid #F56565", "none"
                                            ),
                                            width="100%",
                                        ),
                                        rx.cond(
                                            ContableState.error_nombre != "",
                                            rx.text(ContableState.error_nombre, color="#F56565", size="1"),
                                        ),
                                        width="100%", spacing="1",
                                    ),
                                    rx.vstack(
                                        rx.text("Correo", color="#718096", size="1"),
                                        rx.input(
                                            placeholder="correo@dominio.com",
                                            value=ContableState.correo_proveedor,
                                            on_change=ContableState.validar_correo_proveedor_live,
                                            bg="#2D3748", color="#FFFFFF",
                                            border=rx.cond(
                                                ContableState.error_correo != "",
                                                "1px solid #F56565", "none"
                                            ),
                                            width="100%",
                                        ),
                                        rx.cond(
                                            ContableState.error_correo != "",
                                            rx.text(ContableState.error_correo, color="#F56565", size="1"),
                                        ),
                                        width="100%", spacing="1",
                                    ),
                                    rx.vstack(
                                        rx.text("Folio / Remisión", color="#718096", size="1"),
                                        rx.input(
                                            placeholder="N° de factura",
                                            value=ContableState.numero_factura,
                                            on_change=ContableState.set_numero_factura,
                                            bg="#2D3748", color="#FFFFFF",
                                            border=rx.cond(
                                                ContableState.error_general != "",
                                                "1px solid #F56565", "none"
                                            ),
                                            width="100%",
                                        ),
                                        width="100%", spacing="1",
                                    ),
                                    spacing="3",
                                    width="100%",
                                ),
                                width="100%",
                                spacing="2",
                            ),
                            padding="1em",
                            bg="#141921",
                            border_radius="lg",
                            border="1px solid #2D3748",
                            width="100%",
                        ),

                        # AGREGAR PRODUCTO
                        rx.box(
                            rx.vstack(
                                rx.text("Agregar Producto", weight="bold", color="#A0AEC0", size="2"),
                                rx.hstack(
                                    rx.vstack(
                                        rx.text("Producto", color="#718096", size="1"),
                                        rx.select(
                                            ContableState.nombres_todos_productos,
                                            placeholder="Seleccionar...",
                                            value=ContableState.item_producto_sel,
                                            on_change=ContableState.set_item_producto_sel,
                                            bg="#2D3748", color="#FFFFFF",
                                            border="none", width="100%",
                                        ),
                                        width="260px", spacing="1",
                                    ),
                                    rx.vstack(
                                        rx.text("Cantidad", color="#718096", size="1"),
                                        rx.input(
                                            placeholder="0",
                                            type="number",
                                            value=ContableState.item_cantidad.to(str),
                                            on_change=ContableState.set_item_cantidad,
                                            bg="#2D3748", color="#FFFFFF",
                                            border="none", width="100px",
                                        ),
                                        spacing="1",
                                    ),
                                    rx.vstack(
                                        rx.text("Precio c/IVA", color="#718096", size="1"),
                                        rx.cond(
                                            ContableState.item_producto_sel != "",
                                            rx.box(
                                                rx.hstack(
                                                    rx.icon(tag="tag", size=13, color="#48BB78"),
                                                    rx.text(
                                                        f"${ContableState.precio_compra_producto_sel}",
                                                        color="#48BB78",
                                                        weight="bold",
                                                        size="2",
                                                    ),
                                                    spacing="1",
                                                    align="center",
                                                ),
                                                padding="0.5em 0.8em",
                                                bg="#1A3A2A",
                                                border="1px solid #2F855A",
                                                border_radius="lg",
                                                width="130px",
                                                height="36px",
                                            ),
                                            rx.box(
                                                rx.hstack(
                                                    rx.icon(tag="tag", size=13, color="#4A5568"),
                                                    rx.text("—", color="#4A5568", size="2"),
                                                    spacing="1",
                                                    align="center",
                                                ),
                                                padding="0.5em 0.8em",
                                                bg="#1A202C",
                                                border="1px solid #2D3748",
                                                border_radius="lg",
                                                width="130px",
                                                height="36px",
                                            ),
                                        ),
                                        spacing="1",
                                    ),
                                    rx.vstack(
                                        rx.text(" ", size="1"),
                                        rx.button(
                                            rx.icon(tag="plus", size=16),
                                            "Agregar",
                                            on_click=ContableState.agregar_item_recepcion,
                                            bg="#38A169", color="#FFFFFF",
                                            _hover={"bg": "#2F855A"},
                                            size="2",
                                        ),
                                        spacing="1",
                                    ),
                                    spacing="3",
                                    align="end",
                                    width="100%",
                                ),
                                width="100%",
                                spacing="2",
                            ),
                            padding="1em",
                            bg="#141921",
                            border_radius="lg",
                            border="1px solid #2D3748",
                            width="100%",
                        ),

                        # TABLA DE PRODUCTOS RECIBIDOS
                        rx.box(
                            rx.cond(
                                ContableState.items_recepcion.length() == 0,
                                rx.center(
                                    rx.vstack(
                                        rx.icon(tag="package", size=32, color="#4A5568"),
                                        rx.text("Sin productos agregados", color="#4A5568", size="2"),
                                        spacing="2",
                                        align="center",
                                    ),
                                    padding="2em",
                                ),
                                rx.table.root(
                                    rx.table.header(
                                        rx.table.row(
                                            rx.table.column_header_cell("Producto",     color="#718096"),
                                            rx.table.column_header_cell("N° Serie",     color="#718096"),
                                            rx.table.column_header_cell("Stock actual", color="#718096"),
                                            rx.table.column_header_cell("Cantidad",     color="#718096"),
                                            rx.table.column_header_cell("Precio c/IVA", color="#718096"),
                                            rx.table.column_header_cell("Subtotal",     color="#718096"),
                                            rx.table.column_header_cell("",             color="#718096"),
                                        )
                                    ),
                                    rx.table.body(
                                        rx.foreach(
                                            ContableState.items_recepcion,
                                            lambda item: rx.table.row(
                                                rx.table.cell(
                                                    rx.text(item["nombre"], color="#E2E8F0", size="2")
                                                ),
                                                rx.table.cell(
                                                    rx.text(item["numero_serie"], color="#A0AEC0", size="2")
                                                ),
                                                rx.table.cell(
                                                    rx.badge(
                                                        item["stock_actual"].to(str),
                                                        color_scheme="green",
                                                    )
                                                ),
                                                rx.table.cell(
                                                    rx.text(item["cantidad"].to(str), color="#FFFFFF", weight="bold", size="2")
                                                ),
                                                rx.table.cell(
                                                    rx.text("$" + item["precio_iva"].to(str), color="#48BB78", size="2")
                                                ),
                                                rx.table.cell(
                                                    rx.text(
                                                        "$" + item["subtotal"].to(str),
                                                        color="#4299E1", weight="bold", size="2",
                                                    )
                                                ),
                                                rx.table.cell(
                                                    rx.button(
                                                        rx.icon(tag="trash-2", size=13),
                                                        on_click=ContableState.quitar_item_recepcion(item["nombre"]),
                                                        size="1",
                                                        variant="ghost",
                                                        color="#F56565",
                                                        _hover={"bg": "#1A202C"},
                                                    )
                                                ),
                                                style={"_hover": {"bg": "#1A202C"}},
                                            )
                                        )
                                    ),
                                    width="100%",
                                    variant="ghost",
                                ),
                            ),
                            width="100%",
                            overflow_x="auto",
                            border="1px solid #2D3748",
                            border_radius="lg",
                            min_height="120px",
                        ),

                        # ERROR GENERAL
                        rx.cond(
                            ContableState.error_general != "",
                            rx.hstack(
                                rx.icon(tag="circle-alert", size=12, color="#F56565"),
                                rx.text(ContableState.error_general, color="#F56565", size="2", weight="bold"),
                                spacing="1",
                            ),
                        ),

                        # FOOTER: TOTALES + BOTONES
                        rx.hstack(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("Total artículos:", color="#A0AEC0", size="2"),
                                    rx.text(
                                        ContableState.items_recepcion.length().to(str),
                                        color="#FFFFFF", weight="bold", size="2"
                                    ),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("Total piezas:", color="#A0AEC0", size="2"),
                                    rx.text(
                                        ContableState.total_piezas_recepcion.to(str),
                                        color="#FFFFFF", weight="bold", size="2"
                                    ),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("Total con IVA:", color="#A0AEC0", size="2"),
                                    rx.text(
                                        "$" + ContableState.total_recepcion.to(str),
                                        color="#48BB78", weight="bold", size="4"
                                    ),
                                    spacing="2",
                                ),
                                spacing="1",
                                align="start",
                            ),
                            rx.spacer(),
                            rx.hstack(
                                rx.button(
                                    "Cancelar",
                                    on_click=ContableState.cerrar_modal_proveedor_recepcion,
                                    variant="ghost",
                                    color="#718096",
                                    _hover={"color": "#FFFFFF"},
                                ),
                                rx.button(
                                    rx.icon(tag="save", size=16),
                                    "Guardar Recepción",
                                    on_click=ContableState.confirmar_recepcion,
                                    bg="#3182CE",
                                    color="#FFFFFF",
                                    _hover={"bg": "#2B6CB0"},
                                ),
                                spacing="3",
                            ),
                            width="100%",
                            align="center",
                            padding_top="0.5em",
                            border_top="1px solid #2D3748",
                        ),

                        spacing="4",
                        width="100%",
                    ),
                    padding="2em",
                    bg="#1A202C",
                    border_radius="2xl",
                    border="1px solid #4A5568",
                    width="900px",
                    max_height="90vh",
                    overflow_y="auto",
                ),
                position="fixed",
                top="0", left="0",
                width="100%", height="100%",
                bg="rgba(0,0,0,0.85)",
                z_index="1000",
            )
        ),

        width="100%",
        min_height="100vh",
        bg="#0B0E14",
        padding="2em",
        padding_left="100px",
        padding_right="2em",
    )