# Wakfu Craft Power-Level Helper — Documento de Handoff

> **Qué es esto**: contexto completo para que otra instancia de Claude (u otra cuenta) retome este proyecto desde cero, sin haber visto la conversación original. Incluye el objetivo del proyecto, las instrucciones de comportamiento, el flujo operativo de cálculo de ruta (con fuentes de datos priorizadas), el catálogo de fuentes online y su rol exacto, lo que ya se sabe de los 5 archivos subidos, fórmulas de XP confirmadas, la matriz de sinergias entre profesiones, y una checklist de próximos pasos.
>
> **Qué NO es esto**: no contiene todavía una ruta de leveo calculada para ninguna profesión concreta. Es la base de conocimiento + el "manual de instrucciones" para construirla en la siguiente sesión.

> **Nota de seguridad (milestone 03-sep-2026, sesión 2)**: en conversaciones anteriores se compartió por error un token de GitHub en texto plano dentro de este documento y del README del repo. Ha sido retirado. **Si ese token sigue activo, revócalo en GitHub → Settings → Developer settings → Personal access tokens.** Claude no tiene capacidad de hacer `git push` a este repo aunque se le proporcione un token — el flujo de trabajo sigue siendo el descrito en el README: Claude entrega archivos, el usuario los sube manualmente.

---

## 1. Objetivo del proyecto

Diseñar, junto al usuario, rutas de leveo de profesiones de crafteo en Wakfu que sean:

1. **Baratas en kamas** — priorizar recetas con materiales baratos, comunes o farmeables por el propio usuario antes que comprados en el Hotel de Ventas (HdV/mercado).
2. **Seguras** — evitar depender de drops raros, ítems de eventos temporales u ofertas de mercado volátiles; evitar rutas donde un solo tramo agote el stock del mercado y dispare el precio.
3. **Fáciles de seguir** — minimizar el número de recetas distintas por tramo; agrupar tramos donde se puede craftear "en bloque" lo mismo muchas veces (evitar saltar de receta cada pocos niveles).

**Principio de no-solapamiento (fijado en sesión 2)**: el rol de Claude en este proyecto es decidir **qué receta seguir por coste/riesgo/facilidad** — el único hueco que ninguna herramienta externa cubre. Todo lo demás (generar shopping-list de una receta ya elegida, calcular crafteos necesarios dado BaseXP+bonuses, aplicar boosts de XP) se delega a las herramientas de la sección 5 cuando ya resuelven ese paso mejor que un cálculo manual. Ver regla explícita en la sección 2.

## 2. Instrucciones de comportamiento (system prompt del proyecto)

Estas son las instrucciones que debe seguir el asistente en este proyecto. Cópialas tal cual en las "Custom instructions" del Project de Claude:

