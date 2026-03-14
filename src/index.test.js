const {
  sortCsvByLastItem,
  isRowInCategory,
  clearDataTable,
  putDataInTable,
  loadData,
  DATABASE_NAME,
} = require('./index')

const TEST_CSV_NAME = 'FAKE_DATA.csv'

describe('We are using the real database in index.html', () => {
  test('DATABASE_NAME should be defined and point to a CSV file', () => {
    expect(DATABASE_NAME).toBeDefined()
    expect(DATABASE_NAME).toMatch(/\.csv$/)
  })

  test('DATABASE_NAME is not fakedata.csv', () => {
    expect(DATABASE_NAME).not.toBe('FAKE_DATA.csv')
  })
})

describe('CSV and Data Table Functions', () => {
  describe('sortCsvByLastItem', () => {
    test('should sort CSV data by last item', () => {
      fetch(TEST_CSV_NAME)
        .then(response => response.text())
        .then(data => {
          const rows = data.split('\n').slice(1) // Skip header row
          const sortedRows = sortCsvByLastItem(rows)
            const lastItems = sortedRows.map(row => row.split(',').slice(-1)[0])
            for (let i = 1; i < lastItems.length; i++) {
                expect(lastItems[i - 1]).toBeLessThanOrEqual(lastItems[i])
            }
        })
    })
  })

  describe('isRowInCategory', () => {
    test('should return true if row is in category', () => {
      // TODO: Add test implementation
    })
  })

  describe('clearDataTable', () => {
    test('should clear the data table', () => {
      // TODO: Add test implementation
    })
  })

  describe('putDataInTable', () => {
    test('should insert data into table', () => {
      // TODO: Add test implementation
    })
  })

  describe('loadData', () => {
    test('should load data correctly', () => {
      // TODO: Add test implementation
    })
  })
})
