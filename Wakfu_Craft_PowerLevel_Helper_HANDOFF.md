
# Handoff — Proyecto rutas de leveo Wakfu (v6, 03-sep-2026)

> **Qué es esto**: documento único de contexto para que cualquier instancia de
> Claude (u otra cuenta) retome este proyecto desde cero. **Sustituye** al
> handoff v5 (mismo día). A partir de ahora usar **solo este archivo**.
>
> **Qué cambió respecto a v5** (resumen, detalle en cada sección): las 9
> profesiones de fabricación ya tienen su `categoryId` confirmado y su base
> de recetas completa extraída; existe una herramienta propia,
> `recetario_wakfu.html` (el "Recetario"), que explora recetas y genera
> listas de compra con expansión recursiva, selector manual de variante e
> iconos reales; y **el servidor del usuario deja de preguntarse** — decisión
> explícita del usuario, no es relevante para el alcance de esta herramienta.
>
> **Qué NO es esto**: no contiene todavía una ruta de leveo terminada para
> ninguna profesión. Ebanista 0→30 sigue a medio resolver — lo único que
> falta ya son precios de mercado (ver sección 6), y su gestión está
> pospuesta por decisión explícita del usuario (sección 4.1).


## 1. Objetivo del proyecto

Diseñar, junto al usuario, rutas de leveo de profesiones de crafteo en
Wakfu que sean:

1. **Baratas en kamas** — priorizar recetas con materiales baratos, comunes
   o farmeables por el propio usuario antes que comprados en el Hotel de
   Ventas (HdV/mercado).
2. **Seguras** — evitar depender de drops raros, ítems de eventos
   temporales u ofertas de mercado volátiles; evitar rutas donde un solo
   tramo agote el stock del mercado y dispare el precio.
3. **Fáciles de seguir** — minimizar el número de recetas distintas por
   tramo; agrupar tramos donde se puede craftear "en bloque" lo mismo
   muchas veces.

**Principio de no-solapamiento**: el rol de Claude es decidir **qué receta
seguir por coste/riesgo/facilidad** — el único hueco que ninguna
herramienta externa (ni el Recetario propio) cubre. Todo lo demás (generar
shopping-list de una receta ya elegida con expansión recursiva → Recetario,
sección 4.5; calcular crafteos necesarios dado BaseXP+bonuses → Jobkfu,
sección 7) se delega cuando ya resuelve ese paso mejor que un cálculo
manual (ver regla explícita abajo).

## 2. Instrucciones de comportamiento (system prompt del proyecto)

Copiar tal cual en las "Custom instructions" del Project de Claude:

> Eres un asistente especializado en optimizar el leveo de profesiones de
> crafteo en el MMO Wakfu (Ankama). Tu objetivo es ayudar al usuario a
> diseñar una ruta de leveo para una profesión concreta que sea barata en
> kamas, segura y fácil de seguir (ver definiciones arriba).
>
> **Al empezar** (si no se ha dicho ya), pregunta: profesión, nivel actual,
> nivel objetivo y restricciones (ej. "no quiero comprar recursos premium",
> "solo puedo farmear tal zona"). **No preguntes por el servidor** —
> decisión explícita del usuario, no es relevante para el alcance de esta
> herramienta. No hace falta preguntar explícitamente si va a levear una
> pareja de profesiones a la vez — usa la matriz de sinergias (sección 8.8)
> para sugerirlo de forma proactiva si aplica, sin convertirlo en checklist
> obligatoria.
>
> **Para calcular la ruta**, sigue el flujo operativo de la sección 3:
> delimitar tramos → listar recetas candidatas → obtener BaseXP/materiales
> exactos de esas recetas concretas vía el extractor de datos (sección 4,
> nunca a mano ni de todo el juego) → calcular → comparar alternativas →
> entregar tabla.
>
> **Regla de delegación**: antes de calcular a mano algo que una
> herramienta ya resuelve mejor:
> - **Shopping list de una receta elegida, con expansión recursiva de
>   sub-recetas** → usar el Recetario propio del proyecto
>   (`recetario_wakfu.html`, sección 4.5). Craftkfu queda solo como
>   referencia externa de comparación, ya no como paso obligatorio.
> - **Crafteos necesarios con bonuses de XP aplicados** → pedir al usuario
>   que lo saque de Jobkfu/wakfujobcalculator y te pase el resultado.
>
> No reimplementar estos cálculos a mano.
>
> **Fuente de verdad**: el usuario irá pasando recursos (JSON del feed
> oficial de Ankama, capturas de precios, hojas de cálculo de la
> comunidad). Trata esa información como más fiable que tu conocimiento
> previo — Wakfu recibe parches frecuentes que cambian recetas y XP. Si
> algo aportado por el usuario contradice lo que "sabes", dilo
> explícitamente y usa el dato del usuario.
>
> **Mantén una tabla de referencia acumulada** por profesión con: nivel de
> receta, ítem, XP que da, materiales necesarios y cantidad, coste
> estimado, y excedente vendible / kamas recuperados (sección 8.9).
>
> **Cuando haya info suficiente de un tramo**, propone la ruta en formato
> tabla: rango de niveles → receta recomendada → cantidad de crafteos
> necesarios → materiales totales → coste estimado → kamas recuperados por
> excedente vendido → coste neto → alternativa más barata/segura si existe.
>
> **Si falta información** (precio actual de un material o de venta del
> ítem resultante, vigencia de una receta), dilo claramente y pide al
> usuario que lo confirme, en vez de inventar cifras.
>
> **Sé explícito con los trade-offs**: p.ej. "esta receta es más barata
> pero necesita farmear X mob poco frecuente" vs. "esta es más cara pero
> 100% comprable en el mercado".
>
> **Formato de entrega**: si el usuario pide una tabla larga o un plan
> completo para guardar, ofrece generarlo como documento descargable (xlsx
> o md); si es una consulta puntual o ajuste rápido, responde en el chat.
>
> **Estilo**: directo, en español, con tablas cuando ayuden a comparar, sin
> relleno innecesario. Evita afirmaciones categóricas sobre precios de
> mercado si no vienen de datos del usuario o de una búsqueda reciente.
>


