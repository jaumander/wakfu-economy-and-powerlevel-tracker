# Wakfu Craft Power-Level Helper — Documento de Handoff

> **Qué es esto**: contexto completo para que otra instancia de Claude (u otra cuenta) retome este proyecto desde cero, sin haber visto la conversación original. Incluye el objetivo del proyecto, las instrucciones de comportamiento, el flujo operativo de cálculo de ruta, el catálogo de fuentes que el usuario va a usar, lo que ya se sabe de los 5 archivos que subió, fórmulas de XP confirmadas, y una checklist de próximos pasos.
>
> **Qué NO es esto**: no contiene todavía una ruta de leveo calculada para ninguna profesión concreta. Es la base de conocimiento + el "manual de instrucciones" para construirla en la siguiente sesión.

---

## 1. Objetivo del proyecto

Diseñar, junto al usuario, rutas de leveo de profesiones de crafteo en Wakfu que sean:

1. **Baratas en kamas** — priorizar recetas con materiales baratos, comunes o farmeables por el propio usuario antes que comprados en el Hotel de Ventas (HdV/mercado).
2. **Seguras** — evitar depender de drops raros, ítems de eventos temporales u ofertas de mercado volátiles; evitar rutas donde un solo tramo agote el stock del mercado y dispare el precio.
3. **Fáciles de seguir** — minimizar el número de recetas distintas por tramo; agrupar tramos donde se puede craftear "en bloque" lo mismo muchas veces (evitar saltar de receta cada pocos niveles).

## 2. Instrucciones de comportamiento (system prompt del proyecto)

Estas son las instrucciones que debe seguir el asistente en este proyecto. Cópialas tal cual en las "Custom instructions" del Project de Claude:

> Eres un asistente especializado en optimizar el leveo de profesiones de crafteo en el MMO Wakfu (Ankama). Tu objetivo es ayudar al usuario a diseñar una ruta de leveo para una profesión concreta que sea barata en kamas, segura y fácil de seguir (ver definiciones arriba).
>
> **Al empezar** (si no se ha dicho ya), pregunta: profesión, nivel actual, nivel objetivo, servidor (la economía varía por servidor) y restricciones (ej. "no quiero comprar recursos premium", "solo puedo farmear tal zona").
>
> **Para calcular la ruta**, sigue el flujo operativo formalizado en la sección 3 de este documento: delimitar tramos → listar recetas candidatas → pedir solo el BaseXP/precio de esas recetas concretas (nunca de todo el juego) → calcular → comparar alternativas → entregar tabla. Este flujo es el que cubre el hueco que ninguna herramienta externa del usuario resuelve por sí sola.
>
> **Fuente de verdad**: el usuario irá pasando recursos (capturas, texto pegado, enlaces a wikis/calculadoras, hojas de cálculo de la comunidad). Trata esa información como más fiable que tu conocimiento previo — Wakfu recibe parches frecuentes que cambian recetas y XP. Si algo aportado por el usuario contradice lo que "sabes", dilo explícitamente y usa el dato del usuario.
>
> **Mantén una tabla de referencia acumulada** por profesión con: nivel de receta, ítem, XP que da, materiales necesarios y cantidad, y coste estimado (si se conoce).
>
> **Cuando haya info suficiente de un tramo**, propone la ruta en formato tabla: rango de niveles → receta recomendada → cantidad de crafteos necesarios → materiales totales → coste estimado → alternativa más barata/segura si existe.
>
> **Si falta información** (precio actual de un material, vigencia de una receta), dilo claramente y pide al usuario que lo confirme o aporte un enlace/captura, en vez de inventar cifras.
>
> **Sé explícito con los trade-offs**: p.ej. "esta receta es más barata pero necesita farmear X mob poco frecuente" vs. "esta es más cara pero 100% comprable en el mercado".
>
> **Formato de entrega**: si el usuario pide una tabla larga o un plan completo para guardar, ofrece generarlo como documento descargable (xlsx o md); si es una consulta puntual o ajuste rápido, responde en el chat.
>
> **Estilo**: directo, en español, con tablas cuando ayuden a comparar, sin relleno innecesario. Evita afirmaciones categóricas sobre precios de mercado si no vienen de datos del usuario o de una búsqueda reciente.

## 3. Flujo operativo de cálculo de ruta (motor de decisión de recetas)

> Esta sección formaliza cómo se resuelve, turno a turno en el chat, el hueco identificado por el usuario (milestone 03-sep-2026): **elegir qué receta seguir en cada tramo para que la ruta de leveo no resulte extremadamente costosa**, sin depender de ninguna herramienta externa (todas las de la sección 5 sirven para *trackear* progresión/inventario, ninguna decide recetas por coste). No requiere una calculadora aparte — se ejecuta conversacionalmente usando los datos ya consolidados de este documento (secciones 7-9) más los datos puntuales que solo el usuario puede aportar.

**Principio clave**: en vez de pedir al usuario que vuelque todo Craftkfu/Jobkfu para su profesión, solo se le pide el BaseXP y precio de las recetas que tocan los 2-4 tramos concretos de SU ruta (nivel actual → nivel objetivo). Esto reduce la fricción de "tarea manual en una SPA que Claude no puede leer" (ver limitación en sección 5) a algo asumible en un par de capturas.

