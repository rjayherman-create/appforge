import "../styles/tokens.css";

export default function Table({ columns, data, onDelete }) {
  return (
    <table
      style={{
        width: "100%",
        borderCollapse: "collapse",
        marginBottom: "var(--space-32)",
      }}
    >
      <thead>
        <tr>
          {columns.map((col) => (
            <th
              key={col}
              style={{
                textAlign: "left",
                padding: "var(--space-12)",
                borderBottom: "1px solid #eee",
                fontSize: "var(--font-small)",
              }}
            >
              {col}
            </th>
          ))}
          <th style={{ padding: "var(--space-12)" }}>Actions</th>
        </tr>
      </thead>

      <tbody>
        {data.map((row) => (
          <tr key={row.id}>
            {columns.map((col) => (
              <td
                key={col}
                style={{
                  padding: "var(--space-12)",
                  borderBottom: "1px solid #f3f3f3",
                }}
              >
                {row[col]}
              </td>
            ))}
            <td style={{ padding: "var(--space-12)" }}>
              <button
                onClick={() => onDelete(row.id)}
                style={{
                  background: "var(--color-error)",
                  color: "white",
                  padding: "var(--space-8) var(--space-12)",
                  borderRadius: "4px",
                  border: "none",
                  cursor: "pointer",
                }}
              >
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