## 3. Flujo operativo de cálculo de ruta

**Principio clave**: no hace falta volcar todo Craftkfu/Jobkfu para una
profesión — solo el BaseXP y precio de las recetas que tocan los 2-4 tramos
concretos de la ruta del usuario (nivel actual → nivel objetivo).

**Pasos**:

1. **Recoger inputs del usuario**: profesión, nivel actual, nivel objetivo,
   restricciones y bonuses activos (checklist sección 5 — **sin
   servidor**). Si la profesión tiene pareja en la matriz de sinergias
   (sección 8.8), mencionarlo como sugerencia, no como pregunta
   obligatoria.
2. **Delimitar tramos**: con la tabla de calidad/tramo (sección 8.2) y el
   nivel máx. por profesión (sección 8.3).
3. **Listar recetas candidatas por tramo**: usando la base de datos ya
   extraída de la profesión (sección 4, hay una por cada una de las 9
   profesiones) — se puede navegar visualmente con el Recetario (sección
   4.5) o las hojas de la comunidad (sección 9).
4. **Obtener el dato bloqueante mínimo** (BaseXP, materiales exactos,
   precio) siguiendo la cascada de fuentes de la sección 4.1 — el método
   por defecto ya no es pedir captura de Craftkfu, es correr el extractor
   sobre el feed oficial de Ankama.
5. **Calcular**, aplicando la fórmula de la sección 8.4 — o, por la regla
   de delegación (sección 1-2), pedir al usuario que lo saque directamente
   de Jobkfu/wakfujobcalculator.
6. **Comparar candidatas**: coste total, coste neto tras excedente vendible
   (sección 8.9 — el Recetario ya calcula el excedente de las sub-recetas
   expandidas automáticamente), ¿depende de drop raro o evento?, ¿cuántas
   recetas distintas obliga a aprender?
7. **Entregar la tabla final** en el formato de la sección 2. Marcar
   explícitamente cualquier cifra no confirmada.

**Cuándo repetir el ciclo**: cada vez que el usuario pida una ruta nueva,
desde el paso 2 — los tramos ya calculados y confirmados no hace falta
recalcularlos salvo que cambien precios/bonuses.

## 4. Arquitectura de datos (vigente — reemplaza toda la cascada de fuentes anterior para BaseXP/materiales)

### 4.0 Cómo se llegó aquí (para no repetir investigación ya descartada)

En sesiones anteriores el flujo era: usuario abre Craftkfu → clic en una
receta → pasa captura a Claude → Claude la transcribe a mano. Era lento,
incompleto y propenso a errores (materiales de varias recetas mezclados en
una sola captura).

También se investigó si se podía clonar o inspeccionar Craftkfu
(`craftkfu.waklab.fr`, una SPA que Claude no puede leer por fetch) para
extraer su fuente de datos directamente. Se localizó al mantenedor
(Mathieu Féry / MathiusD) y sus repos en GitLab (`wakdata-rest-api-crystal`,
`wakdata`, `WakTisanat`). **Conclusión: no aporta nada nuevo** — el propio
`wakdata` confirma que sus datos vienen "from JSON files distributed in
Wakfu CDN", exactamente la misma fuente ya conocida, y GitLab renderiza sus
archivos con JavaScript igual que Craftkfu, así que tampoco son legibles
por Claude ahí. **No merece la pena volver a intentar esto**: el cuello de
botella nunca fue no saber dónde están los datos, sino que Claude no puede
abrir URLs no indexadas.

La solución real: **el usuario sí puede abrir esas URLs sin problema en su
propio navegador** (JSON plano, sin JavaScript, el bloqueo de indexación no
aplica a un humano). Una vez descargados y subidos a Claude, este los
procesa con código y extrae TODAS las recetas de una profesión de una vez,
con datos exactos.

### 4.1 Cascada de fuentes para BaseXP / materiales / precio (versión final)

