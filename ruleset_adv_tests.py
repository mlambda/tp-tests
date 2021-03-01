import pytest

from ruleset import RuleSet


@pytest.fixture
def rs():
    rs = RuleSet()
    rs.add_dep("a", "b")
    rs.add_dep("b", "c")
    rs.add_dep("c", "d")
    return rs


@pytest.mark.parametrize(
    "deps,conflicts,expected",
    [([], [("a", "b")], False), ([("d", "a")], [("a", "e")], True)],
)
def test_depends_aa(rs, deps, conflicts, expected):
    for a, b in deps:
        rs.add_dep(a, b)
    for a, b in conflicts:
        rs.add_conflict(a, b)
    assert rs.is_coherent() == expected


def test_depends_ab_ba(rs):
    rs = RuleSet()

    rs.add_dep("b", "a")

    assert rs.is_coherent()


def test_exclusive_ab(rs):
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
