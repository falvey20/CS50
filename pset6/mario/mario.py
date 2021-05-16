import cs50

while True:
    towerHeight = cs50.get_int("Pyramid Height?")
    if towerHeight < 1 or towerHeight > 8:
        towerHeight = cs50.get_int("Pyramid Height?")
    if towerHeight >= 1 or towerHeight <= 8:
        break

for i in range(towerHeight):
    print((towerHeight - i - 1) * " ", end = "")
    print((i + 1) * "#")
    