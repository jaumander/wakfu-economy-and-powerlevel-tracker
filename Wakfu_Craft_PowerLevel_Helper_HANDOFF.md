Handoff — Proyecto rutas de leveo Wakfu (v5, unificado, 03-sep-2026)

Qué es esto: documento único de contexto para que cualquier instancia de Claude (u otra cuenta) retome este proyecto desde cero. Sustituye y fusiona a los dos documentos anteriores:

Wakfu_Craft_PowerLevel_Helper_HANDOFF.md (sesión 2)
handoff_wakfu_leveling_v4.md (sesión 4)

A partir de ahora usar solo este archivo. Los otros dos se solapaban en gran parte de su contenido (objetivo, system prompt, mecánicas del juego, matriz de sinergias) y el de sesión 4 ya declaraba sustituir parcialmente al de sesión 2 en la parte de fuentes de datos. Este documento resuelve ambos solapamientos en un único texto sin contradicciones.

Qué NO es esto: no contiene todavía una ruta de leveo terminada para ninguna profesión. Ebanista 0→30 está a medio resolver (faltan precios de mercado, ver sección 6).

⚠️ Nota de seguridad (recurrente — leer primero)

Un token de GitHub se ha compartido por error en texto plano en más de una ocasión en este proyecto (documentado ya en los handoffs de sesión 2 y sesión 4, y ha vuelto a ocurrir en la sesión donde se creó este documento unificado). Ninguno de esos tokens se ha usado ni se guarda en este archivo.

Si compartiste un token de GitHub en el chat, revócalo ahora: GitHub → Settings → Developer settings → Personal access tokens → Revoke.

Regla permanente del proyecto: Claude nunca usa ni pide tokens, contraseñas o credenciales pegadas en el chat o en documentos, aunque el usuario diga que los va a revocar después. Si aparece uno, se señala que debe revocarse y se continúa sin usarlo. Claude no tiene capacidad de hacer git push a ningún repo aunque se le dé un token — el flujo de trabajo es siempre: Claude entrega archivos descargables, el usuario los sube manualmente donde corresponda (botón "Add file → Upload files" en GitHub, sin terminal).

1. Objetivo del proyecto

Diseñar, junto al usuario, rutas de leveo de profesiones de crafteo en Wakfu que sean:

Baratas en kamas — priorizar recetas con materiales baratos, comunes o farmeables por el propio usuario antes que comprados en el Hotel de Ventas (HdV/mercado).
Seguras — evitar depender de drops raros, ítems de eventos temporales u ofertas de mercado volátiles; evitar rutas donde un solo tramo agote el stock del mercado y dispare el precio.
Fáciles de seguir — minimizar el número de recetas distintas por tramo; agrupar tramos donde se puede craftear "en bloque" lo mismo muchas veces.

Principio de no-solapamiento: el rol de Claude es decidir qué receta seguir por coste/riesgo/facilidad — el único hueco que ninguna herramienta externa cubre. Todo lo demás (generar shopping-list de una receta ya elegida, calcular crafteos necesarios dado BaseXP+bonuses, aplicar boosts de XP) se delega a las herramientas de la sección 7 cuando ya resuelven ese paso mejor que un cálculo manual (ver regla explícita abajo).

2. Instrucciones de comportamiento (system prompt del proyecto)

Copiar tal cual en las "Custom instructions" del Project de Claude:

Eres un asistente especializado en optimizar el leveo de profesiones de crafteo en el MMO Wakfu (Ankama). Tu objetivo es ayudar al usuario a diseñar una ruta de leveo para una profesión concreta que sea barata en kamas, segura y fácil de seguir (ver definiciones arriba).

Al empezar (si no se ha dicho ya), pregunta: profesión, nivel actual, nivel objetivo, servidor (la economía varía por servidor) y restricciones (ej. "no quiero comprar recursos premium", "solo puedo farmear tal zona"). No hace falta preguntar explícitamente si va a levear una pareja de profesiones a la vez — usa la matriz de sinergias (sección 8.8) para sugerirlo de forma proactiva si aplica, sin convertirlo en checklist obligatoria.

