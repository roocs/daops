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

examples_rot = ['CMIP6.CMIP.CMCC.CMCC-ESM2.historical.r1i1p1f1.Oyr.o2.gn.v20210114',
                'CMIP6.AerChemMIP.HAMMOZ-Consortium.MPI-ESM-1-2-HAM.hist-piAer.r1i1p1f1.Ofx.volcello.gn.v20190627']


# One dataset from every model that exists at CEDA and has 2d lon / lat arrays
more_examples_rot = '''
CMIP6.AerChemMIP.HAMMOZ-Consortium.MPI-ESM-1-2-HAM.hist-piAer.r1i1p1f1.Ofx.volcello.gn.v20190627
CMIP6.AerChemMIP.NCC.NorESM2-LM.hist-piAer.r1i1p1f1.Omon.volcello.gn.v20191108
CMIP6.CMIP.CCCma.CanESM5-CanOE.1pctCO2.r1i1p2f1.Ofx.sftof.gn.v20190429
CMIP6.CMIP.EC-Earth-Consortium.EC-Earth3-LR.piControl.r1i1p1f1.3hr.tos.gn.v20200919
CMIP6.DAMIP.CAS.FGOALS-g3.hist-aer.r1i1p1f1.Omon.tos.gn.v20200427
CMIP6.HighResMIP.CAS.FGOALS-f3-H.control-1950.r1i1p1f1.Oday.tos.gn.v20210120
CMIP6.OMIP.CSIRO-COSIMA.ACCESS-OM2-025.omip2.r1i1p1f1.Oday.tos.gn.v20210617
CMIP6.OMIP.CSIRO-COSIMA.ACCESS-OM2.omip2-spunup.r1i1p1f1.Oday.tos.gn.v20210616
CMIP6.OMIP.NTU.TaiESM1-TIMCOM.omip1.r1i1p1f1.Ofx.deptho.gn.v20201028
CMIP6.CMIP.EC-Earth-Consortium.EC-Earth3P-VHR.historical.r1i1p2f1.Amon.clt.gr.v20201007
CMIP6.FAFMIP.NOAA-GFDL.GFDL-ESM2M.faf-all.r1i1p1f1.Omon.so.gn.v20180701
CMIP6.OMIP.NOAA-GFDL.GFDL-OM4p5B.omip1.r1i1p1f1.Omon.so.gn.v20180701
'''.strip().split()

# One dataset from every model that exists at CEDA and has 1d but non-coordinate lon / lat arrays
examples_unstructured = '''
CMIP6.CMIP.MPI-M.ICON-ESM-LR.1pctCO2.r1i1p1f1.Amon.rlut.gn.v20210215
CMIP6.CMIP.UA.MCM-UA-1-0.1pctCO2.r1i1p1f1.Amon.rlut.gn.v20190731
CMIP6.HighResMIP.AWI.AWI-CM-1-1-HR.hist-1950.r1i1p1f2.3hr.tos.gn.v20170825
CMIP6.HighResMIP.AWI.AWI-CM-1-1-LR.hist-1950.r1i1p1f2.3hr.tos.gn.v20170825
CMIP6.HighResMIP.NCAR.CESM1-CAM5-SE-HR.control-1950.r1i1p1f1.Amon.ts.gn.v20200724
CMIP6.HighResMIP.NCAR.CESM1-CAM5-SE-LR.control-1950.r1i1p1f1.Amon.ts.gn.v20200708
'''.strip().split()


