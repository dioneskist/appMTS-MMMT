import hashlib
import logging
import random


def get_de_ordem():
    lst = list()
    for i in range(6):
        ter = random.sample(range(1, 4), 3)
        for t in ter:
            lst.append(t)
    logging.debug('ordem gerada: {} ({})'.format(lst, len(lst)))
    return lst


def gerar_lista_usando_ordem_de(list_elementos, ordem):
    list_final = list()
    for o in ordem:
        logging.debug('validando {} {}'.format(o, len(list_elementos)))
        for item in list_elementos:
            if int(item[0][2]) == o:
                list_final.append(item)
                list_elementos.remove(item)
                break

    logging.debug('gerada lista final com ordem DE')
    for l in list_final:
        md5 = hashlib.md5(str(l).encode())
        logging.debug('{} {}'.format(l, md5.hexdigest()))
    return list_final


def gerar_todas_combinacoes(list1, list2, combinacoes_teste_DE=False):
    l1 = list(list1)
    l2 = list(list2)
    all_combinations = []
    counter = 0
    for x in l1:
        for y in l2:
            all_combinations.append(x + y)
            counter += 1
    logging.debug(
        'gerar_todas_combinacoes: gerada todas as combinacoes ({}) {}'.format(len(all_combinations), all_combinations))
    all_combinations_random = list()
    choices = random.sample(range(len(all_combinations)), len(all_combinations))
    for choice in choices:
        all_combinations_random.append(all_combinations[choice])
    logging.debug(
        'gerar_todas_combinacoes: gerada todas as combinacoes ({}) {}'.format(len(all_combinations_random),
                                                                              all_combinations_random))
    logging.debug('       combinacoes            ->      combinacoes aleatorias    ')
    index = 0
    for m in all_combinations:
        md5 = hashlib.md5(str(all_combinations_random[index]).encode())
        logging.debug('{} -> {}, {}'.format(all_combinations[index], all_combinations_random[index], md5.hexdigest()))
        index += 1

    if combinacoes_teste_DE:
        # ordena elementos de
        ordem_de = get_de_ordem()
        return gerar_lista_usando_ordem_de(all_combinations_random, ordem_de)
    else:
        return all_combinations_random
