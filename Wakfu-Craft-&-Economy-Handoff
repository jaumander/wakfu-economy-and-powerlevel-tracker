# Wakfu Craft & Economy — HANDOFF MAESTRO

> **Qué es esto**: documento único que fusiona los tres handoffs previos del
> proyecto en uno solo, ahora que el repo también está fusionado:
> - `Wakfu_Craft_PowerLevel_Helper_HANDOFF.md` (v6, 03-sep-2026) — mecánica de
>   profesiones, arquitectura de datos del Optimizer, Recetario.
> - `Wakfu-Craft-&-Economy-Handoff.txt` (08-sep-2026, actualizado 14-sep-2026)
>   — confirmación del repo fusionado, incidente de seguridad del token,
>   auditoría real de `recetario_wakfu.html`, diseño del Broker de precios.
> - `HANDOFF-broker-of-wakfu-street.md` (14-sep-2026) — la app real del
>   Economy Tracker (`wakfu-economy-tracker.html`), su esquema de
>   `window.storage`, principios de seguridad y metodología de edición.
>
> **A partir de ahora usar solo este archivo.** Los tres anteriores quedan
> como referencia histórica pero no se deben actualizar más — cualquier
> cambio de estado va aquí.
>
> Sube o enlaza este `HANDOFF.md` al iniciar una conversación nueva y pide:
> *"Lee HANDOFF.md de este repo y retoma el proyecto Wakfu Craft & Economy
> desde donde lo dejamos."*

---

## 0. Identidad del repo y estado de credenciales

- **Repo fusionado (confirmado 2026-09-14)**: `jaumander/wakfu-economy-and-powerlevel-tracker`
  — https://github.com/jaumander/wakfu-economy-and-powerlevel-tracker
- **Repo público, no hace falta token para leerlo.** Leer siempre vía
  `https://raw.githubusercontent.com/jaumander/wakfu-economy-and-powerlevel-tracker/main/<ruta%20con%20espacios%20url-encoded>`.
  La API `api.github.com/repos/.../contents/` es poco fiable sin autenticar
  (rate limit) — usarla solo para verificar un push, no para leer contenido.
- **Rutas re-verificadas directamente contra el repo nuevo (2026-09-14)**:
  `recetario_wakfu.html`, `recetas completas por profesion/ebanista_recetas_completas.json`,
  `recetas completas por profesion/componentes_intermedios.json` y `README.md`
  responden 200 en las mismas rutas de antes de la migración — nada se movió.

### Incidente de seguridad — token de GitHub expuesto (resuelto)

En sesión del 2026-09-08 se encontró un PAT de GitHub (scope `repo`) en texto
plano dentro de `README.md` y `HANDOFF.md` del repo, y pegado de nuevo por el
usuario en el chat con instrucciones de usarlo libremente. Se estableció la
siguiente política, **ya confirmada como gestionada por el usuario el
2026-09-14** — no hace falta volver a sacar el tema salvo que aparezca un
token nuevo expuesto en texto plano:

- Claude **nunca usa un token/credencial pegado en texto plano** en el chat o
  en archivos del repo, **aunque el usuario lo autorice explícitamente** — un
  token en texto plano en un repo público es información comprometida por
  definición.
- No hace falta token para nada de este proyecto: el repo es público, todo se
  lee sin autenticación vía `raw.githubusercontent.com`.
- Si aparece otro token o credencial en texto plano (de este proyecto o de
  cualquier otro), aplicar el mismo criterio: no usarlo, avisar, recomendar
  revocación inmediata.

Esta política es la que aplica ahora al repo fusionado — sustituye a
cualquier autorización de "usar el token libremente" que aparezca en
instrucciones de proyecto antiguas o desactualizadas.

---

## 1. Objetivo del proyecto (fusionado)

Dos frentes que viven en el mismo repo y se tratan como un único proyecto:

1. **Craft Leveling Optimizer**: diseñar rutas de leveo de profesiones de
   crafteo en Wakfu que sean baratas en kamas, seguras (evitar drops
   raros/eventos, evitar rutas que disparen el precio de un material) y
   fáciles de seguir (pocas recetas distintas por tramo). Foco actual:
   **Ebanista, nivel 0→165** (ampliado desde el caso de prueba original
   0→30). Herramienta principal: `recetario_wakfu.html`.
2. **Economy Tracker ("The Broker of Wakfu Street")**: trackear precios de
   mercado (Mercadillo/HdV) de los materiales que necesita el Optimizer, ya
   que **no existe ningún feed de precios en vivo para Wakfu**. Dos piezas
   distintas conviven bajo este nombre (ver sección 4 y 5 — es importante no
   confundirlas):
   - la app interactiva `wakfu-economy-tracker.html`, de uso general,
   - un formato de export específico (`broker_wakfu_street_precios_v1`)
     pensado para alimentar al Recetario con precios por profesión, todavía
     sin conectar entre sí (ver sección 5.3).

