import "../styles/tokens.css";

export default function Button({ children, variant = "primary", ...props }) {
  return (
    <button
      {...props}
      style={{
        padding: "var(--space-12) var(--space-16)",
        borderRadius: "6px",
        border: "none",
        cursor: "pointer",
        background:
          variant === "primary"
            ? "var(--color-primary)"
            : variant === "secondary"
            ? "var(--color-secondary)"
            : "var(--color-accent)",
        color: "white",
        fontSize: "var(--font-body)",
      }}
    >
      {children}
    </button>
  );
}
