const getTableData = (tableId) => {
    console.log(tableId)
    const table = document.getElementById(tableId);
    const rows = table.rows;
    const data = [];
    const headersQuantity = rows[0].cells.length;
    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].cells;
        const rowData = [];
        let reapeatedCellsOffset = 0
        for (let j = 0; j < headersQuantity; j++) {
            try { rowData.push(cells[j].innerText); }
            catch {
                reapeatedCellsOffset++;
                rowData.push(cells[j - reapeatedCellsOffset].innerText)
            }
        }
        data.push(rowData);
    }
    return data;
}