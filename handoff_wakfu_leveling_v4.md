# Handoff — Proyecto rutas de leveo Wakfu (v4, sesión 4, 03-sep-2026)

Contexto completo para que otra instancia de Claude (u otra cuenta) retome
este proyecto desde cero. Sustituye al handoff de sesión 2 en todo lo
referente a fuentes de datos (sección 3 y 5 de aquella versión quedan
obsoletas y se reemplazan por la sección "Arquitectura de datos" de este
documento). El resto (objetivo, principio de no-solapamiento, matriz de
sinergias) sigue vigente sin cambios.

## Qué es esto / qué NO es esto

**Es:** la base de conocimiento + el cambio de arquitectura decidido en la
sesión 4 para dejar de depender de capturas de pantalla receta a receta.

**No es:** una ruta de leveo ya calculada. Ebanista 0→30 está a medio
resolver (faltan precios de mercado, ver "Estado del caso de prueba" abajo).

## 0. Cambio de paradigma (sesión 4) — LEER PRIMERO

Hasta la sesión 3 el flujo era: usuario abre Craftkfu → hace clic en una
receta → pasa captura a Claude → Claude la transcribe a mano. Esto es lento,
incompleto (solo vemos lo que se nos ocurre pedir) y propenso a errores
(materiales de varias recetas mezclados en una sola captura, sesión 3).

**Se descubrió y confirmó en sesión 4** que el feed oficial de Ankama SÍ es
accesible — no por Claude directamente (bloqueo de indexación, ver handoff
v2), sino porque **el usuario puede abrir esas URLs en su propio navegador
sin ningún problema** y descargar los JSON. Una vez descargados y subidos a
Claude, este puede procesarlos con código (no a mano, no con capturas) y
extraer TODAS las recetas de una profesión de una sola vez, con datos
exactos (no inferidos, no ambiguos).

Esto convierte el "vamos a hacer un Craftkfu local" (idea que se intentó y
se abandonó, ver sección 1 más abajo) en algo mucho más simple: no hace
falta reconstruir la app, solo necesitamos sus mismos datos de origen.

## 1. Camino explorado y descartado: "Craftkfu local" / scraping

Se investigó si se podía clonar o inspeccionar el código de Craftkfu para
extraer su fuente de datos. Hallazgos (útiles como descarte documentado,
para no repetir la búsqueda):

- Craftkfu (`craftkfu.waklab.fr`) es una SPA — Claude no puede leer su HTML
  renderizado ni sus llamadas internas de red.
- Se localizó al mantenedor (Mathieu Féry / MathiusD) y sus repos en
  GitLab: `wakdata-rest-api-crystal`, `wakdata` (cliente Python/Crystal que
  descarga los JSON de Ankama) y `WakTisanat` (473 commits desde 2020, con
  un commit "Update building for 1.83.1.23 (Craftkfu)" — casi seguro es el
  motor real de Craftkfu).
- **Conclusión: no aporta nada nuevo.** El propio `wakdata` confirma en su
  descripción que sus datos vienen "from JSON files distributed in Wakfu
  CDN" — exactamente la misma fuente que ya conocíamos. Y GitLab renderiza
  sus archivos con JavaScript igual que Craftkfu, así que Claude tampoco
  puede leerlos ahí.
- **No merece la pena volver a intentar esto.** El cuello de botella nunca
  fue "no sabemos dónde están los datos", sino "Claude no puede abrir URLs
  no indexadas". La solución no es reconstruir Craftkfu, es que el usuario
  descargue el JSON una vez (sección 2).

## 2. Arquitectura de datos nueva (reemplaza la cascada de fuentes v2)

### 2.1 Los 4 archivos fuente (se piden al usuario, una vez por parche del juego)

El usuario abre en su navegador (JSON plano, sin JavaScript, no hay
bloqueo — el bloqueo de Claude no aplica a un humano navegando):

