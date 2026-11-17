# MIT; adapted from Gathin CleanYourTV recovery.py. See NOTICE.
import re
CORE_RE = re.compile(r"^(android|android\.ext\.(services|shared)|com\.(google\.)?android\.sdksandbox|com\.android\.location\.fused|com\.android\.systemui|com\.android\.shell|com\.android\.phone|com\.android\.settings|com\.android\.tv\.settings|com\.(google\.)?android\.(permissioncontroller|packageinstaller|ext\.services|ext\.shared|modulemetadata)|com\.google\.android\.overlay\.modules.*|com\.android\.providers\..*|com\.cltv\.mal|com\.mediatek\.(tis|tv\.service|tv\.agent))$")
CORE_OK = re.compile(r"^com\.android\.providers\.(calendar|contacts|userdictionary|blockednumber)$")


def core_packages(names):
    """The names in a list that must never be disabled, in list order."""
    return [n for n in names if CORE_RE.match(n) and not CORE_OK.match(n)]

