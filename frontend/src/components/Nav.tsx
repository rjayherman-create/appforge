import { Link } from "react-router-dom";

export default function Nav({ links }) {
  return (
    <nav
      style={{
        padding: "16px",
        borderBottom: "1px solid #eee",
        background: "white",
        marginBottom: "24px",
      }}
    >
      <ul
        style={{
          listStyle: "none",
          display: "flex",
          gap: "16px",
          margin: 0,
          padding: 0,
        }}
      >
        {links.map((link) => (
          <li key={link.path}>
            <Link to={link.path}>{link.label}</Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}
