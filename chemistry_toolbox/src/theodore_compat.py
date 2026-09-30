"""Explicit TheoDORE 2.5 reader adapter; no arbitrary script interception."""
from contextlib import contextmanager
import inspect
import json
from pathlib import Path

ADAPTER_VERSION = "theodore-reader-1"


@contextmanager
def compatible_reader():
    """Opt in within a dedicated analysis process; restore the method on exit."""
    from theodore.cclib_interface import file_parser_cclib
    from .backends.quantum_reader import read_quantum_output
    original = file_parser_cclib.get_data
    if tuple(inspect.signature(original).parameters) != ("self", "rtype", "rfile"):
        raise RuntimeError("Unsupported TheoDORE get_data signature; use its native reader")
    def get_data(self, rtype, rfile):
        data, diagnostic = read_quantum_output(Path(rfile))
        self.reader_diagnostic = {"adapter_version": ADAPTER_VERSION, **diagnostic}
        if data is None:
            raise RuntimeError(json.dumps(self.reader_diagnostic, ensure_ascii=False))
        parser = diagnostic["parser_class"]
        return data, "ORCA" if parser == "CompatibleORCA" else parser
    file_parser_cclib.get_data = get_data
    try:
        yield
    finally:
        file_parser_cclib.get_data = original


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("analyze_tden", "analyze_sden"))
    parser.add_argument("-f", "--ifile", default="dens_ana.in")
    args = parser.parse_args()
    from importlib import import_module
    action = getattr(import_module("theodore.actions." + args.action),
                     {"analyze_tden": "AnalyzeTden", "analyze_sden": "AnalyzeSden"}[args.action])
    with compatible_reader():
        return action.run(ifile=args.ifile)


if __name__ == "__main__":
    main()
