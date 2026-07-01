export default function EmptyState({ title = "No data available", message = "Try changing filters." }) {
  return (
    <div className="empty-state">
      <h3>{title}</h3>
      <p>{message}</p>
    </div>
  );
}