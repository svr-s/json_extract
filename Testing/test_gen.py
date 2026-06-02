import itertools

def gen_a():
    print("Consuming A")
    yield {"A": 1}
    yield {"A": 2}

def gen_b():
    print("Consuming B")
    yield {"B": 1}
    yield {"B": 2}

def gen_dict():
    gens = [gen_a(), gen_b()]
    # itertools.product consumes both generators completely into memory (4 dicts)
    # then yields the 4 combinations.
    for combo in itertools.product(*gens):
        merged = {}
        for d in combo:
            merged.update(d)
        yield merged

for row in gen_dict():
    print("Got row:", row)
