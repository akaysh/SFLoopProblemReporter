from datetime import datetime, timedelta

PRE_PROD_APIKEY = ""
PROD_API_KEY = ""
TAX_YEAR = ''

TOTAL_RELEASES = ""
INSTALLER_RELEASES = ""
ENGINE_RELEASES = ""

TOTAL_RELEASES_18 = ""
INSTALLER_RELEASES_18 = ""
ENGINE_RELEASES_18 = ""



delta_4_days = 4
delta_1_day = 1
delta_2_days = 2
delta_3_days = 3

SFLoopReport = {
  "dateType": "2",
  "fromDate": "05-NOV-19",
  "offset": "1000",
  "pageNumber": 1,
  "productNames": "",
  "productReleases": TOTAL_RELEASES,
  "productVersions": "2019",
  "subproductNames": "",
  "toDate": "",
  "intuit_apikey": PROD_API_KEY
}


YOYCrashPerDayInstaller2019 = {
  "dateType": "2",
  "fromDate": "05-NOV-19",
  "offset": "1000",
  "pageNumber": 1,
  "productNames": "",
  "productReleases": INSTALLER_RELEASES,
  "productVersions": "2019",
  "subproductNames": "",
  "toDate": "30-SEP-20",
  "intuit_apikey": PROD_API_KEY
}

YOYCrashPerDayInstaller2018 = {
  "dateType": "2",
  "fromDate": "05-NOV-17",
  "offset": "100",
  "pageNumber": 1,
  "productNames": "",
  "productReleases": "0.18",
  "productVersions": "2018",
  "subproductNames": "Installer",
  "toDate": "30-SEP-18",
  "intuit_apikey": PRE_PROD_APIKEY
}

ReportSourcePerErrorCode = {
  "dateType": "2",
  "fromDate": "05-NOV-19",
  "offset": "1000",
  "pageNumber": 1,
  "productNames": "",
  "productReleases": TOTAL_RELEASES,
  "productVersions": "2019",
  "subproductNames": "",
  "toDate": "",
  "intuit_apikey": PROD_API_KEY
}

ReportSourcePerErrorCodeCustomData = {
  "customDataName": "ReportSource",
  "dateType": "2",
  "fromDate": "05-NOV-19",
  "offset": "1000",
  "pageNumber": 1,
  "productNames": "",
  "productReleases": TOTAL_RELEASES,
  "productVersions": "2019",
  "subproductNames": "",
  "intuit_apikey": PROD_API_KEY
}

fromDateInstallerDetailed = datetime.now() - timedelta(days=delta_3_days)
fromDateInstallerDetailed = fromDateInstallerDetailed.strftime('%d-%b-%y')
toDateInstallerDetailed = datetime.now()
toDateInstallerDetailed = toDateInstallerDetailed.strftime('%d-%b-%y')

InstallerDetailed = {
  "dateType": "2",
  "fromDate": fromDateInstallerDetailed,
  "offset": "1000",
  "pageNumber": 1,
  "productNames": "",
  "productReleases": INSTALLER_RELEASES,
  "productVersions": "2019",
  "subproductNames": "Installer",
  "toDate": toDateInstallerDetailed,
  "intuit_apikey": PROD_API_KEY
}


InstallerDetailedCustom = {
  "dateType": "2",
  "customDataName":"",
  "fromDate": fromDateInstallerDetailed,
  "offset": "1000",
  "pageNumber": 1,
  "productNames": "",
  "productReleases": INSTALLER_RELEASES,
  "productVersions": "2019",
  "subproductNames": "Installer",
  "toDate": toDateInstallerDetailed,
  "intuit_apikey": PROD_API_KEY
}


YoYCrashPerDay = {
  "dateType": "2",
  "fromDate": "05-NOV-19",
  "offset": "1000",
  "pageNumber": 1,
  "productNames": "",
  "productReleases": ENGINE_RELEASES,
  "productVersions": "2019",
  "subproductNames": "SmallBusiness, HomeAndBusiness, Premier, Deluxe, Basic",
  "toDate": "30-SEP-20",
  "intuit_apikey": PROD_API_KEY
}


fromDatePayloadListing = datetime.now() - timedelta(days=delta_4_days)
fromDatePayloadListing = fromDatePayloadListing.strftime('%d-%b-%y')
toDatePayloadListing = datetime.now() + timedelta(days=delta_1_day)
toDatePayloadListing = toDatePayloadListing.strftime('%d-%b-%y')

PayloadListing = {
  "dateType": "2",
  "fromDate": fromDatePayloadListing,
  "offset": "1000",
  "pageNumber": 1,
  "productNames": "",
  "productReleases": TOTAL_RELEASES,
  "productVersions": "2019",
  "subproductNames": "Installer, SmallBusiness, HomeAndBusiness, Premier, Deluxe, Basic",
  "toDate": toDatePayloadListing,
  "intuit_apikey": PROD_API_KEY
}


DiagnosticCrashReport = {
  "dateType": "2",
  "fromDate": "05-NOV-19",
  "offset": "1000",
  "pageNumber": 1,
  "productNames": "",
  "productReleases": ENGINE_RELEASES,
  "productVersions": "2019",
  "subproductNames": "Installer, SmallBusiness, HomeAndBusiness, Premier, Deluxe, Basic",
  "toDate": "",
  "intuit_apikey": PRE_PROD_APIKEY
}


DiagnosticCrashReportCustomData = {
  "customDataName": "Feature",
  "dateType": "2",
  "fromDate": "05-NOV-19",
  "offset": "1000",
  "pageNumber": 1,
  "productNames": "",
  "productVersions": "2019",
  "productReleases": ENGINE_RELEASES,
  "subproductNames": "SmallBusiness, HomeAndBusiness, Premier, Deluxe, Basic",
  "toDate": "",
  "intuit_apikey": PROD_API_KEY
}


ProblemReportsOverviewEngine = {
  "dateType": "2",
  "fromDate": "05-NOV-19",
  "offset": "1000",
  "pageNumber": 1,
  "productNames": "",
  "productReleases": ENGINE_RELEASES,
  "productVersions": "2019",
  "subproductNames": "HomeAndBusiness, Premier, Deluxe, Basic",
  "toDate": "",
  "intuit_apikey": PROD_API_KEY
}

ProblemReportsOverviewBiz = {
  "dateType": "2",
  "fromDate": "05-NOV-19",
  "offset": "1000",
  "pageNumber": 1,
  "productNames": "",
  "productReleases": ENGINE_RELEASES,
  "productVersions": "2019",
  "subproductNames": "SmallBusiness",
  "toDate": "",
  "intuit_apikey": PROD_API_KEY
}

ProblemReportsOverviewInstaller = {
  "dateType": "2",
  "fromDate": "05-NOV-19",
  "offset": "1000",
  "pageNumber": 1,
  "productNames": "",
  "productReleases": INSTALLER_RELEASES,
  "productVersions": "2019",
  "subproductNames": "Installer",
  "toDate": "",
  "intuit_apikey": PROD_API_KEY
}
