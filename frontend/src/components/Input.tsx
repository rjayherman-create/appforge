import "../styles/tokens.css";

export default function Input({ label, error, ...props }) {
  return (
    <div style={{ marginBottom: "var(--space-16)" }}>
      {label && (
        <label
          style={{
            display: "block",
            marginBottom: "var(--space-8)",
            fontSize: "var(--font-small)",
          }}
        >
          {label}
        </label>
      )}

      <input
        {...props}
        style={{
          width: "100%",
          padding: "var(--space-12)",
          borderRadius: "6px",
          border: error
            ? `1px solid var(--color-error)`
            : "1px solid var(--color-secondary)",
          fontSize: "var(--font-body)",
        }}
      />

      {error && (
        <p style={{ color: "var(--color-error)", fontSize: "var(--font-caption)" }}>
          {error}
        </p>
      )}
    </div>
  );
}
