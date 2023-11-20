This directory provides:

- A command called `data-pools-checks` (implemented in
  `run_data_pools_checks.py`) that runs the subsetter on a number of test
  cases in order to try out a variety of different types of datasets
  (including for example some on curvilinear grids). This will randomly select
  the bounds for the subsets, although there is a command line option to set a
  random seed (for example `--seed 0`) to give repeatable results, and
  optionally this can be combined with a `--cache` option to cache the
  subsetter output (under `/tmp`) rather than rerunning the subsetter every
  time the script is run.  Results from the checks (containing the name of the
  collection, the subsetting ranges used, and the test success value) are
  written initially into an sqlite database and then (periodically and also on
  exit) these are moved into a compressed CSV file.

- A command `merge-test-logs` (implemented in `merge_csv.py`) will merge the
  output logs from the above tester (as obtained from different sites) into a
  single compressed CSV file.  The `data-pools-checks` command takes an
  argument which is the site (e.g. `DKRZ`) and this is written both into the
  contents of the output `.csv.gz` file (a column called "test location") and
  also its filename, so the merge command will take a number of these files,
  and merge them into the specified output file, removing any duplicates.

- Also a file is included with some unit tests (`test_results_db.py`) to
  accompany the `ResultsDB` class (in `results_db.py`) that is used to
  implement how test results are stored.
