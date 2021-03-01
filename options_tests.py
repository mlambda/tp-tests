from options import Options
from ruleset import RuleSet


def test_exclusive_ab_bc_ca_de():
    rs = RuleSet()
    rs.add_dep("a", "b")
    rs.add_dep("b", "c")
    rs.add_dep("c", "a")
    rs.add_dep("d", "e")
    rs.add_conflict("c", "e")

    assert rs.is_coherent()

    opts = Options(rs)

    opts.toggle("a")
    assert opts.selection() == {"a", "c", "b"}

    rs.add_dep("f", "f")
    opts.toggle("f")
    assert opts.selection() == {"a", "c", "b", "f"}

    opts.toggle("e")
    assert opts.selection() == {"e", "f"}

    opts.toggle("b")
    assert opts.selection() == {"a", "c", "b", "f"}

    rs.add_dep("b", "g")
    opts.toggle("g")
    print(opts.selected)
    opts.toggle("b")
    print(opts.selected)
    assert opts.selection() == {"g", "f"}


def test_ab_bc_toggle():
    rs = RuleSet()

    rs.add_dep("a", "b")
    rs.add_dep("b", "c")
    opts = Options(rs)
    opts.toggle("c")

    assert opts.selection() == {"c"}


def test_ab_ac():
    rs = RuleSet()

    rs.add_dep("a", "b")
    rs.add_dep("a", "c")
    rs.add_conflict("b", "d")
    rs.add_conflict("b", "e")

    assert rs.is_coherent()

    opts = Options(rs)
    opts.toggle("d")
    opts.toggle("e")
    opts.toggle("a")
    assert opts.selection() == {"a", "c", "b"}


def test_abcd_e_f_g():
    rs = RuleSet()
    rs.add_dep("a", "b")
    rs.add_dep("a", "c")
    rs.add_dep("a", "c")
    rs.add_dep("a", "d")

    rs.add_conflict("b", "e")
    rs.add_conflict("c", "f")
    rs.add_conflict("d", "g")

    rs.add_conflict("e", "f")
    rs.add_conflict("f", "g")
    rs.add_conflict("g", "a")

    assert rs.is_coherent()

    opts = Options(rs)

    opts.toggle("a")
    assert opts.selection() == {"a", "b", "c", "d"}

    opts.toggle("e")
    assert opts.selection() == {"c", "d", "e"}

    opts.toggle("f")
    assert opts.selection() == {"d", "f"}

    opts.toggle("g")
    assert opts.selection() == {"g"}
