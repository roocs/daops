from collections import OrderedDict

from daops.utils.normalise import ResultSet

from tests._common import MINI_ESGF_MASTER_DIR


def test_file_uris_url(load_esgf_test_data):
    result = ResultSet()

    original_file_urls = OrderedDict(
        [
            (
                "CMIP6.CMIP.IPSL.IPSL-CM6A-LR.historical.r1i1p1f1.Amon.rlds.gr.v20180803",
                [
                    "https://data.mips.copernicus-climate.eu/thredds/fileServer/esg_c3s-cmip6"
                    "/CMIP6/CMIP/IPSL/IPSL-CM6A-LR/historical/r1i1p1f1/Amon/rlds/gr/v20180803/"
                    "rlds_Amon_IPSL-CM6A-LR_historical_r1i1p1f1_gr_185001-201412.nc"
                ],
            )
        ]
    )

    for ds_id, file_urls in original_file_urls.items():
        result.add(ds_id, file_urls)
    assert result.file_uris == [
        "https://data.mips.copernicus-climate.eu/thredds/fileServer"
        "/esg_c3s-cmip6/CMIP6/CMIP/IPSL/IPSL-CM6A-LR/historical"
        "/r1i1p1f1/Amon/rlds/gr/v20180803/rlds_Amon_"
        "IPSL-CM6A-LR_historical_r1i1p1f1_gr_185001-201412.nc"
    ]


def test_file_uris_files(load_esgf_test_data):
    result = ResultSet()

    file_path = OrderedDict(
        [
            (
                "CMIP6.CMIP.IPSL.IPSL-CM6A-LR.historical.r1i1p1f1.Amon.rlds.gr.v20180803",
                [
                    f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip6/data/CMIP6/CMIP/IPSL"
                    "/IPSL-CM6A-LR/historical/r1i1p1f1/Amon/rlds/gr/v20180803"
                    "/rlds_Amon_IPSL-CM6A-LR_historical_r1i1p1f1_gr_185001-201412.nc"
                ],
            )
        ]
    )

    for ds_id, file in file_path.items():
        result.add(ds_id, file)
    assert result.file_uris == [
        f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip6/data/CMIP6/CMIP/IPSL/IPSL-CM6A-LR/historical"
        "/r1i1p1f1/Amon/rlds/gr/v20180803/rlds_Amon_IPSL-CM6A-LR_historical_r1i1p1f1_gr_185001-201412.nc"
    ]