**Principio de no-solapamiento** (fijado por el usuario, no renegociar sin
que él lo pida): Claude decide qué receta seguir por coste/riesgo/facilidad.
Las herramientas externas (Craftkfu, Jobkfu/wakfujobcalculator) hacen lo que
ya hacen bien (listas de la compra ya elegidas, cálculo de crafteos con
bonuses) — Claude redirige a ellas en vez de duplicar esa función.

---

## 2. Instrucciones de comportamiento (system prompt consolidado)

> Eres un asistente especializado en optimizar el leveo de profesiones de
> crafteo en el MMO Wakfu (Ankama) y en trackear la economía de mercado
> necesaria para calcularlo, porque no existe un feed de precios en vivo.
>
> **Al empezar** (si no se ha dicho ya), pregunta: profesión, nivel actual,
> nivel objetivo, restricciones (zonas farmeables, Havre-Sac, gremio) y
> bonuses activos (booster pack, bonus de gremio, pociones/turbo-craft). **No
> preguntes por el servidor** — decisión explícita del usuario, fuera de
> alcance. Si la profesión tiene pareja en la matriz de sinergias (sección
> 8), menciónalo de forma proactiva sin convertirlo en pregunta obligatoria.
>
> **Flujo de cálculo de ruta**: delimitar tramos → listar recetas candidatas
> por tramo (usando las bases de datos ya extraídas, sección 6.3) → obtener
> BaseXP/materiales exactos vía el extractor de datos, nunca a mano →
> calcular (o delegar en Jobkfu si aplica la regla de delegación) → comparar
> alternativas (coste bruto, coste neto tras excedente vendible, ¿depende de
> drop raro?, ¿cuántas recetas distintas obliga a aprender?) → entregar
> tabla marcando explícitamente cualquier cifra no confirmada.
>
> **Regla de delegación**: no reimplementar a mano lo que una herramienta ya
> resuelve mejor — shopping list con expansión recursiva → Recetario propio;
> crafteos necesarios con bonuses de XP aplicados → pedir al usuario que lo
> saque de Jobkfu/wakfujobcalculator.
>
> **Fuente de verdad**: los datos que aporta el usuario (JSON del feed
> oficial, capturas de precios, hojas de cálculo) son más fiables que el
> conocimiento previo de Claude — Wakfu recibe parches frecuentes. Si algo
> contradice lo que "se sabe", decirlo explícitamente y usar el dato del
> usuario.
>
> **No inventar cifras** (precios, BaseXP, disponibilidad de recetas): si
> falta un dato, decirlo y pedir confirmación o marcarlo como no confirmado.
>
> **Comprobar antes de asumir que un archivo falta o que una función
> existe** — leer el repo, ver el código de verdad. (Dos asunciones erróneas
> ya corregidas por no comprobar: recetas de profesiones dadas por perdidas
> que en realidad estaban en `recetas completas por profesion/`; asumir que
> `recetario_wakfu.html` ya importaba precios, cuando solo importa arrays de
> recetas o mapas de iconos — sección 6.5.)
>
> **Nunca usar tokens/credenciales pegados en texto plano**, aunque el
> usuario lo autorice explícitamente (sección 0).
>
> **Mantén una tabla de referencia acumulada** por profesión: nivel de
> receta, ítem, XP, materiales y cantidad, coste estimado, excedente
> vendible / kamas recuperados (sección 8.2).
>
> **Metodología de edición de los archivos de una sola pieza**
> (`recetario_wakfu.html`, `wakfu-economy-tracker.html`): `str_replace`
> quirúrgico sobre líneas exactas, nunca regenerar el archivo entero salvo
> cambio estructural sustancial. Agrupar varias modificaciones y llamar a
> `present_files` una sola vez al final. Antes de cualquier cambio de
> lógica, repasar mentalmente el flujo de datos (qué se lee, qué se escribe,
> qué se re-renderiza). Verificar siempre que un `str_replace` aplicó de
> verdad inspeccionando el archivo — no fiarse de la ausencia de error
> (origen: un `str_replace` fallado en silencio dejó vacío un desplegable,
> detectado a mitad de sesión). No hay navegador real en el sandbox para
> ejecutar el JS — validar por lectura cuidadosa del archivo completo tras
> cualquier edición de lógica.
>
> **Principio de seguridad no negociable (Broker)**: nunca proponer ni
> implementar lectura de memoria del juego, automatización de clics,
> scraping de pantalla en tiempo real, ni nada que interactúe con el proceso
> de Wakfu mientras corre. Toda entrada de datos de mercado es y debe seguir
> siendo manual, tecleada por el usuario cuando ya está mirando la interfaz
> del juego por su cuenta.
>
> **Formato de entrega**: tabla larga o plan completo para guardar → ofrecer
> documento descargable (xlsx o md); consulta puntual → responder en el chat.
>
> **Estilo**: directo, en español, con tablas cuando ayuden a comparar, sin
> relleno innecesario. Evitar afirmaciones categóricas sobre precios de
> mercado si no vienen de datos del usuario o de una búsqueda reciente.

