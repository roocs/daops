""" Tests for daops library """
# FutureWarning: In xarray version 0.15 the default behaviour of `open_mfdataset`
# will change. To retain the existing behavior, pass
# combine='nested'. To use future default behavior, pass
# combine='by_coords'.
# create class to test each function - has different tests defined within it?


def test_subset_data_ref():
    """ Tests daops api.subset function with only a data ref"""
    pass


def test_subset_time():
    """Tests daops api.subset function with a time subset.
    Check ResultSet contains the correct info"""
    pass


def test_subset_invalid_time():
    """ Tests daops api.subset function with an invalid time subset."""
    pass


def test_subset_space():
    """Tests daops api.subset function with a space subset.
    Check ResultSet contains the correct info"""
    pass


def test_subset_invalid_space():
    """ Tests daops api.subset function with an invalid space subset."""
    pass


def test_subset_level():
    """Tests daops api.subset function with a level subset.
    Check ResultSet contains the correct info"""
    pass


def test_subset_invalid_level():
    """ Tests daops api.subset function with an invalid level subset."""
    pass


def test_subset_all():
    """Tests daops api.subset function with time, space, level subsets.
    Check ResultSet contains the correct info"""
    pass


def test_wrap_sequence_str():
    """Tests daops utils._wrap_sequence with string.
    Check correct type is returned when string passed."""
    pass


def test_wrap_sequence_not_str():
    """Tests daops utils._wrap_sequence with object that isn't a string.
    Check correct response when passed."""
    pass


def test_is_data_ref_characterised_true():
    """Tests daops utils.is_dataref_characterised.
    Check correct response for data ref that is characterised."""
    pass


def test_is_data_ref_characterised_false():
    """Tests daops utils.is_dataref_characterised.
    Check correct response for data ref that is not characterised."""
    pass


def test_is_characterised_all_required_true_mixed():
    """Tests daops utils.is_characterised.
    Check response when all required is True for mixed characterisation."""
    pass


def test_is_characterised_all_required_true_all():
    """Tests daops utils.is_characterised.
    Check response when all required is True for all characterised."""
    pass


def test_is_characterised_all_required_true_none():
    """Tests daops utils.is_characterised.
    Check response when all required is True for none characterised."""
    pass


def test_is_characterised_all_required_false_mixed():
    """Tests daops utils.is_characterised.
    Check response when all required is False for mixed characterisation."""
    pass


def test_is_characterised_all_required_false_all():
    """Tests daops utils.is_characterised.
    Check response when all required is False for all characterised."""
    pass


def test_is_characterised_all_required_false_none():
    """Tests daops utils.is_characterised.
    Check response when all required is False for none characterised."""
    pass


# consolidate fixes data inputs so they can be passed to xarray
def test_consolidate_data_ref_fpath():
    """Tests daops utils._consolidate_data_ref with file path e.g.
    /badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/atmos/Amon/r1i1p1/latest/tas/*.nc"""
    pass


def test_consolidate_data_ref_drs():
    """Tests daops utils._consolidate_data_ref with DRS e.g.
    cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh"""
    pass


def test_consolidate_data_ref_invalid():
    """ Tests daops utils._consolidate_data_ref with an invalid data ref """
    pass


def test_consolidate_mixed():
    """Tests daops utils.consolidate.
    Test when drefs are a mixture of file paths and drs."""
    pass


def test_consolidate_all_fpath():
    """Tests daops utils.consolidate.
    Test when drefs are all file paths."""
    pass


def test_consolidate_one_invalid():
    """Tests daops utils.consolidate.
    Test when one dref is invalid."""
    pass


def test_consolidate_all_dref():
    """Tests daops utils.consolidate.
    Test when drefs are all drs."""
    pass


def test_consolidate_with_time():
    """Tests daops utils.consolidate.
    Test when a valid time is passed as a kwarg."""
    pass


def test_consolidate_with_invalid_time():
    """Tests daops utils.consolidate.
    Test when an invalid time range is passed as a kwarg."""
    pass


def test_consolidate_all_kwargs():
    """Tests daops utils.consolidate.
    Test when all kwargs are provided."""
    pass


def test_normalise_character_problem():  # create tests for different types of character problem
    """Tests daops utils.normalise which fixes data based on character"""
    pass


def test_normalise_character_no_problem():
    """ Tests daops utils.normalise for data with no problems"""
    pass


def test_ResultSet_init():
    """Tests init function of ResultSet class in daops utils.
    Checks the metadata is as expected."""
    pass


def test_ResultSet_add():
    """Tests add function of ResultSet class in daops utils.
    Checks the file paths and _results are expected."""
    pass


def test_dispatch():  # can test with different operations
    """ Tests daops processor.dispatch."""
    pass


def test_process_serial():
    """ Tests daops processor.process with mode='serial'"""
    pass


def test_process_other_mode():
    """ Tests daops processor.process with mode other than 'serial'"""
    pass
