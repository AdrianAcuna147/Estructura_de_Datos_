import reflex as rx
from PROYECTO_ED_APP.state import ContableState


def vista_inventario() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Título principal
            rx.heading(
                "Inventario de productos",
                size="9",
                weight="bold",
                color="white",
                margin_bottom="0.5em",
            ),

            # Fila: búsqueda + MEJORA 1: control de stock mínimo configurable
            rx.hstack(
                rx.icon(tag="search", size=20, color="#718096"),
                rx.input(
                    placeholder="Buscar producto por nombre o ID...",
                    value=ContableState.texto_busqueda_producto,
                    on_change=ContableState.set_texto_busqueda_producto,
                    width="400px",
                    variant="surface",
                    bg="#1A202C",
                    color="white",
                    border="1px solid #2D3748",
                    style={"_hover": {"bg": "#0C0F15"}},
                ),
                rx.spacer(),
                # Solo el admin puede cambiar el umbral de alerta
                rx.cond(
                    ContableState.usuario_rol == "administrador",
                    rx.hstack(
                        rx.icon(tag="triangle-alert", size=16, color="#F6AD55"),
                        rx.text("Alerta stock ≤", color="#A0AEC0", size="2", weight="bold"),
                        rx.input(
                            type="number",
                            value=ContableState.stock_minimo_alerta.to(str),
                            on_change=ContableState.set_stock_minimo_alerta,
                            width="70px",
                            bg="#2D3748",
                            color="#F6AD55",
                            border="1px solid #744210",
                            style={"_hover": {"bg": "#1A202C"}},
                        ),
                        spacing="2",
                        align="center",
                        padding="0.4em 0.8em",
                        bg="#1A1500",
                        border="1px solid #744210",
                        border_radius="lg",
                    ),
                ),
                spacing="3",
                align="center",
                margin_bottom="1.5em",
                width="100%",
            ),

            # Formulario de Registro
            rx.box(
                rx.vstack(
                    rx.text("Registrar Nuevo Producto", weight="bold", color="white", size="2"),

                    # Fila 1: Nombre, Marca, Modelo
                    rx.hstack(
                        rx.input(
                            placeholder="Nombre",
                            value=ContableState.nombre_producto_nuevo,
                            on_change=ContableState.set_nombre_producto_nuevo,
                            bg="#3D4A5C",
                            color="white",
                            border="1px solid #4A5568",
                            style={"_hover": {"bg": "#4A5568"}, "_placeholder": {"color": "#E2E8F0"}},
                        ),
                        rx.input(
                            placeholder="Marca",
                            value=ContableState.marca_producto_nuevo,
                            on_change=ContableState.set_marca_producto_nuevo,
                            bg="#3D4A5C",
                            color="white",
                            border="1px solid #4A5568",
                            style={"_hover": {"bg": "#4A5568"}, "_placeholder": {"color": "#E2E8F0"}},
                        ),
                        rx.input(
                            placeholder="Modelo",
                            value=ContableState.modelo_producto_nuevo,
                            on_change=ContableState.set_modelo_producto_nuevo,
                            bg="#3D4A5C",
                            color="white",
                            border="1px solid #4A5568",
                            style={"_hover": {"bg": "#4A5568"}, "_placeholder": {"color": "#E2E8F0"}},
                        ),
                        width="100%",
                        spacing="3",
                    ),

                    # Fila 2: N° Serie, Stock, Compra, Venta, Botón
                    rx.hstack(
                        rx.input(
                            placeholder="N° de Serie (mín. 6 caracteres)",
                            value=ContableState.numero_serie_producto_nuevo,
                            on_change=ContableState.set_numero_serie_producto_nuevo,
                            bg="#3D4A5C",
                            color="white",
                            border="1px solid #4A5568",
                            style={"_hover": {"bg": "#4A5568"}, "_placeholder": {"color": "#E2E8F0"}},
                        ),
                        rx.input(
                            placeholder="Stock",
                            type="number",
                            value=rx.cond(ContableState.stock_inicial == 0, "", ContableState.stock_inicial.to(str)),
                            on_change=ContableState.set_stock_inicial,
                            bg="#3D4A5C",
                            color="white",
                            border="1px solid #4A5568",
                            width="100px",
                            style={"_hover": {"bg": "#4A5568"}, "_placeholder": {"color": "#E2E8F0"}},
                        ),
                        rx.input(
                            placeholder="Compra",
                            type="number",
                            value=rx.cond(ContableState.precio_compra == 0, "", ContableState.precio_compra.to(str)),
                            on_change=ContableState.set_precio_compra,
                            bg="#3D4A5C",
                            color="white",
                            border="1px solid #4A5568",
                            width="120px",
                            style={"_hover": {"bg": "#4A5568"}, "_placeholder": {"color": "#E2E8F0"}},
                        ),
                        rx.input(
                            placeholder="Venta",
                            type="number",
                            value=rx.cond(ContableState.precio_venta == 0, "", ContableState.precio_venta.to(str)),
                            on_change=ContableState.set_precio_venta,
                            bg="#3D4A5C",
                            color="white",
                            border="1px solid #4A5568",
                            width="120px",
                            style={"_hover": {"bg": "#4A5568"}, "_placeholder": {"color": "#E2E8F0"}},
                        ),
                        rx.button(
                            "Registrar",
                            on_click=ContableState.agregar_producto,
                            color_scheme="blue",
                            bg="#3182CE",
                            _hover={
                                "transform": "translateY(-5px)",
                                "transition": "all 0.2s ease-in-out",
                                "box_shadow": "0 8px 20px #3182CE22",
                            },
                        ),
                        width="100%",
                        spacing="3",
                    ),

                    rx.cond(
                        ContableState.error_inventario != "",
                        rx.hstack(
                            rx.icon(tag="circle-alert", size=12, color="#F56565"),
                            rx.text(
                                ContableState.error_inventario,
                                color="#F56565",
                                size="2",
                                weight="bold",
                            ),
                            spacing="1",
                            margin_top="0.5em",
                        ),
                    ),
                ),
                padding="1.5em",
                bg="#141921",
                border="1px solid #2D3748",
                border_radius="15px",
                width="100%",
                margin_bottom="2em",
            ),

            rx.divider(opacity="0.1", margin_y="1em"),

            # Tabla de Productos
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("ID",       color="#718096"),
                            rx.table.column_header_cell("Nombre",   color="#718096"),
                            rx.table.column_header_cell("Marca",    color="#718096"),
                            rx.table.column_header_cell("Modelo",   color="#718096"),
                            rx.table.column_header_cell("N° Serie", color="#718096"),
                            rx.table.column_header_cell("Stock",    color="#718096"),
                            rx.table.column_header_cell("Compra",   color="#718096"),
                            rx.table.column_header_cell("Venta",    color="#718096"),
                            rx.table.column_header_cell("Acciones", color="#718096"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            ContableState.productos_filtrados,
                            lambda p: rx.table.row(
                                rx.table.cell(p["id"], color="white"),
                                rx.table.cell(p["nombre"], color="#E2E8F0"),
                                rx.table.cell(p["marca"], color="#E2E8F0"),
                                rx.table.cell(p["modelo"], color="#E2E8F0"),
                                rx.table.cell(p["numero_serie"], color="#A0AEC0"),
                                # stock_bajo viene precalculado desde state (evita comparar vars en foreach)
                                rx.table.cell(
                                    rx.cond(
                                        p["stock_bajo"],
                                        rx.hstack(
                                            rx.badge(p["stock"].to(str), color_scheme="orange", variant="soft"),
                                            rx.icon(tag="triangle-alert", size=13, color="#F6AD55"),
                                            spacing="1", align="center",
                                        ),
                                        rx.text(p["stock"].to(str), color="white"),
                                    )
                                ),
                                rx.table.cell(f"${p['precio_compra']}", color="#48BB78"),
                                rx.table.cell(f"${p['precio_venta']}", color="#4299E1"),
                                rx.table.cell(
                                    rx.hstack(
                                        rx.button(
                                            rx.icon(tag="pencil", size=14),
                                            on_click=ContableState.abrir_modal_editar(p["id"]),
                                            size="1",
                                            variant="ghost",
                                            color="#4299E1",
                                            _hover={"bg": "#1A202C", "color": "#63B3ED"},
                                            cursor="pointer",
                                        ),
                                        rx.button(
                                            rx.icon(tag="trash-2", size=14),
                                            on_click=ContableState.confirmar_eliminar(p["id"]),
                                            size="1",
                                            variant="ghost",
                                            color="#F56565",
                                            _hover={"bg": "#1A202C", "color": "#FC8181"},
                                            cursor="pointer",
                                        ),
                                        spacing="2",
                                    )
                                ),
                                style={"_hover": {"bg": "#1A202C"}},
                            )
                        )
                    ),
                    width="100%",
                    variant="ghost",
                ),
                width="100%",
            ),

            # ================================
            # MEJORA 2: Modal de Edición ampliado
            # Antes: solo Nombre, Stock, Compra, Venta
            # Ahora: + Marca, Modelo, N° Serie
            # ================================
            rx.dialog.root(
                rx.dialog.content(
                    rx.dialog.title("Editar Producto", color="white"),
                    rx.vstack(
                        # Fila 1: Nombre, Marca, Modelo
                        rx.hstack(
                            rx.vstack(
                                rx.text("Nombre", color="#A0AEC0", size="2", weight="bold"),
                                rx.input(
                                    value=ContableState.edit_nombre,
                                    on_change=ContableState.set_edit_nombre,
                                    bg="#2D3748", color="white",
                                    border="1px solid #4A5568", width="100%",
                                ),
                                spacing="1", width="100%",
                            ),
                            rx.vstack(
                                rx.text("Marca", color="#A0AEC0", size="2", weight="bold"),
                                rx.input(
                                    value=ContableState.edit_marca,
                                    on_change=ContableState.set_edit_marca,
                                    bg="#2D3748", color="white",
                                    border="1px solid #4A5568", width="100%",
                                ),
                                spacing="1", width="100%",
                            ),
                            rx.vstack(
                                rx.text("Modelo", color="#A0AEC0", size="2", weight="bold"),
                                rx.input(
                                    value=ContableState.edit_modelo,
                                    on_change=ContableState.set_edit_modelo,
                                    bg="#2D3748", color="white",
                                    border="1px solid #4A5568", width="100%",
                                ),
                                spacing="1", width="100%",
                            ),
                            spacing="3", width="100%",
                        ),
                        # N° Serie
                        rx.vstack(
                            rx.text("N° de Serie", color="#A0AEC0", size="2", weight="bold"),
                            rx.input(
                                value=ContableState.edit_numero_serie,
                                on_change=ContableState.set_edit_numero_serie,
                                bg="#2D3748", color="white",
                                border="1px solid #4A5568", width="100%",
                            ),
                            spacing="1", width="100%",
                        ),
                        # Fila 2: Stock, Compra, Venta
                        rx.hstack(
                            rx.vstack(
                                rx.text("Stock", color="#A0AEC0", size="2", weight="bold"),
                                rx.input(
                                    type="number",
                                    value=ContableState.edit_stock.to(str),
                                    on_change=ContableState.set_edit_stock,
                                    bg="#2D3748", color="white",
                                    border="1px solid #4A5568", width="100%",
                                ),
                                spacing="1", width="100%",
                            ),
                            rx.vstack(
                                rx.text("Precio Compra", color="#A0AEC0", size="2", weight="bold"),
                                rx.input(
                                    type="number",
                                    value=ContableState.edit_precio_compra.to(str),
                                    on_change=ContableState.set_edit_precio_compra,
                                    bg="#2D3748", color="white",
                                    border="1px solid #4A5568", width="100%",
                                ),
                                spacing="1", width="100%",
                            ),
                            rx.vstack(
                                rx.text("Precio Venta", color="#A0AEC0", size="2", weight="bold"),
                                rx.input(
                                    type="number",
                                    value=ContableState.edit_precio_venta.to(str),
                                    on_change=ContableState.set_edit_precio_venta,
                                    bg="#2D3748", color="white",
                                    border="1px solid #4A5568", width="100%",
                                ),
                                spacing="1", width="100%",
                            ),
                            spacing="3", width="100%",
                        ),
                        rx.hstack(
                            rx.dialog.close(
                                rx.button(
                                    "Cancelar",
                                    variant="ghost",
                                    color="#718096",
                                    on_click=ContableState.cerrar_modal_editar,
                                )
                            ),
                            rx.dialog.close(
                                rx.button(
                                    "Guardar",
                                    bg="#3182CE",
                                    color="white",
                                    on_click=ContableState.guardar_edicion,
                                )
                            ),
                            spacing="3",
                            justify="end",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    bg="#1A202C",
                    border="1px solid #2D3748",
                    border_radius="15px",
                    padding="2em",
                    max_width="580px",
                ),
                open=ContableState.mostrar_modal_editar,
            ),

            # Modal de confirmación de eliminación
            rx.dialog.root(
                rx.dialog.content(
                    rx.vstack(
                        rx.hstack(
                            rx.icon(tag="triangle-alert", size=22, color="#F56565"),
                            rx.dialog.title(
                                "¿Seguro que quiere eliminar el producto?",
                                color="white",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.text(
                            "Esta acción no se puede deshacer.",
                            color="#A0AEC0",
                            size="2",
                        ),
                        rx.hstack(
                            rx.dialog.close(
                                rx.button(
                                    "Cancelar",
                                    variant="ghost",
                                    color="#718096",
                                    on_click=ContableState.cancelar_eliminar,
                                )
                            ),
                            rx.dialog.close(
                                rx.button(
                                    "Sí, eliminar",
                                    bg="#E53E3E",
                                    color="white",
                                    on_click=ContableState.eliminar_producto,
                                )
                            ),
                            spacing="3",
                            justify="end",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    bg="#1A202C",
                    border="1px solid #F56565",
                    border_radius="15px",
                    padding="2em",
                    max_width="400px",
                ),
                open=ContableState.mostrar_modal_eliminar,
            ),

            spacing="4",
            width="100%",
            align_items="start",
            padding_left="250px",
            padding_right="2em",
        ),
        padding="4em 2em",
        bg="#0B0E14",
        min_height="100vh",
        width="100%",
    )