1. **Feed JSON oficial de Ankama, vía descarga manual del usuario +
   extractor de Claude — método por defecto.** El usuario abre en su
   navegador y guarda con Ctrl+S:
   - `https://wakfu.cdn.ankama.com/gamedata/config.json` → da la versión
     actual del juego (confirmada en vivo dos veces, misma versión ambas:
     **1.92.1.60**. Nota: una captura de Craftkfu en esta sesión mostró
     "1.92.1.58" — Craftkfu va 2 parches por detrás; no es un problema,
     solo una observación).
   - `https://wakfu.cdn.ankama.com/gamedata/{version}/recipes.json` (~900 KB)
   - `https://wakfu.cdn.ankama.com/gamedata/{version}/recipeIngredients.json` (~4 MB)
   - `https://wakfu.cdn.ankama.com/gamedata/{version}/recipeResults.json` (~750 KB)
   - `https://wakfu.cdn.ankama.com/gamedata/{version}/jobsItems.json` (~8.7 MB;
     incluye título + descripción en 4 idiomas, y `graphicParameters.gfxId`
     — este último es lo que usa el Recetario para los iconos, sección 4.5)

   Sube esos 4 archivos al chat y Claude corre `wakfu_recipe_extractor.py`
   (sección 4.2) sobre ellos.

   **Nunca usar `items.json` completo** (descripciones, efectos de combate,
   gráficos de cada ítem del juego — coste en tokens muy alto). El
   `jobsItems.json` del feed es la versión ligera correcta para esto.

   **Un fetch/descarga por sesión de cálculo, no por turno**: traer los
   archivos una sola vez al empezar a trabajar y reutilizar el resultado
   el resto de la conversación.

2. **(Fallback, poco fiable) Intento de fetch directo por Claude.**
   `config.json` es una URL fija y siempre accesible por Claude. Los
   archivos de la versión exacta más reciente (`{version}/recipes.json`,
   etc.) siguen sin ser accesibles por fetch de Claude — confirmado de
   nuevo en sesión 5, no depender de esto.

3. **Precio de mercado (HdV) — siempre manual, no tiene atajo.** No existe
   ninguna fuente viva de precios (confirmado: Wakfu-Elements, el único
   parser de mercado que existió, está abandonado). Pedir captura al
   usuario del precio actual, tanto de materiales como del ítem resultante
   (para el excedente vendible, sección 8.9). Tratar como snapshot con
   fecha, no reutilizable entre sesiones. **Gestión pospuesta**: decisión
   explícita del usuario en sesión 5 — el tema de precios es importante
   pero se resolverá más adelante; no insistir pidiendo capturas hasta que
   el usuario lo saque él mismo.

4. **Clasificación "farmeable vs. drop de mob"**: el feed de Ankama no lo
   distingue directamente. Se infiere por patrón (1 material x1 raro + otro
   x7 común = probable drop de mob, visto en las Orbes de Ebanista) pero no
   está confirmado con datos duros. Pendiente de probar: `harvestLoots.json`
   y `monsterDrops.json` (repo `Vertylo/wakassets` en GitHub — este mismo
   repo es ahora, además, la fuente de iconos del Recetario, sección 4.5).

5. **Si nada de lo anterior está disponible**: estimación explícitamente
   marcada como no confirmada, nunca inventada como si fuera real.

### 4.2 El script: `wakfu_recipe_extractor.py`

Cruza los 4 JSON del nivel 1 y produce una tabla limpia: nivel de receta,
XP, resultado (ítem + cantidad), materiales (ítem + cantidad), todo con
nombres en español, para una profesión y rango de nivel concretos.

**Uso normal:**
```
python3 wakfu_recipe_extractor.py \
  --recipes recipes.json --items jobsItems.json \
  --results recipeResults.json --ingredients recipeIngredients.json \
  --category-id 81 --min-level 0 --max-level 200 \
  --output ebanista_recetas_completas.json
```

**Para identificar el categoryId de una profesión que aún no conocemos:**
```
python3 wakfu_recipe_extractor.py --items jobsItems.json \
  --results recipeResults.json --recipes recipes.json \
  --find-category-id "Nombre exacto de un ítem craftable en español"
```
(usa un ítem que sepas con certeza que pertenece a esa profesión — el
método que confirmó las 9 profesiones de la sección 4.3 fue usar DOS ítems
por profesión: la versión "tosca" y la "rudimentaria" del componente base,
para confirmar por partida doble.)

**Nuevo en sesión 5 — listar profesión↔categoryId** (best-effort, sin
probar contra datos reales porque nunca hizo falta):
```
python3 wakfu_recipe_extractor.py --categories recipeCategories.json --list-categories
```

**Nuevo en sesión 5 — exportar mapa de iconos** (para el Recetario,
sección 4.5; no filtra por profesión, cubre TODOS los ítems del feed):
```
python3 wakfu_recipe_extractor.py --items jobsItems.json \
  --export-icon-map --output iconos.json
```

### 4.3 Mapeo de profesiones → categoryId (completo)

**Las 9 profesiones de fabricación objetivo están 100% identificadas**,
confirmado cruzando 2 ítems conocidos por profesión contra `recipes.json` +
`recipeResults.json` + `jobsItems.json` reales de la versión 1.92.1.60:

| categoryId | Profesión | Recetas | Base de datos |
|---|---|---|---|
| 40 | Panadero | 89 | `panadero_recetas_completas.json` |
| 74 | **Peletero** | 49 | `peletero_recetas_completas.json` |
| 76 | Cocinero | 132 | `cocinero_recetas_completas.json` |
| 77 | Armero | 966 | `armero_recetas_completas.json` |
| 78 | Joyero | 964 | `joyero_recetas_completas.json` |
| 79 | Sastre | 1010 | `sastre_recetas_completas.json` |
| 80 | Marroquinero | 953 | `marroquinero_recetas_completas.json` |
| 81 | Ebanista | 640 | `ebanista_recetas_completas.json` |
| 83 | Maestro de Armas | 696 | `maestro_armas_recetas_completas.json` |

**Corrección respecto a v5**: el categoryId 74 (Peletero) se sospechaba
como "probablemente recolección" — es fabricación, una de las 9 objetivo.

Categorías restantes del feed, **sin asignar a ninguna profesión
objetivo**, con volumen mucho menor (materia intermedia compartida entre
profesiones, no profesiones en sí):

| categoryId | Produce | Recetas |
|---|---|---|
| 64 | Harina tosca | 22 |
| 71 | Tabla tosca | 21 |
| 72 | Hilo tosco | 21 |
| 73 | Acero tosco | 33 |
| 75 | Encantártaro tosco | 20 |

Estas 5 categorías se extrajeron igual y viven juntas en
`componentes_intermedios.json` (117 recetas) porque aparecen como
ingrediente dentro de recetas de las 9 profesiones principales — ej.
"Tabla tosca" es ingrediente de "Cartel de rebajas" (Ebanista) — y el
Recetario (sección 4.5) las necesita cargadas para poder expandir la lista
de compra hasta el final en vez de quedarse a medias.

**Vía alternativa explorada y no usada**: el feed de Ankama tiene un
archivo más, `recipeCategories.json` ("contains the jobs", según el foro
oficial de Wakfu), que en teoría mapea categoryId→nombre de profesión
directamente. Nunca se llegó a descargar (mismo bloqueo de fetch de
archivos versionados). No hizo falta — el método de dos ítems conocidos
por profesión, con datos que ya se tenían, fue más rápido. El script
conserva el modo `--list-categories` por si algún día aparece ese archivo,
pero sigue sin probarse contra datos reales — no asumir que funciona a la
primera.

### 4.4 Dónde vive esto de forma persistente

El usuario sube los archivos tanto a **Project Knowledge** como al **repo
público de GitHub** (`https://github.com/jaumander/Wakfu-craft-leveling-optimizer`,
confirmado en uso en sesión 5). Lista completa de archivos que deben estar
en ambos sitios:

- Este `HANDOFF.md`
- `wakfu_recipe_extractor.py` (incluye ahora `--list-categories` y
  `--export-icon-map`)
- `recetario_wakfu.html` (herramienta de exploración/lista de compra,
  sección 4.5)
- Las 9 bases de recetas completas, una por profesión, mismo formato
  (nivel 0-200): `ebanista_recetas_completas.json`,
  `armero_recetas_completas.json`, `joyero_recetas_completas.json`,
  `sastre_recetas_completas.json`, `marroquinero_recetas_completas.json`,
  `maestro_armas_recetas_completas.json`, `cocinero_recetas_completas.json`,
  `panadero_recetas_completas.json`, `peletero_recetas_completas.json`
- `componentes_intermedios.json` (las 5 categorías utilitarias de la
  sección 4.3 — imprescindible para que el Recetario expanda del todo)
- `iconos.json` (mapa nombre→gfxId, ~5000 ítems, para los iconos del
  Recetario — opcional, la herramienta funciona sin él pero sin iconos)
- Los 5 archivos originales de la comunidad (sección 9)

Cuando Ankama saque un parche que cambie recetas: repetir la descarga de
los 4 JSON crudos de la nueva versión y volver a correr el script para
regenerar TODOS los archivos de arriba (las 9 bases + `componentes_intermedios.json`
+ `iconos.json`).

### 4.5 El Recetario: `recetario_wakfu.html`

Herramienta propia del proyecto, creada en sesión 5 porque el script de
Python por sí solo no daba una forma cómoda de explorar recetas y armar
una lista de compra — la idea explícita del usuario **no es sustituir
Craftkfu, es tener algo propio sobre lo que seguir iterando** para las
necesidades concretas del proyecto (kamas, riesgo, excedente vendible).

**Qué es**: un único archivo HTML, sin backend, sin dependencias externas
de red salvo los iconos (sección de abajo). Se abre con doble clic. No
persiste nada entre sesiones del navegador a propósito (no usa
`localStorage`) — hay que volver a cargar los archivos cada vez.