1. `https://wakfu.cdn.ankama.com/gamedata/config.json` → da el nº de
   versión actual (confirmado en vivo, sesión 4: **1.92.1.60**).
2. `https://wakfu.cdn.ankama.com/gamedata/{version}/recipes.json`
3. `https://wakfu.cdn.ankama.com/gamedata/{version}/recipeIngredients.json`
4. `https://wakfu.cdn.ankama.com/gamedata/{version}/recipeResults.json`
5. `https://wakfu.cdn.ankama.com/gamedata/{version}/jobsItems.json`

Guarda cada uno con Ctrl+S y los sube al chat. Tamaños reales confirmados
en sesión 4: recipes.json ~900 KB, recipeIngredients.json ~4 MB,
recipeResults.json ~750 KB, jobsItems.json ~8.7 MB (este último incluye
descripciones largas en 4 idiomas — es el más pesado pero sigue siendo
manejable).

**Nota:** el archivo llamado `jobsItems.json` en la documentación del feed
resultó tener más contenido del esperado (título + descripción en 4
idiomas, no solo id/nivel/imagen como decía el handoff v2). Esto no es un
problema — simplemente úsalo igual, es la fuente de nombres en español.

### 2.2 El script: `wakfu_recipe_extractor.py`

Entregado en esta sesión (ver archivos adjuntos). Cruza los 4 JSON y
produce una tabla limpia: nivel de receta, XP, resultado (ítem + cantidad),
materiales (ítem + cantidad), todo con nombres en español, para una
profesión y rango de nivel concretos.

**Uso normal:**
```
python3 wakfu_recipe_extractor.py \
  --recipes recipes.json --items jobsItems.json \
  --results recipeResults.json --ingredients recipeIngredients.json \
  --category-id 81 --min-level 0 --max-level 160 \
  --output ebanista_recetas.json
```

**Para identificar el categoryId de una profesión que aún no conocemos:**
```
python3 wakfu_recipe_extractor.py --items jobsItems.json \
  --results recipeResults.json --recipes recipes.json \
  --find-category-id "Nombre exacto de un ítem craftable en español"
```
(busca un ítem que sepas con certeza que pertenece a esa profesión, p.ej.
un componente básico como hicimos con "Orbe tosco" para Ebanista).

### 2.3 Mapeo de profesiones → categoryId (ir completando)

| categoryId | Profesión | Estado |
|---|---|---|
| 81 | **Ebanista** | ✅ Confirmado (sesión 4, cruzado con 4 ítems conocidos) |
| 76, 77, 78, 79, 80, 83 | Candidatos sin confirmar | Por volumen de recetas (132 a 1010) coinciden con perfil de profesión de fabricación, pero no se ha confirmado cuál es cuál |
| 40, 64, 71-75 | Sin explorar | Probablemente profesiones de recolección u otras categorías (herramientas, decoración general, etc.) |

**Para confirmar las que faltan:** usar `--find-category-id` con un ítem
conocido de cada profesión (Armero, Joyero, Sastre, Panadero, Cocinero,
Maestro de Armas, Marroquinero, Peletero). 5 minutos por profesión.

### 2.4 Dónde vive esto de forma persistente (para no repetir el proceso)

**Recomendación para el usuario:** subir estos 2 archivos a la sección de
**Project Knowledge / archivos del Proyecto** de Claude (no al chat) —así
está disponible en cualquier conversación nueva dentro del proyecto sin
tener que volver a pasarlos:

- `wakfu_recipe_extractor.py` (el script, para cuando haya un parche nuevo)
- `ebanista_recetas_completas.json` (la base ya procesada, 640 recetas,
  niveles 0-160, 148 KB — cabe sin problema)

Cuando Ankama saque un parche que cambie recetas, basta con repetir el
paso 2.1 (descargar los 4 JSON de la nueva versión) y volver a correr el
script — no hace falta rehacer nada de este análisis.

### 2.5 Qué sigue sin tener solución automática

