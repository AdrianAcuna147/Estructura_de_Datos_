import reflex as rx
from ..state import ContableState # <--- El backend

# ================================
# INVENTARIO
# ================================
def vista_inventario() -> rx.Component:
    return rx.box(
        rx.vstack(

            rx.heading("Inventario de productos", size="6"),

            # Cuadro de entrada para buscar en el inventario
            rx.input(
                placeholder="Buscar producto por nombre o ID...",
                value=ContableState.texto_busqueda_producto,
                on_change=ContableState.set_texto_busqueda_producto,
                width="300px"
            ),
            
            # Permite ingresar el nombre del producto en el inventario
            rx.hstack(
                rx.input(
                    placeholder="Nombre producto",
                    value=ContableState.nombre_producto_nuevo,
                    on_change=ContableState.set_nombre_producto_nuevo
                ),
                # Permite ingresar el stock del producto en el inventario
                rx.input(
                    placeholder="Stock inicial",
                    type="number",
                    value=ContableState.stock_inicial,
                    on_change=ContableState.set_stock_inicial
                ),
                # Permite ingresar el precio compra del producto en el inventario
                rx.input(
                    placeholder="Precio compra",
                    type="number",
                    value=ContableState.precio_compra,
                    on_change=ContableState.set_precio_compra
                ),
                # Permite ingresar el precio venta del producto en el inventario
                rx.input(
                    placeholder="Precio venta",
                    type="number",
                    value=ContableState.precio_venta,
                    on_change=ContableState.set_precio_venta
                ),
                # Permite registrar el boton
                rx.button(
                    "Registrar producto",
                    on_click=ContableState.agregar_producto
                ),
            ),

            rx.divider(),
            # Registra en el .json el producto con sus datos
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID"),
                        rx.table.column_header_cell("Nombre"),
                        rx.table.column_header_cell("Stock"),
                        rx.table.column_header_cell("Compra"),
                        rx.table.column_header_cell("Venta"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        ContableState.productos_filtrados,
                        lambda p: rx.table.row(
                            rx.table.cell(p["id"]),
                            rx.table.cell(p["nombre"]),
                            rx.table.cell(p["stock"]),
                            rx.table.cell(f"${p['precio_compra']}"),
                            rx.table.cell(f"${p['precio_venta']}"),
                        )
                    )
                ),
                width="100%",
            )
        ),
        padding="2em"
    )