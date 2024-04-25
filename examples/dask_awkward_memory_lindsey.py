import distributed
import dask.array as da
import dask_awkward as dak

if __name__ == "__main__":
    with distributed.Client() as _:
        N_files = 10_000
        events_per_file = 100_128

        events = da.random.normal(
            size=N_files * events_per_file, chunks=events_per_file
        )

        dak_events = dak.from_dask_array(events)

        unflatten = dak.from_dask_array(da.tile(da.arange(448), N_files))

        jagged_events = dak.unflatten(dak_events, unflatten)

        nonzeros_axis1 = dak.count_nonzero(jagged_events, axis=1)

        nonzeros_reduction = dak.count_nonzero(nonzeros_axis1)

        computed = nonzeros_reduction.compute()

        print(computed)
