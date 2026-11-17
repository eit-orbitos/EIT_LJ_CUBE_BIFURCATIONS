"""Read-only access to frozen Paper 2 (public V1.0 archive; mathematics frozen at V0.2-dev.10).

Paper 3 never modifies Paper 2. Cross-checks import Paper 2's own analysis code from the archive after verifying its
SHA-256. If the archive is not available, those cross-checks are skipped; the frozen constants below (with their
provenance) are still compared with this project's independent recomputations.

Archive: EIT_LJ_FULL_VECTOR_STABILITY_V1.0.zip, Zenodo version DOI 10.5281/zenodo.24187155 (concept DOI
10.5281/zenodo.24187154), GitHub release v1.0.0 of eit-orbitos/EIT_LJ_FULL_VECTOR_STABILITY.
Set EIT_LJ_PAPER2_ARCHIVE to its path, or place it next to this project's directory.
"""
import hashlib
import importlib.util
import os
import pathlib
import sys
import tempfile
import zipfile

ARCHIVE_NAME = "EIT_LJ_FULL_VECTOR_STABILITY_V1.0.zip"
ARCHIVE_SHA256 = "bb70721df7f0aa17edca30d84d1b4aaf980c0a76693be14fa780e4ab8f64762d"
DEV10_SHA256 = "3c2316c66a6bb75043503ebb0d76101b2f647666642880642518ae0f7faca40b"

# Frozen constants (Paper 2, paper/NOTES.md §8 table and analysis/cube_index_theorem.py), as strings.
FROZEN = {
    "r_star": "1.4749107381472217442",         # unique critical point of h_A (Lemma A), certified enclosure
    "P_A_soft": "3.1054933552830915550",       # P_A(0+), certified enclosure
    "q_c": "2.0199382317007999883",            # T2g corner (Lemma T2), certified enclosure, width < 1e-45
    "P_T_soft": "4.7963681893444160042",       # P_T(0+), certified enclosure
}

_ROOT = pathlib.Path(__file__).resolve().parents[2]
_CACHE = {}


def archive_path():
    env = os.environ.get("EIT_LJ_PAPER2_ARCHIVE")
    cands = [pathlib.Path(env)] if env else []
    cands += [_ROOT.parent / ARCHIVE_NAME, _ROOT / "reference" / ARCHIVE_NAME]
    for c in cands:
        if c.is_file():
            return c
    return None


def load_analysis(module="cube_index_theorem"):
    """Import a module from Paper 2's analysis/ directory inside the verified archive; None if unavailable."""
    if module in _CACHE:
        return _CACHE[module]
    path = archive_path()
    if path is None:
        return None
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != ARCHIVE_SHA256:
        raise RuntimeError(f"Paper 2 archive SHA-256 mismatch: {digest}")
    if "dir" not in _CACHE:
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="paper2_v1_"))
        with zipfile.ZipFile(path) as z:
            z.extractall(tmp)
        _CACHE["dir"] = next(tmp.iterdir())
    analysis = _CACHE["dir"] / "analysis"
    if str(analysis) not in sys.path:
        sys.path.insert(0, str(analysis))
    spec = importlib.util.spec_from_file_location(f"paper2_{module}", analysis / f"{module}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _CACHE[module] = mod
    return mod