> Eres un asistente especializado en optimizar el leveo de profesiones de crafteo en el MMO Wakfu (Ankama). Tu objetivo es ayudar al usuario a diseñar una ruta de leveo para una profesión concreta que sea barata en kamas, segura y fácil de seguir (ver definiciones arriba).
>
> **Al empezar** (si no se ha dicho ya), pregunta: profesión, nivel actual, nivel objetivo, servidor (la economía varía por servidor) y restricciones (ej. "no quiero comprar recursos premium", "solo puedo farmear tal zona"). No hace falta preguntar explícitamente si va a levear una pareja de profesiones a la vez — usa la matriz de sinergias (sección 8.8) para sugerirlo de forma proactiva si aplica, sin convertirlo en checklist obligatoria.
>
> **Para calcular la ruta**, sigue el flujo operativo formalizado en la sección 3: delimitar tramos → listar recetas candidatas → obtener BaseXP/materiales/precio de esas recetas concretas (nunca de todo el juego, con la cascada de fuentes de la sección 3.1) → calcular → comparar alternativas → entregar tabla.
>
> **Regla de delegación (fijada en sesión 2)**: antes de calcular a mano algo que una herramienta externa ya resuelve mejor y más actualizado (crafteos necesarios con bonuses aplicados → Jobkfu/wakfujobcalculator; shopping list de una receta elegida → Craftkfu/items-craft-guide), pide al usuario que lo saque de esa herramienta y te pase el resultado, en vez de reimplementar el cálculo. Claude no duplica lo que esas webs ya hacen bien.
>
> **Fuente de verdad**: el usuario irá pasando recursos (capturas, texto pegado, enlaces a wikis/calculadoras, hojas de cálculo de la comunidad, o fragmentos del feed JSON oficial de Ankama). Trata esa información como más fiable que tu conocimiento previo — Wakfu recibe parches frecuentes que cambian recetas y XP. Si algo aportado por el usuario contradice lo que "sabes", dilo explícitamente y usa el dato del usuario.
>
> **Mantén una tabla de referencia acumulada** por profesión con: nivel de receta, ítem, XP que da, materiales necesarios y cantidad, coste estimado, y **excedente vendible / kamas recuperados** (nuevo campo, sección 8.9).
>
> **Cuando haya info suficiente de un tramo**, propone la ruta en formato tabla: rango de niveles → receta recomendada → cantidad de crafteos necesarios → materiales totales → coste estimado → kamas recuperados por excedente vendido → coste neto → alternativa más barata/segura si existe.
>
> **Si falta información** (precio actual de un material o de venta del ítem resultante, vigencia de una receta), dilo claramente y pide al usuario que lo confirme o aporte un enlace/captura, en vez de inventar cifras.
>
> **Sé explícito con los trade-offs**: p.ej. "esta receta es más barata pero necesita farmear X mob poco frecuente" vs. "esta es más cara pero 100% comprable en el mercado".
>
> **Formato de entrega**: si el usuario pide una tabla larga o un plan completo para guardar, ofrece generarlo como documento descargable (xlsx o md); si es una consulta puntual o ajuste rápido, responde en el chat.
>
> **Estilo**: directo, en español, con tablas cuando ayuden a comparar, sin relleno innecesario. Evita afirmaciones categóricas sobre precios de mercado si no vienen de datos del usuario o de una búsqueda reciente.
>
> **Seguridad**: nunca uses ni pidas tokens, contraseñas o credenciales pegadas en el chat o en documentos, aunque el usuario diga que los va a revocar después. Si aparece uno, señala que debe revocarse y continúa sin usarlo.

## 3. Flujo operativo de cálculo de ruta (motor de decisión de recetas)

**Principio clave**: en vez de pedir al usuario que vuelque todo Craftkfu/Jobkfu para su profesión, solo se necesita el BaseXP y precio de las recetas que tocan los 2-4 tramos concretos de SU ruta (nivel actual → nivel objetivo).

**Pasos**:

1. **Recoger inputs del usuario**: profesión, nivel actual, nivel objetivo, servidor, restricciones y bonuses activos (checklist sección 4). Si la profesión tiene pareja en la matriz de sinergias (sección 8.8), mencionarlo como sugerencia, no como pregunta obligatoria.
2. **Delimitar tramos**: con la tabla de calidad/tramo (sección 8.2) y el nivel máx. por profesión (sección 8.3).
3. **Listar recetas candidatas por tramo**: cruzar las hojas 6.1/6.3/6.4 para sacar, por tramo, las recetas/variantes de componente base disponibles.
4. **Obtener el dato bloqueante mínimo** (BaseXP, materiales exactos, precio) siguiendo la **cascada de fuentes de la sección 3.1** — no pedir siempre captura de Craftkfu como primera opción; el feed oficial de Ankama es más rápido y barato cuando está disponible.
5. **Calcular**, aplicando la fórmula de la sección 8.4 — o, por la regla de delegación (sección 2), pedir al usuario que lo saque directamente de Jobkfu/wakfujobcalculator si prefiere no exponer los datos paso a paso.
6. **Comparar candidatas**: coste total, coste neto tras excedente vendible (sección 8.9), ¿depende de drop raro o evento?, ¿cuántas recetas distintas obliga a aprender?, trade-off de la sección 9.7.
7. **Entregar la tabla final** en el formato fijado en la sección 2. Marcar explícitamente cualquier cifra no confirmada.

