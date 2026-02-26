import "../styles/tokens.css";

export default function PageLayout({ title, children }) {
  return (
    <div style={{ padding: "var(--space-32)" }}>
      <h1 style={{ fontSize: "var(--font-h1)", marginBottom: "var(--space-24)" }}>
        {title}
      </h1>
      {children}
    </div>
  );
}
