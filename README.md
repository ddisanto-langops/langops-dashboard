# langops-dashboard

## Goal
See in real time the progress of all files being worked on as well as deadlines, leveraging Trello and Crowdin APIs.

## Implementation
**Main endpoints:** 
- Get products: /langops-dashboard/products
- Manually refresh the databse: /langops-dashboard/refresh

**Authorization**
All endpoints for this app expect you to set 'X-Auth' header and provide the correct key.

**Overview**
- Trello is the source of truth for all products, with translation status updates from Crowdin where available.
- A local database is saved to the server, and can be manually re-created in the event of a crash.
- Basic frontend output is via Google Sheets, with options for a dedicated web UI.

## Timeframe
Ideally in production by February.

## Note on Deploying Updates
When the code is changed, especially if the database and class TranslationProduct were modified, it is necessary to: 1. delete the database on the server; 2. Run a manual refresh to populate the database.