import Plot from "react-plotly.js";

const GraficoPrueba = ({ plotData }) => {
    return (
        <Plot
            data={plotData.data}
            layout={plotData.layout}
            config={{
                modeBarButtonsToRemove: [
                    "pan2d",
                    "select2d",
                    "lasso2d",
                    "resetScale2d",
                    "zoomOut2d",
                ],
                displaylogo: false,
                responsive: true,
            }}
        />
    );
};

export default GraficoPrueba;
