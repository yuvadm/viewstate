from viewstate.utils import list_to_tuple


def test_list_to_tuple():
    assert list_to_tuple([1, 2, 3]) == (1, 2, 3)
    assert list_to_tuple((9, 8, 7)) == (9, 8, 7)
    assert list_to_tuple((None, [2, 3, None])) == (None, (2, 3, None))
    assert list_to_tuple(("abc", [2, [3], (9, 8, True, False)])) == (
        "abc",
        (2, (3,), (9, 8, True, False)),
    )
    assert list_to_tuple("abc") == "abc"