Para calcular la ruta, sigue el flujo operativo de la sección 3: delimitar tramos → listar recetas candidatas → obtener BaseXP/materiales exactos de esas recetas concretas vía el extractor de datos (sección 4, nunca a mano ni de todo el juego) → calcular → comparar alternativas → entregar tabla.

Regla de delegación: antes de calcular a mano algo que una herramienta externa ya resuelve mejor y más actualizado (crafteos necesarios con bonuses aplicados → Jobkfu/wakfujobcalculator; shopping list de una receta elegida → Craftkfu/items-craft-guide), pide al usuario que lo saque de esa herramienta y te pase el resultado, en vez de reimplementar el cálculo.

Fuente de verdad: el usuario irá pasando recursos (JSON del feed oficial de Ankama, capturas de precios, hojas de cálculo de la comunidad). Trata esa información como más fiable que tu conocimiento previo — Wakfu recibe parches frecuentes que cambian recetas y XP. Si algo aportado por el usuario contradice lo que "sabes", dilo explícitamente y usa el dato del usuario.

Mantén una tabla de referencia acumulada por profesión con: nivel de receta, ítem, XP que da, materiales necesarios y cantidad, coste estimado, y excedente vendible / kamas recuperados (sección 8.9).

Cuando haya info suficiente de un tramo, propone la ruta en formato tabla: rango de niveles → receta recomendada → cantidad de crafteos necesarios → materiales totales → coste estimado → kamas recuperados por excedente vendido → coste neto → alternativa más barata/segura si existe.

Si falta información (precio actual de un material o de venta del ítem resultante, vigencia de una receta), dilo claramente y pide al usuario que lo confirme, en vez de inventar cifras.

Sé explícito con los trade-offs: p.ej. "esta receta es más barata pero necesita farmear X mob poco frecuente" vs. "esta es más cara pero 100% comprable en el mercado".

Formato de entrega: si el usuario pide una tabla larga o un plan completo para guardar, ofrece generarlo como documento descargable (xlsx o md); si es una consulta puntual o ajuste rápido, responde en el chat.

Estilo: directo, en español, con tablas cuando ayuden a comparar, sin relleno innecesario. Evita afirmaciones categóricas sobre precios de mercado si no vienen de datos del usuario o de una búsqueda reciente.

Seguridad: nunca uses ni pidas tokens, contraseñas o credenciales pegadas en el chat o en documentos, aunque el usuario diga que los va a revocar después. Si aparece uno, señala que debe revocarse y continúa sin usarlo.

3. Flujo operativo de cálculo de ruta

Principio clave: no hace falta volcar todo Craftkfu/Jobkfu para una profesión — solo el BaseXP y precio de las recetas que tocan los 2-4 tramos concretos de la ruta del usuario (nivel actual → nivel objetivo).

Pasos:

Recoger inputs del usuario: profesión, nivel actual, nivel objetivo, servidor, restricciones y bonuses activos (checklist sección 5). Si la profesión tiene pareja en la matriz de sinergias (sección 8.8), mencionarlo como sugerencia, no como pregunta obligatoria.
Delimitar tramos: con la tabla de calidad/tramo (sección 8.2) y el nivel máx. por profesión (sección 8.3).
Listar recetas candidatas por tramo: usando la base de datos ya extraída de la profesión (sección 4) o las hojas de la comunidad (sección 9).
Obtener el dato bloqueante mínimo (BaseXP, materiales exactos, precio) siguiendo la cascada de fuentes de la sección 4.1 — el método por defecto ya no es pedir captura de Craftkfu, es correr el extractor sobre el feed oficial de Ankama.
Calcular, aplicando la fórmula de la sección 8.4 — o, por la regla de delegación (sección 1-2), pedir al usuario que lo saque directamente de Jobkfu/wakfujobcalculator.
Comparar candidatas: coste total, coste neto tras excedente vendible (sección 8.9), ¿depende de drop raro o evento?, ¿cuántas recetas distintas obliga a aprender?
Entregar la tabla final en el formato de la sección 2. Marcar explícitamente cualquier cifra no confirmada.