**Cómo se usa**: un botón "Cargar datos" acepta varios `.json` a la vez —
cualquier combinación de las 9 bases de recetas, `componentes_intermedios.json`
(necesario para expandir del todo) e `iconos.json` (opcional, solo iconos).
Tres paneles, calcados en estructura a Craftkfu pero con estilo propio:
- **Buscar**: por profesión, rango de nivel, texto.
- **Recetas seleccionadas**: cantidad editable por receta, XP total de la
  selección (extra que Craftkfu no tiene, útil directamente para calcular
  tramos).
- **Lista de compra**: expansión recursiva de sub-recetas — si un material
  necesario tiene su propia receta entre los datos cargados, se desglosa en
  SUS materiales, redondeando crafteos hacia arriba y calculando el
  excedente vendible (conecta directo con la fórmula de la sección 8.9).

**Control de la expansión (arreglado en sesión 5, antes era un interruptor
único y opaco)**: un panel "Sub-recetas detectadas" lista cada material
intermedio craftable encontrado en la selección actual, con:
- checkbox individual para expandirlo o no (más botones "Expandir todo" /
  "No expandir nada"),
- si ese material tiene **varias recetas que lo producen** (ej. las 5
  variantes de "Orbe imperfecto", una por mob), un desplegable mostrando
  los materiales reales de cada variante — ya **no se elige la más barata
  en silencio**, elige el usuario con criterio.

**Iconos**: `iconos.json` mapea nombre de ítem → `gfxId` (extraído de
`jobsItems.json` → `definition.graphicParameters.gfxId`). Se pintan cargando
`https://raw.githubusercontent.com/Vertylo/wakassets/master/items/{gfxId}.png`
— mirror comunitario en GitHub, **verificado en vivo en sesión 5** (HTTP 200
contra varios gfxId reales del proyecto, curl directo). Existe también un
patrón oficial equivalente documentado por Ankama en su foro
(`s.ankama.com/www/static.ankama.com/wakfu/portal/game/item/{size}/{gfxId}.png`)
pero no se pudo verificar en vivo por las restricciones de fetch de Claude,
así que se usa el mirror de GitHub porque ese sí se confirmó que funciona.
Si un icono no carga, el hueco queda vacío sin romper el layout de la fila
(no hay iconos rotos visibles).

**Validación**: se probó de extremo a extremo con un navegador simulado
(jsdom, no solo revisión de código), reproduciendo exactamente el ejemplo
de una captura de Craftkfu que pasó el usuario (receta "Cartel de rebajas"
+ "Orbe imperfecto" → **35 recursos, 7 ítems distintos**, mismas cantidades
exactas) y probando el selector de variante y los checkboxes individuales
con una segunda receta real ("Archisfera imperfecta").

**Limitaciones actuales / por dónde seguir mejorándolo**:
- Sin precios ni coste neto todavía — hueco natural para cuando se resuelva
  el tema de precios (sección 4.1, punto 3).
- No hay forma de guardar/cargar una selección entre sesiones (a propósito,
  sin `localStorage`).
- Nadie ha confirmado todavía, abriendo el archivo en un navegador de
  verdad con conexión a internet, que los iconos cargan tal cual — Claude
  solo pudo validar la lógica con jsdom, no una carga real de imágenes por
  red (sección 11, pendientes).

## 5. Preguntas pendientes para arrancar el trabajo real

> **Nota**: el servidor NO se pregunta — decisión explícita del usuario en
> sesión 5, no es relevante para el alcance de esta herramienta. No
> reintroducir esta pregunta en ningún flujo.

- [ ] **Profesión objetivo** (Armero, Joyero, Sastre, Panadero, Cocinero,
      Ebanista, Maestro de Armas, Marroquinero, Peletero — separar de las
      de recolección: Minero, Campesino, Herbolario, Leñador, Pescador,
      Trampero).
- [ ] **Nivel actual** de esa profesión.
- [ ] **Nivel objetivo** (el juego tiene contenido hasta ~lvl 245/260;
      algunas hojas subidas llegan a 160-170; MethodWakfu confirma 160-170
      según profesión, sección 8.3).
- [ ] **Restricciones**: ¿puede farmear? ¿qué zonas conoce/tiene
      desbloqueadas? ¿tiene Havre Sac con parcelas de cultivo? ¿tiene
      gremio con bonus de oficio? ¿usa pociones/boosters de XP de crafteo?
- [ ] **Bonuses activos**: booster pack (✅ confirmado activo), bonus de
      gremio de crafteo básico (✅ confirmado activo), bonus de gremio de
      recolección/plantación (%), evento de oficios activo (sí/no),
      pociones turbo-craft, fichas de Turbo Craft 30 disponibles.

(No incluida como pregunta obligatoria: pareja de profesión — se cubre
proactivamente vía sección 8.8.)

## 6. Caso de prueba en curso: Ebanista 0→30

Datos ya extraídos y confirmados (ver `ebanista_recetas_completas.json`
filtrado a nivel ≤30, o navegarlo directamente en el Recetario, sección 4.5):