- **Precios de mercado (HdV):** confirmado en sesiones anteriores que no
  existe ninguna fuente viva. Sigue siendo captura del usuario, con fecha,
  no reutilizable entre sesiones. Esto no cambia con la nueva arquitectura.
- **Clasificación "farmeable vs. drop de mob":** el feed de Ankama no
  distingue esto directamente en los 4 archivos que tenemos. Se infiere
  por patrón (1 material x1 + otro x7 = probable drop de mob, visto en las
  Orbes de Ebanista) pero no está confirmado con datos duros. Los archivos
  `harvestLoots.json` y `monsterDrops.json` (de Vertylo/wakassets, ver
  handoff v2 sección 5.1) probablemente resuelvan esto si se descargan
  igual que los 4 anteriores — pendiente de probar.

## 3. Estado del caso de prueba: Ebanista 0→30

Datos ya extraídos y confirmados (ver `ebanista_recetas_completas.json`
filtrado a nivel ≤30, o repetir con `--max-level 30`):

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
Armas en paralelo por la sinergia de madera). Bonuses activos: gremio
básico + booster pack.

**Falta para cerrar la ruta:** precios de mercado de las 8 maderas
distintas y de los drops de mob más accesibles para el usuario en su
servidor (pendiente: preguntar servidor, no se ha hecho aún).

## 4. Checklist de próximos pasos

Ya hechos (no repetir):
- [x] Confirmado que "Craftkfu local" no aporta nada — descartado con
      justificación documentada (sección 1).
- [x] Descubierta y probada la vía de descarga directa del feed de Ankama
      por parte del usuario (sección 2.1).
- [x] Creado `wakfu_recipe_extractor.py`, script reutilizable.
- [x] Generada base de datos completa de Ebanista (640 recetas, niveles
      0-160) en JSON y CSV.
- [x] Identificado categoryId 81 = Ebanista.
- [x] Extraídas y confirmadas las 7 recetas clave del tramo 0-30 de
      Ebanista con materiales exactos.

Pendientes reales:
- [ ] Subir `wakfu_recipe_extractor.py` y `ebanista_recetas_completas.json`
      a Project Knowledge (acción del usuario, fuera del alcance de Claude).
- [ ] Preguntar servidor del usuario (sigue pendiente desde sesión 2).
- [ ] Pedir precios de mercado de las 8 maderas + drops de mob del tramo
      0-30 (única pieza que falta para cerrar la ruta de Ebanista).
- [ ] Calcular en Jobkfu (regla de delegación) el nº de crafteos necesarios
      con el booster pack + bonus de gremio ya confirmados.
- [ ] Entregar tabla final de la ruta Ebanista 0-30 con coste neto.
- [ ] Confirmar los categoryId de las 8 profesiones de fabricación
      restantes usando `--find-category-id` (5 min cada una), para dejar
      el sistema listo para cualquier profesión futura, no solo Ebanista.
- [ ] (Opcional, baja prioridad) Descargar `harvestLoots.json` y explorar
      si permite clasificar automáticamente "farmeable vs. drop de mob" en
      vez de inferirlo por patrón.

## 5. Nota de seguridad (heredada de sesión 2, sigue vigente)

Un token de GitHub compartido por error en sesiones anteriores fue
retirado de la documentación. Si sigue activo, revocarlo en GitHub →
Settings → Developer settings → Personal access tokens. Claude no hace
`git push`; el flujo sigue siendo: Claude entrega archivos, el usuario los
sube manualmente donde corresponda.

## 6. Referencia: todo lo demás sin cambios

Objetivo del proyecto, instrucciones de comportamiento (system prompt),
principio de no-solapamiento, regla de delegación a Jobkfu/wakfujobcalculator,
matriz de sinergias entre profesiones (8.8 del handoff v2), y los 5
archivos de hojas de cálculo originales (6.1-6.5) siguen vigentes tal cual
se documentaron en el handoff de sesión 2. Consultar ese documento para el
detalle completo de esas secciones.
