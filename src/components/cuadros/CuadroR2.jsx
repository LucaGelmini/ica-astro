// const renderTableData = (tableData) => {
//     let data = Object.values(tableData).map(Object.values); // R2 matrix
//     data = data[0].map((col, c) => data.map((row, r) => data[r][c])); // transposed data

//     return data.map((row, rowIdx) => (
//         <tr
//             className={`text-right ${
//                 rowIdx % 2 === 1 ? "bg-gray-300" : "bg-gray-100"
//             } hover:bg-gray-400`}
//         >
//             {row.map((cell, cellIdx) => (
//                 <th className={cellIdx === 0 ? "text-left" : ""}>{cell}</th>
//             ))}
//         </tr>
//     ));
// };

const CuadroR2 = ({ tableData }) => {
    const cuadroId = "R2";
    return (
        <table>
            <thead>
                <tr className="text-center">
                    {console.log(tableData.schema.fields.map((f) => f.name))}
                    {tableData.schema.fields.map((f, i) => (
                        <th key={`${cuadroId}-header-${i}`}>{f.name}</th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {tableData.data.map((r) => (
                    <tr key={`${cuadroId}-row-${r.index}`}>
                        {Object.values(r).map((c, i) => (
                            <td key={`${cuadroId}-data-${r.index}-${i}`}>
                                {c}
                            </td>
                        ))}
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default CuadroR2;