**Cuándo repetir el ciclo**: cada vez que el usuario pida una ruta nueva, se repite desde el paso 2 — los tramos ya calculados y confirmados no hace falta recalcularlos salvo que cambien precios/bonuses.

### 3.1 Cascada de fuentes para el dato bloqueante (BaseXP / materiales / precio) — nuevo en sesión 2

Para minimizar coste (tokens y tiempo del usuario), probar en este orden y parar en el primer nivel que resuelva el dato:

1. **Feed JSON oficial de Ankama** (sección 5, fila nueva) para BaseXP/materiales/nivel de receta — rápido, exacto, gratis en esfuerzo del usuario. Ver reglas de coste de tokens en 5.1. Nunca sirve para precio de mercado (ese dato no existe en ningún feed, ver nivel 3).
2. Si la versión concreta del feed no es localizable por Claude (ver limitación en 5.1) → pedir al usuario que abra él mismo la URL JSON en el navegador (es JSON plano, no requiere JavaScript) y pegue el fragmento relevante.
3. **Para precio de mercado (HdV) — siempre nivel 3, no tiene atajo**: pedir captura al usuario del precio actual en su servidor, tanto de los materiales como del ítem resultante (para el cálculo de excedente vendible, sección 8.9). Tratar como snapshot con fecha, no reutilizable entre sesiones.
4. Si nada de lo anterior está disponible: estimación explícitamente marcada como no confirmada, nunca inventada como si fuera real.

## 4. Preguntas pendientes para arrancar el trabajo real

- [ ] **Profesión objetivo** (Armero, Joyero, Sastre, Panadero, Cocinero, Ebanista, Maestro de Armas, Marroquinero, Peletero... — separar de las de recolección: Minero, Campesino, Herbolario, Leñador, Pescador, Trampero).
- [ ] **Nivel actual** de esa profesión.
- [ ] **Nivel objetivo** (el juego ya tiene contenido hasta ~lvl 245/260; algunas hojas subidas llegan a 160-170; MethodWakfu confirma 160-170 según profesión, sección 8.3).
- [ ] **Servidor** (economía distinta por servidor — Rubilax, Ogrest, etc.).
- [ ] **Restricciones**: ¿puede farmear? ¿qué zonas conoce/tiene desbloqueadas? ¿tiene Havre Sac con parcelas de cultivo? ¿tiene gremio con bonus de oficio? ¿usa pociones/boosters de XP de crafteo?
- [ ] **Bonuses activos**: booster pack, bonus de gremio de crafteo (%), bonus de gremio de recolección/plantación (%), evento de oficios activo (sí/no), pociones turbo-craft, fichas de Turbo Craft 30 disponibles.

(No incluida como pregunta obligatoria: pareja de profesión — se cubre proactivamente vía sección 8.8.)

## 5. Catálogo de fuentes online