**Pasos**:

1. **Recoger inputs del usuario** (si no los ha dado ya): profesión, nivel actual, nivel objetivo, servidor, restricciones y bonuses activos — usar la checklist de la sección 4.
2. **Delimitar tramos**: con la tabla de calidad/tramo (sección 8.2) y el nivel máx. por profesión (sección 8.3), identificar exactamente qué tramos de 10 niveles cubre la ruta pedida.
3. **Listar recetas candidatas por tramo**: cruzar las hojas ya analizadas (sección 6, especialmente 6.1/6.3/6.4) para sacar, por tramo, todas las recetas/variantes de componente base disponibles para esa profesión (ej. si Ébéniste tiene Équerres + Orbes como componentes distintos, listarlos como candidatos separados).
4. **Pedir el dato bloqueante mínimo**: para cada receta candidata de esos tramos (normalmente 1-3 por tramo), pedir al usuario BaseXP (de Craftkfu) y precio de mercado o indicación de "lo puedo farmear gratis" (de Stratfu/Wakfu Tracker o su conocimiento del servidor). Si el usuario no lo tiene a mano, ofrecer seguir con una estimación marcada explícitamente como no confirmada — nunca inventar cifras como si fueran reales (regla ya fijada en la sección 2).
5. **Calcular**, aplicando la fórmula de la sección 8.4: crafteos necesarios = XP del tramo (sección 7) ÷ XP por crafteo (con los bonuses del usuario aplicados); materiales totales = crafteos × materiales por receta; coste = materiales comprados × precio (los farmeables cuentan como 0 kamas pero se anota el tiempo/zona de farmeo).
6. **Comparar candidatas** cuando haya más de una por tramo: coste total, ¿depende de drop raro o evento?, ¿cuántas recetas distintas obliga a aprender/seguir?, y aplicar el trade-off de la sección 9.7 (menos recetas vs. XP degresiva a partir de +10/+20 niveles sobre el nivel de la receta, sección 8.5).
7. **Entregar la tabla final** en el formato ya fijado por el system prompt (sección 2): rango de niveles → receta recomendada → cantidad de crafteos → materiales totales → coste estimado → alternativa más barata/segura si existe. Marcar explícitamente cualquier cifra no confirmada.

**Cuándo repetir el ciclo**: cada vez que el usuario pida una ruta nueva (otra profesión, o ampliar el nivel objetivo), se repite desde el paso 2 — los tramos ya calculados y confirmados en la conversación no hace falta recalcularlos salvo que cambien precios/bonuses.

## 4. Preguntas pendientes para arrancar el trabajo real

En la próxima sesión, antes de calcular ninguna ruta, pedir al usuario (si no las ha dado ya en el mismo mensaje) — este es el input del **paso 1** del flujo operativo (sección 3):

- [ ] **Profesión objetivo** (Armero, Joyero, Sastre, Panadero, Cocinero, Ebanista, Maestro de Armas, Marroquinero, Peletero... — y separar de las de recolección: Minero, Campesino, Herbolario, Leñador, Pescador, Trampero).
- [ ] **Nivel actual** de esa profesión.
- [ ] **Nivel objetivo** (recordar que el juego ya tiene contenido hasta ~lvl 245/260, algunas hojas subidas llegan a 160-170).
- [ ] **Servidor** (economía distinta por servidor — Rubilax, Ogrest, etc.).
- [ ] **Restricciones**: ¿puede farmear? ¿qué zonas conoce/tiene desbloqueadas? ¿tiene Havre Sac (Havenbag) con parcelas de cultivo? ¿tiene gremio con bonus de oficio? ¿usa pociones/boosters de XP de crafteo?
- [ ] **Bonuses activos**: booster pack (tosco/rubí/ogrest), bonus de gremio de crafteo (%), bonus de gremio de recolección/plantación (%), evento de oficios activo (sí/no), pociones turbo-craft.

## 5. Catálogo de fuentes online aportadas por el usuario

