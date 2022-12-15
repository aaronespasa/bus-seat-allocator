#!/bin/bash
echo "--------Random case---------"
python CSPCargaBus.py ./CSP-tests/alumnos.csv ./CSP-tests/bus.json
echo "--------T-Main case---------"
python CSPCargaBus.py ./CSP-tests/alumnos_T_main.csv ./CSP-tests/bus.json
echo "--------F-movred---------"
python CSPCargaBus.py ./CSP-tests/alumnos_F_movred.csv ./CSP-tests/bus.json
echo "--------T-all_seats---------"
python CSPCargaBus.py ./CSP-tests/alumnos_T_all_seats.csv ./CSP-tests/bus.json
#echo "--------F-too_much_seats---------"
# python CSPCargaBus.py ./CSP-tests/F_too_much_students.csv ./CSP-tests/bus.csv
echo "--------T-movred_siblings---------"
python CSPCargaBus.py ./CSP-tests/alumnos_T_movred_siblings.csv ./CSP-tests/bus.json
echo "--------T-Different-bus---------"
python CSPCargaBus.py ./CSP-tests/alumnos_T_all_seats.csv ./CSP-tests/bus_more_seats.json
echo "--------T-Differentbus_change_mov---------"
python CSPCargaBus.py ./CSP-tests/alumnos_T_main.csv ./CSP-tests/bus_change_mov.json

