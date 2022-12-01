import fs from "fs";
import Plot from "react-plotly.js";

const GraficoPrueba = ({ plotData }) => {
    return <Plot data={plotData.data} layout={plotData.layout} />;
};

export default GraficoPrueba;
