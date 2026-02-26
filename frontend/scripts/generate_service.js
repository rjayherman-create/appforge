const fs = require("fs");
const path = require("path");

const MODELS = ["item"]; // Add more model names as needed
const SERVICES_DIR = path.join(__dirname, "..", "src", "services");

MODELS.forEach((model) => {
  const capModel = model.charAt(0).toUpperCase() + model.slice(1);
  const plural = model.endsWith("s") ? model + "es" : model + "s";
  const fileContent = `import { api } from "./api";

export const fetch${capModel}s = () => api.get("/${plural}");
export const create${capModel} = (data) => api.post("/${plural}", data);
export const delete${capModel} = (id) => api.delete(\`/${plural}/\${id}\`);
`;
  fs.writeFileSync(path.join(SERVICES_DIR, `${model}.ts`), fileContent);
  console.log(`✔ Generated service: ${model}.ts`);
});
