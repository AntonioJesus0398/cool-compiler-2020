import pytest
from .utils import getclfiles
from coolcmp.cmp_utils.parser import Parser

tests = getclfiles('.') + getclfiles('../tests')

@pytest.mark.ast_rep
@pytest.mark.parametrize("file", tests)
def test_parser_errors(file):
    p = Parser()
    p.build()

    content = ""

    with open(file) as file:
        content = file.read()

    res = p.parser.parse(content)
    
    if len(p.errors) == 0:
        print(res.__repr__())
        assert(res.__class__.__name__ == "Program")