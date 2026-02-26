import os
import inflect

p = inflect.engine()

SERVICE_TEMPLATE = """
import { api } from "./api";

export const fetch{ModelNamePlural} = () => api.get("/{table}");
export const create{ModelName} = (data) => api.post("/{table}", data);
export const delete{ModelName} = (id) => api.delete(`/{table}/${id}`);
"""

def generate_frontend_service(model_name: str, output_dir: str):
    table = model_name.lower()
    model_name_cap = model_name.capitalize()
    model_name_plural = p.plural(model_name_cap)

    content = SERVICE_TEMPLATE.format(
        ModelName=model_name_cap,
        ModelNamePlural=model_name_plural,
        table=table
    )

    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, f"{table}.ts")
    with open(file_path, "w") as f:
        f.write(content)

    print(f"✔ Generated service: {file_path}")


def generate_all_services(app_spec: dict, frontend_root: str):
    services_dir = os.path.join(frontend_root, "src", "services")

    for model in app_spec["models"]:
        generate_frontend_service(model["name"], services_dir)