| Nivel | Componente | Materiales | Riesgo |
|---|---|---|---|
| 0 | Escuadrita tosca | Madera de fresno x5, Madera de avellano x5 | Ninguno |
| 5 | Orbe tosco | 1 drop raro + 7 comunes (3 variantes de mob: jalató/tofu/larva) | Depende de mob |
| 10 | Escuadrita rudimentaria | Madera de ñiamzamo x5, Madera de castaño x5 | Ninguno |
| 15 | Orbe rudimentario | 1 raro + 7 comunes (3 variantes de mob) | Depende de mob |
| 20 | Escuadrita imperfecta | Madera de boabob x5, Madera de abedul x5 | Ninguno |
| 25 | Orbe imperfecto | 1 raro + 7 comunes (5 variantes de mob — la más flexible) | Depende de mob |
| 30 | Escuadrita frágil | Madera de bananaranjo x5, Madera de sauce llorón x5 | Ninguno |

Patrón confirmado: cada tramo de calidad tiene un componente 100% madera
(Escuadrita) y uno con drop de mob (Orbe), ambos dan 450 XP por crafteo.

**Preferencias del usuario ya recogidas:** compra materiales (no farmea
activamente, aunque está abierto a ello si compensa levear Maestro de
Armas en paralelo por la sinergia de madera, sección 8.8). Bonuses activos:
gremio básico + booster pack.

**Falta para cerrar la ruta:** precios de mercado de las 8 maderas
distintas y de los drops de mob más accesibles para el usuario. Gestión de
precios pospuesta explícitamente por el usuario (sección 4.1, punto 3) —
ya no es cuestión de servidor, es cuestión de cuándo/cómo abordar precios;
no insistir hasta que el usuario lo saque él mismo.

## 7. Catálogo de fuentes online

| Fuente | URL | Para qué sirve | Notas de uso |
|---|---|---|---|
| **Feed JSON oficial de Ankama** | `https://wakfu.cdn.ankama.com/gamedata/{version}/{tipo}.json`, versión en `.../gamedata/config.json` | Fuente oficial y versionada: `recipes`, `recipeIngredients`, `recipeResults`, `jobsItems`, `harvestLoots`, `resources`. Resuelve el BaseXP real y los `gfxId` de iconos. | Ver sección 4.1: método por defecto es descarga manual del usuario + extractor, no fetch directo de Claude. |
| **Iconos de ítems — Vertylo/wakassets** | `https://github.com/Vertylo/wakassets`, servido vía `raw.githubusercontent.com/Vertylo/wakassets/master/items/{gfxId}.png` | Iconos de (casi) todos los ítems del juego, indexados por `gfxId` (mismo id que `jobsItems.json` → `definition.graphicParameters.gfxId`). Usado por el Recetario, sección 4.5. | Verificado en vivo en sesión 5 (HTTP 200 con curl contra gfxId reales del proyecto). Existe un patrón oficial equivalente de Ankama pero no se pudo verificar por las restricciones de fetch de Claude. |
| Stratfu — Craft | https://stratfu.fr/outils/craft/ | El usuario la usa para trackear los objetos de su Mercasaco | Fuente de inventario propio del usuario, no del asistente. |
| wakfu-farm-tracker (GitHub) | https://github.com/olivo28/wakfu-farm-tracker-public | App de tracking de farmeo (no consultable por HTTP) | Que el usuario la use como tracker personal y pase capturas/cifras. |
| Craftkfu (waklab) | https://craftkfu.waklab.fr/ | Buscador de recetas y costes de recursos | SPA JS, no accesible por fetch de Claude. Sigue sin ser fuente estructural (sección 4.0), pero es la referencia visual que inspiró el Recetario (sección 4.5) y sirve para comparar resultados. |
| MethodWakfu — Métiers | https://methodwakfu.com/artisanat/les-metiers/ | Mecánicas: niveles máx., fórmula XP, probabilidad de éxito, Havre-Sac | Ya leída con éxito (sección 8). Fetch funciona en este dominio. |
| jobkfu (vertylo) | https://vertylo.github.io/jobkfu/ | Nivel de receta + XP base + bonuses + nivel actual/objetivo → nº de crafteos | Regla de delegación (sección 1-2): pedir al usuario que lo use en vez de calcularlo a mano. |
| wakfujobcalculator.com | https://wakfujobcalculator.com/ | Misma función que jobkfu, verificación cruzada | Idem regla de delegación. |
| wakfujobcalculator.com — Items Craft Guide | https://wakfujobcalculator.com/items-craft-guide | Árbol de recetas con shopping list acumulativo | Función ahora cubierta también por el Recetario propio (sección 4.5); esta sigue siendo útil como comparación externa. |

## 8. Datos verificados en methodwakfu.com/artisanat/les-metiers/ (23-nov-2025, Wakfu 1.79)

Secciones 8.1 a 8.7 (lista de profesiones, tabla de tramos, niveles
máximos, fórmula de XP de crafteo, probabilidad de éxito/XP degresiva,
Havre-Sac y talleres, herramientas comunitarias confirmadas) — sin cambios,
consultar el histórico de la conversación si se necesita el detalle
completo; lo relevante para el flujo actual está resumido en las
secciones 3, 6 y 8.8-8.9 de este documento.

