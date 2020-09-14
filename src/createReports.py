import json
import requests
import queryParams
from datetime import datetime
import pandas as pd
import numpy as np

BASE_SFLOOP_QAL = ""
BASE_SFLOOP_PROD = ""

URL_ReportDataByErrorCode = BASE_SFLOOP_QAL + "/getReportDataByErrorCode"
URL_PROD_ReportDataByErrorCode = BASE_SFLOOP_PROD + "/getReportDataByErrorCode"

URL_ReportDataByDateRange = BASE_SFLOOP_QAL + "/getReportDataByDateRange"
URL_PROD_ReportDataByDateRange = BASE_SFLOOP_PROD + "/getReportDataByDateRange"

#/sfloopws/api/v1/getErrorCodesAndCustomData
URL_CustomDataByDateRange = BASE_SFLOOP_QAL + "/getErrorCodesAndCustomData"
URL_PROD_CustomDataByDateRange = BASE_SFLOOP_PROD + "/getErrorCodesAndCustomData"


def fetchData():

    SFLoopReport(URL_PROD_ReportDataByDateRange)
    YOYCrashPerDayInstaller(URL_PROD_ReportDataByDateRange)
    # ReportSourcePerErrorCode(URL_PROD_CustomDataByDateRange)
    # YoYCrashPerDay(URL_PROD_ReportDataByDateRange)
    # PayloadListing(URL_PROD_ReportDataByDateRange)
    InstallerDetailed(URL_PROD_ReportDataByDateRange, URL_PROD_CustomDataByDateRange)
    # ProblemReportsOverview(URL_PROD_ReportDataByDateRange)
    # DiagnosticCrashReport(URL_PROD_CustomDataByDateRange)



def SFLoopReport(url):

    print("[INFO]: SFloopReport Initiated.")
    querystring = queryParams.SFLoopReport
    page = int(querystring['pageNumber'])
    print("[INFO]: SFLoopReport API request initiated.")
    response = requests.request("GET", url, params=querystring)
    if "reportDataResponse" in response.json():
        reportDataResponse = response.json()["reportDataResponse"]
        data = pd.DataFrame.from_dict(reportDataResponse["reportData"], orient='columns')

        while True:
            pageable = reportDataResponse["pageable"]
            if page >= pageable["totalPages"]:
                break
            page = page + 1
            print("[INFO]: API Request page number - " + str(page))
            querystring['pageNumber'] = page
            response_current = requests.request("GET", url, params=querystring)
            reportDataResponse_current = response_current.json()["reportDataResponse"]
            data_current = pd.DataFrame.from_dict(reportDataResponse_current["reportData"], orient='columns')
            data = data.append(data_current, ignore_index = True)

        global report_data
        report_data = data
        print("INFO]: API Request completed. ")
        data_new = data.groupby("errorCode").agg(
        {
            "reportId": "count",
            "payloadLink": "count",
            "productRelease": [min,max],
            "subProductName": "first",
            "productProgramDirectory": "first"

        }
        ).reset_index()

        mi = data_new.columns
        ind = pd.Index([e[0] + e[1] for e in mi.tolist()])
        data_new.columns = ind
        data_new = data_new.rename(columns={
            "errorCode":"Error Code", "reportIdcount":"Reports Count", "payloadLinkcount":"Payoads Count", "productReleasemin": "First Reported Version", "productReleasemax": "Last Reported Version", "productProgramDirectoryfirst": "Product Program Directory", "subProductNamefirst":"Sub Product Name"
        })

        writer = pd.ExcelWriter(queryParams.TAX_YEAR + 'SFLoopReport.xlsx', engine='xlsxwriter')
        data_new.to_excel(writer, 'ErrorsPerCode', index=False)
        writer.save()
        print("[INFO]: SFLoopReport report written to Excel.")




