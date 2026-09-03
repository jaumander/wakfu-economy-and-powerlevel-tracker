Wakfu Craft Leveling Optimizer — contexto para Claude

Este repo existe para que cualquier cuenta de Claude (Claude.ai, Projects, etc.) pueda retomar este proyecto sin perder el contexto acumulado, aunque cambie de conversación o de cuenta.

Cómo usar este repo con Claude
Sube (o enlaza) el contenido de HANDOFF.md al iniciar una conversación nueva — es el documento de contexto completo: objetivo del proyecto, system prompt, arquitectura de datos, herramientas del proyecto, datos ya verificados y checklist de próximos pasos.
Sube también los archivos de datos ya generados (ver Índice de archivos abajo) a Project Knowledge o adjúntalos al chat: las 9 bases de recetas, componentes_intermedios.json, iconos.json y recetario_wakfu.html. Sin ellos, Claude tiene que volver a pedirte los 4 JSON crudos del feed de Ankama y regenerarlo todo desde cero.
Si tienes los 5 archivos originales de la comunidad (Wakfu_Crafting_Professions_Leveling_Calculator__to_lvl_160_.xlsx, Wakfu_Sheets.xlsx, Copia_de_New_tabla_de_oficios_wakfu.xlsx, Tabla_de_oficios_de_fabricación__ES_.xlsx, _Wakfu__Récolte_métiers.docx), súbelos también en la carpeta sources/ de este repo — Claude no puede leerlos si no están en el repo o adjuntos al chat.
Pide a Claude explícitamente: "Lee HANDOFF.md de este repo y retoma el proyecto Wakfu Craft Leveling Optimizer desde donde lo dejamos."
Qué es el proyecto

Diseñar rutas de leveo de profesiones de crafteo en Wakfu que sean:

Baratas en kamas (priorizar materiales farmeables/baratos sobre comprados).
Seguras (evitar drops raros, eventos temporales, ofertas volátiles de mercado).
Fáciles de seguir (pocas recetas distintas, craftear en bloque).

Ver el detalle completo, el "system prompt" del asistente y todo lo ya investigado en HANDOFF.md.

Estado actual (resumen rápido)
✅ Mecánicas de crafteo (fórmula de XP, niveles máximos por profesión, probabilidad de éxito) verificadas contra methodwakfu.com.
✅ 5 hojas/documentos de la comunidad ya analizados y resumidos.
✅ BaseXP y materiales reales de recetas resuelto — ya no depende de sacarlo a mano de Craftkfu. Hay un script (wakfu_recipe_extractor.py) que cruza el feed JSON oficial de Ankama y genera una base de datos limpia por profesión.
✅ Las 9 profesiones de fabricación identificadas y extraídas por completo (Ebanista, Armero, Joyero, Sastre, Panadero, Cocinero, Maestro de Armas, Marroquinero, Peletero) — un archivo *_recetas_completas.json por cada una, más componentes_intermedios.json para los materiales compartidos entre profesiones.
✅ Herramienta propia de exploración y lista de compra: recetario_wakfu.html. Se abre en el navegador, sin instalación; busca recetas, arma una selección y genera la lista de materiales expandiendo sub-recetas automáticamente (con control manual de qué expandir y qué variante de receta usar cuando hay varias).
⚠️ Pendiente: precios de mercado (HdV) — no hay fuente automática, hace falta que el usuario los aporte cuando quiera cerrar una ruta con coste real. Gestión pospuesta a propósito por ahora.
⚠️ Pendiente: elegir profesión, nivel actual/objetivo y restricciones del usuario antes de calcular una ruta real. (El servidor ya no se pregunta — no es relevante para esta herramienta.)

Detalle completo de qué está resuelto y qué falta: sección 10 y 11 de HANDOFF.md.

Limitación importante

Claude no puede hacer git push a este repo (no tiene tus credenciales de GitHub). El flujo de trabajo es:

Claude te da los archivos actualizados (markdown, JSON, HTML, etc.) para descargar.
Tú los subes manualmente a este repo (botón "Add file → Upload files" en GitHub, sin necesitar terminal).
En la siguiente conversación, adjuntas o enlazas el repo actualizado a Claude.
Índice de archivos
Archivo	Contenido
HANDOFF.md	Documento de contexto completo — léelo primero
wakfu_recipe_extractor.py	Script que genera todas las bases de recetas y el mapa de iconos a partir del feed oficial de Ankama
recetario_wakfu.html	Herramienta de exploración de recetas y lista de compra — abrir directamente en el navegador
ebanista_recetas_completas.json	Base de recetas de Ebanista (640, niveles 0-200)
armero_recetas_completas.json	Base de recetas de Armero (966)
joyero_recetas_completas.json	Base de recetas de Joyero (964)
sastre_recetas_completas.json	Base de recetas de Sastre (1010)
marroquinero_recetas_completas.json	Base de recetas de Marroquinero (953)
maestro_armas_recetas_completas.json	Base de recetas de Maestro de Armas (696)
cocinero_recetas_completas.json	Base de recetas de Cocinero (132)
panadero_recetas_completas.json	Base de recetas de Panadero (89)
peletero_recetas_completas.json	Base de recetas de Peletero (49)
componentes_intermedios.json	Materiales base compartidos entre profesiones (Tabla, Hilo, Acero, Harina, Encantártaro) — necesario para que el Recetario expanda las listas de compra del todo
iconos.json	Mapa nombre de ítem → icono, usado por el Recetario
sources/ (a rellenar por el usuario)	copia de los 5 archivos originales de la comunidad
