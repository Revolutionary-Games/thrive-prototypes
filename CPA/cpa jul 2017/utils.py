def addDict(dict1, dict2):
    res = dict1.copy()
    for key, value in dict2.items():
        if key in res:
            res[key] += value
        else:
            res[key] = value
    return res
