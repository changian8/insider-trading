const { 
  sortingByInsiderTradingSuspicionFunction,
  toStringDollarValue,
  clearDataTable,
  putJsonDataInTable,
  loadData,
  DATABASE_NAME 
} = require('./index.js')


/**
 * Tests the following cases for the sortingByInsiderTradingSuspicionFunction function:
 * 
 * ISTI are all strings - High Risk -> Medium Risk -> Low Risk -> all other strings if ISTI is a string
 * potential winnings serve as a tiebreaker if the string value is the same
 * ISTI are all numbers - descending order
 * ISTI are a mix of strings and numbers - strings first, then numbers if ISTI is a string
 * ISTI does not exist - sort by potential winnings descending
 * ISTI and potential winnings do not exist - return the same order
 */
describe('sortingByInsiderTradingSuspicionFunction', () => {
  it('should sort rows by Insider Trading Suspicion Index', () => {
    const rows = [
      { Insider_scores: 'High Risk', size: 100 },
      { Insider_scores: 'Medium Risk', size: 200 },
      { Insider_scores: 'Low Risk', size: 300 },
      { Insider_scores: 'not a string we have defined', size: 200 },
    ]
    const sortedRows = rows.sort(sortingByInsiderTradingSuspicionFunction)
    expect(sortedRows).toEqual([
      { Insider_scores: 'High Risk', size: 100 },
      { Insider_scores: 'Medium Risk', size: 200 },
      { Insider_scores: 'Low Risk', size: 300 },
      { Insider_scores: 'not a string we have defined', size: 200 },
    ])
  })

  it('potential winnings serve as a tiebreaker if the string value is the same', () => {
    const rows = [
      { Insider_scores: 'High Risk', size: 100 },
      { Insider_scores: 'High Risk', size: 200 },
    ]
    const sortedRows = rows.sort(sortingByInsiderTradingSuspicionFunction)
    expect(sortedRows).toEqual([
      { Insider_scores: 'High Risk', size: 200 },
      { Insider_scores: 'High Risk', size: 100 },
    ])
  })

  it('ISTI are all numbers - descending order', () => {
    const rows = [
      { Insider_scores: 100, size: 100 },
      { Insider_scores: 200, size: 200 },
    ]
    const sortedRows = rows.sort(sortingByInsiderTradingSuspicionFunction)
    expect(sortedRows).toEqual([
      { Insider_scores: 200, size: 200 },
      { Insider_scores: 100, size: 100 },
    ])
  })

  it('ISTI are a mix of strings and numbers - strings first, then numbers if ISTI is a string', () => {
    const rows = [
      { Insider_scores: 'High Risk', size: 100 },
      { Insider_scores: 200, size: 200 },
    ]
    const sortedRows = rows.sort(sortingByInsiderTradingSuspicionFunction)
    expect(sortedRows).toEqual([
      { Insider_scores: 'High Risk', size: 100 },
      { Insider_scores: 200, size: 200 },
    ])
  })

  it('ISTI does not exist - sort by winnings descending', () => {
    const rows = [
      { size: 100 },
      { size: 200 },
    ]
    const sortedRows = rows.sort(sortingByInsiderTradingSuspicionFunction)
    expect(sortedRows).toEqual([
      { size: 200 },
      { size: 100 },
    ])
  })

  it('ISTI and total_trade_value do not exist - return the same order', () => {
    const rows = [
      { someOtherKey: 'this goes first' },
      { someOtherKey: 'this goes second' },
    ]
    const sortedRows = rows.sort(sortingByInsiderTradingSuspicionFunction)
    expect(sortedRows).toEqual([
      { someOtherKey: 'this goes first' },
      { someOtherKey: 'this goes second' },
    ])
  })
})

/**
 * Tests the following cases for the toStringDollarValue function:

 * Positive numbers - add dollar sign, round to 2 decimal places, add comma every 3 digits
 * Negative numbers - add dollar sign, round to 2 decimal places, add comma every 3 digits
 * 0 - return $0.00
 * any number less than one - return $0.[the number with 2 decimal places]
 * any number betweeen zero and negative one - return -$0.[the number with 2 decimal places]
 * No number - send back that same string
 */
describe('toStringDollarValue', () => {
  it('should convert a positive number to a string dollar value', () => {
    const value = 1000.123456789
    const expected = '$1,000.12'
    const result = toStringDollarValue(value)
    expect(result).toEqual(expected)
  })
  it('should convert a negative number to a string dollar value', () => {
    const value = -1000.123456789
    const expected = '-$1,000.12'
    const result = toStringDollarValue(value)
    expect(result).toEqual(expected)
  })
  it('should convert a 0 to a string dollar value', () => {
    const value = 0
    const expected = '$0.00'
    const result = toStringDollarValue(value)
    expect(result).toEqual(expected)
  })
  it('should convert a number less than one to a string dollar value', () => {
    const value = 0.123456789
    const expected = '$0.12'
    const result = toStringDollarValue(value)
    expect(result).toEqual(expected)
  })
  it('should convert a number between zero and negative one to a string dollar value', () => {
    const value = -0.123456789
    const expected = '-$0.12'
    const result = toStringDollarValue(value)
    expect(result).toEqual(expected)
  })
  it('should send back the same string if no number is provided', () => {
    const value = 'not a number'
    const expected = 'not a number'
    const result = toStringDollarValue(value)
    expect(result).toEqual(expected)
  })
})

/**
 * Makes sure we are sending the real data (JSON) and not the fake data (CSV)
 */
describe('DATABASE_NAME', () => {
  it('should be a JSON and not a CSV', () => {
    expect(DATABASE_NAME).toMatch(/\.json$/)
    expect(DATABASE_NAME).not.toMatch(/\.csv$/)
  })
})

/**
 * Makes sure there is a valid path for each value for the chart filename dictionaries
 */
describe('DATA_FILTER_TO_PRICEHISTORY_CHART_FILENAME', () => {
  it('should be a dictionary with valid paths for each value', () => {
    expect(DATA_FILTER_TO_PRICEHISTORY_CHART_FILENAME).toBeDefined()
    expect(DATA_FILTER_TO_GOOGLE_SEARCH_CHART_FILENAME).toBeDefined()
    for (const key in DATA_FILTER_TO_PRICEHISTORY_CHART_FILENAME) {
      expect(DATA_FILTER_TO_PRICEHISTORY_CHART_FILENAME[key]).toBeDefined()
      expect(DATA_FILTER_TO_GOOGLE_SEARCH_CHART_FILENAME[key]).toBeDefined()
    }
  })
})