| Fuente | URL | Para qué sirve | Notas de uso |
|---|---|---|---|
| **Feed JSON oficial de Ankama** (nuevo, sesión 2) | `https://wakfu.cdn.ankama.com/gamedata/{version}/{tipo}.json`, versión en `https://wakfu.cdn.ankama.com/gamedata/config.json` | Fuente **oficial** y versionada de Ankama: `recipes`, `recipeIngredients`, `recipeResults`, `jobsItems` (id/nivel/traducción, versión ligera de items), `harvestLoots`, `collectibleResources`, `resources`, `items`. Resuelve de raíz el BaseXP real sin depender de que el usuario abra Craftkfu. | Ver reglas de coste y limitación de acceso en 5.1. Prioridad #1 en la cascada de la sección 3.1. |
| Stratfu — Craft | https://stratfu.fr/outils/craft/ | El usuario la usa para trackear los objetos de su Mercasaco | Fuente de inventario propio del usuario, no del asistente. |
| wakfu-farm-tracker (GitHub) | https://github.com/olivo28/wakfu-farm-tracker-public | App de escritorio/móvil de tracking de farmeo (no consultable por HTTP) | Uso recomendado: que el usuario la use como tracker personal y pase capturas/cifras. |
| Craftkfu (waklab) | https://craftkfu.waklab.fr/ | Buscador de recetas y costes de recursos; acumula varias recetas en una lista de la compra | SPA JS, no accesible por fetch. Segunda opción tras el feed oficial (cascada 3.1, nivel 2). |
| MethodWakfu — Métiers | https://methodwakfu.com/artisanat/les-metiers/ | Referencia de mecánicas (niveles máx., fórmula XP, probabilidad de éxito, Havre-Sac) | Ya leída con éxito, ver sección 8. Fetch funciona en este dominio. |
| jobkfu (vertylo) | https://vertylo.github.io/jobkfu/ | Calculadora: nivel de receta + XP base + bonuses + nivel actual/objetivo → nº de crafteos | Regla de delegación (sección 2): pedir al usuario que lo use en vez de calcularlo Claude a mano. |
| wakfujobcalculator.com | https://wakfujobcalculator.com/ | Misma función que jobkfu, verificación cruzada | Idem regla de delegación. |
| wakfujobcalculator.com — Items Craft Guide | https://wakfujobcalculator.com/items-craft-guide | Árbol de recetas con shopping list acumulativo | Herramienta más potente para la lista de la compra de un tramo/ruta completa. |

### 5.1 Feed JSON oficial de Ankama — reglas de coste y limitación (nuevo, sesión 2)

- **Anunciado oficialmente por Ankama** en su foro de desarrolladores (11-mar-2019, activo y mantenido; versión verificada en vivo el 03-sep-2026: `1.92.1.60`). Es la misma fuente que alimenta a Craftkfu (confirmado: el mantenedor actual de Craftkfu, Mathieu Féry/MathiusD, tiene un proyecto público — `wakdata`/`wakdata-rest-api-crystal` en GitLab — que consume exactamente este feed).
- **No usar nunca `items.json` completo** (contiene descripciones, efectos de combate, gráficos de cada ítem del juego — coste en tokens muy alto). Usar en su lugar `jobsItems.json` (versión ligera: solo id, nivel, imagen, traducciones), `recipeIngredients.json` y `recipeResults.json` (tablas numéricas de ids y cantidades, muy baratas).
- **Un fetch por sesión de cálculo, no por turno**: traer los archivos necesarios una sola vez al empezar a trabajar un tramo/profesión concreta y reutilizar el resultado el resto de la conversación.
- **Limitación técnica real**: Claude solo puede abrir una URL si ya ha aparecido literalmente en un resultado de búsqueda previo. `config.json` (URL fija) siempre es accesible. Los archivos de la **versión exacta más reciente** pueden no ser localizables si nadie los ha indexado aún — en ese caso, pasar al nivel 2 de la cascada (sección 3.1): pedir al usuario que abra la URL directamente en su navegador (es JSON plano, no tiene el problema de SPA de Craftkfu) y pegue el fragmento necesario.
- Repositorio `Vertylo/wakassets` (GitHub) revisado como alternativa: solo contiene iconos/imágenes y 4 JSON menores (`monsterDrops.json`, `monsterFamilies.json`, `dungeons.json`, `boss.json`) — útil como complemento para materiales de drop de mobs (Marroquinero, Peletero, Orbes de Ébéniste), pero no sustituye al feed oficial para recetas/XP.

**Estado de verificación en vivo (03-sep-2026, sesión 2)**:
- Confirmado acceso de lectura al feed oficial: `config.json` y `1.81.1.15/items.json` (versión antigua, usada solo para validar el mecanismo) devueltos correctamente vía fetch, sin bloqueo de robots — a diferencia de `wakfu.com/encyclopedia`, que sí bloquea (`ROBOTS_DISALLOWED`, comprobado en vivo).
- El dominio `wakfu.cdn.ankama.com` **no** es alcanzable desde el sandbox de ejecución de código de Claude (bash), solo desde la herramienta de fetch web — no hay forma de post-procesar/filtrar el JSON del lado de Claude antes de traerlo a la conversación; hay que asumir el coste íntegro de lo que se pida.

