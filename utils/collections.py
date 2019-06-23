def find_first(collection, predicate):
    for item in collection:
        if predicate(item):
            return item
    return None
