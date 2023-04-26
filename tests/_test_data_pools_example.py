# an example with 3 files, including this for the first file:
#
#        time = UNLIMITED ; // (588 currently)
#        bnds = 2 ;
#        plev = 19 ;
#        lat = 144 ;
#        lon = 192 ;
#
#        float ta(time, plev, lat, lon)
#
example_4d = 'CMIP6.CDRMIP.MOHC.UKESM1-0-LL.esm-ssp585ext.r1i1p1f2.Amon.ta.gn.v20211018'

# an example with 5 files, including this for the first file:
#
#        time = UNLIMITED ; // (120 currently)
#        bnds = 2 ;
#        lat = 144 ;
#        lon = 192 ;
#
#        float ci(time, lat, lon) ;
#
example_3d = 'CMIP6.C4MIP.MOHC.UKESM1-0-LL.ssp534-over-bgc.r4i1p1f2.Amon.ci.gn.v20220708'


data_pool_tests_db = [example_3d, example_4d]