Cuándo repetir el ciclo: cada vez que el usuario pida una ruta nueva, desde el paso 2 — los tramos ya calculados y confirmados no hace falta recalcularlos salvo que cambien precios/bonuses.

4. Arquitectura de datos (vigente — reemplaza toda la cascada de fuentes anterior para BaseXP/materiales)
4.0 Cómo se llegó aquí (para no repetir investigación ya descartada)

En sesiones anteriores el flujo era: usuario abre Craftkfu → clic en una receta → pasa captura a Claude → Claude la transcribe a mano. Era lento, incompleto y propenso a errores (materiales de varias recetas mezclados en una sola captura).

También se investigó si se podía clonar o inspeccionar Craftkfu (craftkfu.waklab.fr, una SPA que Claude no puede leer por fetch) para extraer su fuente de datos directamente. Se localizó al mantenedor (Mathieu Féry / MathiusD) y sus repos en GitLab (wakdata-rest-api-crystal, wakdata, WakTisanat). Conclusión: no aporta nada nuevo — el propio wakdata confirma que sus datos vienen "from JSON files distributed in Wakfu CDN", exactamente la misma fuente ya conocida, y GitLab renderiza sus archivos con JavaScript igual que Craftkfu, así que tampoco son legibles por Claude ahí. No merece la pena volver a intentar esto: el cuello de botella nunca fue no saber dónde están los datos, sino que Claude no puede abrir URLs no indexadas.

La solución real, confirmada en sesión 4: el usuario sí puede abrir esas URLs sin problema en su propio navegador (JSON plano, sin JavaScript, el bloqueo de indexación no aplica a un humano). Una vez descargados y subidos a Claude, este los procesa con código y extrae TODAS las recetas de una profesión de una vez, con datos exactos.

4.1 Cascada de fuentes para BaseXP / materiales / precio (versión final)
Feed JSON oficial de Ankama, vía descarga manual del usuario + extractor de Claude — método por defecto. El usuario abre en su navegador y guarda con Ctrl+S:
https://wakfu.cdn.ankama.com/gamedata/config.json → da la versión actual del juego (confirmada en vivo, sesión 4: 1.92.1.60).
https://wakfu.cdn.ankama.com/gamedata/{version}/recipes.json (~900 KB)
https://wakfu.cdn.ankama.com/gamedata/{version}/recipeIngredients.json (~4 MB)
https://wakfu.cdn.ankama.com/gamedata/{version}/recipeResults.json (~750 KB)
https://wakfu.cdn.ankama.com/gamedata/{version}/jobsItems.json (~8.7 MB; incluye título + descripción en 4 idiomas — más pesado de lo que documentaba el feed oficial pero sigue siendo manejable, y es la fuente de nombres en español)
Sube esos 4 archivos al chat y Claude corre wakfu_recipe_extractor.py (sección 4.2) sobre ellos. Nunca usar items.json completo (descripciones, efectos de combate, gráficos de cada ítem del juego — coste en tokens muy alto). El jobsItems.json del feed es la versión ligera correcta para esto. Un fetch/descarga por sesión de cálculo, no por turno: traer los archivos una sola vez al empezar a trabajar una profesión y reutilizar el resultado el resto de la conversación.
(Fallback, poco fiable) Intento de fetch directo por Claude. config.json es una URL fija y siempre accesible por Claude. Los archivos de la versión exacta más reciente ({version}/recipes.json, etc.) pueden no ser localizables por Claude si nadie los ha indexado aún — no depender de esto, usar el nivel 1 como método estándar. wakfu.cdn.ankama.com tampoco es alcanzable desde el sandbox de código de Claude (bash), solo desde la herramienta de fetch web.
Precio de mercado (HdV) — siempre manual, no tiene atajo. No existe ninguna fuente viva de precios (confirmado: Wakfu-Elements, el único parser de mercado que existió, está abandonado). Pedir captura al usuario del precio actual en su servidor, tanto de materiales como del ítem resultante (para el excedente vendible, sección 8.9). Tratar como snapshot con fecha, no reutilizable entre sesiones.
Clasificación "farmeable vs. drop de mob": el feed de Ankama no lo distingue directamente en los 4 archivos anteriores. Se infiere por patrón (1 material x1 raro + otro x7 común = probable drop de mob, visto en las Orbes de Ebanista) pero no está confirmado con datos duros. Pendiente de probar: harvestLoots.json y monsterDrops.json (repo Vertylo/wakassets en GitHub — revisado, solo tiene iconos/imágenes y 4 JSON menores: monsterDrops.json, monsterFamilies.json, dungeons.json, boss.json; útil como complemento, no sustituye al feed oficial para recetas/XP).
Si nada de lo anterior está disponible: estimación explícitamente marcada como no confirmada, nunca inventada como si fuera real.
4.2 El script: wakfu_recipe_extractor.py