def YOYCrashPerDayInstaller(url):

    print("[INFO]: YOY crash per day installer called.")

    data = report_data.loc[(report_data['productRelease'].eq(queryParams.INSTALLER_RELEASES)) & (report_data['subProductName'].eq("Installer"))].copy()
    data["receivedTimestamp"] = data.agg(
        {
            "receivedTimestamp": lambda x: "" if x==None else datetime.strptime(x.split("T")[0],'%Y-%m-%d').strftime('%m/%d/%Y')
        }
    )


    data_new = data.groupby("receivedTimestamp").agg(
    {
        "productVersion": "first",
        "reportId": "count"

    }
    ).reset_index()


    data_new = data_new.rename(columns={
        "receivedTimestamp":"Day", "productVersion":"Product Version", "reportId":"Crash Count"
    })
    data_new = data_new.sort_values(by=['Day'], ascending=False)
    writer = pd.ExcelWriter(queryParams.TAX_YEAR + 'ProblemReports_YoYCrashPerDay_Installer.xlsx', engine='xlsxwriter')
    data_new.to_excel(writer, 'YoYCrashByDay', index=False)
    writer.save()

    print("[INFO]: YOYCrashPerDayInstaller Report saved to Excel.")


def ReportSourcePerErrorCode(url):

    print("[INFO]: ReportSourcePerErrorCode called.")

    querystring = queryParams.ReportSourcePerErrorCodeCustomData
    page = int(querystring['pageNumber'])
    print("[INFO]: ReportSourcePerErrorCode API call Initiated.")

    response = requests.request("GET", url, params=querystring)
    if "customErrorDataResponse" in response.json():

        reportCustomDataResponse = response.json()["customErrorDataResponse"]

        data = pd.DataFrame.from_dict(reportCustomDataResponse["customErrorData"], orient='columns')

        while True:
            pageable = reportCustomDataResponse["pageable"]
            if page >= pageable["totalPages"]:
                break

            page = page + 1
            print("[INFO]: ReportSourcePerErrorCode Request Page - " + str(page))
            querystring['pageNumber'] = page
            response_current = requests.request("GET", url, params=querystring)
            reportDataResponse_current = response_current.json()["customErrorDataResponse"]
            data_current = pd.DataFrame.from_dict(reportDataResponse_current["customErrorData"], orient='columns')
            data = data.append(data_current, ignore_index = True)


        cols = ["errorCode", "customdatavalue"]
        data = data[cols]
        data = data.rename(columns={
            "errorCode":"Error Code", "customdatavalue":"Report Source"
        })

        writer = pd.ExcelWriter(queryParams.TAX_YEAR + 'ReportSourcePerErrorCode.xlsx', engine='xlsxwriter')
        data.to_excel(writer, 'ReportSourcePerErrorCode', index=False)
        writer.save()
        print("[INFO]: ReportSourcePerErrorCode report written to Excel.")



