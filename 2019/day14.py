import collections
import math
import re


def main():
    with open("day14.txt", "rt") as input_file:
        lines = [line.rstrip() for line in input_file.readlines()]
    line_re = re.compile(r"(.+) => (.+)")
    raw_reactions = [line_re.match(line).groups() for line in lines]
    reactions = {}
    for inputs, outputs in raw_reactions:
        mult, result = outputs.split(" ")
        input_comps = [i.split(" ") for i in inputs.split(", ")]
        input_tuples = [(int(q), n) for q, n in input_comps]
        reactions[result] = int(mult), input_tuples

    # Part 1
    ore_per_full = get_required_ore(reactions, 1)
    print("Required ore for 1 FUEL:", ore_per_full)

    # Part 2
    # Input gives 397771 OPF.
    # 10^12 ores with 13312 OPF example gives 82892753 FUEL.
    # 10^12 ores with 180697 OPF example gives 5586022 FUEL.
    # 10^12 ores with 2210736 OPF example gives 460664 FUEL.
    # 10^12 / 82892753 / 13312 ~= 0.91
    # 10^12 / 5586022 / 180697 ~= 0.99
    # 10^12 / 460664 / 2210736 ~= 0.98
    # Let's say our reaction will have an efficiency of ~ 0.985.
    # 10^12 / x / 397771 = 0.985  ->  x = 2552294
    # Now on to our search.

    fuel_q = 2552294
    cursor = 2**16
    last_result = 0
    min_target = 10**12 - ore_per_full
    max_target = 10**12
    was_below = False
    while True:
        last_result = get_required_ore(reactions, fuel_q)
        print(f"{fuel_q} FUEL requires {last_result} ORE.")
        if cursor == 1:
            break
        if last_result < min_target:
            if not was_below:
                cursor //= 2
            fuel_q += cursor
            was_below = True
        elif last_result > max_target:
            if was_below:
                cursor //= 2
            fuel_q -= cursor
            was_below = False
        else:
            break
    
def get_required_ore(reactions, quantity):
    stored_map = collections.defaultdict(int)
    needs = [("FUEL", quantity)]
    ore_per_full = 0
    while needs:
        needed, needed_q = needs.pop(0)
        if needed == "ORE":
            ore_per_full += needed_q
            continue
        react_mult, subcomps = reactions[needed]
        if stored_map[needed]:
            needed_q -= stored_map[needed]
            stored_map[needed] = 0
        num_reacts = math.ceil(needed_q / react_mult)
        if num_reacts:
            new_needs = [(name_sc, num_sc * num_reacts) for num_sc, name_sc in subcomps]
            needs += new_needs
        produced = react_mult * num_reacts
        if produced - needed_q > 0:
            stored_map[needed] += produced - needed_q
    return ore_per_full


if __name__ == "__main__":
    main()
