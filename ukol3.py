import pathlib, json, sys

cesta = pathlib.Path('C:/Users/Marie Šašková/Desktop/marie_ukol')

# vypsat co je v adresáři

def iter_podadresar(filepath, points_list, lines_list, polygons_list):
    try:
        adir = filepath
        for files in adir.iterdir():
            try:
                if files.is_file():
                    if files.suffix in (".json", ".geojson"):
                        print(files)
                        with files.open(mode="r", encoding="utf-8") as f:
                            data = json.load(f)
                            features = data["features"]

                            if len(features) == 0:
                                print("Error: soubor:" , filepath," je prázdný!")
                                continue

                            for fts in features:
                                try:
                                    fts["properties"]["path"] = str(files)
                                    geom_type = (fts["geometry"]["type"])

                                    if geom_type in ("MultiPoint","Point"):
                                        points_list.append(fts)
                                    elif geom_type in ("MultiLineString", "LineString"):
                                        lines_list.append(fts)
                                    elif geom_type in ("MultiPolygon", "Polygon"):
                                        polygons_list.append(fts)
                                    else:
                                        print("Error: v souboru: ", files, " se objevuje jiný typ objektu!")
                                except KeyError:
                                    print("Error: v souboru:" ,files, " se objevuje chybná geometrie!")

                elif files.is_dir():
                    iter_podadresar(files, points_list, lines_list, polygons_list)

            except ValueError:
                print("Error: soubor geoJSON:", files, " je poškozený! ")

    except FileNotFoundError:
        print("Error: zadaná cesta k souboru: ", files, " je chybná!")

points = []
lines = []
polygons = []
iter_podadresar(cesta, points,lines, polygons)

# tvorba json - points
gj_structure_points = {"type": "FeatureCollection"}
gj_structure_points['features'] = points
# zapis souboru
with open("points.geojson", "w", encoding="utf-8") as f:
    json.dump(gj_structure_points, f, indent=2)


# tvorba json - lines
gj_structure_lines = {"type": "FeatureCollection"}
gj_structure_lines['features'] = lines
# zapis souboru
with open("lines.geojson", "w", encoding="utf-8") as f:
    json.dump(gj_structure_lines, f, indent=2)


# tvorba json - polygons
gj_structure_polygons = {"type": "FeatureCollection"}
gj_structure_polygons['features'] = polygons
# zapis souboru
with open("polygons.geojson", "w", encoding="utf-8") as f:
    json.dump(gj_structure_polygons, f, indent=2)