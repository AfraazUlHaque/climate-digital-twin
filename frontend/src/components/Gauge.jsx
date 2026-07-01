import {

RadialBarChart,

RadialBar,

ResponsiveContainer

}

from "recharts";

export default function Gauge({

value,

title,

color

}){

const data=[{

name:title,

value

}];

return(

<div className="gauge-card">

<h3>

{title}

</h3>

<ResponsiveContainer

width="100%"

height={250}

>

<RadialBarChart

innerRadius="70%"

outerRadius="100%"

data={data}

startAngle={180}

endAngle={0}

>

<RadialBar

dataKey="value"

fill={color}

/>

</RadialBarChart>

</ResponsiveContainer>

<h1>

{value.toFixed(1)}%

</h1>

</div>

)

}