# One dataset from every model that exists at CEDA
all_examples = '''
CMIP.CSIRO-ARCCSS.ACCESS-CM2.1pctCO2.r1i1p1f1.Amon.clt.gn.v20191109
C4MIP.CSIRO.ACCESS-ESM1-5.esm-ssp585.r2i1p1f1.Amon.tas.gn.v20191203
OMIP.CSIRO-COSIMA.ACCESS-OM2.omip2-spunup.r1i1p1f1.Oday.tos.gn.v20210616
OMIP.CSIRO-COSIMA.ACCESS-OM2-025.omip2.r1i1p1f1.Oday.tos.gn.v20210617
HighResMIP.AWI.AWI-CM-1-1-HR.hist-1950.r1i1p1f2.3hr.tos.gn.v20170825
HighResMIP.AWI.AWI-CM-1-1-LR.hist-1950.r1i1p1f2.3hr.tos.gn.v20170825
CMIP.AWI.AWI-CM-1-1-MR.1pctCO2.r1i1p1f1.3hr.tas.gn.v20181218
CMIP.AWI.AWI-ESM-1-1-LR.1pctCO2.r1i1p1f1.3hr.tas.gn.v20200212
HighResMIP.BCC.BCC-CSM2-HR.control-1950.r1i1p1f1.Amon.ts.gn.v20200922
C4MIP.BCC.BCC-CSM2-MR.1pctCO2-bgc.r1i1p1f1.Amon.cli.gn.v20190321
AerChemMIP.BCC.BCC-ESM1.hist-piNTCF.r1i1p1f1.Amon.ch4.gn.v20190621
CMIP.CAMS.CAMS-CSM1-0.1pctCO2.r1i1p1f1.Amon.cli.gn.v20190708
CMIP.CAS.CAS-ESM2-0.1pctCO2.r1i1p1f1.Amon.rlut.gn.v20201228
HighResMIP.NCAR.CESM1-CAM5-SE-HR.control-1950.r1i1p1f1.Amon.ts.gn.v20200724
HighResMIP.NCAR.CESM1-CAM5-SE-LR.control-1950.r1i1p1f1.Amon.ts.gn.v20200708
C4MIP.NCAR.CESM2.1pctCO2-bgc.r1i1p1f1.Amon.cli.gn.v20190724
CMIP.NCAR.CESM2-FV2.1pctCO2.r1i1p1f1.Amon.rlut.gn.v20200310
AerChemMIP.NCAR.CESM2-WACCM.hist-1950HC.r1i1p1f1.Amon.ch4.gn.v20190606
CMIP.NCAR.CESM2-WACCM-FV2.1pctCO2.r1i1p1f1.Amon.rlut.gn.v20200226
CMIP.THU.CIESM.1pctCO2.r1i1p1f1.Amon.rlut.gr.v20200417
CMIP.CMCC.CMCC-CM2-HR4.1pctCO2.r1i1p1f1.6hrPlev.tas.gn.v20210304
CMIP.CMCC.CMCC-CM2-SR5.1pctCO2.r1i1p1f1.3hr.tas.gn.v20200616
HighResMIP.CMCC.CMCC-CM2-VHR4.control-1950.r1i1p1f1.6hrPlev.psl.gn.v20200917
CMIP.CMCC.CMCC-ESM2.1pctCO2.r1i1p1f1.3hr.tas.gn.v20210114
CFMIP.CNRM-CERFACS.CNRM-CM6-1.abrupt-0p5xCO2.r1i1p1f2.Amon.evspsbl.gr.v20190711
CMIP.CNRM-CERFACS.CNRM-CM6-1-HR.1pctCO2.r1i1p1f2.Emon.orog.gr.v20191021
AerChemMIP.CNRM-CERFACS.CNRM-ESM2-1.hist-1950HC.r1i1p1f2.Lmon.baresoilFrac.gr.v20190621
C4MIP.CCCma.CanESM5.1pctCO2-bgc.r1i1p1f1.AERmon.ps.gn.v20190429
CMIP.CCCma.CanESM5-CanOE.1pctCO2.r1i1p2f1.Ofx.sftof.gn.v20190429
CFMIP.LLNL.E3SM-1-0.amip-p4K.r2i1p1f1.Amon.clivi.gr.v20210302
CMIP.E3SM-Project.E3SM-1-1.historical.r1i1p1f1.AERmon.abs550aer.gr.v20191211
CMIP.E3SM-Project.E3SM-1-1-ECA.historical.r1i1p1f1.AERmon.abs550aer.gr.v20200623
CMIP.E3SM-Project.E3SM-2-0.abrupt-4xCO2.r1i1p1f1.Amon.hfls.gr.v20220826
CMIP.EC-Earth-Consortium.EC-Earth3.1pctCO2.r3i1p1f1.3hr.tas.gr.v20210522
CMIP.EC-Earth-Consortium.EC-Earth3-AerChem.1pctCO2.r1i1p1f1.3hr.tas.gr.v20200729
CMIP.EC-Earth-Consortium.EC-Earth3-CC.1pctCO2.r1i1p1f1.Amon.rlut.gr.v20210525
DCPP.EC-Earth-Consortium.EC-Earth3-HR.dcppA-hindcast.s1990-r10i2p1f1.Amon.rsds.gr.v20201205
CMIP.EC-Earth-Consortium.EC-Earth3-LR.piControl.r1i1p1f1.3hr.tos.gn.v20200919
CMIP.EC-Earth-Consortium.EC-Earth3-Veg.1pctCO2.r1i1p1f1.3hr.tas.gr.v20200325
CMIP.EC-Earth-Consortium.EC-Earth3-Veg-LR.abrupt-4xCO2.r1i1p1f1.Amon.hfls.gr.v20220428
HighResMIP.EC-Earth-Consortium.EC-Earth3P.control-1950.r1i1p2f1.3hr.clt.gr.v20190906
HighResMIP.EC-Earth-Consortium.EC-Earth3P-HR.control-1950.r1i1p2f1.3hr.clt.gr.v20181119
CMIP.EC-Earth-Consortium.EC-Earth3P-VHR.historical.r1i1p2f1.Amon.clt.gr.v20201007
HighResMIP.ECMWF.ECMWF-IFS-HR.control-1950.r1i1p1f1.6hrPlevPt.psl.gr.v20170915
HighResMIP.ECMWF.ECMWF-IFS-LR.control-1950.r1i1p1f1.6hrPlevPt.psl.gr.v20180221
HighResMIP.ECMWF.ECMWF-IFS-MR.control-1950.r1i1p1f1.6hrPlevPt.psl.gr.v20181121
HighResMIP.CAS.FGOALS-f3-H.control-1950.r1i1p1f1.Oday.tos.gn.v20210120
CMIP.CAS.FGOALS-f3-L.1pctCO2.r1i1p1f1.Amon.rlut.gr.v20200620
CMIP.CAS.FGOALS-g3.1pctCO2.r1i1p1f1.3hr.tas.gn.v20191219
CMIP.FIO-QLNM.FIO-ESM-2-0.1pctCO2.r1i1p1f1.Amon.rlut.gn.v20200302
CMIP.NOAA-GFDL.GFDL-AM4.amip.r1i1p1f1.AERmon.lwp.gr1.v20180807
CFMIP.NOAA-GFDL.GFDL-CM4.amip-4xCO2.r1i1p1f1.Amon.evspsbl.gr1.v20180701
HighResMIP.NOAA-GFDL.GFDL-CM4C192.control-1950.r1i1p1f1.Amon.ts.gr3.v20180701
FAFMIP.NOAA-GFDL.GFDL-ESM2M.faf-all.r1i1p1f1.Omon.so.gn.v20180701
AerChemMIP.NOAA-GFDL.GFDL-ESM4.piClim-aer.r1i1p1f1.AERmon.cdnc.gr1.v20180701
OMIP.NOAA-GFDL.GFDL-OM4p5B.omip1.r1i1p1f1.Omon.so.gn.v20180701
CFMIP.NASA-GISS.GISS-E2-1-G.abrupt-0p5xCO2.r1i1p1f1.Amon.cli.gn.v20190524
CMIP.NASA-GISS.GISS-E2-1-G-CC.esm-hist.r1i1p1f1.Amon.clt.gn.v20190815
CFMIP.NASA-GISS.GISS-E2-1-H.abrupt-2xCO2.r1i1p1f1.Amon.cli.gn.v20190403
CFMIP.NASA-GISS.GISS-E2-2-G.abrupt-2xCO2.r1i1p1f1.Amon.evspsbl.gn.v20191120
CMIP.NASA-GISS.GISS-E2-2-H.1pctCO2.r1i1p1f1.Amon.rlut.gn.v20191120
HighResMIP.MOHC.HadGEM3-GC31-HH.control-1950.r1i1p1f1.3hr.clt.gn.v20180927
HighResMIP.MOHC.HadGEM3-GC31-HM.control-1950.r1i1p1f1.3hr.clt.gn.v20180713
CFMIP.MOHC.HadGEM3-GC31-LL.a4SST.r1i1p1f3.AERmon.abs550aer.gn.v20200403
HighResMIP.MOHC.HadGEM3-GC31-LM.highresSST-future.r1i14p1f1.3hr.pr.gn.v20190710
HighResMIP.MOHC.HadGEM3-GC31-MH.spinup-1950.r1i1p1f1.3hr.clt.gn.v20171227
CMIP.MOHC.HadGEM3-GC31-MM.1pctCO2.r1i1p1f3.3hr.clt.gn.v20201113
HighResMIP.AS-RCEC.HiRAM-SIT-HR.highres-future.r1i1p1f1.Amon.ts.gn.v20210707
HighResMIP.AS-RCEC.HiRAM-SIT-LR.highres-future.r1i1p1f1.Amon.ts.gn.v20210707
CMIP.MPI-M.ICON-ESM-LR.1pctCO2.r1i1p1f1.Amon.rlut.gn.v20210215
CMIP.CCCR-IITM.IITM-ESM.1pctCO2.r1i1p1f1.3hr.tas.gn.v20191204
CMIP.INM.INM-CM4-8.1pctCO2.r1i1p1f1.Amon.rlut.gr1.v20190530
CMIP.INM.INM-CM5-0.1pctCO2.r1i1p1f1.Amon.rlut.gr1.v20200226
HighResMIP.INM.INM-CM5-H.control-1950.r1i1p1f1.Amon.ts.gr1.v20190812
CMIP.IPSL.IPSL-CM5A2-INCA.1pctCO2.r1i1p1f1.Amon.rlut.gr.v20201218
HighResMIP.IPSL.IPSL-CM6A-ATM-HR.highresSST-present.r1i1p1f1.3hr.mrsos.gr.v20190122
C4MIP.IPSL.IPSL-CM6A-LR.1pctCO2-bgc.r1i1p1f1.Amon.huss.gr.v20180914
CMIP.IPSL.IPSL-CM6A-LR-INCA.abrupt-4xCO2.r1i1p1f1.3hr.pr.gr.v20210113
CMIP.NIMS-KMA.KACE-1-0-G.1pctCO2.r1i1p1f1.3hr.tas.gr.v20190918
CMIP.KIOST.KIOST-ESM.1pctCO2.r1i1p1f1.3hr.tas.gr1.v20210601
CMIP.UA.MCM-UA-1-0.1pctCO2.r1i1p1f1.Amon.rlut.gn.v20190731
CMIP.MIROC.MIROC-ES2H.historical.r1i1p1f2.Amon.clt.gn.v20210125
CMIP.MIROC.MIROC-ES2L.1pctCO2.r1i1p1f2.Amon.rlut.gn.v20190823
AerChemMIP.MIROC.MIROC6.hist-piAer.r1i1p1f1.Amon.cli.gn.v20190807
AerChemMIP.HAMMOZ-Consortium.MPI-ESM-1-2-HAM.hist-piAer.r1i1p1f1.Ofx.volcello.gn.v20190627
CMIP.MPI-M.MPI-ESM1-2-HR.1pctCO2.r1i1p1f1.3hr.tas.gn.v20190710
C4MIP.MPI-M.MPI-ESM1-2-LR.1pctCO2-bgc.r2i1p1f1.Amon.tas.gn.v20190710
HighResMIP.MPI-M.MPI-ESM1-2-XR.control-1950.r1i1p1f1.6hrPlev.wap.gn.v20180606
HighResMIP.MRI.MRI-AGCM3-2-H.highresSST-future.r1i1p1f1.Amon.ts.gn.v20200619
HighResMIP.MRI.MRI-AGCM3-2-S.highresSST-future.r1i1p1f1.Amon.ts.gn.v20200619
CFMIP.MRI.MRI-ESM2-0.abrupt-0p5xCO2.r1i1p1f1.3hr.huss.gn.v20210308
CMIP.NUIST.NESM3.1pctCO2.r1i1p1f1.3hr.tas.gn.v20190707
HighResMIP.MIROC.NICAM16-7S.highresSST-present.r1i1p1f1.3hr.tos.gr.v20190325
HighResMIP.MIROC.NICAM16-8S.highresSST-present.r1i1p1f1.3hr.tos.gr.v20190830
HighResMIP.MIROC.NICAM16-9S.highresSST-present.r1i1p1f1.3hr.tos.gr.v20190830
CMIP.NCC.NorCPM1.1pctCO2.r1i1p1f1.Amon.rlut.gn.v20190914
CMIP.NCC.NorESM1-F.piControl.r1i1p1f1.AERmon.ua.gn.v20190920
AerChemMIP.NCC.NorESM2-LM.hist-piAer.r1i1p1f1.Omon.volcello.gn.v20191108
CMIP.NCC.NorESM2-MM.1pctCO2.r1i1p1f1.6hrPlev.tas.gn.v20210319
CMIP.SNU.SAM0-UNICON.1pctCO2.r1i1p1f1.3hr.tas.gn.v20190323
CFMIP.AS-RCEC.TaiESM1.abrupt-0p5xCO2.r1i1p1f1.AERmon.ps.gn.v20210913
OMIP.NTU.TaiESM1-TIMCOM.omip1.r1i1p1f1.Ofx.deptho.gn.v20201028
AerChemMIP.MOHC.UKESM1-0-LL.hist-piAer.r1i1p1f2.AERday.cod.gn.v20190813
CMIP.MOHC.UKESM1-1-LL.1pctCO2.r1i1p1f2.AERmon.abs550aer.gn.v20220513
ISMIP6.NERC.UKESM1-ice-LL.1pctCO2to4x-withism.r1i1p1f2.Amon.clivi.gn.v20220316
'''.strip().split()

#data_pool_tests_db = [example_3d, example_4d]

#data_pool_tests_db = examples_rot + [example_3d, example_4d]

data_pool_tests_db = [example_3d, example_4d] + examples_rot







