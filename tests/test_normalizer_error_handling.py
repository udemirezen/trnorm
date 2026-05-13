import pytest

from trnorm.normalizer import normalize


def test_normalize_does_not_swallow_converter_internal_typeerror():
    def broken_converter(text, context_text=None):
        raise TypeError("internal converter bug")

    with pytest.raises(TypeError, match="internal converter bug"):
        normalize("metin", converters=[broken_converter])


def test_normalize_supports_single_argument_converter():
    def single_arg_converter(text):
        return f"{text} ok"

    assert normalize("metin", converters=[single_arg_converter]) == "metin ok"
