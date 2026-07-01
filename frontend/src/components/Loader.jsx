export default function Loader({ text = "Loading Climate Engine..." }) {
  return (
    <div className="loader-wrap">
      <div>
        <div className="loader-ring" />
        <p>{text}</p>
      </div>
    </div>
  );
}