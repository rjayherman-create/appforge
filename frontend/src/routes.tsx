import { Routes, Route } from "react-router-dom";
import ItemList from "./pages/ItemList";
import CreateItem from "./pages/CreateItem";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/items" element={<ItemList />} />
      <Route path="/items/create" element={<CreateItem />} />
    </Routes>
  );
}
