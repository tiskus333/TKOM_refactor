# TKOM_2021
Projekt na przedmiot TKOM 21L. Refaktoryzacja kodu.

# Pobranie wymaganych pakietow
pip3 install coverage
# Uruchomienie programu
python main.py
# Uruchomienie testow
coverage run -m  unittest Tests.lexerTest.test_lexer -v; coverage xml; coverage report -m