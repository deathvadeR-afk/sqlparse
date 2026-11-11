import pytest

from sqlparse import tokens
from sqlparse.lexer import Lexer
from sqlparse.lexer import tokenize


class TestSQLREGEX:
    @pytest.mark.parametrize('number', ['1.0', '-1.0',
                                        '1.', '-1.',
                                        '.1', '-.1'])
    def test_float_numbers(self, number):
        ttype = next(tt for action, tt in Lexer.get_default_instance()._SQL_REGEX if action(number))
        assert tokens.Number.Float == ttype


def _tokens_without_whitespace(sql):
    return [(tt, value) for tt, value in tokenize(sql) if tt is not tokens.Whitespace]


def test_qp_qtpy_30_1_between_leading_dot_numbers_are_numbers():
    # [QP-QTPY-30-1] Tokenises .03 and .06 as number tokens in a BETWEEN expression
    token_types = {value: tt for tt, value in _tokens_without_whitespace('a BETWEEN .03 AND .06')}
    assert token_types['.03'] in tokens.Number
    assert token_types['.06'] in tokens.Number


def test_qp_qtpy_30_2_between_and_are_keywords_not_names():
    # [QP-QTPY-30-2] Tokenises BETWEEN and AND as keywords when numbers lack a leading zero
    token_types = {value: tt for tt, value in _tokens_without_whitespace('a BETWEEN .03 AND .06')}
    for word in ('BETWEEN', 'AND'):
        assert token_types[word] in tokens.Keyword
        assert token_types[word] not in tokens.Name
