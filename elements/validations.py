import random


def get_de_ordem():
    lst = list()

    for i in range(6):
        ter = random.sample(range(0, 3), 3)
        for t in ter:
            lst.append(t)
    print(lst, len(lst))
    return lst