def InstallerDetailed(urlReport, urlCustom):
    print("[INFO]: Installer Detailed Report called.")
    querystringReport = queryParams.InstallerDetailed
    page = int(querystringReport['pageNumber'])
    print("[INFO]: Installer Detailed request (getReportDataByDateRange) initiated.")
    responseDataReport = requests.request("GET", urlReport, params=querystringReport)
    if "reportDataResponse" in responseDataReport.json():
        reportDataResponse = responseDataReport.json()["reportDataResponse"]

        data = pd.DataFrame.from_dict(reportDataResponse["reportData"], orient='columns')

        while True:
            pageable = reportDataResponse["pageable"]
            if page >= pageable["totalPages"]:
                break

            page = page + 1
            print("INFO: Request Page " + str(page))
            querystring['pageNumber'] = page
            response_current = requests.request("GET", urlReport, params=querystring)
            reportDataResponse_current = response_current.json()["reportDataResponse"]
            data_current = pd.DataFrame.from_dict(reportDataResponse_current["reportData"], orient='columns')
            data = data.append(data_current, ignore_index = True)

        print("[INFO]: Installer Detailed request (getReportDataByDateRange) completed.")
        cols = ["reportId", "message", "errorCode", "notificationEmail", "payloadLink", "productName", "productRelease", "productVersion", "receivedTimestamp", "subProductName"]
        data = data[cols]

        data["receivedTimestamp"] = data.agg(
            {
                ""
                "receivedTimestamp": lambda x: "" if x==None else datetime.strptime(x.split("T")[0],'%Y-%m-%d').strftime('%m/%d/%Y')
            }
        )

        data = data.rename(columns={
            "reportId":"Report Data.Report Id", "message":"Message", "errorCode":"Error Code", "notificationEmail":"Notification Email", "payloadLink":"Payload Link", "productName":"Product Name", "productRelease":"Product Release",  "productVersion":"Product Version", "receivedTimestamp":"Received Timestamp", "subProductName":"Sub Product Name"
        })
        # print(data)

        writer = pd.ExcelWriter(queryParams.TAX_YEAR + 'SFLoopInstallerDetailedReport.xlsx', engine='xlsxwriter')
        data.to_excel(writer, 'ErrorsPerCode', index=False)


        print("[INFO]: Installer Detailed request Errors Per Code written")

    querystringCustom = queryParams.InstallerDetailedCustom
    page = int(querystringCustom['pageNumber'])
    print("[INFO]: Installer Detailed request (getErrorCodesAndCustomData) initiated.")
    responseCustomData = requests.request("GET", urlCustom, params=querystringCustom)

    if "customErrorDataResponse" in responseCustomData.json():
        reportCustomDataResponse = responseCustomData.json()["customErrorDataResponse"]

        dataCustom = pd.DataFrame.from_dict(reportCustomDataResponse["customErrorData"], orient='columns')

        while True:
            pageable = reportDataResponse["pageable"]
            if page >= pageable["totalPages"]:
                break

            page = page + 1
            print("INFO: Request Page " + page)
            querystringCustom['pageNumber'] = page
            response_current = requests.request("GET", urlCustom, params=querystringCustom)
            reportDataResponse_current = response_current.json()["customErrorDataResponse"]
            data_current = pd.DataFrame.from_dict(reportDataResponse_current["customErrorData"], orient='columns')
            dataCustom = data.append(data_current, ignore_index = True)

        print("[INFO]: Installer Detailed request (getErrorCodesAndCustomData) completed.")
        cols = ["reportId", "customdataname", "customdatavalue"]
        dataCustom = dataCustom[cols]
        dataCustom = dataCustom.rename(columns={
            "reportId":"Custom Data.Report Id", "customdataname":"Name", "customdatavalue":"Value"
        })
        dataCustom.to_excel(writer, 'CustomData', index=False)

    saved = writer.save()
    if(saved):
        print("[INFO]: Installer Detailed Custom Data excel written")
    else:
        print("Excel save exited with : " + str(saved))

def YoYCrashPerDay(url):
    print("[INFO]: Crash per day engine called.")


    data = report_data.loc[(report_data['productRelease'].ne(queryParams.INSTALLER_RELEASES)) | (report_data['subProductName'].ne('Installer'))].copy()
    data["receivedTimestamp"] = data.agg(
        {
            ""
            "receivedTimestamp": lambda x: "" if x==None else datetime.strptime(x.split("T")[0],'%Y-%m-%d').strftime('%d-%b-%y')
        }
    )


    data_new = data.groupby("receivedTimestamp").agg(
    {
        "productVersion": "first",
        "reportId": "count"

    }
    ).reset_index()


    data_new = data_new.rename(columns={
        "receivedTimestamp":"Day", "productVersion":"Product Version", "reportId":"Crash Count"
    })

    writer = pd.ExcelWriter(queryParams.TAX_YEAR + 'ProblemReports_YoYCrashPerDay.xlsx', engine='xlsxwriter')
    data_new.to_excel(writer, 'YoYCrashByDay', index=False)
    writer.save()
    print("[INFO]: ProblemReports_YoYCrashPerDay excel report saved to disk.")




