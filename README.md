# SFLoopProblemReporter

Problem Reporter Report Generator for TurboTax Desktop.

The code runs everyday at 6 a.m. IST as a Circle CI build job. It pulls the SFLoop Crash Data using APIs and create Excel Reports which are then uploaded to Nexus repository. These reports can be used to get a high level view and triaging of the trending crashes.

### New Nexus Link for the SFLoop Reports

[SFLoop Reports](http://sdgctgdevrepo.corp.intuit.net/nexus/content/repositories/ENG.CTG.Intuit-Releases/com/intuit/cg/SFLoopReports/)

### Circle CI Job for creating and uploading the reports

[Circle CI Cron Job - Runs everyday at 6 a.m. IST](https://circle.circleci.sbg.intuit.com/gh/TurboTaxDesktop/SFLoopProblemReporter)

### Docker Image

[Docker Image](https://github.com/akaysh/my-docker)