| Fuente | URL | Para qué sirve | Notas de uso |
|---|---|---|---|
| Stratfu — Craft | https://stratfu.fr/outils/craft/ | El usuario la usa para **trackear los objetos de su Mercasaco** (inventario del banco/mercado personal) | Es su fuente de inventario propio, no del asistente. Cuando el usuario diga "tengo X en el mercasaco", puede venir de aquí. |
| wakfu-farm-tracker (GitHub) | https://github.com/olivo28/wakfu-farm-tracker-public | Repo de la comunidad para trackear farmeo de recursos | **Pendiente de estudiar en detalle**: entrar al repo, leer el README, ver si expone datos estructurados (JSON/CSV) de recursos, ubicaciones, tiempos de respawn, o si es solo una app de tracking personal. Evaluar si se puede usar como fuente de datos de "qué farmear y dónde" o solo como herramienta de tracking para el propio usuario. |
| Craftkfu (waklab) | https://craftkfu.waklab.fr/ | Buscador de **recetas y costes de recursos**; permite acumular varias recetas para sacar una lista de la compra total | Candidata principal para sacar, receta a receta, los materiales exactos y (si tiene precios) el coste estimado. Hay que verificar si los precios que muestra son en vivo (por servidor) o estáticos/desactualizados. |
| MethodWakfu — Métiers | https://methodwakfu.com/artisanat/les-metiers/ | Página de referencia general para **entender el sistema de oficios** (mecánicas, no cálculo fino) | Usar para contexto/mecánicas, no como fuente numérica de recetas exactas. En francés. |
| jobkfu (vertylo) | https://vertylo.github.io/jobkfu/ | Calculadora: nivel de receta + XP base + bonuses + nivel actual/objetivo → **número de crafteos necesarios** | Útil para el paso "cuántas veces tengo que craftear X para pasar de nivel A a B". |
| wakfujobcalculator.com | https://wakfujobcalculator.com/ | Misma función que jobkfu: profesión, nivel inicial/final, XP por crafteo → nº de crafteos totales | Redundante con jobkfu, sirve de verificación cruzada. Cubre: Armero, Joyero, Cocinero, Sastre, Manitas/Ebanista, Maestro de Armas, Minero, Campesino, Herbolario, Trampero, Leñador, Pescador. |
| wakfujobcalculator.com — Items Craft Guide | https://wakfujobcalculator.com/items-craft-guide | Árbol de recetas: al elegir un ítem final muestra sus materiales, expandibles recursivamente hasta materiales base no crafteables. Tiene un **"shopping list" acumulativo** que suma cantidades de varios ítems | Esta es probablemente la herramienta más potente para generar la "lista de la compra" final de un tramo o de toda la ruta. Datos extraídos directamente de los archivos del juego según la descripción del usuario. |

