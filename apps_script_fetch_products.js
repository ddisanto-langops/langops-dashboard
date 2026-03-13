// IMPORTANT NOTE: For authorization to work, you must set the X-Auth header.
// In Google Apps Script, the value of the X-Auth key must be set in the settings -> properties of the project.
// See readme for more details.

function button() {
  // Assign to the refresh button in Google Sheets frontend
  // Synchronously refreshes the database and then fetches the products
  try {
    request_refresh();
    fetch_products();
  }
  catch (error) {
    console.log(`Error getting or displaying data: ${error}`)
  }
  
}

function fetch_products() {
  // Gets products from the database. Does not refresh database.
  // To refresh the products in the database, use request_refresh(),
  // and then call fetch_products() again.
  const endpoint = "https://products.pcglangops.com/getproducts"
  const properties = PropertiesService.getScriptProperties();
  const cfAccessId = properties.getProperty('CF-Access-Client-Id');
  const cfClientSecret = properties.getProperty('CF-Access-Client-Secret');
  const options = {
    'method': 'get',
    'headers': {
      'CF-Access-Client-Id': cfAccessId,
      'CF-Access-Client-Secret': cfClientSecret,
      'Accept': 'application/json'
    }
  }
  try {
    const response = UrlFetchApp.fetch(endpoint, options);
    const data_array = JSON.parse(response)
    const data = data_array.map(item => [
      `=HYPERLINK("${item.trello_url}", "${item.title}")`,
      item.target_language,
      item.status,
      item.crowdin_url,
      item.due_by ? new Date(item.due_by) : "",
      item.last_activity ? new Date(item.last_activity): "",
      item.published,
      item.progress.translation,
      item.progress.approval
      ]);

    const headers = [[
      "Title",
      "Target Language",
      "Product Status",
      "Crowdin URL",
      "Due",
      "Last Activity",
      "Published",
      "Translation Progress",
      "Approval Progress"
    ]];

    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName("Tracker");

    const dataRange = sheet.getRange(15,1,data.length, headers[0].length);
    dataRange.setValues(data);
    
  }
  catch (error) {
    console.log(`Error fetching products: ${error}`);
  }
}

function request_refresh() {
  const refreshEndpoint = "https://products.pcglangops.com/refresh"
  const properties = PropertiesService.getScriptProperties();
  const cfAccessId = properties.getProperty('CF-Access-Client-Id');
  const cfClientSecret = properties.getProperty('CF-Access-Client-Secret');
  const options = {
    'method': 'post',
    'headers': {
      'CF-Access-Client-Id': cfAccessId,
      'CF-Access-Client-Secret': cfClientSecret,
      'Accept': 'application/json'
    }
  }
  try {
    const request = UrlFetchApp.fetch(refreshEndpoint, options)
    console.log(`Refresh successful: ${request}`)

  } catch (error) {
    console.log(`Error refreshing database: ${error}`)
  }
}
