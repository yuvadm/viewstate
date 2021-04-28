def list_to_tuple(lst):
    if isinstance(lst, list) or isinstance(lst, tuple):
        return tuple([list_to_tuple(e) for e in lst])
    else:
        return lst
