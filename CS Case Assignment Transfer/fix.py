with open("cases(copy).txt", "r") as f:
    splits = [line.split() for line in f]

    for i in splits:
        if i[0] == "0441":
            i[0] = "50"
        elif i[0] == "0475":
            i[0] = "51"
        elif i[0] == "0486":
            i[0] = "64"
        elif i[0] == "0322":
            i[0] = "42"
        elif i[0] == "0428":
            i[0] = "83"

with open("cases.txt", "w"):
    pass

with open("cases.txt", "a") as f:
    for i in splits:
        f.write(f"{i[0]}\t{i[1]}\n")