# langops-dashboard

## Goal
See in real time the progress of all files being worked on as well as deadlines, leveraging Trello and Crowdin APIs.

## Overview
- Trello is the source of truth for all products, with translation status updates from Crowdin where available.
- A local database is saved to the server, and can be manually re-created in the event of a crash.
- Basic frontend output is via Google Sheets, with options for a dedicated web UI.

## Implementation
**Main endpoints:** 
- Get products: /langops-dashboard/products
- Manually refresh the databse: /langops-dashboard/refresh

## Authorization
### X-Auth
All endpoints for this app expect you to set 'X-Auth' header and provide the correct key. For the Google Sheets frontend to work, you must set 'X-Auth' in 'Script Properties' at the bottom of the project's settings. On the server, you must define X_AUTH in the app's environment variables, otherwise the request will be rejected.  

### API Keys and OAUTH
Crowdin requires a standard API Key. Trello requires three-legged OAUTH. You must generate a power-up, and use the API key, token and secret (found in the powerup's admin page).  

### Other ENV Variables  
This app is meant to work with ONE Trello board. You must define the board's ID in the app's environment variables.

## Timeframe
Ideally in production by February.

## Note on Updates and Dependencies
- When the database and/or class TranslationProduct are modified, it is necessary to: 1. delete the database on the server; 2. Run a manual refresh to populate the database.
- The tzdata package doesn't need to be imported but is a dependency of built-in zoneinfo for some systems and recommended for cross-platform compatibility. If not present, you will likely see a ZoneInfoNotFoundError.
