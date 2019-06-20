def find_first(collection, predicate):
    return next((x for x in collection if predicate(x)), None)