def PayloadListing(url):
    print("[INFO]: PayloadListing Report creation called.")
    querystring = queryParams.PayloadListing
    print(str(querystring["fromDate"]))
    print(str(querystring["toDate"]))
    page = int(querystring['pageNumber'])
    print("[INFO]: Payload Listing API Request Initiated.")
    response = requests.request("GET", url, params=querystring)

    if "reportDataResponse" in response.json():
        reportDataResponse = response.json()["reportDataResponse"]

        data = pd.DataFrame.from_dict(reportDataResponse["reportData"], orient='columns')

        while True:
            pageable = reportDataResponse["pageable"]
            if page >= pageable["totalPages"]:
                print(pageable["totalPages"])
                break
            print(page)
            page = page + 1
            print("[INFO]: PayloadListing Request page: " + str(page))
            querystring['pageNumber'] = page
            response_current = requests.request("GET", url, params=querystring)
            reportDataResponse_current = response_current.json()["reportDataResponse"]
            data_current = pd.DataFrame.from_dict(reportDataResponse_current["reportData"], orient='columns')
            data = data.append(data_current, ignore_index = True)
        print("[INFO]: Payload Listing API Request End.")

        data["receivedTimestamp"] = data.agg(
            {
                "receivedTimestamp": lambda x: "" if x==None else datetime.strptime(x.split("T")[0],'%Y-%m-%d').strftime('%m/%d/%Y')
            }
        )


        data["reportTimestamp"] = data.agg(
            {
                "reportTimestamp": lambda x: "" if x==None else datetime.strptime(x.split("T")[0],'%Y-%m-%d').strftime('%m/%d/%Y')

            }
        )


        data = data[["reportId", "errorCode", "productRelease", "receivedTimestamp", "reportTimestamp", "payloadLink"]]
        data = data.rename(columns={
            "reportId":"Report Id", "errorCode":"Error Code", "productRelease":"Product Release", "receivedTimestamp":"Received Timestamp", "reportTimestamp": "Report Timestamp", "payloadLink":"Payload Link"
        })
        data = data[pd.notnull(data["Payload Link"])]
        data = data.sort_values(by=["Received Timestamp"], ascending=False)

        writer = pd.ExcelWriter(queryParams.TAX_YEAR  + 'PayloadListing.xlsx', engine='xlsxwriter')
        data.to_excel(writer, 'Report 1', index=False)
        writer.save()
        print("[INFO]: PayloadListing Excel report saved to disk.")


def DiagnosticCrashReport(url):
    print("[INFO]: DiagnosticCrashReport called.")
    querystring = queryParams.DiagnosticCrashReportCustomData
    page = int(querystring["pageNumber"])
    response = requests.request("GET", url, params=querystring)
    if "customErrorDataResponse" in response.json():

        reportCustomDataResponse = response.json()["customErrorDataResponse"]

        data = pd.DataFrame.from_dict(reportCustomDataResponse["customErrorData"], orient='columns')
        print("[INFO]: DiagnosticCrashReport API request initiated.")
        while True:
            pageable = reportCustomDataResponse["pageable"]
            if page >= pageable["totalPages"]:
                break

            page = page + 1
            print("[INFO]: DiagnosticCrashReport Request page: " + str(page))
            querystring['pageNumber'] = page
            response_current = requests.request("GET", url, params=querystring)
            reportDataResponse_current = response_current.json()["customErrorDataResponse"]
            data_current = pd.DataFrame.from_dict(reportDataResponse_current["customErrorData"], orient='columns')
            data = data.append(data_current, ignore_index = True)

        print("INFO]: DiagnosticCrashReport API Request complete.")
        cols = ["errorCode", "customdataname", "customdatavalue"]
        data_diagnostic = data[cols]
        data_diagnostic = data_diagnostic.rename(columns={
            "errorCode":"Error Code", "customdataname":"Name", "customdatavalue":"Value"
        })

        writer = pd.ExcelWriter(queryParams.TAX_YEAR + 'DiagnosticCrashReport.xlsx', engine='xlsxwriter')
        data_diagnostic.to_excel(writer, 'DiagnosticCrashReport', index=False)

        features = data.customdatavalue.unique()

        data["createDate"] = data.agg(
            {
                "createDate": lambda x: "" if x==None else datetime.strptime(x.split("T")[0],'%Y-%m-%d').strftime('%m/%d/%y')

            }
        )

        data_new = data.groupby(['createDate', 'customdatavalue']).agg({"reportId":"count"}).reset_index()
        data_new = data_new.pivot_table(values='reportId', columns='customdatavalue', index='createDate')
        data_new.columns.name = None
        data_new = data_new.reset_index()
        data_new = data_new.rename(columns={
            "createDate":"Create Date (without timestamp)"
        })
        data_new = data_new.replace(np.nan, '', regex=True)

        for feature in features:
            data_feature = data_new[['Create Date (without timestamp)',feature]]
            data_feature.to_excel(writer, feature + 'Report', index=False)


        writer.save()
        print("INFO]: DiagnosticCrashReport Excel written to disk.")




