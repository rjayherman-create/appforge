import { api } from "./api";

export const fetchItems = () => api.get("/items");
export const createItem = (data) => api.post("/items", data);
export const deleteItem = (id) => api.delete(`/items/${id}`);
