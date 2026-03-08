import reflex as rx
from ..state import ContableState # <--- El backend

# ================================
# CONTABLE (CENTRADO)
# ================================
def vista_contable() -> rx.Component:
    return rx.center(
        rx.vstack(

            # ======================
            # TÍTULO
            # ======================
            rx.heading(
                "Sistema Contable",
                size="7",
                font_size="3em",
            ),
            rx.divider(),

            # ======================
            # SALDO INICIAL
            # ======================
            rx.text("Saldo inicial"),
            rx.input(
                placeholder="Monto",
                type="number",
                value=ContableState.saldo_inicial,
                on_change=ContableState.set_saldo_inicial,
                width="100%",
            ),

            rx.divider(),

            # ======================
            # FACTURA
            # ======================
            rx.text("Factura"),

            #Permite el ingreso del numero de la factura
            rx.input(
                placeholder="Número de factura",
                value=ContableState.numero_factura,
                on_change=ContableState.set_numero_factura,
                width="100%",
            ),

            #Permite el ingreso del nombre del producto
            rx.input(
                placeholder="Nombre del producto",
                value=ContableState.nombre_producto,
                on_change=ContableState.set_nombre_producto,
                width="100%",
            ),

            #Permite el ingreso del monto de la factura
            rx.input(
                placeholder="Monto",
                type="number",
                value=ContableState.monto_factura,
                on_change=ContableState.set_monto_factura,
                width="100%",
            ),

            # ======================
            # BOTONES
            # ======================
            rx.hstack(
                rx.button(
                    "Agregar cliente",
                    on_click=ContableState.abrir_modal_cliente,
                    color_scheme="green",
                    width="48.5%",
                ),
                rx.button(
                    "Agregar proveedor",
                    on_click=ContableState.abrir_modal_proveedor,
                    color_scheme="red",
                    width="48.5%",
                ),
                width="100%",
            ),

            rx.divider(),

            # ======================
            # TOTALES
            # ======================
            rx.text(f"Ingresos: ${ContableState.total_ingresos}"),
            rx.text(f"Egresos: ${ContableState.total_egresos}"),
            rx.text(
                f"Saldo total: ${ContableState.saldo_total}",
                font_weight="bold",
            ),

            # ======================
            # MODAL (Ventana de registro)
            # ======================
            rx.cond(
                ContableState.mostrar_modal,
                rx.center(
                    rx.box(
                        rx.vstack(

                            # TITULO MODAL
                            rx.heading(
                                rx.cond(
                                    ContableState.tipo_modal == "cliente",
                                    "Datos del Cliente",
                                    "Datos del Proveedor",
                                ),
                                size="5",
                                color="black",
                            ),

                            # ======================
                            # FORMULARIO CLIENTE
                            # ======================
                            rx.cond(
                                ContableState.tipo_modal == "cliente",
                                rx.vstack(

                                    rx.input(
                                        placeholder="Nombre del cliente",
                                        color="black",
                                        value=ContableState.nombre_cliente,
                                        on_change=ContableState.set_nombre_cliente,
                                    ),

                                    rx.cond(
                                        ContableState.error_nombre != "",
                                        rx.text(
                                            ContableState.error_nombre,
                                            color="red",
                                            font_size="0.9em",
                                        ),
                                    ),

                                    rx.input(
                                        placeholder="Correo del cliente",
                                        color="black",
                                        value=ContableState.correo_cliente,
                                        on_change=ContableState.set_correo_cliente,
                                    ),

                                    rx.cond(
                                        ContableState.error_correo != "",
                                        rx.text(
                                            ContableState.error_correo,
                                            color="red",
                                            font_size="0.9em",
                                        ),
                                    ),

                                ),

                                # ======================
                                # FORMULARIO PROVEEDOR
                                # ======================
                                rx.vstack(

                                    rx.input(
                                        placeholder="Nombre del proveedor",
                                        color="black",
                                        value=ContableState.nombre_proveedor,
                                        on_change=ContableState.set_nombre_proovedor,
                                    ),

                                    rx.cond(
                                        ContableState.error_nombre != "",
                                        rx.text(
                                            ContableState.error_nombre,
                                            color="red",
                                            font_size="0.9em",
                                        ),
                                    ),

                                    rx.input(
                                        placeholder="Correo del proveedor",
                                        color="black",
                                        value=ContableState.correo_proveedor,
                                        on_change=ContableState.set_correo_proovedor,
                                    ),

                                    rx.cond(
                                        ContableState.error_correo != "",
                                        rx.text(
                                            ContableState.error_correo,
                                            color="red",
                                            font_size="0.9em",
                                        ),
                                    ),
                                ),
                            ),

                            # Manejo de errores del modal
                            rx.cond(
                                ContableState.error_general != "",
                                rx.text(
                                    ContableState.error_general,
                                    color="red",
                                    font_weight="bold",
                                ),
                            ),

                            #Botones dentro del modal
                            rx.hstack(
                                rx.button(
                                    "Cancelar",
                                    on_click=ContableState.cerrar_modal,
                                    variant="outline",
                                ),
                                rx.button(
                                    "Confirmar",
                                    on_click=ContableState.confirmar_modal,
                                    color_scheme="green",
                                ),
                            ),

                        ),
                        padding="2em",
                        bg="white",
                        border_radius="md",
                        box_shadow="lg",
                        width="320px",
                    ),
                    position="fixed",
                    top="0",
                    left="0",
                    right="0",
                    bottom="0",
                    bg="rgba(0,0,0,0.4)",
                    z_index="999",
                ),
            ),

            width="420px",
            spacing="4",
        ),

        #CONTENEDOR QUE CENTRA
        width="100%",
        height="100vh",
    )
