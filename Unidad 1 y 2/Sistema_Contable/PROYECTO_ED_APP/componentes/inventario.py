import reflex as rx
from PROYECTO_ED_APP.state import ContableState 

# ================================
# INVENTARIO (FONDO OSCURO - FIX DEFINITIVO)
# ================================
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

            # Fila de búsqueda
            rx.hstack(
                rx.icon(
                    tag="search",
                    size=20,
                    color="#718096",
                    ),
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
                spacing="3",
                align="center",
                margin_bottom="1.5em",
            ),
            
            # Formulario de Registro
            rx.box(
                rx.vstack(
                    rx.text("Registrar Nuevo Producto",
                            weight="bold",
                            color="#A0AEC0",
                            size="2"
                            ),
                    rx.hstack(
                        rx.input(
                            placeholder="Nombre",
                            value=ContableState.nombre_producto_nuevo,
                            on_change=ContableState.set_nombre_producto_nuevo,
                            bg="#2D3748",
                            color="white",
                            border="none",
                            style={"_hover": {"bg": "#1A202C"}},
                            ),
                        rx.input(
                            placeholder="Stock",
                                type="number",
                                value=ContableState.stock_inicial,
                                on_change=ContableState.set_stock_inicial,
                                bg="#2D3748",
                                color="white",
                                border="none",
                                width="100px",
                                style={"_hover": {"bg": "#1A202C"}},
                                ),
                        rx.input(
                            placeholder="Compra",
                            type="number",
                            value=ContableState.precio_compra,
                            on_change=ContableState.set_precio_compra,
                            bg="#2D3748",
                            color="white",
                            border="none",
                            width="120px",
                            style={"_hover": {"bg": "#1A202C"}},
                            ),
                        rx.input(placeholder="Venta", 
                        type="number",
                        value=ContableState.precio_venta,
                        on_change=ContableState.set_precio_venta,
                        bg="#2D3748",
                        color="white",
                        border="none",
                        width="120px",
                        style={"_hover": {"bg": "#1A202C"}},
                        ),
                        rx.button("Registrar",
                                on_click=ContableState.agregar_producto,
                                color_scheme="blue",
                                bg="#3182CE",
                                _hover={
                        "transform": "translateY(-5px)",
                        "transition": "all 0.2s ease-in-out",
                        "box_shadow": f"0 8px 20px {"#3182CE"}22",
                        },
                                ),
                        width="100%",
                        spacing="3",
                    ),
                ),
                padding="1.5em",
                bg="#141921",
                border="1px solid #2D3748",
                border_radius="15px",
                width="100%",
                margin_bottom="2em",
            ),

            rx.divider(
                opacity="0.1",
                margin_y="1em"
                ),

            # Tabla de Productos (VERSION SIMPLIFICADA PARA EVITAR ERRORES)
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell(
                                "ID",
                                color="#718096",
                                ),
                            rx.table.column_header_cell(
                                "Nombre",
                                color="#718096",
                                ),
                            rx.table.column_header_cell(
                                "Stock",
                                color="#718096",
                                ),
                            rx.table.column_header_cell(
                                "Compra",
                                color="#718096"
                                ),
                            rx.table.column_header_cell(
                                "Venta",
                                color="#718096"
                                ),
                        )
                    ),
                    rx.table.body(
                        # Usamos .to(list[dict]) para ayudar a Reflex con el tipo de dato si es necesario
                        rx.foreach(
                            ContableState.productos_filtrados,
                            lambda p: rx.table.row(
                                rx.table.cell(
                                    p["id"],
                                    color="white",
                                    ),
                                rx.table.cell(
                                    p["nombre"],
                                    color="#E2E8F0"
                                ),
                                rx.table.cell(
                                    p["stock"],
                                    color="white",
                                    ),
                                rx.table.cell(
                                    f"${p['precio_compra']}",
                                    color="#48BB78"
                                    ),
                                rx.table.cell(
                                    f"${p['precio_venta']}",
                                    color="#4299E1"),
                                style={"_hover": {"bg": "#1A202C"}},
                            )
                        )
                    ),
                    width="100%",
                    variant="ghost",
                ),
                width="100%",
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