import gc
import multiprocessing
import time
import warnings
from pathlib import Path

import awkward as ak
import psutil
import uproot
import yaml

process = psutil.Process()


def watcher(pid):
    other_process = psutil.Process(pid)  # noqa: F841
    while True:
        time.sleep(0.5)
        print(
            f"        RSS: {process.memory_full_info().rss / 1024**2:.0f} USS: {process.memory_full_info().uss / 1024**2:.0f} MB"
        )


other_process = multiprocessing.Process(
    target=watcher, args=(process.pid,), daemon=True
)
other_process.start()

gc.collect()
print(
    f"beginning of time RSS: {process.memory_full_info().rss / 1024**2:.0f} USS: {process.memory_full_info().uss / 1024**2:.0f} MB"
)

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


def everything(file_name, branch_list):
    events = uproot.concatenate({file_name: "CollectionTree"}, filter_name=branch_list)
    task = materialize_branches(events, branch_list)
    task["_counter"]


if __name__ == "__main__":
    data_dir = Path("/tmp") / "data"
    if not data_dir.exists():
        data_dir.mkdir()

    example_file = data_dir / "DAOD_PHYSLITE.37233417._000052.pool.root.1"

    if not (example_file).exists():
        import urllib.request

        # download input file (~1.1 GB):
        urllib.request.urlretrieve(
            "https://cernbox.cern.ch/remote.php/dav/public-files/BPIO76iUaeYuhaF/DAOD_PHYSLITE.37233417._000052.pool.root.1",
            example_file,
        )

    with open("branch_list.yml") as read_file:
        branch_list = yaml.safe_load(read_file)["branch_list"]

    for i in range(10):
        gc.collect()
        print(
            f"begin {i} RSS: {process.memory_full_info().rss / 1024**2:.0f} USS: {process.memory_full_info().uss / 1024**2:.0f} MB"
        )
        everything(example_file, branch_list)

    gc.collect()
    print(
        f"end of time RSS: {process.memory_full_info().rss / 1024**2:.0f} USS: {process.memory_full_info().uss / 1024**2:.0f} MB"
    )