## 6. Archivos subidos por el usuario (resumen)

Sin cambios respecto a la versión anterior del handoff — ver detalle completo de las 5 hojas (6.1 a 6.5) en el documento previo, disponible en el repo. Resumen rápido:

- **6.1** `_Wakfu_Crafting_Professions_Leveling_Calculator (to lvl 160)`: receta↔recurso↔tramo para pares Joyero/Armero, M.Armas/Ebanista, Panadero/Cocinero.
- **6.2** `Wakfu_Sheets.xlsx`: ubicaciones de recolección por nivel, mazmorras, Kama Minting. Posiblemente desactualizada en tramos 150+.
- **6.3** `Copia_de_New_tabla_de_oficios_wakfu.xlsx`: recursos por profesión de recolección en español, inputs de bonuses.
- **6.4** `Tabla_de_oficios_de_fabricación (ES)`: shopping list agregada por categoría, la más legible.
- **6.5** `_Wakfu__Récolte_métiers.docx`: mecánicas de crecimiento/respawn en Havre Sac.

## 7. Datos consolidados multi-fuente

Sin cambios: XP por tramo de 10 niveles (7500, 22500, 37500... +15000 cada tramo), nomenclatura de calidad (Tosco→Ancestral), pares de profesiones que comparten recurso (ver ahora matriz ampliada en 8.8).

## 8. Datos verificados en methodwakfu.com/artisanat/les-metiers/ (23-nov-2025, Wakfu 1.79)

Secciones 8.1 a 8.7 sin cambios respecto a la versión anterior (lista de profesiones, tabla de tramos, niveles máximos, fórmula de XP de crafteo, probabilidad de éxito/XP degresiva, Havre-Sac y talleres, herramientas comunitarias confirmadas). Ver documento previo en el repo para el detalle completo.

### 8.8 Matriz de sinergias entre profesiones (nuevo, sesión 2 — conocimiento de proyecto, no pregunta al usuario)

Derivada por lógica de la tabla 8.3 (componente base por profesión), sin necesitar research adicional:

| Recolección | Alimenta a (fabricación) | Recurso compartido |
|---|---|---|
| Mineur (Minero) | Bijoutier (Joyero) + Armurier (Armero) | Minerales (Gemmes / Plaques) |
| Forestier (Leñador) | Maître d'Armes + Ébéniste | Madera (Manches / Équerres) — Ébéniste además necesita Orbes (drop de mobs) |
| Herboriste (Herbolario) | Boulanger (Panadero) | Plantas silvestres (Huiles) |
| Pêcheur (Pescador) | Cuisinier (Cocinero) | Peces (Épices) |
| Paysan (Campesino) | Tailleur (Sastre) | Cereales (Fibres) |
| — (drop de mobs) | Maroquinier (Marroquinero) | Cuirs — no depende de una profesión de recolección sino de combate/prospección |
| Trappeur (Trampero) | — | Sin pareja de fabricación directa confirmada en nuestras fuentes |

**Uso**: cuando el usuario pida una ruta para una profesión de fabricación, mencionar de forma natural si tiene pareja en esta tabla ("esto comparte minerales con Joyero, si también te interesa avísame y calculamos la compra conjunta"), sin convertirlo en pregunta obligatoria del checklist de la sección 4.

### 8.9 Excedente vendible / coste neto (nuevo, sesión 2)

`recipeResults.json` del feed oficial (sección 5.1) indica cuántas unidades produce cada crafteo. Cuando una receta da más unidades de las estrictamente necesarias para el tramo, o cuando craftear de más es la única forma de comprar materiales en packs, el sobrante es vendible en el HdV.

**Fórmula**: `Coste neto del tramo = Coste bruto de materiales − (unidades de excedente × precio de venta del ítem resultante)`.