Cruza los 4 JSON del nivel 1 y produce una tabla limpia: nivel de receta, XP, resultado (ítem + cantidad), materiales (ítem + cantidad), todo con nombres en español, para una profesión y rango de nivel concretos.

Uso normal:

python3 wakfu_recipe_extractor.py \
  --recipes recipes.json --items jobsItems.json \
  --results recipeResults.json --ingredients recipeIngredients.json \
  --category-id 81 --min-level 0 --max-level 160 \
  --output ebanista_recetas.json

Para identificar el categoryId de una profesión que aún no conocemos:

python3 wakfu_recipe_extractor.py --items jobsItems.json \
  --results recipeResults.json --recipes recipes.json \
  --find-category-id "Nombre exacto de un ítem craftable en español"

(usa un ítem que sepas con certeza que pertenece a esa profesión, p.ej. un componente básico, como se hizo con "Orbe tosco" para Ebanista.)

4.3 Mapeo de profesiones → categoryId (ir completando)
categoryId	Profesión	Estado
81	Ebanista	✅ Confirmado (cruzado con 4 ítems conocidos)
76, 77, 78, 79, 80, 83	Candidatos sin confirmar	Por volumen de recetas (132 a 1010) coinciden con perfil de profesión de fabricación, pero no se ha confirmado cuál es cuál
40, 64, 71-75	Sin explorar	Probablemente profesiones de recolección u otras categorías (herramientas, decoración general, etc.)

Para confirmar las que faltan: usar --find-category-id con un ítem conocido de cada profesión (Armero, Joyero, Sastre, Panadero, Cocinero, Maestro de Armas, Marroquinero, Peletero). ~5 minutos por profesión.

4.4 Dónde vive esto de forma persistente

Recomendación para el usuario: subir estos archivos a Project Knowledge / archivos del Proyecto de Claude (no solo al chat), para que estén disponibles en cualquier conversación nueva sin volver a pasarlos:

Este HANDOFF.md
wakfu_recipe_extractor.py (el script, para cuando haya un parche nuevo)
ebanista_recetas_completas.json (base ya procesada: 640 recetas, niveles 0-160, 148 KB)
Los 5 archivos originales de la comunidad (sección 9), en una carpeta sources/ si además se usa el repo de GitHub

Cuando Ankama saque un parche que cambie recetas, basta con repetir la descarga de los 4 JSON de la nueva versión y volver a correr el script — no hace falta rehacer este análisis.

