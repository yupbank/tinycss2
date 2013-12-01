if str is bytes:  # pragma: no cover
    # Python 2
    unichr = unichr
    basestring = basestring
else:
    unichr = chr
    basestring = str


def try_cython():
    try:
        import cython
    except ImportError:
        class Mock(object):
            def __getattr__(self, _name):
                return self

            def __call__(self, *args, **kwargs):
                pass

        sys.modules['cython'] = Mock()
    else:
        import pyximport
        py_importer, pyx_importer = pyximport.install(pyimport=True)
        from . import tokenizer
        pyximport.uninstall(py_importer, pyx_importer)
