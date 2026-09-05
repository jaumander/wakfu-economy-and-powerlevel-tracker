# Instrucciones del proyecto — The Broker of Wakfu Street

## Changelog (para saber si la copia subida al proyecto está desactualizada)

- 2026-08-12: Versión inicial — vigía/snapshots, tendencias/alertas, mis ventas, cuaderno de nichos.
- 2026-08-12: Renombrado de "Krosly Ledger" a "The Broker of Wakfu Street".
- 2026-08-12: Añadido export/import de datos (botones "Exportar datos" / "Importar datos", backup en `.json`).
- 2026-08-15: Corregido bug de duplicados al guardar snapshot dos veces el mismo día (ahora actualiza en vez de duplicar). Añadida validación anti-negativos en precio/cantidad. Añadido resumen rápido (objetos vigilados / actualizados hoy / último snapshot) en la pestaña Vigía.
- 2026-08-15: Incrustado catálogo oficial de Ankama (solo equipamiento, 8.400 objetos, ~400 KB) para autocompletar nombre + categoría al añadir a la lista de vigilancia. Pendiente: añadir recursos/materias primas (resources.json) cuando el usuario suba ese archivo — no cubierto todavía.
- 2026-08-15: Encontrada y añadida la fuente correcta de recursos/materias primas: jobsItems.json (no resources.json, que es solo los árboles/nodos de recolección). Fusionado con el catálogo de equipamiento y deduplicado por nombre+categoría → catálogo final de 6.734 objetos únicos, 346 KB, cubre Equipables + Recursos + Cosechas + Componentes.
- 2026-08-15: Evaluado states.json para cubrir disfraces/cosméticos — descartado: sin campo de categoría, mezclado con estados de combate no relacionados. Monturas/familiares no están expuestos públicamente por Ankama en ningún tipo JSON documentado ni descubierto. Cobertura de catálogo se considera suficiente para el caso de uso real (Equipables + Recursos).
- 2026-08-15: Sustituido el campo de texto libre "Categoría" por un desplegable con la jerarquía oficial exacta del filtro "Tipos" del Mercadillo (8 grupos, capturas aportadas por el usuario). Añadido CAT_MAP para traducir las categorías internas de Ankama a esta jerarquía oficial y autorrellenar el desplegable al elegir un objeto del catálogo. Categorías internas sin correspondencia clara (p. ej. "Decoración de sala mercante") se dejan sin mapear intencionadamente en vez de adivinar.
- 2026-08-15 (auditoría): Se detectó que el cambio anterior (desplegable de categorías) nunca se aplicó realmente — un str_replace había fallado silenciosamente en la sesión previa y no se reintentó, dejando el `<select id="wl-cat">` vacío de opciones (nadie podía elegir categoría, ni manual ni automáticamente). Corregido y verificado por extracción directa del archivo (no solo por lectura del diff). Auditoría completa del resto del archivo: sin IDs de HTML huérfanos, sin funciones `render*` referenciadas sin definir. Lección para futuras sesiones: tras cualquier str_replace, si la herramienta devuelve error, no asumir que un intento posterior lo resolvió sin volver a verificar con grep/vista directa del archivo final.

Cuando termines una sesión con cambios, añade una línea nueva aquí antes de entregar el `.html` final, con la fecha y un resumen de una línea. Así el usuario puede comparar rápido si la copia que tiene subida al proyecto sigue vigente.


Este proyecto es una herramienta de rastreo de economía para Wakfu ("The Broker of Wakfu Street"): lista de vigilancia de objetos, snapshots manuales de precio/cantidad del Mercadillo, historial de ventas propias y un cuaderno de ideas de nicho. Vive en un único archivo HTML/JS con almacenamiento persistente vía `window.storage` — no hay repo de GitHub, no hay dataset externo que descargar ni parsear.

## Cómo continuar el proyecto en una sesión nueva

No hay `git clone`. El equivalente aquí es:

1. El usuario sube de nuevo el archivo `.html` (lo tiene descargado localmente) — léelo con `view` antes de tocar nada, nunca asumas su contenido de memoria de sesiones pasadas.
2. Si el usuario menciona que puede haber perdido datos (cuenta nueva, navegador distinto), pídele el `.json` de "Exportar datos" y ofrécele restaurarlo vía el botón "Importar datos" del propio HTML — no hay forma de que tú, como modelo, leas o escribas directamente ese storage; solo el usuario puede hacerlo desde la interfaz.
3. No existe un `HANDOFF.md` separado. Si una tarea queda a medias, dilo explícitamente al usuario en el chat (qué falta, qué archivo tocar) en vez de dejarlo implícito — la continuidad depende de que el usuario guarde bien el `.html`, no de un archivo de estado.

