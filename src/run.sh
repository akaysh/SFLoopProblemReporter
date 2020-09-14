python createReports.py

mvn deploy:deploy-file -s "settings.xml" \
-Durl="http://sdgctgdevrepo.corp.intuit.net/nexus/content/repositories/ENG.CTG.Intuit-Releases/" \
-DrepositoryId="ReleaseRepository" \
-DgroupId="com.intuit.cg.SFLoopReports" \
-DartifactId="com.intuit.cg.SFLoopReports" \
-Dversion="1" \
-Dfile="TY18SFLoopInstallerDetailedReport-1.1.xlsx"


curl -v -F r=ReleaseRepository -F hasPom=false -F e=xlxs -F g=com.intuit.cg.SFLoopReports -F a=com.intuit.cg.SFLoopReports -F v=1.1 -F file=@./TY18SFLoopInstallerDetailedReport.xlxs -u wtabuild:wtabuild1 http://sdgctgdevrepo.corp.intuit.net/nexus/content/repositories/ENG.CTG.Intuit-Releases

curl -v -u wtabuild:wtabuild1 --upload-file TY18SFLoopInstallerDetailedReport-1.1.xlsx http://sdgctgdevrepo.corp.intuit.net/nexus/content/repositories/ENG.CTG.Intuit-Releases/com/intuit/cg/SFLoopReports/TY18SFLoopInstallerDetailedReport.xlxs

curl -v -u wtabuild:wtabuild1 --upload-file {TY18SFLoopInstallerDetailedReport-1.1.xlsx,TY18ProblemReports_YoYCrashPerDay_Installer.xlsx} http://sdgctgdevrepo.corp.intuit.net/nexus/content/repositories/ENG.CTG.Intuit-Releases/com/intuit/cg/SFLoopReports/1.0/

curl -i -u wtabuild:wtabuild1 -F files[]=@TY18SFLoopInstallerDetailedReport-1.1.xlsx -F files[]=@TY18ProblemReports_YoYCrashPerDay_Installer.xlsx http://sdgctgdevrepo.corp.intuit.net/nexus/content/repositories/ENG.CTG.Intuit-Releases/com/intuit/cg/SFLoopReports/1.0/

artifact upload --version 1.1 TY18SFLoopInstallerDetailedReport-1.1.xlsx ENG.CTG.Intuit-Releases com.intuit.cg.SFLoopReports



➜ cat TY18ProblemReports_YoYCrashPerDay_Installer.xlsx | md5
9ca3059bff5ddc93aa9176f3af721043
(base)
SFLoopProblemReporter/src on  master [!?] via 🅒 base
➜ cat TY18SFLoopInstallerDetailedReport.xlsx| md5
51ad9d0fe0836e2a6f2cc87dab9f0f80



cat TY18SFLoopInstallerDetailReport.xlsx| md5
cf5ec1e42ea3751086a7104d9de0b562
cat TY18ProblemReports_YoYCrashPerDay_Installer\ \(2\).xlsx | md5
9ca3059bff5ddc93aa9176f3af721043
