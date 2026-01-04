// IMPORTANT NOTE: For authorization to work, you must set the X-Auth header.
// In Google Apps Script, the value of the X-Auth key must be set in the settings -> properties of the project.
// See readme for more details.

function fetch_products() {
  // Gets products from the database. Does not refresh database.
  // To refresh the products in the database, use request_refresh(),
  // and then call fetch_products() again.
  const server_url = "langops-ca.com/langops-dashboard/products"
  const properties = PropertiesService.getScriptProperties();
  const xAuth = properties.getProperty('X-Auth')
  const options = {
    'method': 'get',
    'headers': {
      'X-Auth': xAuth
    }
  }
  try {
    const response = UrlFetchApp.fetch(server_url, options);
    const data_array = JSON.parse(response)
    const values = data_array.map(item => [
      item.title,
      item.target_language,
      item.crowdin_url,
      item.due_by,
      item.last_activity,
      item.published,
      item.progress.translation,
      item.progress.approval
      ]);

    const headers = [[
      "Title",
      "Target Language",
      "Crowdin URL",
      "Due",
      "Last Activity",
      "Published",
      "Translation Progress",
      "Approval Progress"
    ]];

    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName("Tracker");
    
    const headersRange = sheet.getRange(23,1, 1, headers[0].length);
    headersRange.setValues(headers);

    const dataRange = sheet.getRange(24,1,values.length, headers[0].length);
    dataRange.setValues(values);
    
  }
  catch (error) {
    console.log(`Error fetching products: ${error}`);
  }
}

function request_refresh() {
  const refreshURL = "langops-ca.com/langops-dashboard/refresh"
  const properties = PropertiesService.getScriptProperties();
  const xAuth = properties.getProperty('X-Auth')
  const options = {
    'method': 'post',
    'headers': {
      'X-Auth': xAuth
    }
  }
  try {
    const request = UrlFetchApp.fetch(refreshURL, options)
    console.log(`Refresh successful: ${request}`)

  } catch (error) {
    console.log(`Error refreshing database: ${error}`)
  }
}