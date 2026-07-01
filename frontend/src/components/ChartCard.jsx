import Panel from "./Panel";

import {

ResponsiveContainer,

LineChart,

Line,

XAxis,

YAxis,

CartesianGrid,

Tooltip,

Legend

}

from "recharts";

export default function ChartCard({

title,

data,

x,

lines

}){

return(

<Panel title={title}>

<ResponsiveContainer

width="100%"

height={350}

>

<LineChart data={data}>

<CartesianGrid strokeDasharray="3 3"/>

<XAxis dataKey={x}/>

<YAxis/>

<Tooltip/>

<Legend/>

{

lines.map(line=>

<Line

key={line.dataKey}

type="monotone"

stroke={line.color}

strokeWidth={3}

dataKey={line.dataKey}

/>

)

}

</LineChart>

</ResponsiveContainer>

</Panel>

)

}