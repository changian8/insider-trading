const JSON_HEADERS_TO_PAGE_HEADERS = {
  price: 'Cost Per Share at Purchase',
  timestamp: 'Purchase Time',
  total_trade_value: 'Total Trade Value',
  size: 'Potential Winnings',
  user_trades_before_this_trade: 'User Trades Before This Trade',
  user_trades_after_this_trade: 'User Trades After This Trade',
  winnings: 'User Total Winnings',
  user_mean_winnings: 'User Mean Winnings',
  user_90th_percentile_winnings: 'User 90th Percentile Winnings',
  outcome: 'Winner?',
  Insider_scores: 'Insider Scores',
}

const DATA_FILTER_TO_PRICEHISTORY_CHART_FILENAME = {
  'Maduro in U.S. custody by January 31?': 'maduro_capture_pricehistory.png',
  'Will Lady Gaga perform during the Super Bowl LX halftime show?': 'halftime_guest_pricehistory.png',
  'US strikes Iran by February 28, 2026?': 'iran_strike_pricehistory.png',
}

const DATA_FILTER_TO_GOOGLE_SEARCH_CHART_FILENAME = {
  'Maduro in U.S. custody by January 31?': 'Venezuela_googlesearch.png',
  'Will Lady Gaga perform during the Super Bowl LX halftime show?': 'Superbowl_googlesearch.png',
  'US strikes Iran by February 28, 2026?': 'Iran_googlesearch.png',
}

const isDollarValueCategory = ['total_trade_value', 'winnings', 'user_mean_winnings', 'user_90th_percentile_winnings', 'size', 'price']
const DATABASE_NAME = 'trades_for_website.json'
const MAXIMUM_ROWS_TO_DISPLAY = 8
const FIRST_CATEGORY = 'Maduro in U.S. custody by January 31?'

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
 * Sorts the rows by the Insider Trading Suspicion Index
 * "High Risk" -> "Medium Risk" -> "Low Risk" -> all other strings if ISTI is a string
 * If tied, sort by the total potential winnings of the trade
 *
 * If ISTI is an integer, sort by the integer value
 *
 * @param {Object} a - The first trade object to compare
 * @param {Object} b - The second trade object to compare
 * @returns {number} - The difference between the Insider Trading Suspicion Index of the two rows
 */
const sortingByInsiderTradingSuspicionFunction = function (a, b) {
  // Helper function to determine "risk" order for string ISTI
  function getRiskOrder(isti) {
    if (typeof isti === 'string') {
      switch (isti) {
        case 'High Risk': return 0
        case 'Medium Risk': return 1
        case 'Low Risk': return 2
        default: return 3
      }
    }
    return 4
  }

  const aIsti = a['Insider_scores']
  const bIsti = b['Insider_scores']

  // If both are numbers, sort numerically (descending)
  if (typeof aIsti === 'number' && typeof bIsti === 'number') {
    if (bIsti !== aIsti) return bIsti - aIsti
    // If tied, sort by total trade value descending
    return (b['size'] || 0) - (a['size'] || 0)
  }

  // If both are strings
  if (typeof aIsti === 'string' && typeof bIsti === 'string') {
    const aOrder = getRiskOrder(aIsti)
    const bOrder = getRiskOrder(bIsti)

    if (aOrder !== bOrder) return aOrder - bOrder
    // If tied, sort by winnings descending
    return (b['size'] || 0) - (a['size'] || 0)
  }

  // If one is string and other is number, numbers first
  if (typeof aIsti === 'number' && typeof bIsti !== 'number') return 1
  if (typeof bIsti === 'number' && typeof aIsti !== 'number') return -1

  // Fallback: sort by winnings descending
  return (b['size'] || 0) - (a['size'] || 0)
}

/**
 * Converts a value to a string dollar value that makes sense for a visual display
 * Adds dollar sign, rounds to 2 decimal places, and adds a comma every 3 digits
 *
 * @param {number} value - The value to convert
 * @returns {string} - The string dollar value
 */
const toStringDollarValue = function (value) {
  if (typeof value !== 'number') return value

  const sign = value < 0 ? '-' : ''
  const absoluteValue = Math.abs(value)
  const formattedNumber = absoluteValue.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  return `${sign}$${formattedNumber}`
}

/**
 * Takes a unix timestamp and returns the date in m/d/y/h:m:s
 *
 * @param {string} unixTimestamp - The unix timestamp to convert
 * @returns {string} - The date in m/d/y/h:m:s
 */
