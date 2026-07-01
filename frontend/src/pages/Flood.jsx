import {useEffect,useState} from "react";

import Loader from "../components/Loader";
import Panel from "../components/Panel";
import RiskGauge from "../components/RiskGauge";
import RegionSelector from "../components/RegionSelector";
import {apiClient} from "../api/api";

export default function Flood(){

const [region,setRegion]=useState("Kerala");

const [risk,setRisk]=useState(null);

const [loading,setLoading]=useState(true);

useEffect(()=>{

async function load(){

setLoading(true);

const res=await apiClient.flood(region);

setRisk(res.data);

setLoading(false);

}

load();

},[region]);

if(loading){

return <Loader/>

}

return(

<>

<div className="hero-row">

<div>

<h1 className="page-title">

Flood Intelligence

</h1>

<p className="subtitle">

Flood Risk Analysis

</p>

</div>

<RegionSelector

region={region}

setRegion={setRegion}

/>

</div>

<div className="two-col">

<RiskGauge

title="Flood Risk"

value={risk.score}

color="#ef4444"

/>

<Panel

title="AI Advisory"

>

<h2>

Risk Level :

{risk.level}

</h2>

<br/>

<p>

{risk.advisory}

</p>

</Panel>

</div>

</>

)

}