Datos consolidados de múltiples fuentes: XP por tramo de 10 niveles (7500,
22500, 37500... +15000 cada tramo), nomenclatura de calidad
(Tosco→Ancestral).

### 8.8 Matriz de sinergias entre profesiones

Derivada por lógica del componente base por profesión, conocimiento de
proyecto (no se pregunta al usuario):

| Recolección | Alimenta a (fabricación) | Recurso compartido |
|---|---|---|
| Mineur (Minero) | Bijoutier (Joyero) + Armurier (Armero) | Minerales (Gemmes / Plaques) |
| Forestier (Leñador) | Maître d'Armes + Ébéniste | Madera (Manches / Équerres) — Ébéniste además necesita Orbes (drop de mobs) |
| Herboriste (Herbolario) | Boulanger (Panadero) | Plantas silvestres (Huiles) |
| Pêcheur (Pescador) | Cuisinier (Cocinero) | Peces (Épices) |
| Paysan (Campesino) | Tailleur (Sastre) | Cereales (Fibres) |
| — (drop de mobs) | Maroquinier (Marroquinero) | Cuirs — depende de combate/prospección, no de recolección |
| Trappeur (Trampero) | — | Sin pareja de fabricación directa confirmada |

**Nota (sesión 5)**: falta situar a **Peletero** en esta matriz — se
confirmó que es fabricación (categoryId 74, sección 4.3) pero no se ha
determinado con qué profesión de recolección empareja (probablemente
Trampero, dado que "Esencia" suena a componente de curtido/peletería, pero
sin confirmar — no asumir).

**Uso**: al calcular una ruta de fabricación, mencionar de forma natural si
tiene pareja en esta tabla, sin convertirlo en pregunta obligatoria.

### 8.9 Excedente vendible / coste neto

`recipeResults.json` del feed oficial indica cuántas unidades produce cada
crafteo. Cuando sobran unidades del tramo, o craftear de más es la única
forma de comprar materiales en packs, el sobrante es vendible en el HdV.

**Fórmula**: `Coste neto del tramo = Coste bruto de materiales − (unidades de excedente × precio de venta del ítem resultante)`.

El precio de venta se pide al usuario igual que el de los materiales
(nivel 3 de la cascada, sección 4.1: captura de HdV, con fecha, no
reutilizable entre sesiones — gestión pospuesta, ver ahí mismo).

El Recetario (sección 4.5) ya calcula automáticamente el excedente en
*unidades* de cada sub-receta expandida (al redondear crafteos hacia
arriba); falta multiplicarlo por precio de venta para llegar al coste neto
en kamas — siguiente paso natural cuando se resuelva el tema de precios.

## 9. Archivos de la comunidad subidos por el usuario (resumen)

- **9.1** `_Wakfu_Crafting_Professions_Leveling_Calculator (to lvl 160).xlsx`:
  receta↔recurso↔tramo para pares Joyero/Armero, M.Armas/Ebanista,
  Panadero/Cocinero.
- **9.2** `Wakfu_Sheets.xlsx`: ubicaciones de recolección por nivel,
  mazmorras, Kama Minting. Posiblemente desactualizada en tramos 150+.
- **9.3** `Copia_de_New_tabla_de_oficios_wakfu.xlsx`: recursos por
  profesión de recolección en español, inputs de bonuses.
- **9.4** `Tabla_de_oficios_de_fabricación (ES).xlsx`: shopping list
  agregada por categoría, la más legible.
- **9.5** `_Wakfu__Récolte_métiers.docx`: mecánicas de crecimiento/respawn
  en Havre Sac.

Estos 5 archivos siguen siendo un complemento útil (sobre todo para
recolección/ubicaciones), pero para BaseXP/materiales exactos de fabricación
la fuente de verdad es la arquitectura de la sección 4 (las 9 bases +
componentes intermedios), no estas hojas.

## 10. Contradicciones / huecos resueltos y pendientes

**Resueltos (v5 y anteriores):**
- **BaseXP real** → resuelto vía sección 4 (feed oficial + script).
- **"Craftkfu local" / scraping del motor de Craftkfu** → descartado con
  justificación documentada (sección 4.0); no repetir esta investigación.
- **No existe fuente de precios de mercado (HdV) viva** → confirmado
  (Wakfu-Elements, abandonado). Workaround de capturas del usuario, nivel 3
  fijo de la cascada (sección 4.1).

**Resueltos en sesión 5:**
- **categoryId de las 9 profesiones de fabricación** → 100% confirmado
  (sección 4.3), incluida la corrección de Peletero (es fabricación, no
  recolección).
- **Servidor del usuario** → decisión explícita: no se pregunta, no es
  relevante para el alcance de la herramienta. Eliminado de la sección 5 y
  del system prompt (sección 2).
- **Selección automática y silenciosa de variante** cuando un material
  tiene varias recetas (ej. 5 variantes de "Orbe imperfecto") → resuelto en
  el Recetario (sección 4.5): selector manual visible, ya no se elige solo.
- **Interruptor único y opaco de "expandir sub-recetas"** → sustituido por
  un panel con checkbox por ítem y visibilidad de en qué se convierte cada
  uno (sección 4.5).