## Principio de seguridad (no negociable)

Esta herramienta existe precisamente porque el usuario no quiere arriesgar el baneo de su cuenta. Por tanto:

- Nunca propongas ni implementes lectura de memoria del juego, automatización de clics, scraping de pantalla en tiempo real, ni nada que interactúe con el proceso de Wakfu mientras corre.
- Toda entrada de datos de mercado (precio, cantidad, ventas) es y debe seguir siendo manual, tecleada por el usuario cuando él ya está mirando la interfaz del juego por su cuenta.
- Si en algún momento se te ocurre una forma de "automatizar" la recogida de datos para hacerlo más cómodo, para — ese es exactamente el tipo de atajo que este proyecto existe para evitar.

## Verificación antes de asumir

El Mercadillo del juego puede cambiar de columnas, filtros o comportamiento entre parches, igual que el JSON de Ankama puede cambiar de esquema. Antes de asumir un campo nuevo (p. ej. "cantidad de vendedores", "nivel mínimo/máximo", una columna que no hemos visto):

- Pide una captura de pantalla actualizada de esa parte de la interfaz antes de programar el parser o el formulario correspondiente.
- No asumas nombres de campo "porque suena lógico" ni por lo que ya viste en capturas antiguas si ha pasado tiempo — el juego se actualiza.

## Metodología de edición

- El HTML es de un solo archivo. Para cambios puntuales (texto, color, una función), usa `str_replace` sobre las líneas exactas que cambian — nunca regeneres el archivo entero salvo que la estructura cambie de forma sustancial.
- Si el usuario pide varias modificaciones seguidas, agrúpalas: aplica todos los `str_replace` primero y llama a `present_files` una sola vez al final, no tras cada cambio individual.
- Antes de entregar cualquier cambio de lógica (no solo estético), repasa mentalmente el flujo de datos: ¿qué se lee de `window.storage`, qué se escribe, qué se re-renderiza? Un error de guardado silencioso es peor que uno visible.
- Da siempre un contexto breve en lenguaje no técnico de qué cambió y por qué, igual que en wakfu-gear-compare — el usuario no necesita el diff, necesita saber qué esperar al abrir la herramienta.
- Piensa en gastar pocos tokens: prioriza ediciones quirúrgicas sobre reescrituras completas.

## Esquema de datos (para no romper nada al editar)

Cuatro claves en `window.storage`, todas `shared:false`, cada una un array JSON:

- `watchlist`: `{id, name, cat}`
- `snapshots`: `{id, itemId, date, price, qty}` — `price`/`qty` pueden ser `null` si el usuario solo rellenó uno de los dos
- `sales`: `{id, name, price, sold, date}`
- `journal`: `{id, date, tag, text}`

Si añades un campo nuevo a cualquiera de estas formas, hazlo opcional (con fallback razonable al leer) para no romper datos ya guardados por el usuario ni el import/export.

## Sistema de diseño (mantener consistencia)

- Fondo tinta `#14171c`, paneles `#1b1f26` / `#20252d`, línea `#2c323c`.
- Acento principal (kamas, precios): oro apagado `#c9a227`. Acento secundario (cantidad/oferta): verde-teal `#3a8a76`.
- Subida de precio / oportunidad: `#5fa777`. Bajada / aviso: `#c1554b`.
- Tipografía: `Fraunces` para títulos, `IBM Plex Sans` para cuerpo, `IBM Plex Mono` (tabular) para cualquier número — kamas, cantidades, fechas en tablas. No mezclar fuentes fuera de estos tres roles.
- Nada de gradientes decorativos ni animaciones de carga innecesarias — es una herramienta de trabajo, no una landing page.

## Antes de entregar

Repasa el archivo completo mentalmente (o con `view`) tras cualquier edición de lógica, comprobando que las funciones `render*` referenciadas existen y que no queda ningún `id` de HTML sin su selector correspondiente en JS. No hay entorno de navegador en este sandbox para ejecutar el JS de verdad — la validación es por lectura cuidadosa, así que sé especialmente riguroso antes de decir que algo "ya funciona".
