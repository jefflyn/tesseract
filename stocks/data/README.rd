HDFStore is a dict-like object which reads and writes pandas using the high performance HDF5 format using the excellent PyTables library.
HDFStore supports an top-level API using read_hdf for reading and to_hdf for writing, similar to how read_csv and to_csv work.
Fixed Format
    pd.DataFrame(randn(10,2)).to_hdf('test_fixed.h5','df')
Table Format
    store = pd.HDFStore('store.h5')