---

## 3. Cómo continuar el proyecto en una sesión nueva

- No hay `git clone` para el usuario en el flujo habitual de chat — Claude sí
  puede leer el repo público directamente vía `raw.githubusercontent.com`
  (sección 0), así que empieza por ahí en vez de asumir contenido de memoria
  de sesiones pasadas.
- El `wakfu-economy-tracker.html` usa `window.storage`, no hay forma de que
  Claude lea o escriba directamente ese storage — si el usuario ha perdido
  datos (cuenta nueva, navegador distinto), pídele el `.json` de "Exportar
  datos" y ofrécele restaurarlo vía "Importar datos" desde la propia
  interfaz.
- Si una tarea queda a medias, dilo explícitamente en el chat (qué falta,
  qué archivo tocar) en vez de dejarlo implícito — la continuidad depende de
  que este `HANDOFF.md` esté al día y de que el usuario suba los archivos
  nuevos al repo, no de un estado oculto.

---

## 4. Economy Tracker — la app real: `wakfu-economy-tracker.html`

Único archivo HTML/JS con almacenamiento persistente vía `window.storage`.
Sin backend, sin dataset externo que descargar ni parsear en este archivo
más allá del catálogo embebido (sección 4.4).

### 4.1 Las cuatro pestañas

1. **Vigía & Snapshots** — lista de vigilancia de objetos (nombre + categoría
   opcional) y formulario para capturar precio/cantidad del Mercadillo en el
   momento en que el usuario ya está mirando el juego.
2. **Tendencias & Alertas** — historial por objeto con sparklines de
   precio/cantidad, y alertas automáticas (subida de precio + oferta bajando
   = posible nicho; bajada de precio + oferta subiendo = posible saturación;
   oferta baja y estable = pocos vendedores activos).
3. **Mis Ventas** — registro manual de ventas propias (vendido/no vendido),
   con stats agregados: kamas cobrados, tasa de venta, precio medio.
4. **Cuaderno de Nichos** — notas de texto libre con tag opcional, para
   hipótesis de mercado que no encajan en datos estructurados.

Export/import JSON es el mecanismo de portabilidad entre cuentas — formato
`{exportedAt, watchlist, snapshots, sales, journal}`. **El importador hace
overwrite completo de las cuatro claves, no merge** — un import parcial
borra lo que no incluya.

### 4.2 Esquema de datos (`window.storage`, todas `shared:false`)

- `watchlist`: `{id, name, cat}`
- `snapshots`: `{id, itemId, date, price, qty}` — `price`/`qty` pueden ser
  `null` si el usuario solo rellenó uno de los dos
- `sales`: `{id, name, price, sold, date}`
- `journal`: `{id, date, tag, text}`

Cualquier campo nuevo debe ser opcional con fallback razonable al leer, para
no romper datos ya guardados ni el import/export.

### 4.3 Sistema de diseño

- Fondo tinta `#14171c`, paneles `#1b1f26` / `#20252d`, línea `#2c323c`.
- Acento principal (kamas, precios): oro apagado `#c9a227`. Acento
  secundario (cantidad/oferta): verde-teal `#3a8a76`.
- Subida de precio / oportunidad: `#5fa777`. Bajada / aviso: `#c1554b`.
- Tipografía: Fraunces para títulos, IBM Plex Sans para cuerpo, IBM Plex Mono
  (tabular) para cualquier número. No mezclar fuentes fuera de estos tres
  roles.
- Nada de gradientes decorativos ni animaciones de carga innecesarias — es
  una herramienta de trabajo, no una landing page.

### 4.4 Catálogo embebido

- ~6.734 objetos únicos de Wakfu, fusionados desde datos del CDN de Ankama.
- Jerarquía oficial completa de categorías del Mercadillo (~8 grupos, ~73
  subcategorías).

### 4.5 Verificación antes de asumir

El Mercadillo puede cambiar de columnas, filtros o comportamiento entre
parches, igual que el JSON de Ankama puede cambiar de esquema. Antes de
asumir un campo nuevo (cantidad de vendedores, nivel mínimo/máximo, una
columna no vista antes): pedir una captura actualizada de esa parte de la
interfaz antes de programar el parser o el formulario, y no asumir nombres
de campo "porque suena lógico" ni por capturas antiguas si ha pasado tiempo.

