from itertools import product


def gen_comb_list(list_set):
    '''
    Parameters:
        list_set: a list of lists where each contains at least one element

    Returns:
        a list of lists, each of which is made from a combination of elements in each list in list_set
    '''
    all_combinations = list(product(*list_set))

    result = [list(combination) for combination in all_combinations]

    return result


print(gen_comb_list([[1, 2, 3]]))
print(gen_comb_list([[1, 2, 3], [4, 5]]))
print(gen_comb_list([[1, 2, 3], [4, 5], [6, 7, 8]]))