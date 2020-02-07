import pathlib, json, sys

def split_json(filepath, points_list, lines_list, polygons_list):
    """
    funkce projde všechny soubory v zadaném adresáři a jeho podadresářích, vybere všechny soubory geoJSON a podle typu geometrie
    rozdělí objekty do seznamů, zároveň ošetřuje výjimky, které mohou nastat
    :param filepath: cesta k vstupnímu adresáři
    :param points_list: seznam bodů
    :param lines_list: seznam linií
    :param polygons_list: seznam polygonů
    """
    try:
        for files in filepath.iterdir():
            try:
                if files.is_file():
                    if files.suffix in (".json", ".geojson"):
                        print(files)
                        with files.open(mode="r", encoding="utf-8") as f:   # otevření souboru
                            data = json.load(f)
                            features = data["features"]

                            if len(features) == 0:   # ošetření případu, kdy seznam 'features' je prázdný
                                print("Error: soubor:", files," neobsahuje objekty!")
                                continue

                            for fts in features:
                                try:
                                    fts["properties"]["path"] = str(files)   # zapsání cesty k původnímu souboru do properties
                                    geom_type = (fts["geometry"]["type"])

                                    if geom_type in ("MultiPoint","Point"):
                                        points_list.append(fts)
                                    elif geom_type in ("MultiLineString", "LineString"):
                                        lines_list.append(fts)
                                    elif geom_type in ("MultiPolygon", "Polygon"):
                                        polygons_list.append(fts)
                                    else:
                                        print("v souboru: ", files, " se objevuje jiný typ objektu!")
                                except KeyError:
                                    print("Error: v souboru:" ,files, " se objevuje chybná geometrie!")

                elif files.is_dir():
                    split_json(files, points_list, lines_list, polygons_list)   # rekurzivní volání funkce

            except ValueError:
                print("Error: soubor:", files, " je poškozený! ")

    except FileNotFoundError:
        print("Error: adresář ", filepath, " neexistuje!")



points = []
lines = []
polygons = []

cesta = pathlib.Path(sys.argv[1])

split_json(cesta, points,lines, polygons)
try:
    # tvorba json - points
    gj_structure_points = {"type": "FeatureCollection"}
    gj_structure_points['features'] = points
    # zapis souboru
    with open("points.geojson", "w", encoding="utf-8") as f:
        json.dump(gj_structure_points, f, indent=2,  ensure_ascii=False)

    # tvorba json - lines
    gj_structure_lines = {"type": "FeatureCollection"}
    gj_structure_lines['features'] = lines
    # zapis souboru
    with open("lines.geojson", "w", encoding="utf-8") as f:
        json.dump(gj_structure_lines, f, indent=2, ensure_ascii=False)

    # tvorba json - polygons
    gj_structure_polygons = {"type": "FeatureCollection"}
    gj_structure_polygons['features'] = polygons
    # zapis souboru
    with open("polygons.geojson", "w", encoding="utf-8") as f:
        json.dump(gj_structure_polygons, f, indent=2, ensure_ascii=False)

except PermissionError:
    print("Error: v daném adresáři nemáte oprávnění vytvořit nový soubor")