---

## 5. Broker de precios para el Optimizer — `broker_wakfu_street_precios_v1`

Formato distinto del anterior: no es lo que exporta
`wakfu-economy-tracker.html` (sección 4.2), sino un esqueleto de precios
generado específicamente para alimentar al Recetario con los materiales de
una profesión concreta.

### 5.1 Esquema

```json
{
  "schema": "broker_wakfu_street_precios_v1",
  "profesion": "Ebanista",
  "generado": "2026-09-08",
  "nota": "...",
  "total_materiales": 237,
  "materiales": [
    {
      "material": "nombre del recurso",
      "precio_hdv": null,
      "farmable": null,
      "usos": [
        {
          "profesion": "Ebanista",
          "tramo_nivel_oficio": 0,
          "tipo_componente": "escuadrita_madera | orbe_drop",
          "receta_origen": "nombre del ítem que se craftea con este material",
          "cantidad_por_crafteo": 5,
          "variante_idx": 0,
          "activo_por_defecto": true
        }
      ]
    }
  ]
}
```

### 5.2 Decisión de escalabilidad ya tomada

- El cierre completo de Ebanista (Escuadrita + todas las variantes de Orbe,
  0→150) son **237 materiales únicos** — inviable para trackear precio a
  mano de golpe.
- Enfoque escalable: el JSON incluye las 237 entradas, pero solo **64**
  (Escuadrita de cada uno de los 16 tramos + **1 variante de Orbe por
  tramo**, la primera listada en los datos fuente) quedan
  `"activo_por_defecto": true`. El resto queda documentado
  (`activo_por_defecto: false`) para activarse más adelante sin regenerar el
  archivo.
- **No decidido todavía**: qué variante de Orbe es la "mejor" por tramo — el
  default actual es simplemente la primera que aparece en los datos de
  Ankama, no una elección informada. Revisar cuando haya precios reales de
  varias variantes.

### 5.3 Estado — pendiente de conectar con la app real (pregunta de arquitectura abierta)

- **Ningún precio está relleno todavía** (`precio_hdv: null` en las 237
  entradas). El fichero generado es solo el esqueleto de qué trackear, no
  datos de mercado reales.
- `broker_wakfu_street_ebanista.json` fue entregado al usuario como descarga
  y **todavía no está subido al repo** — Claude no hace push directo de
  este tipo de archivo, el usuario debe subirlo manualmente.
- **`recetario_wakfu.html` no reconoce este schema todavía** (sección 6.5) —
  hacen falta dos piezas nuevas de código antes de que sea importable tal
  cual.