**Estado de verificación en vivo (actualizado, milestone 2026-09-03)**:
- **wakfu-farm-tracker-public** (GitHub): revisado el README. **No es una fuente de datos consultable por la IA, es una app de escritorio/móvil** ("Wakfu Tracker", v1.1.1w, Electron + Expo + Node.js API) que el propio usuario debe instalar. Funciones relevantes: filtro inteligente de drops, selector multi-receta, "crafteo en cascada" que reparte cantidades entre tarjetas activas del mismo ítem, cálculo "Auto" de lo que falta en tiempo real, sincronización cloud entre PC y móvil. **Uso recomendado**: que el usuario la use como su tracker personal de inventario/progreso y nos pase capturas o cifras concretas de ahí — no se puede scrapear ni consultar por HTTP.
- **craftkfu.waklab.fr** y **wakfujobcalculator.com** (incl. `/items-craft-guide`): son **SPAs (single-page apps) en JavaScript puro**; un `web_fetch` normal solo devuelve el esqueleto HTML vacío ("Craftkfu doesn't work properly without JavaScript"). **No se pueden leer sus datos mediante fetch/búsqueda desde el chat.** Para usarlas hace falta que el usuario las abra en su navegador y pegue aquí los resultados (texto o captura), o usarlas manualmente él mismo. Esta es la limitación que motiva el "principio clave" de pedir datos mínimos en la sección 3.
- **methodwakfu.com/artisanat/les-metiers/** — ✅ **fetch exitoso y con contenido muy valioso**, ver sección 8 más abajo: resuelve varias de las dudas de la sección 9.

**Pendiente aún**: leer `methodwakfu.com/artisanat/localisation-des-ressources/` y `methodwakfu.com/artisanat/plans-et-recettes/` (enlazadas desde la página ya leída) para completar ubicaciones de recolección y el sistema de planos/recetas especiales.

## 6. Archivos subidos por el usuario (ya analizados, resumen)

Los 5 archivos están en `/mnt/user-data/uploads/`. Si se pierden, pedir al usuario que los vuelva a subir. Resumen de cada uno:

### 6.1 `_Wakfu_Crafting_Professions_Leveling_Calculator__to_lvl_160__.xlsx`
- Calculadora (en inglés) hasta nivel ~160-170.
- Inputs configurables: **crafting EXP potion (0% o 100%)**, **bonus de gremio (0-20%)**, **base EXP per craft** (editable por si Ankama rebalancea).
- Contiene tablas por tramo de 10 niveles con: EXP necesaria, cantidad a recolectar de cada recurso, número de crafteos, y **la receta exacta con sus 2 recursos** para:
  - Profesiones "solo mineral": **Joyero** (Gemas: Coarse→Ancestral) y **Armero** (Placas), que comparten los mismos 2 recursos por tramo (columna que ya suma "overlapping resources x2" para ambas profesiones a la vez — muy útil si se levean juntas).
  - Profesiones "solo madera": **Maestro de Armas** (Mangos/Handle) y **Ebanista/Handyman** (Soportes/Bracket), mismo patrón, mismos recursos por tramo.
  - **Panadero** (Oil → Bread, con fórmula especial: 3 agua + 1 aceite = 1 pan) y **Cocinero** (Spice), que dependen de recursos de Herbolario y Pescador respectivamente.
  - Nota propia del archivo: "Panadero se puede levear un poco más fácil que las demás: craftear Oil y hornear pan alternando."
- **Valor para el proyecto**: es la fuente más directa y ya lista para extraer la tabla receta↔recurso↔tramo de nivel para varias profesiones de fabricación. Hay que revisar si sigue vigente (puede haber parches posteriores).

### 6.2 `Wakfu_Sheets.xlsx` (comunidad, en inglés, multi-pestaña)
Pestañas: `WELCOME, Resources, Locations, Dungeon Info, Crafting Machines, Prospecting, Gathering bonuses, Resource Boxes, Kama Minting, Runes, Almanax bonuses, Rune2, 110 Weapons, Sublimations, SublimationsOtherSource, COMMENTS, Rifts`.
- **Resources**: tabla por nivel (0 a 155, de 5 en 5) con recurso normal y variante rara para **Farmer, Fisher, Herbalist, Lumberjack, Miner**, más ubicación de recolección. Es la mejor fuente para saber **dónde farmear cada material de recolección** por nivel.
- **Locations**: mapa de zonas del juego con Zaap, mazmorras, profesión asociada al PNJ del área, y rango de recolección disponible en cada zona.
- **Dungeon Info, Crafting Machines, Resource Boxes, Kama Minting, Gathering bonuses**: pendientes de explorar en detalle (no se ha volcado su contenido aún en este documento). Kama Minting parece relevante para saber qué minerales convertir en kamas (economía).
- El propio archivo se declara **incompleto y colaborativo** (creado hace ~7 años reactivado, con celdas para marcar "x" si un dato no aplica). Cuidado con desactualización: **puede tener años**, contrastar cifras de recetas/XP con fuentes más recientes (craftkfu, wakfujobcalculator).

### 6.3 `Copia_de_New_tabla_de_oficios_wakfu.xlsx` (comunidad, en español)
- Hoja de cálculo con macros de inputs: booster pack, bonus de gremio de crafteo, bonus de gremio de recolección/plantación (10-70%), evento de oficios (0/1).
- Tabla principal (tramos de 10 niveles, 0→160): Exp necesaria por tramo (igual patrón: 7500, 22500, 37500... +15000 cada tramo), Exp por componente (constante 660 en esta hoja — **contradice** los 300 EXP/craft "base" de la hoja 6.1; puede deberse a que ya incluye algún bonus, o a una versión distinta del juego — **hay que preguntar al usuario o contrastar**), cantidad de componentes necesarios, calidad del componente (Tosco→Ancestral, 17 tramos hasta 160).
- Trae **recursos concretos por tramo y por profesión de recolección** (Campesino, Leñador, Minero, Herbolario, Pescador, Peletero, Marroquinero) con nombres en español, incluyendo variante especial de Peletero/Marroquinero que usa "recolecciones especiales/cadáveres" (drops de mobs).
- Incluye una tabla auxiliar con "% de recolección (cantidad de recursos)" — parece un sistema de bonus de recolección por nivel/gremio que determina cuántos recursos caen por acción (de 1 a 3 según %).
- Notas propias del archivo: "Recordar Esquejes valen 0,5" (los esquejes/cuttings de árboles cuentan como media recolección), "Los Esquejes cuentan la mitad pero son dos por árbol", fórmulas específicas de Panadero (pan con/sin componente).

### 6.4 `Tabla_de_oficios_de_fabricación__ES_.xlsx` (comunidad, en español)
- Tabla más simple y muy legible: por cada tramo de 10 niveles de oficio (0-10 hasta 160-170, con el último marcado "???" = sin confirmar/próximo a publicarse), da:
  - Rango de **nivel de personaje** recomendado (ej. "6 al 20" para oficio 0-10).
  - **Calidad** del tramo (tosco→ancestral, igual nomenclatura que las otras hojas).
  - XP total necesaria (coincide con las otras hojas: 7500, 22500, 37500...).
  - Cantidad de ítems a craftear.
  - **Lista de la compra agregada** por tramo, separada en 5 categorías con emoji: 💎 minerales, 🌲 madera, 🌾 cultivos, 🐟 peces, 🌸 flores, y una columna aparte de "recursos de mobs" (con ejemplos de mobs, no cantidad exacta).
- Es la hoja **más fácil de leer para sacar rápidamente "cuánto necesito de cada categoría de recurso" por tramo**, aunque no dice qué receta concreta craftear (para eso hacen falta las hojas 6.1/6.2/6.3 o las webs).

### 6.5 `_Wakfu__Récolte_métiers.docx` (comunidad, en francés — mecánicas de recolección/cultivo)
Documento de investigación de la comunidad (autor Discord: .vesperal, basado en/complemento de MethodWakfu) sobre las **mecánicas exactas de recolección y cultivo en el Havre Sac (Havenbag)**. Datos ya extraídos y confirmados como útiles para el proyecto:

- **Velocidad de crecimiento** (Herbolista, Campesino, Leñador): el tiempo entre niveles de crecimiento es constante dentro de una misma "racha" de niveles.
  - Leñador (bouture/esqueje): 3 min/nivel hasta nivel 15; 5 min/nivel después.
  - Herbolista y Campesino (semilla): 5 min/nivel hasta nivel 15; 10 min/nivel después.
  - El estado activo/inactivo del Havre Sac afecta a la pausa del crecimiento (ver más abajo) — mismo ritmo dentro o fuera del HS mientras esté "activo".
- **Verrouillage (bloqueo) de recursos**: al plantar, el recurso queda bloqueado ~20 min para el que lo plantó, garantizando que puede recogerlo antes que otros.
- **Respawn de nodos** (Minero, Pescador, Trampero):
  - Minero: 2:30 hasta nivel 15, luego 5:00.
  - Pescador: 2:45 hasta nivel 15, luego 5:00.
  - Trampero: 5:00 siempre.
- **Desconexión automática**: a los 20 min de inactividad total (un solo movimiento la resetea).
- **Fórmula de XP por nivel de oficio** (la más importante, citarla siempre que se calculen crafteos):
  **`XP necesaria para subir del nivel N = 75 + ((N - 1) × 150)`**
  — Confirmar si esto es XP marginal por nivel o coincide/contradice el patrón de "7500 por tramo de 10 niveles" que aparece en las otras 3 hojas (7500/10 = 750 de media, no 75+150N... **hay una posible discrepancia a resolver con el usuario o con fuentes recientes**, puede que esta fórmula del docx sea de una mecánica distinta —posiblemente de recolección, no de crafteo— o de una versión anterior del juego).
- **Estado del Havre Sac "activo"/"inactivo"**: descubrimiento central del documento — el HS tiene dos estados que afectan si las plantas siguen creciendo mientras el jugador está fuera. Hay tablas comparativas mostrando cómo el mismo cultivo llega a distinto estado de crecimiento en el mismo tiempo real según se esté dentro/fuera del HS. **Relevante para optimizar el farmeo pasivo de recolección** mientras el usuario no está jugando activamente.
- El documento tiene changelog interno (última entrada vista: 29/06/2025), es decir, es relativamente reciente y activo — buena señal de vigencia, pero conviene preguntar al usuario si tiene una versión más nueva.

## 7. Datos consolidados que ya podemos dar por buenos (multi-fuente, coinciden en 3-4 hojas)

- **XP necesaria por tramo de 10 niveles de oficio de fabricación** (coincide en las hojas 6.1, 6.3 y 6.4): 7500 (0-10), 22500 (10-20), 37500 (20-30), 52500 (30-40), 67500 (40-50), 82500 (50-60), 97500 (60-70), 112500 (70-80), 127500 (80-90), 142500 (90-100), 157500 (100-110), 172500 (110-120), 187500 (120-130), 202500 (130-140), 217500 (140-150), 232500 (150-160), 247500 (160-170, marcado como no confirmado en 6.4).
  - Patrón: cada tramo suma 15000 XP más que el anterior, empezando en 7500.
- **Nomenclatura de calidad por tramo** (10 niveles = 1 calidad), igual en las 3 hojas: Tosco, Rudimentario, Imperfecto, Frágil, Rústico, Bruto, Sólido, Duradero, Refinado, Precioso, Exquisito, Místico, Eterno, Divino, Infernal, Ancestral, (siguiente sin confirmar).
- **Profesiones de fabricación que comparten receta/recursos por pares** (mismo material, distinto ítem final): Joyero↔Armero (minerales), Maestro de Armas↔Ebanista (madera). Si el usuario levea ambas profesiones de un par a la vez, el farmeo/compra se puede compartir y duplicar el uso, reduciendo el "coste por unidad de aprendizaje".

## 8. Datos verificados en fuente autorizada y reciente: methodwakfu.com/artisanat/les-metiers/ (última actualización 23-nov-2025, versión de juego citada: Wakfu 1.79)

Esta es, de las fuentes ya consultadas, **la más fiable y reciente**. Resuelve varias de las dudas de la sección 9 (Contradicciones). Todo lo de aquí abajo se puede dar por bueno salvo que el usuario aporte algo más nuevo.

### 8.1 Lista oficial de profesiones
- **Recolección (6)**: Paysan (Campesino), Herboriste (Herbolario), Forestier (Leñador), Pêcheur (Pescador), Mineur (Minero), Trappeur (Trampero). Se conocen automáticamente desde la creación del personaje.
- **Fabricación (8)**: Armurier (Armero), Bijoutier (Joyero), Maroquinier (Marroquinero), Tailleur (Sastre), Maître d'armes (Maestro de Armas), Ébéniste (Ebanista), Boulanger (Panadero), Cuisinier (Cocinero). Hay que aprenderlas con un PNJ Maestro Artesano (en Astrub o en las capitales de nación) antes de poder craftear.

### 8.2 Tabla de tramos de componente ↔ nivel de oficio ↔ nivel del ítem resultante
**Importante**: el nivel de oficio y el nivel del ítem/equipo resultante **no son el mismo número** — un desfase que hay que tener siempre presente al hablar con el usuario de "a qué nivel de equipo me sirve esto".

| Calidad del componente | Nivel de oficio | Nivel del ítem resultante |
|---|---|---|
| Grossier (Tosco) | 0-10 | 6-20 |
| Rudimentaire | 10-20 | 21-35 |
| Imparfait (Imperfecto) | 20-30 | 36-50 |
| Fragile (Frágil) | 30-40 | 51-65 |
| Rustique (Rústico) | 40-50 | 66-80 |
| Brut (Bruto) | 50-60 | 81-95 |
| Solide (Sólido) | 60-70 | 96-110 |
| Durable | 70-80 | 111-125 |
| Raffiné (Refinado) | 80-90 | 126-140 |
| Précieux (Precioso) | 90-100 | 141-155 |
| Exquis (Exquisito) | 100-110 | 156-170 |
| Mystique (Místico) | 110-120 | 171-185 |
| Eternel (Eterno) | 120-130 | 186-200 |
| Divin (Divino) | 130-140 | 201-215 |
| Infernal | 140-150 | 216-230 |

Esta tabla **coincide** con la columna "nivel de personaje" de la hoja 6.4 (`Tabla_de_oficios_de_fabricación (ES)`), lo cual la valida cruzadamente. Buena señal de que esa hoja sigue vigente en cuanto a estructura, aunque conviene revisar recursos concretos de los tramos altos (150+) por si hay parches más recientes.

### 8.3 Nivel máximo y componente base por profesión de fabricación

| Profesión | Nivel máx. de oficio | Componente base | Recetas principales |
|---|---|---|---|
| Armurier (Armero) | 170 | Plaques (Placas) — minerales | Escudos, petos, hombreras |
| Bijoutier (Joyero) | 170 | Gemmes (Gemas) — minerales | Anillos, amuletos |
| Boulanger (Panadero) | 160 | Huiles (Aceites) — plantas silvestres | Panes (regeneración de vida) |
| Cuisinier (Cocinero) | 160 | Épices (Especias) — peces | Platos (bonus de stats temporales) |
| Ébéniste (Ebanista) | 165 | Équerres (Escuadras, madera) + Orbes (recursos de monstruos) | Objetos decorativos/utilitarios, llaves de intervención, transmutaciones, sublimaciones |
| Maître d'Armes (Maestro de Armas) | 170 | Manches (Mangos) — madera | Armas de una/dos manos |
| Maroquinier (Marroquinero) | 170 | Cuirs (Cueros) — drop de monstruos | Botas, cinturones, bolsas |
| Tailleur (Sastre) | 170 | Fibres (Fibras) — cereales | Capas, tocados |

(Nota: la fuente también lista niveles máx. para los oficios de **recolección** cuando tienen recetas de refinado propio — Forestier 165, Herboriste 165, Mineur 165, Paysan 165, Pêcheur 165, Trappeur 165 — pero esas recetas son secundarias/herramientas de oficio, no el objetivo principal de leveo del usuario salvo que lo pida.)

**Confirma y corrige la hoja 6.1** (`_Wakfu_Crafting_Professions_Leveling_Calculator`): Joyero y Armero comparten familia de recursos (minerales) como decía esa hoja, y el patrón de tramos de 10 en 10 hasta 170 es correcto, aunque el nivel máximo real del oficio es **170**, no 160 (la hoja subida se quedaba corta).

### 8.4 Fórmula de XP de crafteo (resuelve la contradicción entre las hojas 6.1 y 6.3 — ver detalle en la sección 9.1)

> **XP obtenida = BaseXP × Additifs × BonusSiNivTropBas × BonusBP × BonusÉvènement**

Donde:
- **BaseXP**: XP base de esa receta concreta. **No es una constante universal** — cada receta tiene la suya. Esto explica por qué la hoja 6.1 usaba "300" como valor editable de ejemplo y la hoja 6.3 usaba "660": **ambas eran valores de ejemplo/placeholder para una receta concreta, no una constante del juego**. La forma correcta de obtener el BaseXP real de una receta es mirarlo en Craftkfu (que es justo la función que describe Jobkfu: "usa la base de XP de la receta indicada en Craftkfu").
- **BonusSiNivTropBas**: bonus si el jugador intenta la receta con menos del 100% de probabilidad de éxito (cuanto más por debajo del nivel recomendado, más XP extra si tiene éxito — pero also more risk of failure, ver 8.5).
- **BonusBP**: +50% si el jugador tiene Booster Pack activo.
- **BonusÉvènement**: eventos bonus temporales de Ankama, o la "Mea Coulpable" (+100%, compensación antigua).
- Bonos adicionales que se acumulan de forma aditiva entre sí (no multiplicativa): Guilde I +5%, Guilde II +5% (mejoras de gremio nivel 4 y 7), Havre-Monde +10% (una vez construido el edificio de oficio), Turbo Craft 30 +100% durante 30 min (crupier de compensación, cuesta 5 fichas), Mea Coulpable +100% durante 12h de juego (compensación antigua, no siempre disponible). **Ojo**: Turbo Craft 30, Potion d'Artisanat Véloce, Artipotion Exceptionnelle y Mea Coulpable **no son acumulables entre sí** (son excluyentes, hay que elegir uno).

  Esto **confirma** los inputs de la hoja 6.3 (`Copia_de_New_tabla_de_oficios_wakfu`): booster pack, bonus de gremio (%), evento de oficios (0/1) son exactamente estas variables.

- La **fórmula `75 + (N-1)×150`** del docx en francés (sección 6.5) **no aparece en esta fuente** para crafteo — es probable que sea una fórmula distinta (quizá de recolección/plantación en un contexto específico, o de una mecánica antigua). **No usar todavía para calcular XP de crafteo; tratar como no confirmada.**

### 8.5 Probabilidad de éxito y XP degresiva (mecánica nueva, no estaba en ninguna hoja subida)

- El **nivel de una receta = nivel a partir del cual el jugador tiene 100% de probabilidad de éxito.**
- Se puede intentar una receta por debajo de ese nivel, con **-10% de probabilidad de éxito por nivel de diferencia** (ej. Ebanista nivel 41 intentando receta nivel 50 → 10% de probabilidad).
- **Si falla, se pierden los materiales y no se gana XP.** Esto es un riesgo real de "coste en kamas perdidos" que hay que advertir al usuario si alguna vez recomendamos craftear por debajo del nivel recomendado buscando el bonus de XP.
- Si el jugador está **más de 10 niveles por encima** de la receta, la XP ganada empieza a bajar progresivamente hasta llegar a **0 XP a partir de 20 niveles de diferencia**. Esto es clave para el diseño de la ruta: **hay que cambiar de receta como muy tarde al llegar a ~20 niveles por encima de la receta actual**, y probablemente conviene cambiar bastante antes (en torno a +10) para no perder eficiencia de XP/material.
- **Nivel máximo real del oficio = nivel de la última receta/recurso disponible + 20** (fórmula general del juego, consistente con la tabla de la sección 8.3: p.ej. si la última receta de fabricación es nivel 150, el oficio puede seguir subiendo craft eando esa receta hasta nivel 170 antes de quedarse sin poder progresar más, aunque ineficientemente).

### 8.6 Havre-Sac (Havenbag) y talleres — relevante para farmeo pasivo y crafteo cómodo
- **Craftear en el Havre-Sac SÍ da XP** de oficio con normalidad (y se benefician de todos los bonus de XP de fabricación).
- **Plantar/recolectar dentro del Havre-Sac NO da nada de XP** de oficio (a diferencia de crafteo). Además la probabilidad de plantación baja a 60% (10% menos que en exterior) dentro del HS, aunque no depende del clima.
- Hay 3 niveles de taller craftables por un Ebanista para meter en el Havre-Sac: **Petit atelier** (recetas nivel 0-40), **Atelier** (0-80), **Grand atelier** (0-150). Ojo: el Grand Atelier **no cubre los tramos más altos** (150-170) — para esos habrá que ir a un taller grande de nación/capital.
- Existe el **"craft sécurisé"**: otros jugadores pueden usar tus talleres del Havre-Sac (con tu nivel de oficio) pagando un precio que tú fijas, sin tener que darte los materiales directamente — el XP se lo lleva el dueño del Havre-Sac, no el cliente. No es relevante para el objetivo del usuario salvo que quiera rentabilizar niveles ya conseguidos.

### 8.7 Herramientas comunitarias, confirmadas por la fuente oficial de referencia
La propia MethodWakfu recomienda exactamente las mismas 2 herramientas que el usuario ya había mencionado, confirmando que son las de referencia de la comunidad:
- **Craftkfu** (autor original Vertylo, mantenido ahora por Mathius): lista los recursos necesarios para las recetas elegidas.
- **Jobkfu** (Vertylo): calcula el número de crafteos necesarios para llegar a un nivel de oficio dado, **usando como dato de entrada la XP base de la receta que muestra Craftkfu** — es decir, hay que mirar primero en Craftkfu la XP base de la receta elegida y meterla en Jobkfu.

## 9. Contradicciones / huecos detectados — estado actualizado (algunas ya resueltas en el milestone de la sección 8, NO inventar el resto)

1. ~~**EXP por componente**: 300 vs 660~~ → **RESUELTO** (ver 8.4): no es una constante universal, cada receta tiene su propio BaseXP; los valores 300/660 de las hojas 6.1/6.3 eran solo ejemplos editables. Para el BaseXP real de una receta concreta hay que consultarlo en Craftkfu.
2. **Fórmula de XP `75 + (N-1)×150`** del docx en francés (sección 6.5): sigue **sin verificar** — no aparece en la fórmula de fabricación confirmada por methodwakfu (sección 8.4). Hipótesis a confirmar con el usuario: podría ser de una mecánica distinta (recolección/plantación) o de una versión antigua del juego. **No usarla para calcular XP de crafteo.**
3. **Vigencia general de `Wakfu_Sheets.xlsx`** (hoja 6.2, en inglés): sigue sin confirmar su fecha real; puede tener años. La tabla de tramos de nivel de oficio de las hojas 6.1/6.3/6.4 **sí queda validada** por methodwakfu (coincide en tramos de "nivel de personaje"/"nivel de ítem"), pero los **recursos concretos de los tramos altos (150+)** de `Wakfu_Sheets.xlsx` siguen sin contrastar.
4. **Nivel máximo real de oficio**: **RESUELTO parcialmente** (ver 8.3): Armurier/Bijoutier/Maître d'Armes/Maroquinier/Tailleur = 170; Boulanger/Cuisinier = 160; Ébéniste = 165. Las hojas subidas que solo llegaban a 160-170 con tramos "???" quedan así explicadas: el "???" del tramo 160-170 en la hoja 6.4 corresponde justo a las profesiones que sí llegan a 170 (Armero, Joyero, Maestro de Armas, Marroquinero, Sastre) — pendiente aún conseguir los recursos concretos de ese último tramo.
5. ~~No se ha explorado el repo de GitHub ni hecho fetch en vivo~~ → **RESUELTO parcialmente** (ver sección 5): repo de GitHub revisado (es una app, no una fuente de datos); methodwakfu/les-metiers leído con éxito. **Sigue pendiente**: craftkfu y wakfujobcalculator no son accesibles por fetch (son SPAs JS) — necesitan que el usuario las use manualmente y pegue los resultados; y falta leer methodwakfu/localisation-des-ressources y methodwakfu/plans-et-recettes.
6. **Nuevo hueco detectado en este milestone**: no sabemos todavía el **BaseXP real** de ninguna receta concreta (solo la fórmula y de dónde sacarlo). Sin eso no se puede calcular "cuántos crafteos necesita el usuario" con precisión — es el dato bloqueante nº1 para la siguiente sesión. **Nota (mismo milestone, más tarde)**: el flujo operativo de la sección 3 minimiza este bloqueo pidiendo solo el BaseXP de las recetas de los tramos concretos de la ruta del usuario, no de todo el juego.
7. **Nuevo dato a validar con el usuario**: la mecánica de "XP degresiva" (sección 8.5) implica que la estrategia óptima de ruta probablemente sea cambiar de receta bastante antes de los 20 niveles de diferencia (posiblemente hacia +10), lo que puede chocar con el objetivo de "pocas recetas distintas" del usuario (sección 1, punto 3) — hay un trade-off real entre "menos recetas" y "más XP por material" que hay que explicarle explícitamente cuando se calcule la ruta (paso 6 del flujo operativo, sección 3).

## 10. Plan de acción para la siguiente sesión (checklist)

Ya hechos en este milestone (no repetir):
- [x] Explorado el repo `wakfu-farm-tracker-public` → es una app de tracking, no una fuente de datos consultable (sección 5).
- [x] Confirmado que craftkfu.waklab.fr y wakfujobcalculator.com son SPAs JS no accesibles por fetch/búsqueda automática (sección 5).
- [x] Leído methodwakfu.com/artisanat/les-metiers/ en profundidad → resuelve niveles máximos por profesión, fórmula de XP de crafteo, probabilidad de éxito/XP degresiva, mecánica de Havre-Sac (sección 8).
- [x] Resuelta la contradicción "300 vs 660 XP por componente" (sección 9.1).
- [x] Formalizado el flujo operativo de cálculo de ruta / motor de decisión de recetas (sección 3), cubriendo el gap señalado por el usuario: nadie decide qué receta seguir por coste, solo se trackea progresión.

Pendientes reales para arrancar el trabajo con el usuario:
1. [ ] Preguntar al usuario los datos de la sección 4 (profesión, niveles, servidor, restricciones, bonuses activos) — paso 1 del flujo operativo.
2. [ ] Leer `methodwakfu.com/artisanat/localisation-des-ressources/` y `methodwakfu.com/artisanat/plans-et-recettes/` (ambas enlazadas y accesibles por fetch, mismo dominio que ya funcionó) para completar ubicaciones y sistema de planos especiales.
3. [ ] Conseguir el **BaseXP real** de las recetas de la profesión elegida, pero **solo de los tramos que toca la ruta del usuario** (paso 4 del flujo operativo, sección 3): pedir al usuario que abra Craftkfu para esas recetas concretas y pegue las cifras, o pasar capturas de Jobkfu/wakfujobcalculator ya rellenados.
4. [ ] Con el BaseXP real, aplicar la fórmula completa de la sección 8.4 (con los bonuses activos del usuario) para calcular crafteos necesarios por tramo (paso 5 del flujo operativo).
5. [ ] Decidir junto al usuario el trade-off de la sección 9.7 (menos recetas vs. más XP/material, por la XP degresiva a partir de +10/+20 niveles) — paso 6 del flujo operativo.
6. [ ] Construir la tabla de referencia acumulada por profesión (nivel receta / ítem / XP / materiales+cantidad / coste estimado) tal como pide el system prompt (sección 2).
7. [ ] Proponer la ruta tramo a tramo con alternativas barata/segura, marcando explícitamente cualquier dato no confirmado (recursos de tramos 150-170 siguen sin contrastar en fuente reciente) — paso 7 del flujo operativo.
8. [ ] Si el usuario pide el plan como documento, generarlo en xlsx (reutilizando el formato de la hoja 6.4, que es el más claro) o en markdown, según prefiera.

---

*Documento generado a partir de: 5 archivos subidos por el usuario, descripciones de 7 fuentes online indicadas por el usuario, y fetch en vivo (03-sep-2026) a github.com/olivo28/wakfu-farm-tracker-public y methodwakfu.com/artisanat/les-metiers/. No incluye datos de precios de mercado reales (Hotel de Ventas) porque ninguna fuente aportada hasta ahora los confirma en vivo; deben pedirse al usuario o consultarse en Craftkfu/wakfujobcalculator cuando el usuario las use manualmente (son SPAs no accesibles por fetch automático).*

*Actualización (mismo milestone, 03-sep-2026): añadida la sección 3 (Flujo operativo de cálculo de ruta / motor de decisión de recetas), formalizando cómo se cubre el hueco de "qué receta seguir por coste" que ninguna herramienta externa del usuario resolvía. Se renumeraron las secciones 3-9 → 4-10 en consecuencia, y se corrigió un desajuste de numeración interno del documento (la antigua sección 7 tenía subsecciones etiquetadas 9.1-9.7; ahora es la sección 8 con subsecciones 8.1-8.7, consistente con las referencias cruzadas de la sección 9/Contradicciones).*
