#!/usr/bin/env python3
"""
Wakfu Recipe Extractor
=======================
Convierte los 4 archivos JSON crudos del feed oficial de Ankama en una
base de datos de recetas limpia, legible y filtrable por profesión y nivel.

POR QUÉ EXISTE ESTE SCRIPT
--------------------------
El feed de Ankama (wakfu.cdn.ankama.com/gamedata/<version>/...) es la fuente
más fiable de recetas del juego, pero viene repartido en varios archivos
enormes y sin nombres de profesión legibles (solo un "categoryId" numérico).
Este script hace UNA VEZ el trabajo de cruzar esos archivos, para no tener
que repetirlo a mano (ni pedirle a un asistente que lo recalcule) cada vez
que se necesite consultar una receta.

CÓMO OBTENER LOS ARCHIVOS DE ENTRADA (una vez por parche del juego)
---------------------------------------------------------------------
1. Abre en tu navegador: https://wakfu.cdn.ankama.com/gamedata/config.json
   Copia el número de "version" que aparece (ej: "1.92.1.60").
2. Sustituye {version} por ese número y abre estas 4 URLs una a una:
   - https://wakfu.cdn.ankama.com/gamedata/{version}/recipes.json
   - https://wakfu.cdn.ankama.com/gamedata/{version}/recipeIngredients.json
   - https://wakfu.cdn.ankama.com/gamedata/{version}/recipeResults.json
   - https://wakfu.cdn.ankama.com/gamedata/{version}/jobsItems.json
3. Guarda cada una con Ctrl+S (nombre libre, pero recuerda cuál es cuál).

USO
---
    python3 wakfu_recipe_extractor.py \
        --recipes recipes.json \
        --items jobsItems.json \
        --results recipeResults.json \
        --ingredients recipeIngredients.json \
        --category-id 81 \
        --min-level 0 --max-level 160 \
        --output ebanista_recetas.json

Si no conoces el categoryId de tu profesión, usa --find-category-id con el
nombre (en español) de un ítem que sepas que pertenece a esa profesión:

    python3 wakfu_recipe_extractor.py --items jobsItems.json \
        --results recipeResults.json --recipes recipes.json \
        --find-category-id "Orbe tosco"

MAPEO DE PROFESIONES DE FABRICACIÓN -> categoryId (confirmado sesión 5, 03-sep-2026)
--------------------------------------------------------------------------------------
Confirmado cruzando 2 ítems conocidos por profesión (tosco + rudimentario) contra
recipes.json + recipeResults.json + jobsItems.json reales (versión 1.92.1.60):

    40 -> Panadero          (Aceite tosco/rudimentario)      89 recetas
    74 -> Peletero          (Esencia tosca/rudimentaria)      49 recetas
    76 -> Cocinero          (Especia tosca/rudimentaria)     132 recetas
    77 -> Armero            (Placa tosca/rudimentaria)       966 recetas
    78 -> Joyero            (Gema tosca/rudimentaria)        964 recetas
    79 -> Sastre            (Fibra tosca/rudimentaria)      1010 recetas
    80 -> Marroquinero      (Cuero tosco/rudimentario)       953 recetas
    81 -> Ebanista          (Escuadrita tosca/rudimentaria)  640 recetas
    83 -> Maestro de Armas  (Mango tosco/rudimentario)       696 recetas

Las 9 profesiones de fabricación objetivo (sección 5 del handoff) quedan así
100% identificadas. NOTA: 74 (Peletero) NO era uno de los candidatos que se
sospechaba en la sesión anterior (se pensaba que 74 era recolección) -- dato
corregido.

Categorías restantes en el feed, SIN asignar a ninguna de las 9 profesiones
objetivo y con volumen mucho menor (probablemente recetas de refinado /
materia intermedia compartida entre profesiones, no profesiones en sí --
sin confirmar, no es necesario para el proyecto):
    64 -> produce "Harina tosca"       (22 recetas)
    71 -> produce "Tabla tosca"        (21 recetas)
    72 -> produce "Hilo tosco"         (21 recetas)
    73 -> produce "Acero tosco"        (33 recetas)
    75 -> produce "Encantártaro tosco" (20 recetas)
"""

