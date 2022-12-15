#!/bin/bash

echo "\nEjemplo simplificado sin personas de movilidad reducida:"
echo "\nalumnos3.prob usando la heurística 1"
python ASTARColaBus.py ./ASTAR-tests/alumnos3.prob 1
echo "\nalumnos3.prob usando la heurística 2"
python ASTARColaBus.py ./ASTAR-tests/alumnos3.prob 2

echo "\nEjemplo con personas de movilidad reducida:"
echo "\nalumnos.prob usando la heurística 1"
python ASTARColaBus.py ./ASTAR-tests/alumnos.prob 1
echo "\nalumnos.prob usando la heurística 2 (como vemos, no da solución con personas de movilidad reducida)"
python ASTARColaBus.py ./ASTAR-tests/alumnos.prob 2
echo "\nalumnos2.prob usando la heurística 1"

echo "\nEjemplo complejo con 21 nodos:"
echo "\nalumnos2.prob usando la heurística 1"
python ASTARColaBus.py ./ASTAR-tests/alumnos2.prob 1
