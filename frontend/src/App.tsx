import { BrowserRouter } from "react-router-dom";
import Nav from "./components/Nav";
import AppRoutes from "./routes";

const links = [
  { path: "/items", label: "Items" },
  { path: "/customers", label: "Customers" }
];

export default function App() {
  return (
    <BrowserRouter>
      <Nav links={links} />
      <div className="container">
        <AppRoutes />
      </div>
    </BrowserRouter>
  );
}
