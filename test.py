
outliersBoosted = ["('2019 1 7', '2019 1 13')", "('2019 6 20', '2019 6 26')", "('2019 7 10', '2019 7 16')", "('2019 7 17', '2019 7 23')", "('2019 7 24', '2019 7 30')", "('2019 8 21', '2019 8 27')", "('2019 11 12', '2019 11 18')", "('2020 7 30', '2020 8 5')", "('2020 12 15', '2020 12 21')", "('2021 1 19', '2021 1 25')", "('2021 4 10', '2021 4 16')", "('2021 5 7', '2021 5 13')", "('2021 6 11', '2021 6 17')", "('2021 7 8', '2021 7 14')", "('2021 8 12', '2021 8 18')", "('2021 10 6', '2021 10 12')", "('2021 12 14', '2021 12 20')"]

for i in outliersBoosted:
    print(type(i))

# A partir de aquí, leer Conductividad_nor.csv -> eliminar las semanas que son outliers accediendo a los índices de sus fechas de comienzo y final contenidos
# en outliersBoosted y guardar la nueva base de datos sin outliers/limpia.
# Luego meter los outliers artificiales y dejarlos marcados en la base de datos en una nueva columan. Efectuar la detacción de nuevo y ver si detecta los outliers marcados.