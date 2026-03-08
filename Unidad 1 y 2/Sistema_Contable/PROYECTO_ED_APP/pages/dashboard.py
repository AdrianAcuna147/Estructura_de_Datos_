import reflex as rx 
from ..state import ContableState # <--- El backend

# ================================
# DASHBOARD
# ================================
def vista_dashboard() -> rx.Component:
    return rx.box(
        rx.vstack(

            rx.heading("Dashboard financiero", size="7"),
            rx.text("Resumen general del sistema contable", color="gray"),

            rx.divider(),

            # ======================
            # TARJETAS PRINCIPALES
            # ======================
            rx.grid(

                # INGRESOS
                rx.box(
                    rx.vstack(
                        rx.text("Ingresos totales", color="black"),
                        rx.heading(f"${ContableState.total_ingresos}", size="6", color="gray"),
                    ),
                    padding="1.5em",
                    bg="#B2D9AF",
                    border_radius="xl",
                    width="220px",
                    box_shadow="md",
                ),

                # EGRESOS
                rx.box(
                    rx.vstack(
                        rx.text("Egresos totales", color="black"),
                        rx.heading(f"${ContableState.total_egresos}", size="6", color="gray"),
                    ),
                    padding="1.5em",
                    bg="#F1CDC6",
                    border_radius="xl",
                    width="220px",
                    box_shadow="md",
                ),

                # SALDO
                rx.box(
                    rx.vstack(
                        rx.text("Saldo total", color="black"),
                        rx.heading(f"${ContableState.saldo_total}", size="6", color="gray"),
                    ),
                    padding="1.5em",
                    bg="#ACD7DC",
                    border_radius="xl",
                    width="220px",
                    box_shadow="md",
                ),

                columns="3",
                spacing="6",
            ),

            rx.divider(),

            # ======================
            # MÉTRICAS GENERALES
            # ======================
            rx.grid(

                rx.box(
                    rx.vstack(
                        rx.text("Clientes registrados", color="black"),
                        rx.heading(ContableState.total_clientes, size="5", color="gray"),
                    ),
                    padding="1.2em",
                    bg="#79E292",
                    border_radius="xl",
                    box_shadow="sm",
                ),

                rx.box(
                    rx.vstack(
                        rx.text("Proveedores registrados", color="black"),
                        rx.heading(ContableState.total_proveedores, size="5", color="gray"),
                    ),
                    padding="1.2em",
                    bg="#E28B79",
                    border_radius="xl",
                    box_shadow="sm",
                ),

                rx.box(
                    rx.vstack(
                        rx.text("Productos en inventario", color="black"),
                        rx.heading(ContableState.total_productos, size="5", color="gray"),
                    ),
                    padding="1.2em",
                    bg="#79D9E2",
                    border_radius="xl",
                    box_shadow="sm",
                ),

                columns="3",
                spacing="6",
            ),

            rx.divider(),

            # ======================
            # GRÁFICA FINANCIERA
            # ======================
            rx.box(
                rx.vstack(
                    rx.heading("Ingresos vs Egresos por mes", size="5", color = "black"),
                    rx.text("Comparación mensual del flujo financiero", color="gray"),

                    rx.recharts.bar_chart(
                        rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                        rx.recharts.x_axis(data_key="mes"),
                        rx.recharts.y_axis(),
                        rx.recharts.tooltip(),
                        rx.recharts.legend(),

                        rx.recharts.bar(
                            data_key="ingresos",
                            fill="#4CAF50",
                            radius=[6, 6, 0, 0],
                        ),

                        rx.recharts.bar(
                            data_key="egresos",
                            fill="#F44336",
                            radius=[6, 6, 0, 0],
                        ),

                        data=ContableState.grafica_financiera,
                        width="100%",
                        height=350,
                    ),
                ),
                padding="2em",
                bg="white",
                border_radius="xl",
                box_shadow="lg",
                width="100%",
            ),

        ),
        padding="2em",
        width="100%",
        min_height="100vh",
    )
