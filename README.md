# langops-dashboard

## Goal
See in real time the progress of all files being worked on as well as deadlines, leveraging Trello and Crowdin APIs.

## Implementation
Trello shall be the source of truth for products, and real-time info can come from Crowdin.  
In the spreadsheet, a button could be configured to send a simple post request to the langops server; otherwise, an hourly refresh will be the standard.  
Output data will be pushed to Google Sheets for further evaluation.

## Timeframe
Ideally in production by February.
