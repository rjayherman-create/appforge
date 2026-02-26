import "../styles/tokens.css";

export default function Card({ children }) {
  return (
    <div
      style={{
        padding: "var(--space-24)",
        borderRadius: "8px",
        background: "white",
        boxShadow: "0 2px 6px rgba(0,0,0,0.08)",
        marginBottom: "var(--space-24)",
      }}
    >
      {children}
    </div>
  );
}
