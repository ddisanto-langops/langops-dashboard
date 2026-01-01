function fetch_products() {
  // Gets products from the database. Does not refresh database.
  // To refresh the products in the database, use request_refresh(),
  // and then call fetch_products() again.
  const server_url = "langops-ca.com/langops-dashboard/products"
  try {
    const response = UrlFetchApp.fetch(server_url);
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
  const options = {'method': 'post'}
  try {
    const request = UrlFetchApp.fetch(refreshURL, options)
    console.log(`Refresh successful: ${request}`)

  } catch (error) {
    console.log(`Error refreshing database: ${error}`)
  }
}