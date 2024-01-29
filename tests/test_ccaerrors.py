import sys

import pytest

from ccaerrors import __version__, errorNotify, errorRaise, errorExit, onErrorNotify


def test_version():
    assert __version__ == "0.1.1"


class TheException(Exception):
    """A test Exception.
    Args:
        Exception:
    """

    pass


def test_errorNotify(capsys):
    try:
        msg = "This is the test exception"
        raise TheException(msg)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        errorNotify(exci, e)
    finally:
        emsg = f"{ename} Exception at line {lineno} in function {fname}: {msg}\n"
        out, err = capsys.readouterr()
        assert out == emsg


def test_errorRaise(capsys):
    """It raises the TheException Exception after printing the error."""
    try:
        msg = "This is the test exception"
        raise TheException(msg)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        with pytest.raises(TheException):
            errorRaise(exci, e)
    finally:
        emsg = f"{ename} Exception at line {lineno} in function {fname}: {msg}\n"
        out, err = capsys.readouterr()
        assert out == emsg


def test_errorExit(capsys):
    """It attempts sys.exit after printing the error."""
    try:
        msg = "This is the test exception"
        raise TheException(msg)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        with pytest.raises(SystemExit):
            errorExit(exci, e)
    finally:
        emsg = f"{ename} Exception at line {lineno} in function {fname}: {msg}\n"
        out, err = capsys.readouterr()
        assert out == emsg


def test_decorate_notify(capsys):
    try:

        @onErrorNotify
        def decorate_notify():
            msg = "This is the test exception"
            raise TheException(msg)

        with pytest.raises(TheException):
            decorate_notify()

    except Exception as e:
        print("this is the exception handler in the test")
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
    finally:
        emsg = "calling func.__name__='decorate_notify'\n\n"
        out, err = capsys.readouterr()
        estr = f"{out}\n{err}"
        assert estr == emsg
