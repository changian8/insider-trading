const CSV_HEADERS_TO_PAGE_HEADERS = {
  account_creation_date: 'Account Creation Date',
  wager_date: 'Wager Date',
  wager_amount: 'Wager Amount',
  total_bets_made_before_wager: 'Total Bets Made Before Wager',
  total_categories_bet_on_before_wager: 'Total Categories Bet On Before Wager',
  wager_outcome: 'Wager Outcome',
  insider_trading_suspicion: 'Insider Trading Suspicion Index',
  wager_category: 'Category',
}
const DATABASE_NAME = 'FAKE_DATA.csv'
const MAXIMUM_ROWS_TO_DISPLAY = 8
const FIRST_CATEGORY = 'Geopolitics'

/**
 * Sorts the CSV rows based on the last item in each row, in ascending order
 * This is used to sort the trades by their insider trading suspicion index,
 *  which is assumed to be the last column in the CSV file
 * 
 * @param {string[]} rows - The CSV rows to sort
 * @returns {string[]} - The sorted CSV rows
 */
const sortCsvByLastItem = function (rows) {
  return rows.sort((a, b) => {
    const aLastItem = parseFloat(a.split(',').slice(-1)[0])
    const bLastItem = parseFloat(b.split(',').slice(-1)[0])
    return bLastItem - aLastItem // Sort in descending order
  })
}

/**
 * Gets the index of the category column in the CSV file based on the header
 * 
 * @param {string[]} headers - The first row of the CSV file, split by comma
 * @returns {number} - The index of the category column, or -1 if not found
 */
const getCategoryColumnIndex = function (headers) {
  for (let i = 0; i < headers.length; i++) {
    console.log(headers[i])
    if (headers[i].trim() == 'wager_category') {
      return i
    }
  }
  return -1
}

/**
 * Checks if a row belongs to the specified category
 * Used to filter the rows so that only rows of the selected category are displayed
 * 
 * @param {string} row - The CSV row to check
 * @param {string} trueCategoryName - The category name to compare against
 * @param {number} categoryColumnIndex - The index of the category column in the CSV row
 * @returns {boolean} - True if the row belongs to the specified category, false otherwise
 */
const isRowInCategory = function (row, trueCategoryName, categoryColumnIndex) {
  const rowAsList = row.split(',')
  const actualCategoryName = rowAsList[categoryColumnIndex]
  if (actualCategoryName.trim() == trueCategoryName.trim()) {
    return true
  }
  return false
}

/** 
 * This function clears the table of all data
 * We need this when we want to load a new category of data after a button click
 * 
 * @params none 
 * @returns none
**/
const clearDataTable = function () {
  const headerRow = document.getElementById('headerRow')
  const dataBody = document.getElementById('dataBody')

  // clear the table
  for (let i = headerRow.children.length - 1; i >= 0; i--) {
    headerRow.removeChild(headerRow.children[i])
    dataBody.innerHTML = ''
  }
}

/**
 * Takes the raw CSV text and displays it in the table on the webpage
 * filtering the data as to only show a specified category
 * 
 * @param {string} csvText - The raw text of the CSV file
 * @param {string} categoryFilter - The category to filter the rows by
 */
const putDataInTable = function (csvText, categoryFilter) {
  const rows = csvText.trim().split('\n')
  // we might need a csv handler - this doesn't resolve for the "comma in string" case
  const headers = rows[0].split(',')
  const headerRow = document.getElementById('headerRow')
  const dataBody = document.getElementById('dataBody')

  const categoryColumnIndex = getCategoryColumnIndex(headers)
  console.log(categoryColumnIndex)

  headers.forEach((header) => {
    if (CSV_HEADERS_TO_PAGE_HEADERS[header.trim()]) {
      const th = document.createElement('th')
      th.textContent = CSV_HEADERS_TO_PAGE_HEADERS[header.trim()] || header.trim()
      headerRow.appendChild(th)
    }
  })

  const sortedRows = sortCsvByLastItem(rows)
  // the logic here - we want to iterate through sortedRows while respecting MAX_ROWS_TO_DISPLAY
  let rowsDisplayed = 0
  for (let i = 1; i < sortedRows.length; i++) {
    if (rowsDisplayed == MAXIMUM_ROWS_TO_DISPLAY) {
      break
    }
    if (!isRowInCategory(sortedRows[i], categoryFilter, categoryColumnIndex)) {
      continue
    }
    rowsDisplayed++
    const cells = sortedRows[i].split(',')
    const tr = document.createElement('tr')
    cells.forEach((cell, index) => {
      if (CSV_HEADERS_TO_PAGE_HEADERS[headers[index].trim()]) {
        const td = document.createElement('td')
        td.textContent = cell.trim()
        tr.appendChild(td)
      }
    })
    dataBody.appendChild(tr)
  }
}

/**
 * This function loads the data from the CSV file located in the repository 
 * and filters it by the specified category
 * 
 * @param {string} categoryFilter - The category to filter the rows by
 */
const loadData = function (categoryFilter) {
  fetch(DATABASE_NAME)
    .then(response => response.text())
    .then((data) => {
      putDataInTable(data, categoryFilter)
    })
}

// On page load, we want to load the first category of data by default
document.addEventListener('DOMContentLoaded', () => {
  loadData(FIRST_CATEGORY)
})

// Add event listeners to the filter buttons
const filterButtons = document.querySelectorAll('.filter-button')
filterButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const filter = button.getAttribute('data-filter')
    console.log(`Filter button clicked: ${filter}`)
    // get rid of active class on all buttons
    filterButtons.forEach(btn => btn.classList.remove('active'))
    // set the clicked button as active
    button.classList.add('active')

    clearDataTable()
    loadData(filter)
  })
})

module.exports = {
  sortCsvByLastItem,
  isRowInCategory,
  clearDataTable,
  putDataInTable,
  loadData,
  DATABASE_NAME,
}
