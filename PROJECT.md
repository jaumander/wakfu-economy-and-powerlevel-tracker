# PROJECT.md — The Broker of Wakfu Street

## Propósito
Herramienta de rastreo de economía para Wakfu: identificar nichos de mercado poco explotados, rastrear tendencias de oferta/demanda, y llevar un registro de ventas propias — sin automatizar nada que interactúe con el juego en ejecución (riesgo de baneo).

## Estado actual
Single-file HTML/JS (`wakfu-economy-tracker.html`) con 4 pestañas:
1. Vigía & Snapshots — watchlist + entrada manual por lotes
2. Tendencias & Alertas — señales automáticas + sparklines
3. Mis Ventas — historial propio con estadísticas
4. Cuaderno de Nichos — notas de hipótesis

Catálogo oficial de Ankama incrustado (6.734 objetos: equipamiento + recursos/oficio) para autocompletar nombre y categoría del Mercadillo al añadir a la watchlist. Ver `PROJECT_INSTRUCTIONS.md` para el changelog completo y decisiones de diseño.

## Arquitectura
- Cero backend, cero build step. Todo vive en un archivo `.html`.
- Persistencia vía `window.storage` (API de Claude Artifacts), 4 claves: `watchlist`, `snapshots`, `sales`, `journal`.
- Export/Import JSON como backup portátil entre cuentas/navegadores.

## Aprendizajes clave
- `items.json` de Ankama solo cubre equipamiento; `jobsItems.json` es la fuente correcta para recursos/materias primas.
- `resources.json` son los nodos de recolección (árboles), no los objetos comerciables.
- Cosméticos/monturas/familiares no están expuestos públicamente por Ankama en ningún JSON conocido.
- La jerarquía de categorías del filtro "Tipos" del Mercadillo se replicó a mano a partir de capturas del juego (no viene de ningún JSON de Ankama).

## Cómo continuar
Clona el repo, lee `HANDOFF.md` primero. Si dice "Nada en curso", trabaja normal desde este archivo. Si no, hay trabajo a medias — continúa desde ahí.
