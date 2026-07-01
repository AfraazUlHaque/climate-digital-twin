export default function StatusCard({

title,

status

}){

return(

<div className="status-card">

<div>

<h4>

{title}

</h4>

</div>

<div>

{

status

?

<span className="green">

● Online

</span>

:

<span className="red">

● Offline

</span>

}

</div>

</div>

)

}