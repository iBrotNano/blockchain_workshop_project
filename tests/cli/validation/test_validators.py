from validation.validators import striped_str_is_not_empty


def test_striped_str_is_not_empty():
    assert striped_str_is_not_empty("valid input") is True
    assert striped_str_is_not_empty("") is False
    assert striped_str_is_not_empty("   ") is False

    assert (
        striped_str_is_not_empty("   valid input   ") is True
    )  # Leading/trailing whitespace should be ignored

    assert (
        striped_str_is_not_empty("\n\t") is False
    )  # Only whitespace characters should be considered invalid