5. Preguntas pendientes para arrancar el trabajo real
 Profesión objetivo (Armero, Joyero, Sastre, Panadero, Cocinero, Ebanista, Maestro de Armas, Marroquinero, Peletero — separar de las de recolección: Minero, Campesino, Herbolario, Leñador, Pescador, Trampero).
 Nivel actual de esa profesión.
 Nivel objetivo (el juego tiene contenido hasta ~lvl 245/260; algunas hojas subidas llegan a 160-170; MethodWakfu confirma 160-170 según profesión, sección 8.3).
 Servidor (economía distinta por servidor — Rubilax, Ogrest, etc.) — sigue pendiente desde la sesión 2.
 Restricciones: ¿puede farmear? ¿qué zonas conoce/tiene desbloqueadas? ¿tiene Havre Sac con parcelas de cultivo? ¿tiene gremio con bonus de oficio? ¿usa pociones/boosters de XP de crafteo?
 Bonuses activos: booster pack (✅ confirmado activo), bonus de gremio de crafteo básico (✅ confirmado activo), bonus de gremio de recolección/plantación (%), evento de oficios activo (sí/no), pociones turbo-craft, fichas de Turbo Craft 30 disponibles.

(No incluida como pregunta obligatoria: pareja de profesión — se cubre proactivamente vía sección 8.8.)

6. Caso de prueba en curso: Ebanista 0→30

Datos ya extraídos y confirmados (ver ebanista_recetas_completas.json filtrado a nivel ≤30, o repetir con --max-level 30):

Nivel	Componente	Materiales	Riesgo
0	Escuadrita tosca	Madera de fresno x5, Madera de avellano x5	Ninguno
5	Orbe tosco	1 drop raro + 7 comunes (3 variantes de mob: jalató/tofu/larva)	Depende de mob
10	Escuadrita rudimentaria	Madera de ñiamzamo x5, Madera de castaño x5	Ninguno
15	Orbe rudimentario	1 raro + 7 comunes (3 variantes de mob)	Depende de mob
20	Escuadrita imperfecta	Madera de boabob x5, Madera de abedul x5	Ninguno
25	Orbe imperfecto	1 raro + 7 comunes (5 variantes de mob — la más flexible)	Depende de mob
30	Escuadrita frágil	Madera de bananaranjo x5, Madera de sauce llorón x5	Ninguno

Patrón confirmado: cada tramo de calidad tiene un componente 100% madera (Escuadrita) y uno con drop de mob (Orbe), ambos dan 450 XP por crafteo.

Preferencias del usuario ya recogidas: compra materiales (no farmea activamente, aunque está abierto a ello si compensa levear Maestro de Armas en paralelo por la sinergia de madera, sección 8.8). Bonuses activos: gremio básico + booster pack.

Falta para cerrar la ruta: precios de mercado de las 8 maderas distintas y de los drops de mob más accesibles para el usuario, en su servidor (pendiente: preguntar servidor, sección 5).

7. Catálogo de fuentes online
Fuente	URL	Para qué sirve	Notas de uso
Feed JSON oficial de Ankama	https://wakfu.cdn.ankama.com/gamedata/{version}/{tipo}.json, versión en .../gamedata/config.json	Fuente oficial y versionada: recipes, recipeIngredients, recipeResults, jobsItems, harvestLoots, resources. Resuelve el BaseXP real.	Ver sección 4.1: método por defecto es descarga manual del usuario + extractor, no fetch directo de Claude.
Stratfu — Craft	https://stratfu.fr/outils/craft/	El usuario la usa para trackear los objetos de su Mercasaco	Fuente de inventario propio del usuario, no del asistente.
wakfu-farm-tracker (GitHub)	https://github.com/olivo28/wakfu-farm-tracker-public	App de tracking de farmeo (no consultable por HTTP)	Que el usuario la use como tracker personal y pase capturas/cifras.
Craftkfu (waklab)	https://craftkfu.waklab.fr/	Buscador de recetas y costes de recursos	SPA JS, no accesible por fetch de Claude. Descartado como fuente estructural (sección 4.0); el usuario puede seguir usándolo manualmente si quiere.
MethodWakfu — Métiers	https://methodwakfu.com/artisanat/les-metiers/	Mecánicas: niveles máx., fórmula XP, probabilidad de éxito, Havre-Sac	Ya leída con éxito (sección 8). Fetch funciona en este dominio.
jobkfu (vertylo)	https://vertylo.github.io/jobkfu/	Nivel de receta + XP base + bonuses + nivel actual/objetivo → nº de crafteos	Regla de delegación (sección 1-2): pedir al usuario que lo use en vez de calcularlo a mano.
wakfujobcalculator.com	https://wakfujobcalculator.com/	Misma función que jobkfu, verificación cruzada	Idem regla de delegación.
wakfujobcalculator.com — Items Craft Guide	https://wakfujobcalculator.com/items-craft-guide	Árbol de recetas con shopping list acumulativo	Herramienta más potente para la lista de la compra de un tramo/ruta completa.
8. Datos verificados en methodwakfu.com/artisanat/les-metiers/ (23-nov-2025, Wakfu 1.79)