def ProblemReportsOverview(url):
    print("[INFO]: ProblemReportsOverview called.")

    data = report_data.loc[(report_data['productRelease'].ne(queryParams.INSTALLER_RELEASES)) | (report_data['subProductName'].ne('Installer'))].copy()
    # Errors Per Code

    dataErrorsPerCode = data.groupby("errorCode").agg(
    {
        "reportId": "count",
        "payloadLink": "count"
    }
    ).reset_index()


    dataErrorsPerCode = dataErrorsPerCode.rename(columns={
        "errorCode":"Error Code", "reportId":"Reports Count", "payloadLink":"Payoads Count"
    })

    # print(dataErrorsPerCode.head(20))

    writer = pd.ExcelWriter(queryParams.TAX_YEAR + '_ProblemReportsOverview.xlsx', engine='xlsxwriter')
    dataErrorsPerCode.to_excel(writer, 'ErrorsPerCode',index=False)
    print("[INFO]: ProblemReportsOverview ErrorsPerCode written to excel.")



    # Errors Per Release
    dataErrorsPerRelease = data.groupby(['errorCode', 'productRelease']).agg({"reportId":"count"}).reset_index()
    dataErrorsPerRelease = dataErrorsPerRelease.pivot_table(values='reportId', columns='productRelease', index='errorCode')
    dataErrorsPerRelease.columns.name = None
    dataErrorsPerRelease = dataErrorsPerRelease.reset_index()
    dataErrorsPerRelease = dataErrorsPerRelease.replace(np.nan, '', regex=True)
    dataErrorsPerRelease.to_excel(writer, 'ErrorsPerRelease',index=False)
    print("[INFO]: ProblemReportsOverview ErrorsPerRelease written to excel.")


    # Errors Per Day
    data["receivedTimestamp"] = data.agg(
        {
            "receivedTimestamp": lambda x: "" if x==None else datetime.strptime(x.split("T")[0],'%Y-%m-%d').strftime('%d-%b-%y')
        }
    )

    dataErrorsPerDay = data.groupby("receivedTimestamp").agg(
    {
        "reportId": "count",
        "payloadLink": "count"

    }
    ).reset_index()

    dataErrorsPerDay = dataErrorsPerDay.rename(columns={
        "receivedTimestamp":"Date", "reportId":"Reports Count", "payloadLink":"Payoads Count"
    })
    dataErrorsPerDay.to_excel(writer,'ErrorsPerDay',index=False)
    print("[INFO]: ProblemReportsOverview ErrorsPerDay written to excel.")

    # Errors Per Day2

    dataErrorsPerDay2 = data.groupby(['errorCode', 'receivedTimestamp']).agg({"reportId":"count"}).reset_index()
    dataErrorsPerDay2 = dataErrorsPerDay2.pivot_table(values='reportId', columns='receivedTimestamp', index='errorCode')
    dataErrorsPerDay2.columns.name = None
    dataErrorsPerDay2 = dataErrorsPerDay2.reset_index()
    dataErrorsPerDay2 = dataErrorsPerDay2.replace(np.nan, '', regex=True)
    dataErrorsPerDay2.to_excel(writer, 'ErrorsPerDay2',index=False)
    print("[INFO]: ProblemReportsOverview ErrorsPerDay2 written to excel.")


    # Errors Per SKU

    dataErrorsPerSKU = data.groupby(['errorCode', 'subProductName']).agg({"reportId":"count", "payloadLink":"count"}).reset_index()
    dataErrorsPerSKU = dataErrorsPerSKU.pivot_table(values=['reportId', "payloadLink"], columns='subProductName', index='errorCode')
    dataErrorsPerSKU.columns.name = None
    dataErrorsPerSKU = dataErrorsPerSKU.reset_index()
    dataErrorsPerSKU = dataErrorsPerSKU.replace(np.nan, '', regex=True)
    dataErrorsPerSKU = dataErrorsPerSKU.rename(columns={
        "reportId":"Reports Count", "payloadLink":"Payoads Count"
    })
    dataErrorsPerSKU.unstack()
    dataErrorsPerSKU.to_excel(writer, 'ErrorsPerSKU')
    print("[INFO]: ProblemReportsOverview ErrorsPerSKU written to excel.")
    # print(dataErrorsPerSKU.head(20))

