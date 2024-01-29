import sys

__version__ = "0.1.1"


def errorNotify(exci, e, fname=None):
    lineno = exci.tb_lineno
    if fname is None:
        fname = exci.tb_frame.f_code.co_name
    ename = type(e).__name__
    msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
    # log.error(msg)
    print(msg)


def errorRaise(exci, e, fname=None):
    errorNotify(exci, e, fname)
    raise


def errorExit(exci, e, fname=None):
    errorNotify(exci, e, fname)
    sys.exit(1)


def onErrorNotify(func):
    try:

        def wrapper(*args, **kwargs):
            print(f"calling {func.__name__=}")
            res = func(*args, **kwargs)
            print(f"finished calling {func.__name__}")

        return wrapper
    except Exception as e:
        print(f"exception handler in decorator")
        print(f"an exception occurred: {e=}, {func.__name__=}")
        print("calling errorNotify")
        errorNotify(sys.exc_info()[2], e, func.__name__)
