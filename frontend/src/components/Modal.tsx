import "../styles/tokens.css";

export default function Modal({ open, onClose, children }) {
  if (!open) return null;

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.4)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "var(--space-32)",
      }}
    >
      <div
        style={{
          background: "white",
          padding: "var(--space-32)",
          borderRadius: "8px",
          minWidth: "400px",
        }}
      >
        {children}

        <button
          onClick={onClose}
          style={{
            marginTop: "var(--space-24)",
            background: "var(--color-secondary)",
            color: "white",
            padding: "var(--space-12) var(--space-16)",
            borderRadius: "6px",
            border: "none",
            cursor: "pointer",
          }}
        >
          Close
        </button>
      </div>
    </div>
  );
}
