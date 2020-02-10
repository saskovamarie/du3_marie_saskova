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
    for file in filepath.iterdir():
        try:
            if file.is_file():
                if file.suffix in (".json", ".geojson"):
                    print(file)
                    with file.open(mode="r", encoding="utf-8") as f:   # otevření souboru
                        data = json.load(f)
                        features = data["features"]

                        if len(features) == 0:   # ošetření případu, kdy seznam 'features' je prázdný
                            print("Error: soubor:", file," neobsahuje objekty!")
                            continue

                        for ft in features:
                            try:
                                ft["properties"]["filepath"] = str(file)   # zapsání cesty k původnímu souboru do properties
                                geom_type = (ft["geometry"]["type"])

                                if geom_type in ("MultiPoint","Point"):
                                    points_list.append(ft)
                                elif geom_type in ("MultiLineString", "LineString"):
                                    lines_list.append(ft)
                                elif geom_type in ("MultiPolygon", "Polygon"):
                                    polygons_list.append(ft)
                                else:
                                    print("v souboru: ", file, " se objevuje jiný typ objektu:", geom_type)
                            except KeyError:
                                print("Error: v souboru:" ,file, " se objevuje chybná geometrie!")

            elif file.is_dir():
                split_json(file, points_list, lines_list, polygons_list)   # rekurzivní volání funkce

        except ValueError:
            print("Error: soubor:", file, " je poškozený! ")




points = []
lines = []
polygons = []

try:
    cesta = pathlib.Path(sys.argv[1])
    split_json(cesta, points, lines, polygons)
except FileNotFoundError:
    print("Error: adresář ", cesta, " neexistuje!")


try:
    # tvorba json - points
    gj_structure_points = {"type": "FeatureCollection"}
    gj_structure_points['features'] = points
    # zapis souboru
    with open("points.geojson", "w", encoding="utf-8") as f:
        json.dump(gj_structure_points, f, indent=2,  ensure_ascii=False)
except PermissionError:
    print("Error: v daném adresáři nemáte oprávnění vytvořit nový soubor")

try:
    # tvorba json - lines
    gj_structure_lines = {"type": "FeatureCollection"}
    gj_structure_lines['features'] = lines
    # zapis souboru
    with open("lines.geojson", "w", encoding="utf-8") as f:
        json.dump(gj_structure_lines, f, indent=2, ensure_ascii=False)
except PermissionError:
    print("Error: v daném adresáři nemáte oprávnění vytvořit nový soubor")

try:
    # tvorba json - polygons
    gj_structure_polygons = {"type": "FeatureCollection"}
    gj_structure_polygons['features'] = polygons
    # zapis souboru
    with open("polygons.geojson", "w", encoding="utf-8") as f:
        json.dump(gj_structure_polygons, f, indent=2, ensure_ascii=False)
except PermissionError:
    print("Error: v daném adresáři nemáte oprávnění vytvořit nový soubor")
