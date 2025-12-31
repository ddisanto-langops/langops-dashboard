# langops-dashboard

## Goal
See in real time the progress of all files being worked on as well as deadlines, leveraging Trello and Crowdin APIs.

## Implementation
Trello shall be the source of truth for products, with translation status updates from Crowdin where available.
A local database is saved to the server, and can be re-created in the event of a crash.
Currently in consultation about Google Sheets output vs. a dedicated web UI.
In the spreadsheet, a button could be configured to send a simple post request to the langops server and read the database (which should refresh hourly).

## Timeframe
Ideally in production by February.
