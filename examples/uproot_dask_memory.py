import warnings
from pathlib import Path

import awkward as ak
import uproot
import yaml

warnings.filterwarnings("ignore")


def materialize_branches(events, branch_list):
    num_events = ak.num(events, axis=0)  # track number of events

    _counter = 0
    # see https://github.com/dask-contrib/dask-awkward/issues/499 for context
    for branch in branch_list:
        _counter_to_add = ak.count_nonzero(events[branch], axis=-1)  # reduce innermost

        # reduce >2-dimensional (per event) branches further
        for _ in range(_counter_to_add.ndim - 1):
            _counter_to_add = ak.count_nonzero(_counter_to_add, axis=-1)

        _counter = _counter + _counter_to_add  # sum 1-dim array built from new branch
        # gc.collect()  # does nothing?

    _counter = ak.count_nonzero(_counter, axis=0)  # reduce to int

    return {"nevts": num_events, "_counter": _counter}


if __name__ == "__main__":
    data_dir = Path("/tmp") / "data"
    if not data_dir.exists():
        data_dir.mkdir()

    example_file = data_dir / "DAOD_PHYSLITE.37233417._000052.pool.root.1"

    if not (example_file).exists():
        import urllib.request

        urllib.request.urlretrieve(
            "https://cernbox.cern.ch/remote.php/dav/public-files/BPIO76iUaeYuhaF/DAOD_PHYSLITE.37233417._000052.pool.root.1",
            example_file,
        )

    with open("branch_list.yml") as read_file:
        branch_list = yaml.safe_load(read_file)["branch_list"]

    filter_name = lambda branch: branch in branch_list  # noqa: E731
    events = uproot.dask({example_file: "CollectionTree"}, filter_name=filter_name)
    task = materialize_branches(events, branch_list)
    task["_counter"].compute()
