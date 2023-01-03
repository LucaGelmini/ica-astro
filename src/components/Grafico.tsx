import { useLayoutEffect, useRef, useState } from "react";
import { useInView } from "react-intersection-observer";
import Plot from "react-plotly.js";

const Grafico = ({ plotAndTitleData, divClassName = "w-full h-[500px]" }) => {
    const {title, plot:plotData} = plotAndTitleData;

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

        <div ref={ref} className={divClassName}>
            {/* {title&&<h3 className=" font-semibold">{title}</h3>} */}
            <Plot
                data={plotData.data}
                layout={{
                    width,
                    height,
                    margin: { l: 50, r: 0, t: 0, b: 10 },
                    ...plotData.layout,
                }}
                config={{
                    modeBarButtonsToRemove: [
                        // "pan2d",
                        "select2d",
                        "lasso2d",
                        "autoScale2d",
                        // "resetScale2d",
                        //"zoom2d",
                        "zoomOut2d",
                        "zoomIn2d",
                        "toImage",
                    ],
                    displaylogo: false,
                    responsive: true,
                }}
            />
        </div>
    );
};

export default Grafico;
