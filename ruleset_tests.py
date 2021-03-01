from ruleset import RuleSet


def test_depends_aa():
    rs = RuleSet()

    rs.add_dep("a", "a")

    assert rs.is_coherent()


def test_depends_ab_ba():
    rs = RuleSet()

    rs.add_dep("a", "b")
    rs.add_dep("b", "a")

    assert rs.is_coherent()


def test_exclusive_ab():
    rs = RuleSet()

    rs.add_dep("a", "b")
    rs.add_conflict("a", "b")

    assert not rs.is_coherent()


def test_exclusive_ab_bc():
    rs = RuleSet()

    rs.add_dep("a", "b")
    rs.add_dep("b", "c")
    rs.add_conflict("a", "c")

    assert not rs.is_coherent()


def test_deep_deps():
    rs = RuleSet()

    rs.add_dep("a", "b")
    rs.add_dep("b", "c")
    rs.add_dep("c", "d")
    rs.add_dep("d", "e")
    rs.add_dep("a", "f")
    rs.add_conflict("e", "f")

    assert not rs.is_coherent()
