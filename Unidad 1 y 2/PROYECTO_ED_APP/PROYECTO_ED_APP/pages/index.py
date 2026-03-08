#   //////////////////////////#
#  //      FRONT-END       // #
# //////////////////////////  #
#index.py

import reflex as rx
from ..state import ContableState # <--- El backend

#    main_folder    |folder| file    |      funcion
from PROYECTO_ED_APP.componentes.dashboard import vista_dashboard
from PROYECTO_ED_APP.componentes.historial import vista_historial, modal_editar_transaccion
from PROYECTO_ED_APP.componentes.contable import vista_contable
from PROYECTO_ED_APP.componentes.inventario import vista_inventario
from PROYECTO_ED_APP.componentes.login import vista_login, modal_recuperacion_contrasena
from PROYECTO_ED_APP.componentes.sidebar import sidebar
from PROYECTO_ED_APP.componentes.vista_usuarios import vista_usuarios
from PROYECTO_ED_APP.componentes.cuentas import vista_cuenta
from PROYECTO_ED_APP.componentes.buscador import vista_buscador


# ================================
# PÁGINA PRINCIPAL
# ================================
@rx.page(on_load=ContableState.on_load)
def index() -> rx.Component:
    return rx.fragment(
        rx.box(
            rx.cond(
                ContableState.usuario_logueado,
                rx.hstack(
                    sidebar(),
                    rx.box(
                        rx.cond(
                            ContableState.pestana_actual == "dashboard",
                            vista_dashboard(),
                            rx.cond(
                                ContableState.pestana_actual == "contable",
                                vista_contable(),
                                rx.cond(
                                    ContableState.pestana_actual == "historial",
                                    vista_historial(),
                                        rx.cond(
                                            ContableState.pagina_actual== "buscador",
                                            vista_buscador(),
                                            rx.cond(
                                            ContableState.pestana_actual == "usuarios",
                                            vista_usuarios(),
                                            rx.cond(
                                                ContableState.pestana_actual == "cuenta",
                                                vista_cuenta(),
                                                vista_inventario(),
                                            )
                                            )
                                        )
                                )
                            )
                        ),
                        width="100%",
                    ),
                    width="100%",
                    min_height="100vh",
                    align="start",
                ),
                vista_login(),
            ),
            width="100%",
        ),
        # Modales globales
        modal_recuperacion_contrasena(),
        modal_editar_transaccion(),
    )