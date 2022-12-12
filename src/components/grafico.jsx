import Plot from "react-plotly.js";
import { useLayoutEffect, useRef, useState } from "react";

const GraficoPrueba = ({ plotData }) => {
    const ref = useRef(null);

    const [width, setWidth] = useState(0);
    const [height, setHeight] = useState(0);

    useLayoutEffect(() => {
        setWidth(ref.current.offsetWidth);
        setHeight(ref.current.offsetHeight);
    }, []);

    return (
        <div ref={ref} className={"w-full h-[500px]"}>
            <Plot
                data={plotData.data}
                layout={{ ...plotData.layout, width, height }}
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
        </div>
    );
};

export default GraficoPrueba;