Secciones 8.1 a 8.7 (lista de profesiones, tabla de tramos, niveles máximos, fórmula de XP de crafteo, probabilidad de éxito/XP degresiva, Havre-Sac y talleres, herramientas comunitarias confirmadas) — sin cambios, consultar el histórico de la conversación si se necesita el detalle completo; lo relevante para el flujo actual está resumido en las secciones 3, 6 y 8.8-8.9 de este documento.

Datos consolidados de múltiples fuentes: XP por tramo de 10 niveles (7500, 22500, 37500... +15000 cada tramo), nomenclatura de calidad (Tosco→Ancestral).

8.8 Matriz de sinergias entre profesiones

Derivada por lógica del componente base por profesión, conocimiento de proyecto (no se pregunta al usuario):

Recolección	Alimenta a (fabricación)	Recurso compartido
Mineur (Minero)	Bijoutier (Joyero) + Armurier (Armero)	Minerales (Gemmes / Plaques)
Forestier (Leñador)	Maître d'Armes + Ébéniste	Madera (Manches / Équerres) — Ébéniste además necesita Orbes (drop de mobs)
Herboriste (Herbolario)	Boulanger (Panadero)	Plantas silvestres (Huiles)
Pêcheur (Pescador)	Cuisinier (Cocinero)	Peces (Épices)
Paysan (Campesino)	Tailleur (Sastre)	Cereales (Fibres)
— (drop de mobs)	Maroquinier (Marroquinero)	Cuirs — depende de combate/prospección, no de recolección
Trappeur (Trampero)	—	Sin pareja de fabricación directa confirmada

Uso: al calcular una ruta de fabricación, mencionar de forma natural si tiene pareja en esta tabla, sin convertirlo en pregunta obligatoria.

8.9 Excedente vendible / coste neto

recipeResults.json del feed oficial indica cuántas unidades produce cada crafteo. Cuando sobran unidades del tramo, o craftear de más es la única forma de comprar materiales en packs, el sobrante es vendible en el HdV.

Fórmula: Coste neto del tramo = Coste bruto de materiales − (unidades de excedente × precio de venta del ítem resultante).

El precio de venta se pide al usuario igual que el de los materiales (nivel 3 de la cascada, sección 4.1: captura de HdV, con fecha, no reutilizable entre sesiones).

9. Archivos de la comunidad subidos por el usuario (resumen)
9.1 _Wakfu_Crafting_Professions_Leveling_Calculator (to lvl 160).xlsx: receta↔recurso↔tramo para pares Joyero/Armero, M.Armas/Ebanista, Panadero/Cocinero.
9.2 Wakfu_Sheets.xlsx: ubicaciones de recolección por nivel, mazmorras, Kama Minting. Posiblemente desactualizada en tramos 150+.
9.3 Copia_de_New_tabla_de_oficios_wakfu.xlsx: recursos por profesión de recolección en español, inputs de bonuses.
9.4 Tabla_de_oficios_de_fabricación (ES).xlsx: shopping list agregada por categoría, la más legible.
9.5 _Wakfu__Récolte_métiers.docx: mecánicas de crecimiento/respawn en Havre Sac.

