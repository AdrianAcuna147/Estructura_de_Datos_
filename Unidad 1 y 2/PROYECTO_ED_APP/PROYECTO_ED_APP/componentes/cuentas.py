import reflex as rx
from PROYECTO_ED_APP.state import ContableState
from PROYECTO_ED_APP.componentes.sidebar import sidebar


def vista_cuenta() -> rx.Component:
    return rx.box(
        sidebar(),

        rx.box(
            rx.vstack(

                # ── CABECERA ──────────────────────────────────────────
                rx.hstack(
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
                    rx.spacer(),
                    rx.button(
                        rx.icon(tag="pencil", size=15),
                        "Editar Perfil",
                        on_click=ContableState.abrir_modal_perfil,
                        bg="#2D3748", color="#E2E8F0", size="2",
                        border="1px solid #4A5568",
                        _hover={"bg": "#3182CE", "border_color": "#3182CE"},
                        cursor="pointer",
                    ),
                    spacing="4", align="center",
                    margin_bottom="2em", width="100%",
                ),

                # ── TRES TARJETAS ──────────────────────────────────────
                rx.flex(

                    # ── TARJETA 1: DATOS PERSONALES ───────────────────
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.icon(tag="user", size=18, color="#4299E1"),
                                rx.text("Información Personal", weight="bold", color="#E2E8F0", size="4"),
                                spacing="2", align="center",
                            ),
                            rx.divider(color_scheme="gray", opacity="0.3"),

                            # Nombre
                            _campo_info("user", "Nombre", ContableState.usuario_nombre),
                            # Apellidos
                            _campo_info("users", "Apellidos", ContableState.usuario_apellidos),
                            # Correo
                            _campo_info("mail", "Correo", ContableState.usuario_correo),
                            # Domicilio
                            _campo_info("map-pin", "Domicilio",
                                rx.cond(
                                    ContableState.usuario_domicilio != "",
                                    ContableState.usuario_domicilio,
                                    rx.text("No registrado", color="#4A5568", size="3"),
                                )
                            ),
                            # Edad
                            _campo_info("calendar", "Edad",
                                rx.cond(
                                    ContableState.usuario_edad > 0,
                                    ContableState.usuario_edad.to(str) + " años",
                                    rx.text("No registrada", color="#4A5568", size="3"),
                                )
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

                            spacing="3", width="100%",
                        ),
                        bg="#141921", border="1px solid #2D3748",
                        border_radius="20px", padding="2em",
                        flex="1",
                    ),

                    # ── TARJETA 2: CAMBIAR CONTRASEÑA ─────────────────
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

                            rx.cond(
                                ContableState.cuenta_error != "",
                                rx.hstack(
                                    rx.icon(tag="circle-alert", size=13, color="#F56565"),
                                    rx.text(ContableState.cuenta_error, color="#F56565", size="2"),
                                    spacing="1", padding="0.75em",
                                    bg="#2D1515", border_radius="8px", width="100%",
                                ),
                            ),
                            rx.cond(
                                ContableState.cuenta_exito != "",
                                rx.hstack(
                                    rx.icon(tag="circle-check", size=13, color="#48BB78"),
                                    rx.text(ContableState.cuenta_exito, color="#48BB78", size="2"),
                                    spacing="1", padding="0.75em",
                                    bg="#152D1F", border_radius="8px", width="100%",
                                ),
                            ),

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

        # ── MODAL EDITAR PERFIL ────────────────────────────────────────
        rx.cond(
            ContableState.mostrar_modal_perfil,
            rx.center(
                rx.box(
                    rx.vstack(
                        # Header
                        rx.hstack(
                            rx.hstack(
                                rx.icon(tag="pencil", size=20, color="#4299E1"),
                                rx.heading("Editar Perfil", size="5", color="#FFFFFF"),
                                spacing="2", align="center",
                            ),
                            rx.spacer(),
                            rx.button(
                                rx.icon(tag="x", size=16),
                                on_click=ContableState.cerrar_modal_perfil,
                                variant="ghost", color="#718096", _hover={"color": "#FFFFFF"}, size="1",
                            ),
                            width="100%", align="center",
                            padding_bottom="1em", border_bottom="1px solid #2D3748",
                        ),

                        # Campos
                        rx.grid(
                            # Nombre
                            rx.vstack(
                                rx.text("Nombre", color="#718096", size="1"),
                                rx.input(
                                    placeholder="Tu nombre",
                                    value=ContableState.editar_perfil_nombre,
                                    on_change=ContableState.set_editar_perfil_nombre,
                                    bg="#2D3748", color="#FFFFFF", border="none", width="100%",
                                ),
                                width="100%", spacing="1",
                            ),
                            # Apellidos
                            rx.vstack(
                                rx.text("Apellidos", color="#718096", size="1"),
                                rx.input(
                                    placeholder="Tus apellidos",
                                    value=ContableState.editar_perfil_apellidos,
                                    on_change=ContableState.set_editar_perfil_apellidos,
                                    bg="#2D3748", color="#FFFFFF", border="none", width="100%",
                                ),
                                width="100%", spacing="1",
                            ),
                            # Edad
                            rx.vstack(
                                rx.text("Edad", color="#718096", size="1"),
                                rx.input(
                                    placeholder="Tu edad",
                                    type="number",
                                    value=ContableState.editar_perfil_edad.to(str),
                                    on_change=ContableState.set_editar_perfil_edad,
                                    bg="#2D3748", color="#FFFFFF", border="none", width="100%",
                                ),
                                width="100%", spacing="1",
                            ),
                            # Correo (solo lectura)
                            rx.vstack(
                                rx.text("Correo (no editable)", color="#718096", size="1"),
                                rx.box(
                                    rx.text(ContableState.editar_perfil_correo, color="#718096", size="2"),
                                    bg="#1A202C", border="1px solid #2D3748", border_radius="8px",
                                    padding="0.5em 1em", width="100%",
                                ),
                                width="100%", spacing="1",
                            ),
                            columns="2", spacing="4", width="100%",
                        ),

                        # Domicilio (full width)
                        rx.vstack(
                            rx.text("Domicilio", color="#718096", size="1"),
                            rx.input(
                                placeholder="Tu domicilio",
                                value=ContableState.editar_perfil_domicilio,
                                on_change=ContableState.set_editar_perfil_domicilio,
                                bg="#2D3748", color="#FFFFFF", border="none", width="100%",
                            ),
                            width="100%", spacing="1",
                        ),

                        # Mensajes
                        rx.cond(
                            ContableState.editar_perfil_error != "",
                            rx.hstack(
                                rx.icon(tag="circle-alert", size=13, color="#F56565"),
                                rx.text(ContableState.editar_perfil_error, color="#F56565", size="2"),
                                spacing="1", padding="0.75em",
                                bg="#2D1515", border_radius="8px", width="100%",
                            ),
                        ),
                        rx.cond(
                            ContableState.editar_perfil_exito != "",
                            rx.hstack(
                                rx.icon(tag="circle-check", size=13, color="#48BB78"),
                                rx.text(ContableState.editar_perfil_exito, color="#48BB78", size="2"),
                                spacing="1", padding="0.75em",
                                bg="#152D1F", border_radius="8px", width="100%",
                            ),
                        ),

                        # Botones
                        rx.hstack(
                            rx.button(
                                "Cancelar",
                                on_click=ContableState.cerrar_modal_perfil,
                                variant="ghost", color="#718096", _hover={"color": "#FFFFFF"},
                            ),
                            rx.button(
                                rx.icon(tag="save", size=15),
                                "Guardar Cambios",
                                on_click=ContableState.guardar_cambios_perfil,
                                bg="#3182CE", color="#FFFFFF",
                                _hover={"bg": "#2B6CB0"},
                            ),
                            spacing="3", justify="end", width="100%",
                        ),

                        spacing="4", width="100%",
                    ),
                    padding="2em",
                    bg="#1A202C", border_radius="2xl",
                    border="1px solid #4A5568",
                    width="560px",
                ),
                position="fixed", top="0", left="0",
                width="100%", height="100%",
                bg="rgba(0,0,0,0.85)", z_index="1000",
            ),
        ),

        width="100%",
        min_height="100vh",
        bg="#0B0E14",
    )


def _campo_info(icono: str, label: str, valor) -> rx.Component:
    """Campo de solo lectura reutilizable."""
    return rx.vstack(
        rx.text(label, color="#718096", size="1"),
        rx.box(
            rx.hstack(
                rx.icon(tag=icono, size=14, color="#4299E1"),
                rx.text(valor, color="#E2E8F0", size="3"),
                spacing="2", align="center",
            ),
            bg="#2D3748", border_radius="8px",
            padding="0.6em 1em", width="100%",
        ),
        width="100%", spacing="1",
    )