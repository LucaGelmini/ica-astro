import Plot from "react-plotly.js";
import { useLayoutEffect, useRef, useState } from "react";
import { useInView } from "react-intersection-observer";

const GraficoPrueba = ({ plotData }) => {
    const [width, setWidth] = useState(0);
    const [height, setHeight] = useState(0);

    const { ref, inView, entry } = useInView({ threshold: 0 });

    useLayoutEffect(() => {
        if (inView) {
            setWidth(entry.target.offsetWidth);
            setHeight(entry.target.offsetHeight);
        }
    }, [inView]);

    return (
        <div ref={ref} className={"w-full h-[500px]"}>
            <Plot
                data={plotData.data}
                layout={{ width, height, ...plotData.layout }}
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
