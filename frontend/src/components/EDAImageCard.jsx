export default function EDAImageCard({ title, subtitle, image }) {
  return (
    <div className="eda-card">
      <div className="eda-card-head">
        <h3>{title}</h3>
        <p>{subtitle}</p>
      </div>

      <div className="eda-img-wrap">
        <img src={image} alt={title} />
      </div>
    </div>
  );
}