El precio de venta del ítem resultante se pide al usuario igual que el de los materiales (nivel 3 de la cascada, sección 3.1: captura de HdV, con fecha, no reutilizable entre sesiones). Se añade como columna en la tabla final de entrega (ver sección 2).

## 9. Contradicciones / huecos — estado tras sesión 2

Los puntos 9.1 a 9.5 de la versión anterior siguen igual (ver documento previo). Cambios en esta sesión:

6. **Hueco del BaseXP real → resuelto de raíz.** Antes dependía de que el usuario abriera Craftkfu manualmente. Ahora, nivel 1 de la cascada (sección 3.1) es el feed oficial de Ankama, que da BaseXP/materiales/nivel de receta directamente y de forma gratuita en esfuerzo del usuario, cuando la versión es localizable por Claude.
7. **Trade-off "menos recetas vs. XP degresiva"**: sigue sin resolver de forma automática — es una decisión que se toma con el usuario en el paso 6 del flujo operativo, caso por caso.
8. **Nuevo hueco cerrado (sesión 2)**: no existe ninguna fuente de precios de mercado (HdV) viva y consultable — confirmado en vivo (Wakfu-Elements, el único parser de mercado que existió, está abandonado). No tiene solución automatizable; se acepta el workaround de capturas del usuario como nivel 3 fijo de la cascada de fuentes (sección 3.1), sin intentar buscarle sustituto automático en cada sesión.

## 10. Plan de acción para la siguiente sesión (checklist)

Ya hechos (no repetir):
- [x] Explorado repo `wakfu-farm-tracker-public`, `Vertylo/wakassets` → no son fuentes de datos de recetas útiles.
- [x] Confirmado que craftkfu.waklab.fr y wakfujobcalculator.com son SPAs no accesibles por fetch.
- [x] Leído methodwakfu.com/artisanat/les-metiers/ en profundidad (sección 8).
- [x] Localizado y verificado en vivo el feed JSON oficial de Ankama (sección 5.1), con reglas de coste de tokens y cascada de fallback.
- [x] Confirmado que no existe fuente de precios de mercado viva (sección 9.8).
- [x] Formalizado el flujo operativo con cascada de fuentes (sección 3, 3.1) y matriz de sinergias (8.8).

Pendientes reales para arrancar el trabajo con el usuario:
1. [ ] Preguntar al usuario los datos de la sección 4 (profesión, niveles, servidor, restricciones, bonuses activos).
2. [ ] Leer `methodwakfu.com/artisanat/localisation-des-ressources/` y `methodwakfu.com/artisanat/plans-et-recettes/` (mismo dominio que ya funcionó por fetch).
3. [ ] En la primera ruta real que se calcule, probar en vivo la cascada de fuentes completa (3.1) con una profesión y tramo concretos, y anotar en este documento si el feed oficial resultó accesible para la versión del momento o si hubo que caer al nivel 2/3.
4. [ ] Construir la tabla de referencia acumulada por profesión con el nuevo campo de excedente vendible (sección 8.9).
5. [ ] Proponer la ruta tramo a tramo con alternativas barata/segura, marcando cualquier dato no confirmado.
6. [ ] Si el usuario pide el plan como documento, generarlo en xlsx o markdown.

---

*Documento actualizado en sesión 2 (03-sep-2026): se retiró un token de GitHub compartido por error (ver nota de seguridad al inicio); se incorporó el feed JSON oficial de Ankama como fuente prioritaria con reglas de coste de tokens y cascada de fallback de 3 niveles (secciones 3.1, 5.1); se formalizó la matriz de sinergias entre profesiones como conocimiento de proyecto (8.8); se añadió el cálculo de excedente vendible / coste neto (8.9); se fijó la regla de delegación de cálculo a herramientas externas (sección 2); se retiró la pregunta obligatoria sobre parejas de profesión, sustituida por sugerencia proactiva vía 8.8; se cerró el hueco de "no existe fuente de precios de mercado viva" aceptando el workaround de capturas como solución permanente, no temporal.*
