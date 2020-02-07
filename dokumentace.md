## SBĚR GEODAT V ADRESÁŘOVÉ STRUKTUŘE

Program najde všechna geodata s příponou `.json` nebo `.geojson` v adresáři a jeho podadresářích a vytvoří 3 soubory - s body, s liniemi a s polygony. Ke každé feature v novém souboru program do properties přidá novou property `filepath` obsahující cestu k původnímu souboru, ve kterém se objekt nacházel. 

Program kontroluje validitu souborů a průběžně vypisuje, který soubor zpracovává. Pokud soubor nelze otevřít, nebo je nějak poškozený, program vypíše chybovou hlášku. 

##### VSTUP

Jako vstupní parametr uživatel zadává výchozí adresář do příkazového řádku.

##### VÝSTUP

Výstupem jsou 3 soubory - `points.geojson`, `lines.geojson` a `polygons.geojson` v aktuálním adresáři. Zároveň uživatel získá informaci o procházených souborech a případně problematických souborech.

##### FUNKCE

- *split_json(filepath, points_list, lines_list, polygons_list)*
  funkce projde všechny soubory v zadaném adresáři a jeho podadresářích, vybere všechny soubory s příponou `.json` nebo `.geojson` a podle typu geometrie rozdělí objekty do seznamů, zároveň ošetřuje výjimky, které mohou nastat

  parametry této funkce jsou cesta k vstupnímu adresáři a seznamy bodů, linií a polygonů, do kterých se ukládají jednotlivé features


