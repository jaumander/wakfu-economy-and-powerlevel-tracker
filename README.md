Wakfu Craft Leveling Optimizer — contexto para Claude

Este repo existe para que cualquier cuenta de Claude (Claude.ai, Projects, etc.) pueda retomar este proyecto sin perder el contexto acumulado, aunque cambie de conversación o de cuenta.

Cómo usar este repo con Claude
Sube (o enlaza) el contenido de HANDOFF.md al iniciar una conversación nueva — es el documento de contexto completo: objetivo del proyecto, system prompt, fuentes online, resumen de los excels/docx de referencia, datos ya verificados y checklist de próximos pasos.
Si tienes los 5 archivos originales (_Wakfu_Crafting_Professions_Leveling_Calculator__to_lvl_160__.xlsx, Wakfu_Sheets.xlsx, Copia_de_New_tabla_de_oficios_wakfu.xlsx, Tabla_de_oficios_de_fabricación__ES_.xlsx, _Wakfu__Récolte_métiers.docx), súbelos también en la carpeta sources/ de este repo — Claude no puede leerlos si no están en el repo o adjuntos al chat.
Pide a Claude explícitamente: "Lee HANDOFF.md de este repo y retoma el proyecto Wakfu Craft Leveling Optimizer desde donde lo dejamos."
Qué es el proyecto

Diseñar rutas de leveo de profesiones de crafteo en Wakfu que sean:

Baratas en kamas (priorizar materiales farmeables/baratos sobre comprados).
Seguras (evitar drops raros, eventos temporales, ofertas volátiles de mercado).
Fáciles de seguir (pocas recetas distintas, craftear en bloque).

Ver el detalle completo, el "system prompt" del asistente y todo lo ya investigado en HANDOFF.md.

Estado actual (resumen rápido)
✅ Mecánicas de crafteo (fórmula de XP, niveles máximos por profesión, probabilidad de éxito) verificadas contra methodwakfu.com (fuente actualizada nov-2025).
✅ 5 hojas/documentos de la comunidad ya analizados y resumidos.
⚠️ Pendiente: BaseXP real de recetas concretas (hay que sacarlo de Craftkfu a mano, es una SPA que Claude no puede leer por fetch).
⚠️ Pendiente: elegir profesión, nivel actual/objetivo, servidor y restricciones del usuario antes de calcular una ruta real.
Limitación importante

Claude no puede hacer git push a este repo (no tiene tus credenciales de GitHub). El flujo de trabajo es:

Claude te da los archivos actualizados (markdown, xlsx, etc.) para descargar.
Tú los subes manualmente a este repo (botón "Add file → Upload files" en GitHub, sin necesitar terminal).
En la siguiente conversación, adjuntas o enlazas el repo actualizado a Claude.
Índice de archivos
Archivo	Contenido
HANDOFF.md	Documento de contexto completo — léelo primero
sources/	(a rellenar por el usuario) copia de los 5 archivos originales de la comunidad
