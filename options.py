from ruleset import RuleSet


class Options:
    def __init__(self, rule_set: RuleSet) -> None:
        self.rule_set = rule_set
        self.selected = set()

    def selection(self):
        return self.selected

    def remove_dependents(self, options):
        to_remove = set(options)
        done = False
        while not done:
            done = True
            for other_option in self.selected:
                if to_remove & self.rule_set.compute_deps(other_option):
                    if other_option not in to_remove:
                        done = False
                    to_remove.add(other_option)
        self.selected -= to_remove

    def toggle(self, option):
        if option in self.selected:
            self.remove_dependents(option)
        else:
            deps = self.rule_set.compute_deps(option)
            self.remove_dependents(
                set().union(*[self.rule_set.conflicts[d] for d in deps])
            )
            self.selected |= deps
