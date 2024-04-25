from pathlib import Path

import uproot
import yaml

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

    all_files = [example_file]

    filter_name = lambda branch: branch in branch_list  # noqa: E731

    with uproot.open(all_files[0], filter_name=filter_name) as read_file:
        uncompressed_total = []
        for branch in branch_list:
            # print(branch)
            file_branch = read_file["CollectionTree"][branch]
            _ = file_branch.array()

            uncompressed_total.append(file_branch.uncompressed_bytes)

        print(
            f"# total read: {read_file.file.source.num_requested_bytes / 1000**2:.2f} MB"
        )
        print(f"# uncompressed total: {sum(uncompressed_total) / 1000**2:.2f} MB")
