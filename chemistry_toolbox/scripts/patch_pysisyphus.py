"""Install Hessian and scan-coordinate fixes in the selected pysisyphus environment."""
from importlib.util import find_spec
from pathlib import Path


def patch_orca_parser(path: Path) -> None:
    text = path.read_text()
    old = "            + act_energy\n            + hessian"
    new = ('            + act_energy\n'
           '            + pp.Optional(pp.Suppress(pp.Literal("$multiplicity") + integer))\n'
           '            + hessian')
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"Unrecognized pysisyphus ORCA Hessian parser: {path}")
    path.write_text(text.replace(old, new, 1))


def patch_scan_driver(path: Path) -> None:
    text = path.read_text()
    if "except RebuiltInternalsException:" in text:
        return
    old = """        new_coords = constr_geom.coords
        new_coords[constr_ind] = cur_val
        constr_geom.set_coords(new_coords, update_constraints=True)"""
    new = """        constr_ind = constr_geom.internal.get_index_of_typed_prim(constr_prim)
        new_coords = constr_geom.coords
        new_coords[constr_ind] = cur_val
        try:
            constr_geom.set_coords(new_coords, update_constraints=True)
        except RebuiltInternalsException:
            # Rebuilding changes primitive indices and only partially applies the step.
            constr_ind = constr_geom.internal.get_index_of_typed_prim(constr_prim)
            new_coords = constr_geom.coords
            new_coords[constr_ind] = cur_val
            constr_geom.set_coords(new_coords, update_constraints=True)"""
    if old not in text:
        raise RuntimeError(f"Unrecognized pysisyphus scan driver: {path}")
    text = text.replace(old, new, 1).replace(
        "from pysisyphus.Geometry import Geometry",
        "from pysisyphus.Geometry import Geometry\nfrom pysisyphus.intcoords.exceptions import RebuiltInternalsException", 1)
    text = text.replace("        scan_vals.append(constr_geom.coords[constr_ind])",
                        "        constr_ind = constr_geom.internal.get_index_of_typed_prim(constr_prim)\n"
                        "        scan_vals.append(constr_geom.coords[constr_ind])", 1)
    path.write_text(text)


if __name__ == "__main__":
    package = Path(next(iter(find_spec("pysisyphus").submodule_search_locations)))
    patch_orca_parser(package / "calculators/ORCA.py")
    patch_scan_driver(package / "drivers/scan.py")