import json
import argparse
import csv
from collections import defaultdict


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_item_name_map(items):
    """id de ítem -> nombre en español."""
    return {
        it["definition"]["id"]: it.get("title", {}).get("es", f"item_{it['definition']['id']}")
        for it in items
    }


def find_category_id(item_name, items, recipes, results):
    """Dado el nombre (ES) de un ítem craftable, encuentra el categoryId de su receta."""
    name_map = build_item_name_map(items)
    target_ids = {iid for iid, name in name_map.items() if name == item_name}
    if not target_ids:
        print(f"No se encontró ningún ítem llamado exactamente '{item_name}'.")
        return None

    recipes_by_id = {r["id"]: r for r in recipes}
    found = []
    for res in results:
        if res["productedItemId"] in target_ids:
            rec = recipes_by_id.get(res["recipeId"])
            if rec:
                found.append(rec)

    if not found:
        print(f"'{item_name}' no aparece como resultado de ninguna receta conocida.")
        return None

    for rec in found:
        print(f"recipeId {rec['id']} | categoryId {rec['categoryId']} | nivel {rec['level']} | XP {rec['xpRatio']}")
    return found[0]["categoryId"]


def _extract_category_name(entry):
    """Intenta sacar un nombre legible de una entrada de recipeCategories.json,
    probando varias formas típicas de estructurar estos JSON en el feed de Ankama."""
    # Forma tipo jobsItems.json: {"title": {"es": "...", "fr": "...", ...}, "definition": {"id": N}}
    if "title" in entry and isinstance(entry["title"], dict):
        name = entry["title"].get("es") or entry["title"].get("fr") or entry["title"].get("en")
        if name:
            return name
    # Forma alternativa: {"name": {"es": "...", ...}}
    if "name" in entry and isinstance(entry["name"], dict):
        name = entry["name"].get("es") or entry["name"].get("fr") or entry["name"].get("en")
        if name:
            return name
    # Forma plana: {"name": "..."} o {"nameId": "..."}
    for key in ("name", "nameId", "label", "code"):
        if key in entry and isinstance(entry[key], str):
            return entry[key]
    return None


def _extract_category_id(entry):
    if "definition" in entry and isinstance(entry["definition"], dict) and "id" in entry["definition"]:
        return entry["definition"]["id"]
    for key in ("id", "categoryId", "recipeCategoryId"):
        if key in entry:
            return entry[key]
    return None


def list_categories(categories, recipes=None):
    """Vuelca id -> nombre de profesión desde recipeCategories.json.
    Si se pasa recipes.json además, añade el nº de recetas de cada categoría
    (útil para contrastar con el volumen ya visto: 640 para Ebanista/81)."""
    counts = defaultdict(int)
    if recipes:
        for r in recipes:
            counts[r.get("categoryId")] += 1

    rows = []
    unparsed_sample = None
    for entry in categories:
        cid = _extract_category_id(entry)
        name = _extract_category_name(entry)
        if cid is None or name is None:
            if unparsed_sample is None:
                unparsed_sample = entry
            continue
        rows.append((cid, name, counts.get(cid, 0)))

    rows.sort(key=lambda x: x[0])
    if not rows:
        print("No se pudo interpretar la estructura de recipeCategories.json con los patrones conocidos.")
        print("Primer registro crudo, para ajustar el parseo a mano:")
        print(json.dumps(categories[0] if categories else {}, ensure_ascii=False, indent=2))
        return

    print(f"{'categoryId':>10}  {'nº recetas':>10}  nombre")
    for cid, name, count in rows:
        count_str = str(count) if recipes else "-"
        print(f"{cid:>10}  {count_str:>10}  {name}")

    if unparsed_sample is not None:
        print("\nAviso: algunos registros no se pudieron parsear con los patrones conocidos. Ejemplo crudo:")
        print(json.dumps(unparsed_sample, ensure_ascii=False, indent=2))


