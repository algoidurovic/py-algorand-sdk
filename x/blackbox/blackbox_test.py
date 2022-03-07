from pathlib import Path
import pytest

from algosdk.future.transaction import StateSchema
from algosdk.v2client import algod

from .teal_blackbox import do_dryrun, cleanup, ApprovalBundle


TEAL = Path.cwd() / "x" / "blackbox" / "teal"


@pytest.fixture(scope="session", autouse=True)
def teardown():
    yield
    cleanup()


reporting_cases = [
    ("demo succeed", ApprovalBundle("demo"), ["succeed"]),
    ("demo FAIL", ApprovalBundle("demo"), ["FAIL"]),
    ("new factorial", ApprovalBundle("fac_by_ref"), []),
    ("old factorial", ApprovalBundle("old_fac"), []),
    ("swap", ApprovalBundle("swapper"), []),
    ("increment", ApprovalBundle("increment"), []),
    ("tally", ApprovalBundle("tallygo"), []),
    ("BAD factorial", ApprovalBundle("fac_by_ref_BAD"), []),
    ("Wilt", ApprovalBundle("wilt_the_stilt"), []),
    (
        "lots O vars",
        ApprovalBundle(
            "lots_o_vars",
            local_schema=StateSchema(num_uints=2, num_byte_slices=2),
            global_schema=StateSchema(num_uints=2, num_byte_slices=2),
        ),
        [39, 100, 42, "fourty two"],
    ),
]


def test_blackbox_with_report():
    for tcase, approval, args in reporting_cases:
        path = TEAL / (approval.teal + ".teal")
        print(f"case={tcase}, approval_path={path}")
        with open(path) as f:
            approval.teal = f.read()
            do_dryrun(tcase, approval, args, col_max=50)