- **Sin herramienta propia de shopping-list** → resuelto: Recetario
  (`recetario_wakfu.html`), validado contra un ejemplo real de Craftkfu.

**Pendientes:**
- **Precios de mercado**: gestión pospuesta explícitamente por decisión del
  usuario (sección 4.1, punto 3) — no insistir, esperar a que el usuario lo
  saque.
- **Trade-off "menos recetas vs. XP degresiva"**: sigue sin resolver de
  forma automática — decisión caso por caso con el usuario en el paso 6
  del flujo operativo (sección 3).
- **Clasificación automática "farmeable vs. drop de mob"**: pendiente de
  probar `harvestLoots.json`/`monsterDrops.json` (sección 4.1, punto 4).
- **Iconos del Recetario sin confirmar en un navegador real**: Claude
  validó la lógica con un navegador simulado (jsdom) pero nadie ha abierto
  todavía el HTML de verdad, con red, para confirmar que las imágenes
  cargan tal cual (sección 4.5).
- **Peletero sin ubicar en la matriz de sinergias** (sección 8.8).

## 11. Checklist de próximos pasos

**Ya hechos (no repetir):**
- [x] Explorado repo `wakfu-farm-tracker-public` → no es fuente de datos de
      recetas útil (solo complemento de drops).
- [x] Confirmado que craftkfu.waklab.fr y wakfujobcalculator.com son SPAs
      no accesibles por fetch de Claude.
- [x] Leído methodwakfu.com/artisanat/les-metiers/ en profundidad
      (sección 8).
- [x] Localizado y verificado en vivo el feed JSON oficial de Ankama,
      versión 1.92.1.60 (confirmado dos veces, sin cambios).
- [x] Confirmado que "Craftkfu local" no aporta nada nuevo (sección 4.0).
- [x] Descubierta y probada la vía de descarga directa del feed por parte
      del usuario, como método por defecto (sección 4.1).
- [x] Creado `wakfu_recipe_extractor.py`, script reutilizable (sección 4.2).
- [x] Generada base de datos completa de Ebanista (640 recetas).
- [x] Formalizada la matriz de sinergias (8.8) y el cálculo de excedente
      vendible (8.9) como conocimiento de proyecto.
- [x] **Confirmados los categoryId de las 9 profesiones de fabricación**
      (sección 4.3), incluida la corrección de Peletero.
- [x] **Generadas las 8 bases de recetas restantes** + `componentes_intermedios.json`
      (5 categorías utilitarias: Tabla, Hilo, Acero, Harina, Encantártaro).
- [x] **Descartada la pregunta de servidor** — decisión explícita del
      usuario, eliminada de todos los flujos.
- [x] **Creado el Recetario** (`recetario_wakfu.html`): explorador de
      recetas + lista de compra con expansión recursiva, validado contra un
      ejemplo real de Craftkfu (35 recursos, mismos ítems y cantidades).
- [x] **Selector manual de variante** cuando un material tiene varias
      recetas (antes se elegía en silencio).
- [x] **Panel de sub-recetas detectadas** con checkbox individual por
      ítem — reemplaza el interruptor global opaco.
- [x] **Iconos de ítems integrados** (`iconos.json` + mirror
      Vertylo/wakassets en GitHub, verificado en vivo con curl).
- [x] Añadidos al script los modos `--list-categories` y `--export-icon-map`.

**Pendientes reales:**
- [ ] Subir todos los archivos nuevos de sesión 5 (8 bases de recetas,
      `componentes_intermedios.json`, `iconos.json`, `recetario_wakfu.html`,
      este `HANDOFF.md` v6) a Project Knowledge y al repo de GitHub.
- [ ] Abrir `recetario_wakfu.html` en un navegador real (con conexión) y
      confirmar que los iconos cargan correctamente — pendiente de
      confirmación humana, Claude solo pudo validarlo con jsdom.
- [ ] Decidir cómo gestionar precios de mercado (pospuesto por el usuario,
      sección 4.1) — no reabrir hasta que el usuario lo pida.
- [ ] Calcular en Jobkfu (regla de delegación) el nº de crafteos necesarios
      para Ebanista 0-30 con el booster pack + bonus de gremio ya
      confirmados.
- [ ] Entregar tabla final de la ruta Ebanista 0-30 con coste neto
      (bloqueado por precios).
- [ ] Ubicar a Peletero en la matriz de sinergias (sección 8.8).
- [ ] (Opcional, baja prioridad) Extender el Recetario con un campo de
      precio por ítem y cálculo de coste neto (sección 8.9), cuando se
      resuelva el tema de precios.
- [ ] (Opcional, baja prioridad) Descargar `harvestLoots.json` y
      `monsterDrops.json` para clasificar automáticamente "farmeable vs.
      drop de mob".
- [ ] (Opcional, baja prioridad) Leer `methodwakfu.com/artisanat/localisation-des-ressources/`
      y `methodwakfu.com/artisanat/plans-et-recettes/`.

---

*Documento v6 (03-sep-2026): sustituye al handoff v5 (mismo día).