- **Pregunta de arquitectura sin resolver**: este esqueleto de precios por
  profesión (`broker_wakfu_street_precios_v1`) y el `watchlist` de la app
  `wakfu-economy-tracker.html` (sección 4.2) son a día de hoy dos cosas
  independientes con formatos distintos, aunque comparten nombre ("Broker of
  Wakfu Street"). No está decidido si conviene:
  - (a) que la app exporte también en formato `precios_v1` para una
    profesión filtrada, o
  - (b) mantenerlos separados — la app para tracking general, el JSON
    `precios_v1` como artefacto puntual generado por Claude por profesión.
  No asumir ninguna de las dos sin que el usuario lo decida explícitamente.

---

## 6. Craft Leveling Optimizer — arquitectura de datos

### 6.1 Cómo se llegó aquí (para no repetir investigación ya descartada)

El flujo antiguo (usuario abre Craftkfu → captura → Claude transcribe a
mano) era lento y propenso a errores. Se investigó clonar/inspeccionar
Craftkfu (`craftkfu.waklab.fr`, SPA no fetcheable) y sus repos de GitLab
(`wakdata-rest-api-crystal`, `wakdata`, `WakTisanat`, del mantenedor Mathieu
Féry/MathiusD). **Conclusión: no aporta nada nuevo** — `wakdata` confirma
que sus datos vienen del mismo CDN de Ankama, y GitLab renderiza con JS
igual que Craftkfu. **No merece la pena repetir esto**: el cuello de botella
nunca fue no saber dónde están los datos, sino que Claude no puede abrir
URLs no indexadas — pero **el usuario sí puede** abrirlas en su navegador
(JSON plano, sin JS) y subirlas para que Claude las procese.

### 6.2 Cascada de fuentes para BaseXP / materiales / precio

1. **Feed JSON oficial de Ankama, vía descarga manual del usuario +
   extractor — método por defecto.** El usuario descarga con Ctrl+S:
   - `https://wakfu.cdn.ankama.com/gamedata/config.json` → versión actual
     (última confirmada: **1.92.1.60**; Craftkfu va 2 parches por detrás,
     no es un problema).
   - `.../{version}/recipes.json` (~900 KB)
   - `.../{version}/recipeIngredients.json` (~4 MB)
   - `.../{version}/recipeResults.json` (~750 KB)
   - `.../{version}/jobsItems.json` (~8.7 MB; incluye título/descripción en
     4 idiomas y `graphicParameters.gfxId`, usado para los iconos del
     Recetario)

   Sube esos 4 archivos y Claude corre `wakfu_recipe_extractor.py` (sección
   6.4) sobre ellos. **Nunca usar `items.json` completo** (coste en tokens
   muy alto). **Un fetch por sesión de cálculo, no por turno.**

2. **(Fallback, poco fiable) Fetch directo por Claude.** Solo `config.json`
   es accesible de forma fiable; los archivos versionados no lo son —
   confirmado repetidamente, no depender de esto.

3. **Precio de mercado (HdV) — siempre manual, no tiene atajo.** No existe
   fuente viva (Wakfu-Elements, el único parser que existió, está
   abandonado). Pedir captura del precio actual de materiales y del ítem
   resultante (para excedente vendible, sección 8.2). Tratar como snapshot
   con fecha, no reutilizable entre sesiones.

4. **Clasificación "farmeable vs. drop de mob"**: el feed no lo distingue
   directamente. Se infiere por patrón (1 material raro x1 + otro común x7 =
   probable drop de mob) pero no está confirmado con datos duros. Pendiente
   de probar `harvestLoots.json`/`monsterDrops.json` (repo
   `Vertylo/wakassets`, también fuente de iconos).

5. **Si nada de lo anterior está disponible**: estimación explícitamente
   marcada como no confirmada, nunca inventada como si fuera real.

### 6.3 El script: `wakfu_recipe_extractor.py`

Cruza los 4 JSON del nivel 1 y produce una tabla limpia (nivel, XP,
resultado, materiales, nombres en español) para una profesión y rango de
nivel concretos.

```
python3 wakfu_recipe_extractor.py \
  --recipes recipes.json --items jobsItems.json \
  --results recipeResults.json --ingredients recipeIngredients.json \
  --category-id 81 --min-level 0 --max-level 200 \
  --output ebanista_recetas_completas.json
```

Modos adicionales: `--find-category-id "<nombre exacto de un ítem>"` (usar
dos ítems por profesión, tosco + rudimentario, para confirmar por partida
doble); `--categories recipeCategories.json --list-categories`
(best-effort, sin probar); `--export-icon-map --output iconos.json`.

### 6.4 Mapeo de profesiones → categoryId (100% confirmado)

| categoryId | Profesión | Recetas | Base de datos |
|---|---|---|---|
| 40 | Panadero | 89 | `panadero_recetas_completas.json` |
| 74 | Peletero | 49 | `peletero_recetas_completas.json` |
| 76 | Cocinero | 132 | `cocinero_recetas_completas.json` |
| 77 | Armero | 966 | `armero_recetas_completas.json` |
| 78 | Joyero | 964 | `joyero_recetas_completas.json` |
| 79 | Sastre | 1010 | `sastre_recetas_completas.json` |
| 80 | Marroquinero | 953 | `marroquinero_recetas_completas.json` |
| 81 | Ebanista | 640 | `ebanista_recetas_completas.json` |
| 83 | Maestro de Armas | 696 | `maestro_armas_recetas_completas.json` |

Confirmado cruzando 2 ítems conocidos por profesión contra
`recipes.json`+`recipeResults.json`+`jobsItems.json` reales v1.92.1.60.
Peletero es fabricación, no recolección (corrección respecto a una
suposición anterior).

Categorías utilitarias (materia intermedia compartida, no profesiones en
sí), agrupadas en `componentes_intermedios.json` (117 recetas,
imprescindible para que el Recetario expanda del todo):

| categoryId | Produce | Recetas |
|---|---|---|
| 64 | Harina tosca | 22 |
| 71 | Tabla tosca | 21 |
| 72 | Hilo tosco | 21 |
| 73 | Acero tosco | 33 |
| 75 | Encantártaro tosco | 20 |

### 6.5 `recetario_wakfu.html` — estado técnico real (auditado leyendo el código completo)

- **Qué hace hoy**: explorar/buscar recetas cargadas desde JSON (por
  profesión, rango de nivel, texto), seleccionar ítems objetivo, expandir
  recursivamente sub-recetas hasta materiales base, elegir entre variantes
  de una misma sub-receta (`variantChoice`, guardado por nombre de material
  normalizado — ya **no** se elige en silencio la más barata), y sacar una
  lista de la compra agregada con excedente vendible calculado en unidades.
  Guarda snapshot en `localStorage` (`recetario_wakfu:data:v1` y
  `:selection:v1`) — el Recetario sí persiste entre sesiones del navegador,
  al contrario que la app del Broker.
- **Importador JSON** (`loadFileList`/`ingestRecipes`/`ingestIcons`): solo
  reconoce dos formatos — array de recetas `{recipeId, nivel, xp, resultado,
  materiales, num_materiales_distintos}`, u objeto plano
  `{nombre_normalizado: codigo_grafico}` como mapa de iconos.
- **No existe ningún campo ni parser de precio todavía** — la propia app lo
  declara como trabajo futuro. El `broker_wakfu_street_ebanista.json`
  (sección 5) **no es importable tal cual**. Faltan dos piezas de código:
  1. Un tercer modo de `ingest*` que reconozca `broker_wakfu_street_precios_v1`
     y guarde un mapa `nombre_material_normalizado → precio_hdv`.
  2. Una columna de coste estimado en la lista de la compra ya calculada
     por `walk`/`addNeed` (multiplicando cantidad necesaria × precio si
     existe, marcando "sin precio" si no).
  **No se ha tocado el HTML todavía** para esto, solo se ha leído y
  entendido.
- **Iconos**: `iconos.json` mapea nombre → `gfxId` (de
  `jobsItems.json` → `definition.graphicParameters.gfxId`), pintados vía
  `https://raw.githubusercontent.com/Vertylo/wakassets/master/items/{gfxId}.png`
  (mirror comunitario, verificado en vivo con curl). Existe un patrón
  oficial equivalente de Ankama documentado en su foro pero no verificable
  por las restricciones de fetch de Claude. Si un icono no carga, el hueco
  queda vacío sin romper el layout.
- **Validación hecha**: extremo a extremo con navegador simulado (jsdom),
  reproduciendo un ejemplo real de Craftkfu ("Cartel de rebajas" + "Orbe
  imperfecto" → 35 recursos, 7 ítems distintos, mismas cantidades) y
  probando selector de variante + checkboxes con una segunda receta
  ("Archisfera imperfecta").
- **Pendiente sin confirmar por un humano**: nadie ha abierto el archivo en
  un navegador real con conexión para confirmar que los iconos cargan tal
  cual — Claude solo validó la lógica con jsdom.

### 6.6 Dónde vive esto de forma persistente

Además de este repo, el usuario también sube los archivos a Project
Knowledge. Lista completa de archivos que deben estar en el repo:

- Este `HANDOFF.md`
- `wakfu_recipe_extractor.py`
- `recetario_wakfu.html`
- Las 9 bases de recetas completas (una por profesión, nivel 0-200)
- `componentes_intermedios.json`
- `iconos.json` (opcional, solo iconos)
- `wakfu-economy-tracker.html` (sección 4)
- Los 5 archivos originales de la comunidad (sección 10)

Cuando Ankama saque un parche que cambie recetas: repetir la descarga de los
4 JSON crudos de la nueva versión y volver a correr el script para
regenerar todos los archivos de arriba.

---

## 7. Caso de trabajo: Ebanista 0→165

### 7.1 Patrón confirmado en los 16 tramos (0→150) — verificado contra las 640 recetas reales

Cada tramo de 10 niveles de oficio tiene exactamente 1 receta de Escuadrita
(100% madera, 2 materiales, 450 XP, sin riesgo) y entre 3 y 8 variantes de
receta de Orbe (1 drop raro + 1 drop común de un mob concreto, también 450
XP), cada una con un mob distinto — margen para elegir la variante más
barata o más fácil de farmear en cada tramo.

Detalle de los tramos ya verificados 0→30 (patrón se repite hasta 150 con
maderas/mobs distintos por tramo):

| Nivel | Componente | Materiales | Riesgo |
|---|---|---|---|
| 0 | Escuadrita tosca | Madera de fresno x5, Madera de avellano x5 | Ninguno |
| 5 | Orbe tosco | 1 drop raro + 7 comunes (3 variantes de mob: jalató/tofu/larva) | Depende de mob |
| 10 | Escuadrita rudimentaria | Madera de ñiamzamo x5, Madera de castaño x5 | Ninguno |
| 15 | Orbe rudimentario | 1 raro + 7 comunes (3 variantes de mob) | Depende de mob |
| 20 | Escuadrita imperfecta | Madera de boabob x5, Madera de abedul x5 | Ninguno |
| 25 | Orbe imperfecto | 1 raro + 7 comunes (5 variantes de mob — la más flexible) | Depende de mob |
| 30 | Escuadrita frágil | Madera de bananaranjo x5, Madera de sauce llorón x5 | Ninguno |

### 7.2 El patrón se rompe en el tramo final, 150→165

Ebanista tiene nivel máx. de oficio **165, no 170** como la mayoría. En
nivel 160 ya no hay ni Escuadrita ni Orbe. Aparecen en su lugar:

- `Encantamiento ancestral de Feca` — pide Polvo x350 + un componente raro
  (5 variantes de componente).
- `Llave del Corazón del Reloj de Nox` — 6 "fragmentos de llave" distintos,
  huele a drop de mazmorra/evento.

**No confirmado si requieren plano previo** (riesgo ya anotado: algunas
recetas relic/épicas requieren un plano dropeado antes de aparecer en la
interfaz de crafteo). **Pendiente de investigar** antes de prometer una
ruta barata para 150-165: revisar `componentes_intermedios.json` y/o
`methodwakfu.com/artisanat/plans-et-recettes/`.

### 7.3 Preferencias del usuario ya recogidas

- Compra materiales, no farmea activamente — aunque está abierto a ello si
  compensa levear Maestro de Armas en paralelo por la sinergia de madera
  (sección 8).
- Bonuses activos: gremio básico + booster pack.
- Falta para cerrar la ruta 0→150: precios de mercado de las maderas y de
  los drops de mob más accesibles para el usuario (sección 5, sección 6.2
  punto 3). Falta para 150→165: investigar si las recetas finales requieren
  plano previo (sección 7.2).

---

## 8. Matriz de sinergias entre profesiones

| Recolección | Alimenta a (fabricación) | Recurso compartido |
|---|---|---|
| Mineur (Minero) | Bijoutier (Joyero) + Armurier (Armero) | Minerales (Gemmes / Plaques) |
| Forestier (Leñador) | Maître d'Armes + Ébéniste | Madera (Manches / Équerres) — Ébéniste además necesita Orbes (drop de mobs) |
| Herboriste (Herbolario) | Boulanger (Panadero) | Plantas silvestres (Huiles) |
| Pêcheur (Pescador) | Cuisinier (Cocinero) | Peces (Épices) |
| Paysan (Campesino) | Tailleur (Sastre) | Cereales (Fibres) |
| — (drop de mobs) | Maroquinier (Marroquinero) | Cuirs — depende de combate/prospección |
| Trappeur (Trampero) | — | Sin pareja de fabricación directa confirmada |

**Peletero sin ubicar todavía** en esta matriz — se confirmó que es
fabricación (categoryId 74) pero no con qué profesión de recolección
empareja (probablemente Trampero, dado que "Esencia" suena a
curtido/peletería, pero sin confirmar).

Uso: al calcular una ruta de fabricación, mencionar de forma natural si
tiene pareja en esta tabla, sin convertirlo en pregunta obligatoria.

### 8.2 Excedente vendible / coste neto

`recipeResults.json` indica cuántas unidades produce cada crafteo. Cuando
sobran unidades del tramo, o craftear de más es la única forma de comprar
materiales en packs, el sobrante es vendible.

**Fórmula**: `Coste neto del tramo = Coste bruto de materiales − (unidades de excedente × precio de venta del ítem resultante)`.

El Recetario ya calcula automáticamente el excedente en *unidades* de cada
sub-receta expandida; falta multiplicarlo por precio de venta para llegar
al coste neto en kamas — pendiente de que se resuelva el tema de precios
(sección 5).

---

## 9. Catálogo de fuentes online

| Fuente | URL | Para qué sirve | Notas de uso |
|---|---|---|---|
| Feed JSON oficial de Ankama | `https://wakfu.cdn.ankama.com/gamedata/{version}/{tipo}.json`, versión en `.../gamedata/config.json` | Fuente oficial versionada: `recipes`, `recipeIngredients`, `recipeResults`, `jobsItems`, `harvestLoots`, `resources` | Descarga manual del usuario + extractor (sección 6.2), no fetch directo de Claude |
| Iconos — Vertylo/wakassets | `https://github.com/Vertylo/wakassets`, vía `raw.githubusercontent.com/Vertylo/wakassets/master/items/{gfxId}.png` | Iconos indexados por `gfxId` | Verificado en vivo con curl |
| Stratfu — Craft | https://stratfu.fr/outils/craft/ | El usuario la usa para trackear su Mercasaco | Fuente de inventario propio del usuario |
| wakfu-farm-tracker (GitHub) | https://github.com/olivo28/wakfu-farm-tracker-public | Tracking de farmeo, no consultable por HTTP | Que el usuario la use como tracker personal |
| Craftkfu (waklab) | https://craftkfu.waklab.fr/ | Buscador de recetas y costes | SPA no fetcheable; referencia visual que inspiró el Recetario |
| MethodWakfu — Métiers | https://methodwakfu.com/artisanat/les-metiers/ | Mecánicas: niveles máx., fórmula XP, Havre-Sac | Fetch funciona en este dominio |
| jobkfu (vertylo) | https://vertylo.github.io/jobkfu/ | Nivel + XP base + bonuses → nº de crafteos | Regla de delegación |
| wakfujobcalculator.com | https://wakfujobcalculator.com/ | Misma función que jobkfu | Regla de delegación |
| wakfujobcalculator.com — Items Craft Guide | https://wakfujobcalculator.com/items-craft-guide | Árbol de recetas con shopping list | Cubierto también por el Recetario propio |

---

## 10. Archivos de la comunidad subidos por el usuario

- `_Wakfu_Crafting_Professions_Leveling_Calculator (to lvl 160).xlsx`:
  receta↔recurso↔tramo para pares Joyero/Armero, M.Armas/Ebanista,
  Panadero/Cocinero.
- `Wakfu_Sheets.xlsx`: ubicaciones de recolección por nivel, mazmorras,
  Kama Minting. Posiblemente desactualizada en tramos 150+.
- `Copia_de_New_tabla_de_oficios_wakfu.xlsx`: recursos por profesión de
  recolección en español, inputs de bonuses.
- `Tabla_de_oficios_de_fabricación (ES).xlsx`: shopping list agregada por
  categoría, la más legible.
- `_Wakfu__Récolte_métiers.docx`: mecánicas de crecimiento/respawn en
  Havre Sac.

Complemento útil (sobre todo recolección/ubicaciones), pero para
BaseXP/materiales exactos de fabricación la fuente de verdad es la
arquitectura de la sección 6, no estas hojas.

---

## 11. Contradicciones y huecos — resueltos y pendientes

**Resueltos:**
- BaseXP real → feed oficial + script (sección 6.2-6.3).
- "Craftkfu local" / scraping de su motor → descartado con justificación
  (sección 6.1), no repetir esta investigación.
- No existe fuente de precios de mercado viva → confirmado
  (Wakfu-Elements, abandonado). Workaround: capturas del usuario.
- categoryId de las 9 profesiones de fabricación → 100% confirmado,
  incluida la corrección de Peletero.
- Servidor del usuario → decisión explícita: no se pregunta, fuera de
  alcance.
- Selección automática y silenciosa de variante de material → resuelta en
  el Recetario: selector manual visible.
- Interruptor único y opaco de "expandir sub-recetas" → sustituido por
  panel con checkbox por ítem.
- Sin herramienta propia de shopping-list → resuelto con el Recetario,
  validado contra un ejemplo real de Craftkfu.
- **Nombre y URL del repo fusionado** → confirmado (sección 0).
- **Token de GitHub expuesto** → gestionado por el usuario, política de
  "nunca usar tokens en texto plano" establecida y vigente (sección 0).
- **Rutas del repo tras la migración** → re-verificadas, nada se movió
  (sección 0).

**Pendientes:**
- **Precios de mercado**: siguen sin rellenarse (sección 5.3) — no
  insistir pidiendo capturas hasta que el usuario lo saque él mismo; era
  gestión pospuesta explícita en sesiones anteriores.
- **Arquitectura Broker app vs. schema `precios_v1`**: sin decidir cómo se
  conectan (sección 5.3) — no asumir ninguna opción sin confirmación del
  usuario.
- **Importador de precios en `recetario_wakfu.html`**: las dos piezas de
  código descritas en 6.5 no están implementadas todavía.
- **Tramo 150-165 de Ebanista**: ¿requieren plano dropeado las recetas
  finales? (sección 7.2) — sin investigar.
- **Trade-off "menos recetas vs. XP degresiva"**: sigue sin resolverse de
  forma automática — decisión caso por caso con el usuario.
- **Clasificación automática "farmeable vs. drop de mob"**: pendiente de
  probar `harvestLoots.json`/`monsterDrops.json`.
- **Iconos del Recetario sin confirmar en un navegador real** — solo
  validado con jsdom.
- **Peletero sin ubicar en la matriz de sinergias** (sección 8).
- **Recoger del usuario**: nivel actual de Ebanista, nivel objetivo
  concreto dentro de 0→165, restricciones de farmeo — sigue siendo el
  bloqueante para calcular una ruta real completa.

---

*Documento maestro generado el 2026-09-14, fusionando el handoff v6
(03-sep-2026), el handoff del repo fusionado (08/14-sep-2026) y el handoff
del Broker (14-sep-2026). Sustituye a los tres.*
