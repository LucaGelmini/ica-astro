const renderTableData = (tableData) => {
    let data = [];
    for (let col in tableData) data.push(Object.values(tableData[col]));
    data = data[0].map((col, c) => data.map((row, r) => data[r][c])); // transposed data
    console.log(data);

    return data.map((row, rowIdx) => (
        <tr
            className={`text-right ${
                rowIdx % 2 === 1 ? "bg-gray-300" : "bg-gray-100"
            } hover:bg-gray-400`}
        >
            {row.map((cell, cellIdx) => (
                <th className={cellIdx === 0 ? "text-left" : ""}>{cell}</th>
            ))}
        </tr>
    ));
};

const CuadroR2 = ({ tableData }) => {
    return (
        <table>
            <thead>
                <tr className="text-center">
                    {Object.keys(tableData).map((colName, i) => (
                        <th key={i}>{colName}</th>
                    ))}
                </tr>
            </thead>
            <tbody>{renderTableData(tableData)}</tbody>
        </table>
    );
};

export default CuadroR2;