const unixTimestampToDate = function (unixTimestamp) {
  const date = new Date(parseInt(unixTimestamp, 10) * 1000)
  return date.toLocaleDateString('en-US', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}
/**
 * Takes the JSON data and displays it in the table on the webpage,
 * filtering the data to only show the specified category.
 *
 * @param {Object[]} jsonData - The array of trade objects from the database file
 * @param {string} categoryFilter - The category to filter the rows by
 */
const putJsonDataInTable = function (jsonData, categoryFilter) {
  const headerRow = document.getElementById('headerRow')
  const dataBody = document.getElementById('dataBody')

  // Assume jsonData is an array of objects, use keys of the first object as headers
  const headers = Object.keys(JSON_HEADERS_TO_PAGE_HEADERS)

  // Render table headers
  headers.forEach((header) => {
    if (JSON_HEADERS_TO_PAGE_HEADERS[header.trim()]) {
      const th = document.createElement('th')
      th.textContent = JSON_HEADERS_TO_PAGE_HEADERS[header.trim()] || header.trim()
      headerRow.appendChild(th)
    }
  })

  // Filter rows by category and sort by "insider_trading_suspicion" property
  const filteredRows = jsonData
    .filter(row => row['title'] && row['title'].trim() === categoryFilter.trim())
    .sort((a, b) => {
      return sortingByInsiderTradingSuspicionFunction(a, b)
    })

  // Display rows up to MAXIMUM_ROWS_TO_DISPLAY
  for (let i = 0; i < Math.min(filteredRows.length, MAXIMUM_ROWS_TO_DISPLAY); i++) {
    const row = filteredRows[i]
    const tr = document.createElement('tr')

    // if outcome is Yes, add a green background to the row
    if (row['outcome'] === 'Yes') {
      tr.classList.add('winner-row')
    }
    else if (row['outcome'] === 'No') {
      tr.classList.add('loser-row')
    }

    headers.forEach((header) => {
      if (JSON_HEADERS_TO_PAGE_HEADERS[header.trim()]) {
        const td = document.createElement('td')
        if (header === 'timestamp') {
          td.textContent = unixTimestampToDate(row[header])
        }
        else {
          td.textContent = isDollarValueCategory.includes(header) ? toStringDollarValue(row[header]) : String(row[header] || '0').trim()
        }
        tr.appendChild(td)
      }
    })
    dataBody.appendChild(tr)
  }
}

/**
 * This function loads the data from the database file located in the repository
 * and filters it by the specified category.
 *
 * @param {string} categoryFilter - The category to filter the rows by
 */
const loadData = function (categoryFilter) {
  if (DATABASE_NAME.endsWith('.json')) {
    fetch(DATABASE_NAME)
      .then(response => response.json())
      .then((jsonData) => {
        putJsonDataInTable(jsonData, categoryFilter)
        displayPriceHistoryChart(categoryFilter)
      })
  }
}

/**
 * Displays the price history and google search charts for the specified category
 *
 * @param {string} categoryFilter - The category to display the charts for
 */
const displayPriceHistoryChart = function (categoryFilter) {
  const priceHistoryChart = document.getElementById('chartsContainer')
  while (priceHistoryChart.firstChild) {
    priceHistoryChart.removeChild(priceHistoryChart.firstChild)
  }

  const priceHistoryFilename = DATA_FILTER_TO_PRICEHISTORY_CHART_FILENAME[categoryFilter]
  const priceHistoryImg = document.createElement('img')
  priceHistoryImg.src = `./charts/${priceHistoryFilename}`

  const googleSearchFilename = DATA_FILTER_TO_GOOGLE_SEARCH_CHART_FILENAME[categoryFilter]
  const googleSearchImg = document.createElement('img')
  googleSearchImg.src = `./charts/${googleSearchFilename}`

  if (!priceHistoryFilename || !googleSearchFilename) {
    throw new Error('No image exists at the path for the specified category filter')
  }

  priceHistoryChart.appendChild(priceHistoryImg)
  priceHistoryChart.appendChild(googleSearchImg)
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
    filterButtons.forEach(btn => btn.classList.remove('active'))
    button.classList.add('active')

    clearDataTable()
    loadData(filter)
  })
})

module.exports = {
  sortingByInsiderTradingSuspicionFunction,
  toStringDollarValue,
  unixTimestampToDate,
  clearDataTable,
  putJsonDataInTable,
  loadData,
  displayPriceHistoryChart,
  DATABASE_NAME,
  FIRST_CATEGORY,
  DATA_FILTER_TO_GOOGLE_SEARCH_CHART_FILENAME,
  DATA_FILTER_TO_PRICEHISTORY_CHART_FILENAME,
}
