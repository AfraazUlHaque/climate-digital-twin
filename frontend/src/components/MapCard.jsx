import {

MapContainer,

TileLayer,

CircleMarker,

Popup

}

from "react-leaflet";

import "leaflet/dist/leaflet.css";

function markerColor(score){

if(score>=70){

return "#ef4444";

}

if(score>=40){

return "#f59e0b";

}

return "#10b981";

}

export default function MapCard({

points=[]

}){

return(

<div

style={{

height:"650px",

borderRadius:"20px",

overflow:"hidden"

}}

>

<MapContainer

center={[10.5,77.4]}

zoom={7}

style={{

height:"100%",

width:"100%"

}}

>

<TileLayer

url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"

/>

{

points.map((p,index)=>(

<CircleMarker

key={index}

center={[

p.lat,

p.lon

]}

radius={9}

fillOpacity={0.9}

color={markerColor(

p.flood_risk_index

)}

>

<Popup>

<h3>

{p.region}

</h3>

<hr/>

<p>

<b>T+1 :</b>

{p.predicted_t1}

mm

</p>

<p>

<b>T+3 :</b>

{p.predicted_t3}

mm

</p>

<p>

<b>T+7 :</b>

{p.predicted_t7}

mm

</p>

<p>

<b>Flood :</b>

{p.flood_risk_index}%

</p>

<p>

<b>Drought :</b>

{p.drought_risk_index}%

</p>

</Popup>

</CircleMarker>

))

}

</MapContainer>

</div>

)

}