import {useEffect,useState} from "react";

import Loader from "../components/Loader";
import Panel from "../components/Panel";
import RiskGauge from "../components/RiskGauge";
import RegionSelector from "../components/RegionSelector";
import {apiClient} from "../api/api";

export default function Drought(){

const [region,setRegion]=useState("Kerala");

const [risk,setRisk]=useState(null);

const [loading,setLoading]=useState(true);

useEffect(()=>{

async function load(){

setLoading(true);

const res=await apiClient.drought(region);

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

Drought Intelligence

</h1>

<p className="subtitle">

Water Stress Prediction

</p>

</div>

<RegionSelector

region={region}

setRegion={setRegion}

/>

</div>

<div className="two-col">

<RiskGauge

title="Drought Risk"

value={risk.score}

color="#f59e0b"

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