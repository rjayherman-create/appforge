import "../styles/tokens.css";

export default function FormLayout({ title, children, onSubmit }) {
  return (
    <form
      onSubmit={onSubmit}
      style={{
        maxWidth: "480px",
        margin: "0 auto",
        padding: "var(--space-32)",
        background: "white",
        borderRadius: "8px",
        boxShadow: "0 2px 6px rgba(0,0,0,0.08)",
      }}
    >
      <h2 style={{ fontSize: "var(--font-h2)", marginBottom: "var(--space-24)" }}>
        {title}
      </h2>

      {children}
    </form>
  );
}
