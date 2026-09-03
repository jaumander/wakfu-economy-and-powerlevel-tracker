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

MAPEO DE PROFESIONES YA CONOCIDO (ir completando con --find-category-id)
--------------------------------------------------------------------------
    81 -> Ebanista   (confirmado en sesión 3, 03-sep-2026)
    (pendiente: Armero, Joyero, Sastre, Panadero, Cocinero, Maestro de Armas,
     Marroquinero, Peletero -- candidatos probables por volumen de recetas:
     76, 77, 78, 79, 80, 83 -- sin confirmar todavía)
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
    parser.add_argument("--recipes", required=True, help="Ruta a recipes.json")
    parser.add_argument("--items", required=True, help="Ruta a jobsItems.json (o items.json)")
    parser.add_argument("--results", required=True, help="Ruta a recipeResults.json")
    parser.add_argument("--ingredients", help="Ruta a recipeIngredients.json (no necesario si solo usas --find-category-id)")
    parser.add_argument("--category-id", type=int, help="ID numérico de la profesión (ver mapeo en la cabecera del script)")
    parser.add_argument("--min-level", type=int, default=0)
    parser.add_argument("--max-level", type=int, default=200)
    parser.add_argument("--output", help="Archivo de salida (.json o .csv según extensión)")
    parser.add_argument("--find-category-id", metavar="NOMBRE_ITEM",
                         help="En vez de extraer, busca el categoryId a partir del nombre en español de un ítem craftable")
    args = parser.parse_args()

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