###############################################################
    # TTBiz OverView
###############################################################
    print("[INFO]: ProblemReportsOverview TTBiz called.")

    data = report_data.loc[report_data['subProductName'].eq('SmallBusiness')].copy()
    # Errors Per Code

    dataErrorsPerCode = data.groupby("errorCode").agg(
    {
        "reportId": "count",
        "payloadLink": "count"
    }
    ).reset_index()


    dataErrorsPerCode = dataErrorsPerCode.rename(columns={
        "errorCode":"Error Code", "reportId":"Reports Count", "payloadLink":"Payoads Count"
    })

    # print(dataErrorsPerCode.head(20))

    dataErrorsPerCode.to_excel(writer, 'ErrorsPerCode (TTBiz)',index=False)
    print("[INFO]: ProblemReportsOverview TTBiz ErrorsPerCode written to excel.")


    # Errors Per Release
    dataErrorsPerRelease = data.groupby(['errorCode', 'productRelease']).agg({"reportId":"count"}).reset_index()
    dataErrorsPerRelease = dataErrorsPerRelease.pivot_table(values='reportId', columns='productRelease', index='errorCode')
    dataErrorsPerRelease.columns.name = None
    dataErrorsPerRelease = dataErrorsPerRelease.reset_index()
    dataErrorsPerRelease = dataErrorsPerRelease.replace(np.nan, '', regex=True)
    dataErrorsPerRelease.to_excel(writer, 'ErrorsPerRelease (TTBiz)',index=False)
    # print(dataErrorsPerRelease.head(20))
    print("[INFO]: ProblemReportsOverview TTBiz ErrorsPerRelease written to excel.")

    # Errors Per Day
    data["receivedTimestamp"] = data.agg(
        {
            "receivedTimestamp": lambda x: "" if x==None else datetime.strptime(x.split("T")[0],'%Y-%m-%d').strftime('%d-%b-%y')
        }
    )

    dataErrorsPerDay = data.groupby("receivedTimestamp").agg(
    {
        "reportId": "count",
        "payloadLink": "count"

    }
    ).reset_index()

    dataErrorsPerDay = dataErrorsPerDay.rename(columns={
        "receivedTimestamp":"Date", "reportId":"Reports Count", "payloadLink":"Payoads Count"
    })
    dataErrorsPerDay.to_excel(writer,'ErrorsPerDay (TTBiz)',index=False)
    print("[INFO]: ProblemReportsOverview TTBiz ErrorsPerDay written to excel.")
    # Errors Per Day2

    dataErrorsPerDay2 = data.groupby(['errorCode', 'receivedTimestamp']).agg({"reportId":"count"}).reset_index()
    dataErrorsPerDay2 = dataErrorsPerDay2.pivot_table(values='reportId', columns='receivedTimestamp', index='errorCode')
    dataErrorsPerDay2.columns.name = None
    dataErrorsPerDay2 = dataErrorsPerDay2.reset_index()
    dataErrorsPerDay2 = dataErrorsPerDay2.replace(np.nan, '', regex=True)
    dataErrorsPerDay2.to_excel(writer, 'ErrorsPerDay2 (TTBiz)',index=False)
    print("[INFO]: ProblemReportsOverview TTBiz ErrorsPerDay2 written to excel.")

    # print(dataErrorsPerDay2.head(20))

    ###############################################################
        # Installer OverView
    ###############################################################
    print("[INFO]: ProblemReportsOverview Installer called.")


    #     # Errors Per Code
    data = report_data.loc[(report_data['subProductName'].eq('Installer')) & (report_data['productRelease'].eq(queryParams.INSTALLER_RELEASES))].copy()

    dataErrorsPerCode = data.groupby("errorCode").agg(
    {
        "reportId": "count",
        "payloadLink": "count"
    }
    ).reset_index()


    dataErrorsPerCode = dataErrorsPerCode.rename(columns={
        "errorCode":"Error Code", "reportId":"Reports Count", "payloadLink":"Payoads Count"
    })

    # print(dataErrorsPerCode.head(20))

    dataErrorsPerCode.to_excel(writer, 'ErrorsPerCode (Installer)',index=False)
    print("[INFO]: ProblemReportsOverview ErrorsPerCode written to excel.")


    # Errors Per Release
    dataErrorsPerRelease = data.groupby(['errorCode', 'productRelease']).agg({"reportId":"count"}).reset_index()
    dataErrorsPerRelease = dataErrorsPerRelease.pivot_table(values='reportId', columns='productRelease', index='errorCode')
    dataErrorsPerRelease.columns.name = None
    dataErrorsPerRelease = dataErrorsPerRelease.reset_index()
    dataErrorsPerRelease = dataErrorsPerRelease.replace(np.nan, '', regex=True)
    dataErrorsPerRelease.to_excel(writer, 'ErrorsPerRelease (Installer)',index=False)
    print("[INFO]: ProblemReportsOverview ErrorsPerRelease written to excel.")


    # Errors Per Day
    data["receivedTimestamp"] = data.agg(
        {
            "receivedTimestamp": lambda x: "" if x==None else datetime.strptime(x.split("T")[0],'%Y-%m-%d').strftime('%d-%b-%y')
        }
    )


    dataErrorsPerDay = data.groupby("receivedTimestamp").agg(
    {
        "reportId": "count",
        "payloadLink": "count"

    }
    ).reset_index()

    dataErrorsPerDay = dataErrorsPerDay.rename(columns={
        "receivedTimestamp":"Date", "reportId":"Reports Count", "payloadLink":"Payoads Count"
    })
    dataErrorsPerDay.to_excel(writer,'ErrorsPerDay (Installer)',index=False)
    print("[INFO]: ProblemReportsOverview ErrorsPerDay written to excel.")
    # Errors Per Day2

    dataErrorsPerDay2 = data.groupby(['errorCode', 'receivedTimestamp']).agg({"reportId":"count"}).reset_index()
    dataErrorsPerDay2 = dataErrorsPerDay2.pivot_table(values='reportId', columns='receivedTimestamp', index='errorCode')
    dataErrorsPerDay2.columns.name = None
    dataErrorsPerDay2 = dataErrorsPerDay2.reset_index()
    dataErrorsPerDay2 = dataErrorsPerDay2.replace(np.nan, '', regex=True)
    dataErrorsPerDay2.to_excel(writer, 'ErrorsPerDay2 (Installer)',index=False)
    print("[INFO]: ProblemReportsOverview ErrorsPerDay2 written to excel.")

    # print(dataErrorsPerDay2.head(20))


    writer.save()
    print("[INFO]: ProblemReportsOverview Excel Report written to disk.")



if __name__ == "__main__" :
    fetchData()
