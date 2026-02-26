CSV_HEADERS_TO_PAGE_HEADERS = {
    account_creation_date: "Account Creation Date",
    wager_date: "Wager Date",
    wager_amount: "Wager Amount",
    total_bets_made_before_wager: "Total Bets Made Before Wager",
    total_categories_bet_on_before_wager: "Total Categories Bet On Before Wager",
    wager_outcome: "Wager Outcome",
    insider_trading_suspicion: "Insider Trading Suspicion Index"
}

DATABASE_NAME = "FAKE_DATA.csv";
MAXIMUM_ROWS_TO_DISPLAY = 8;



// As the last item will be the insider trading suspicion index
const sortCsvByLastItem = function(rows) {
    return rows.sort((a, b) => {
        const aLastItem = parseFloat(a.split(',').slice(-1)[0]);
        const bLastItem = parseFloat(b.split(',').slice(-1)[0]);
        return bLastItem - aLastItem; // Sort in descending order
    });
}

// This function adds the data to the table when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetch(DATABASE_NAME)
        .then(response => response.text())
        .then(data => {
            const rows = data.trim().split('\n');
            const headers = rows[0].split(',');
            const headerRow = document.getElementById('headerRow');
            const dataBody = document.getElementById('dataBody');


            headers.forEach(header => {
                if (CSV_HEADERS_TO_PAGE_HEADERS[header.trim()]) {
                    const th = document.createElement('th');
                    th.textContent = CSV_HEADERS_TO_PAGE_HEADERS[header.trim()] || header.trim();
                    headerRow.appendChild(th);
                }
            });

            const sortedRows = sortCsvByLastItem(rows);
            
 
            for (let i = 1; i < Math.min(sortedRows.length, MAXIMUM_ROWS_TO_DISPLAY + 1); i++) {
                const cells = sortedRows[i].split(',');
                const tr = document.createElement('tr');
                cells.forEach((cell, index) => {
                    if (CSV_HEADERS_TO_PAGE_HEADERS[headers[index].trim()]) {
                        const td = document.createElement('td');
                        td.textContent = cell.trim();
                        tr.appendChild(td);
                    }
                });
                dataBody.appendChild(tr);
            }
        });
});