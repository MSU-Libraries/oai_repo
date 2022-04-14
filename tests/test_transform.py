from oai_repo.transform import Transform

def test_transform():
    tfm = Transform([])
    # _replace transform
    assert tfm._replace("abcdab", "a", "z") == "zbcdzb"
    assert tfm._replace("zbcdzb", "a", "z", reverse=True) == "abcdab"

    # _prefix transform
    assert tfm._prefix("abc", "add", "123") == "123abc"
    assert tfm._prefix("123abc", "del", "123") == "abc"

    # _suffix transform
    assert tfm._suffix("abc", "add", "123") == "abc123"
    assert tfm._suffix("abc123", "del", "123") == "abc"

    # Transform chain 1
    tlist1 = [
        { "replace": [":", "_"] },
        { "prefix": ["add", "oai:d.lib.msu.edu:"] }
    ]
    orig = "etd:1234"
    tfm = Transform(tlist1)
    changed = tfm.forward(orig)
    assert changed == "oai:d.lib.msu.edu:etd_1234"
    revert = tfm.reverse(changed)
    assert revert == orig

    # Transform chain 1
    tlist2 = [
        { "prefix": ["del", "info:fedora/"] },
        { "suffix": ["del", ":root"] }
    ]
    orig = "info:fedora/vvl:root"
    tfm = Transform(tlist2)
    changed = tfm.forward(orig)
    assert changed == "vvl"
    revert = tfm.reverse(changed)
    assert revert == orig
