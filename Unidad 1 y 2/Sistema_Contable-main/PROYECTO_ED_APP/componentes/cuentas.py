import reflex as rx
from PROYECTO_ED_APP.state import ContableState
from PROYECTO_ED_APP.componentes.sidebar import sidebar


def vista_cuenta() -> rx.Component:  # <-- nombre correcto que espera index.py
    return rx.box(
        sidebar(),

        rx.box(
            rx.vstack(

                # ── CABECERA ──────────────────────────────────────────
                rx.hstack(
                    # Avatar con inicial
                    rx.box(
                        rx.text(
                            ContableState.usuario_nombre[:1].upper(),
                            color="#FFFFFF", weight="bold", size="7",
                        ),
                        width="64px", height="64px",
                        bg=rx.cond(ContableState.usuario_rol == "administrador", "#553C9A", "#2B6CB0"),
                        border_radius="50%",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                    ),
                    rx.vstack(
                        rx.heading(ContableState.usuario_nombre, size="7", weight="bold", color="#FFFFFF"),
                        rx.hstack(
                            rx.badge(
                                ContableState.usuario_rol,
                                color_scheme=rx.cond(ContableState.usuario_rol == "administrador", "purple", "blue"),
                                variant="soft",
                            ),
                            rx.text(ContableState.usuario_correo, color="#718096", size="2"),
                            spacing="3", align="center",
                        ),
                        spacing="1", align="start",
                    ),
                    spacing="4", align="center",
                    margin_bottom="2em", width="100%",
                ),

                # ── DOS COLUMNAS ──────────────────────────────────────
                rx.flex(

                    # ── TARJETA IZQUIERDA: DATOS PERSONALES ───────────
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.icon(tag="user", size=18, color="#4299E1"),
                                rx.text("Información Personal", weight="bold", color="#E2E8F0", size="4"),
                                spacing="2", align="center",
                            ),
                            rx.divider(color_scheme="gray", opacity="0.3"),

                            # Nombre
                            rx.vstack(
                                rx.text("Nombre de usuario", color="#718096", size="1"),
                                rx.box(
                                    rx.hstack(
                                        rx.icon(tag="at-sign", size=14, color="#4299E1"),
                                        rx.text(ContableState.usuario_nombre, color="#E2E8F0", weight="bold", size="3"),
                                        spacing="2", align="center",
                                    ),
                                    bg="#2D3748", border_radius="8px",
                                    padding="0.6em 1em", width="100%",
                                ),
                                width="100%", spacing="1",
                            ),

                            # Correo
                            rx.vstack(
                                rx.text("Correo electrónico", color="#718096", size="1"),
                                rx.box(
                                    rx.hstack(
                                        rx.icon(tag="mail", size=14, color="#4299E1"),
                                        rx.text(ContableState.usuario_correo, color="#E2E8F0", size="3"),
                                        spacing="2", align="center",
                                    ),
                                    bg="#2D3748", border_radius="8px",
                                    padding="0.6em 1em", width="100%",
                                ),
                                width="100%", spacing="1",
                            ),

                            # Rol
                            rx.vstack(
                                rx.text("Rol en el sistema", color="#718096", size="1"),
                                rx.box(
                                    rx.hstack(
                                        rx.icon(
                                            tag=rx.cond(ContableState.usuario_rol == "administrador", "shield-check", "user"),
                                            size=14,
                                            color=rx.cond(ContableState.usuario_rol == "administrador", "#9F7AEA", "#4299E1"),
                                        ),
                                        rx.text(
                                            ContableState.usuario_rol,
                                            color=rx.cond(ContableState.usuario_rol == "administrador", "#9F7AEA", "#4299E1"),
                                            weight="bold", size="3",
                                        ),
                                        spacing="2", align="center",
                                    ),
                                    bg="#2D3748", border_radius="8px",
                                    padding="0.6em 1em", width="fit-content",
                                ),
                                width="100%", spacing="1",
                            ),

                            spacing="4", width="100%",
                        ),
                        bg="#141921", border="1px solid #2D3748",
                        border_radius="20px", padding="2em",
                        flex="1",
                    ),

                    # ── TARJETA DERECHA: CAMBIAR CONTRASEÑA ───────────
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.icon(tag="lock", size=18, color="#4299E1"),
                                rx.text("Cambiar Contraseña", weight="bold", color="#E2E8F0", size="4"),
                                spacing="2", align="center",
                            ),
                            rx.divider(color_scheme="gray", opacity="0.3"),
                            rx.text(
                                "Cambia tu contraseña para mantener tu cuenta segura.",
                                color="#718096", size="2",
                            ),

                            # Contraseña actual
                            rx.vstack(
                                rx.text("Contraseña actual", color="#718096", size="1"),
                                rx.input(
                                    placeholder="Tu contraseña actual",
                                    type="password",
                                    value=ContableState.cuenta_pass_actual,
                                    on_change=ContableState.set_cuenta_pass_actual,
                                    bg="#2D3748", color="#FFFFFF", border="none", width="100%",
                                ),
                                width="100%", spacing="1",
                            ),

                            # Nueva contraseña
                            rx.vstack(
                                rx.text("Nueva contraseña", color="#718096", size="1"),
                                rx.input(
                                    placeholder="Mínimo 6 caracteres",
                                    type="password",
                                    value=ContableState.cuenta_pass_nueva,
                                    on_change=ContableState.set_cuenta_pass_nueva,
                                    bg="#2D3748", color="#FFFFFF", border="none", width="100%",
                                ),
                                width="100%", spacing="1",
                            ),

                            # Confirmar
                            rx.vstack(
                                rx.text("Confirmar nueva contraseña", color="#718096", size="1"),
                                rx.input(
                                    placeholder="Repite la nueva contraseña",
                                    type="password",
                                    value=ContableState.cuenta_pass_confirmar,
                                    on_change=ContableState.set_cuenta_pass_confirmar,
                                    bg="#2D3748", color="#FFFFFF", border="none", width="100%",
                                ),
                                width="100%", spacing="1",
                            ),

                            # Error
                            rx.cond(
                                ContableState.cuenta_error != "",
                                rx.hstack(
                                    rx.icon(tag="circle-alert", size=13, color="#F56565"),
                                    rx.text(ContableState.cuenta_error, color="#F56565", size="2"),
                                    spacing="1", padding="0.75em",
                                    bg="#2D1515", border_radius="8px", width="100%",
                                ),
                            ),

                            # Éxito
                            rx.cond(
                                ContableState.cuenta_exito != "",
                                rx.hstack(
                                    rx.icon(tag="circle-check", size=13, color="#48BB78"),
                                    rx.text(ContableState.cuenta_exito, color="#48BB78", size="2"),
                                    spacing="1", padding="0.75em",
                                    bg="#152D1F", border_radius="8px", width="100%",
                                ),
                            ),

                            # Botón
                            rx.button(
                                rx.icon(tag="lock", size=15),
                                "Actualizar Contraseña",
                                on_click=ContableState.cambiar_contrasena,
                                bg="#3182CE", color="#FFFFFF", cursor="pointer",
                                size="3", width="100%",
                                _hover={"bg": "#2B6CB0"},
                            ),

                            spacing="4", width="100%",
                        ),
                        bg="#141921", border="1px solid #2D3748",
                        border_radius="20px", padding="2em",
                        flex="1",
                    ),

                    spacing="6",
                    width="100%",
                    flex_direction=["column", "column", "row"],
                ),

                spacing="4", width="100%",
            ),
            padding_y="2em",
            padding_left="300px",
            padding_right="3em",
        ),

        width="100%",
        min_height="100vh",
        bg="#0B0E14",
    )