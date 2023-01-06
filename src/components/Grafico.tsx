import { useLayoutEffect, lazy, useState, Suspense } from "react";
import { useInView } from "react-intersection-observer";
const Plot = lazy(() => import("react-plotly.js"));

type Props = {
    plotData: { data: Array<object>; layout: Array<object> };
    divClassName: string;
};

const Grafico = ({ plotData, divClassName = "w-full h-[500px]" }: Props) => {
    const [width, setWidth] = useState(0);
    const [height, setHeight] = useState(0);

    const { ref, inView, entry } = useInView({ threshold: 0 });

    useLayoutEffect(() => {
        if (inView) {
            if (entry === undefined) return;
            const t = entry.target as HTMLElement;
            setWidth(t.offsetWidth);
            setHeight(t.offsetHeight);
        }
    }, [inView]);

    return (
        <div ref={ref} className={divClassName}>
            <Suspense
                fallback={
                    <div className="bg-red-500 w-10 h-10 text-center align-middle">
                        Cargando...
                    </div>
                }
            ></Suspense>
            <Plot
                data={plotData.data}
                layout={{
                    width,
                    height,
                    margin: { l: 40, r: 0, t: 0, b: 10 },
                    //pad: { l: 0, r: 0, t: 0, b: 0 },
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