def extract_recipes(recipes, items, results, ingredients, category_id, min_level, max_level):
    name_map = build_item_name_map(items)

    ingredients_by_recipe = defaultdict(list)
    for ing in ingredients:
        ingredients_by_recipe[ing["recipeId"]].append(ing)

    results_by_recipe = defaultdict(list)
    for res in results:
        results_by_recipe[res["recipeId"]].append(res)

    filtered = [
        r for r in recipes
        if r["categoryId"] == category_id and min_level <= r["level"] <= max_level
    ]

    rows = []
    for r in sorted(filtered, key=lambda x: x["level"]):
        rid = r["id"]
        result_items = results_by_recipe.get(rid, [])
        ing_items = ingredients_by_recipe.get(rid, [])

        rows.append({
            "recipeId": rid,
            "nivel": r["level"],
            "xp": r["xpRatio"],
            "resultado": "; ".join(
                f"{name_map.get(res['productedItemId'], res['productedItemId'])} x{res['productedItemQuantity']}"
                for res in result_items
            ),
            "materiales": "; ".join(
                f"{name_map.get(ing['itemId'], ing['itemId'])} x{ing['quantity']}"
                for ing in ing_items
            ),
            "num_materiales_distintos": len(ing_items),
        })
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--recipes", help="Ruta a recipes.json")
    parser.add_argument("--items", help="Ruta a jobsItems.json (o items.json)")
    parser.add_argument("--results", help="Ruta a recipeResults.json")
    parser.add_argument("--ingredients", help="Ruta a recipeIngredients.json (no necesario si solo usas --find-category-id o --list-categories)")
    parser.add_argument("--categories", help="Ruta a recipeCategories.json (para --list-categories)")
    parser.add_argument("--category-id", type=int, help="ID numérico de la profesión (ver mapeo en la cabecera del script)")
    parser.add_argument("--min-level", type=int, default=0)
    parser.add_argument("--max-level", type=int, default=200)
    parser.add_argument("--output", help="Archivo de salida (.json o .csv según extensión)")
    parser.add_argument("--find-category-id", metavar="NOMBRE_ITEM",
                         help="En vez de extraer, busca el categoryId a partir del nombre en español de un ítem craftable")
    parser.add_argument("--list-categories", action="store_true",
                         help="Vuelca id->nombre de profesión desde --categories (recipeCategories.json). "
                              "Si además se pasa --recipes, añade el nº de recetas de cada categoría.")
    args = parser.parse_args()

    if args.list_categories:
        if not args.categories:
            parser.error("--list-categories requiere --categories recipeCategories.json")
        categories = load_json(args.categories)
        recipes = load_json(args.recipes) if args.recipes else None
        list_categories(categories, recipes)
        return

    if not args.recipes or not args.items or not args.results:
        parser.error("--recipes, --items y --results son obligatorios salvo que uses --find-category-id o --list-categories")

    recipes = load_json(args.recipes)
    items = load_json(args.items)
    results = load_json(args.results)

    if args.find_category_id:
        find_category_id(args.find_category_id, items, recipes, results)
        return

    if args.category_id is None or not args.ingredients:
        parser.error("--category-id y --ingredients son obligatorios salvo que uses --find-category-id")

    ingredients = load_json(args.ingredients)
    rows = extract_recipes(recipes, items, results, ingredients, args.category_id, args.min_level, args.max_level)

    print(f"{len(rows)} recetas encontradas para categoryId={args.category_id}, "
          f"nivel {args.min_level}-{args.max_level}")

    if args.output:
        if args.output.endswith(".csv"):
            with open(args.output, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
        else:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(rows, f, ensure_ascii=False, indent=2)
        print(f"Guardado en {args.output}")
    else:
        for row in rows:
            print(f"[Niv {row['nivel']:>3}] XP {row['xp']:>5} | {row['resultado']} <- {row['materiales']}")


if __name__ == "__main__":
    main()