Estos 5 archivos siguen siendo un complemento útil (sobre todo para recolección/ubicaciones), pero para BaseXP/materiales exactos de fabricación la fuente de verdad ahora es la arquitectura de la sección 4, no estas hojas.

10. Contradicciones / huecos resueltos y pendientes

Resueltos:

BaseXP real → resuelto de raíz vía sección 4 (feed oficial + script), ya no depende de que el usuario abra Craftkfu manualmente ni de que Claude pueda hacer fetch directo de los JSON versionados.
"Craftkfu local" / scraping del motor de Craftkfu → explorado y descartado con justificación documentada (sección 4.0); no repetir esta investigación.
No existe fuente de precios de mercado (HdV) viva → confirmado (Wakfu-Elements, el único parser que existió, está abandonado). No tiene solución automatizable; se acepta el workaround de capturas del usuario como nivel 3 fijo y permanente de la cascada (sección 4.1), sin buscarle sustituto en cada sesión.

Pendientes:

Trade-off "menos recetas vs. XP degresiva": sigue sin resolver de forma automática — decisión caso por caso con el usuario en el paso 6 del flujo operativo (sección 3).
Clasificación automática "farmeable vs. drop de mob": pendiente de probar harvestLoots.json/monsterDrops.json (sección 4.1, punto 4).
11. Checklist de próximos pasos

Ya hechos (no repetir):

 Explorado repo wakfu-farm-tracker-public, Vertylo/wakassets → no son fuentes de datos de recetas útiles (solo complemento de drops).
 Confirmado que craftkfu.waklab.fr y wakfujobcalculator.com son SPAs no accesibles por fetch de Claude.
 Leído methodwakfu.com/artisanat/les-metiers/ en profundidad (sección 8).
 Localizado y verificado en vivo el feed JSON oficial de Ankama, versión 1.92.1.60.
 Confirmado que "Craftkfu local" no aporta nada nuevo — descartado con justificación documentada (sección 4.0).
 Descubierta y probada la vía de descarga directa del feed por parte del usuario, como método por defecto (sección 4.1).
 Creado wakfu_recipe_extractor.py, script reutilizable (sección 4.2).
 Generada base de datos completa de Ebanista (640 recetas, niveles 0-160) en JSON.
 Identificado categoryId 81 = Ebanista.
 Extraídas y confirmadas las 7 recetas clave del tramo 0-30 de Ebanista con materiales exactos (sección 6).
 Formalizada la matriz de sinergias (8.8) y el cálculo de excedente vendible (8.9) como conocimiento de proyecto.

Pendientes reales:

 Subir este HANDOFF.md, wakfu_recipe_extractor.py y ebanista_recetas_completas.json a Project Knowledge (acción del usuario, fuera del alcance de Claude).
 Preguntar servidor del usuario (pendiente desde sesión 2).
 Pedir precios de mercado de las 8 maderas + drops de mob del tramo 0-30 de Ebanista (única pieza que falta para cerrar esa ruta).
 Calcular en Jobkfu (regla de delegación) el nº de crafteos necesarios con el booster pack + bonus de gremio ya confirmados.
 Entregar tabla final de la ruta Ebanista 0-30 con coste neto.
 Confirmar los categoryId de las 8 profesiones de fabricación restantes usando --find-category-id (~5 min cada una).
 (Opcional, baja prioridad) Descargar harvestLoots.json y monsterDrops.json y explorar si permiten clasificar automáticamente "farmeable vs. drop de mob" en vez de inferirlo por patrón.
 Leer methodwakfu.com/artisanat/localisation-des-ressources/ y methodwakfu.com/artisanat/plans-et-recettes/ (mismo dominio que ya funcionó por fetch).

Documento v5 (03-sep-2026): fusiona y sustituye a Wakfu_Craft_PowerLevel_Helper_HANDOFF.md (sesión 2) y handoff_wakfu_leveling_v4.md (sesión 4). No contiene ningún token ni credencial — ver nota de seguridad al inicio.
