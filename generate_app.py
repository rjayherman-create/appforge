    name = model["name"]
    ModelName = pascal(name)
    table = snake(name)

    field_lines = []
    for f in model["fields"]:
        if f["name"] in ["id", "created_at", "updated_at"]:
            continue
        zod_type = {
            "string": "z.string()",
            "float": "z.number()",
            "int": "z.number()",
            "boolean": "z.boolean()",
        }.get(f["type"], "z.string()")
        if f.get("required", False):
            field_lines.append(f'  {f["name"]}: {zod_type},')
        else:
            field_lines.append(f'  {f["name"]}: {zod_type}.optional(),')

    content = ZOD_TEMPLATE.format(
        ModelName=ModelName,
        fields="\n".join(field_lines),
    )

    validation_dir = FRONTEND / "src" / "validation"
    validation_dir.mkdir(parents=True, exist_ok=True)
    (validation_dir / f"{table}.ts").write_text(content, encoding="utf-8")
    print(f"✔ Zod schema: {table}.ts")
TYPE_TEMPLATE = """export interface {ModelName} {{\n  id: number;\n  created_at: string;\n  updated_at: string;\n{fields}\n}}\n"""

def ts_type(field_type: str) -> str:
    mapping = {
        "string": "string",
        "float": "number",
        "int": "number",
        "boolean": "boolean",
    }
    return mapping.get(field_type, "string")

def generate_typescript_type(model: dict):
    name = model["name"]
    ModelName = pascal(name)

    field_lines = []
    for f in model["fields"]:
        if f["name"] in ["id", "created_at", "updated_at"]:
            continue
        field_lines.append(f"  {f['name']}: {ts_type(f['type'])};")

    content = TYPE_TEMPLATE.format(
        ModelName=ModelName,
        fields="\n".join(field_lines)
    )

    types_dir = FRONTEND / "src" / "types"
    types_dir.mkdir(parents=True, exist_ok=True)
    (types_dir / f"{snake(name)}.ts").write_text(content, encoding="utf-8")

    print(f"✔ Type: {snake(name)}.ts")
import json
import os
import inflect
from pathlib import Path

p = inflect.engine()

ROOT = Path(__file__).resolve().parent
BACKEND_APP = ROOT / "backend" / "app"
FRONTEND = ROOT / "frontend"

# ---------- Helpers ----------
def snake(name: str) -> str:
    return name.lower()

def pascal(name: str) -> str:
    return name[0].upper() + name[1:]

# ---------- 1) Model generator ----------
MODEL_TEMPLATE = """from sqlalchemy import Column, String, Integer, Float, Boolean
from app.db import Base
from app.models.base_model import BaseModel

class {ModelName}(Base, BaseModel):
    __tablename__ = "{table}"

{fields}
"""

FIELD_TEMPLATE = "    {name} = Column({type}, nullable={nullable})"

def sql_type(field_type: str) -> str:
    mapping = {
        "string": "String",
        "float": "Float",
        "int": "Integer",
        "boolean": "Boolean",
    }
    return mapping.get(field_type, "String")

def generate_model(model: dict):
    name = model["name"]
    table = snake(name)
    fields_src = []
    for f in model["fields"]:
        if f["name"] in ["id", "created_at", "updated_at"]:
            continue
        fields_src.append(
            FIELD_TEMPLATE.format(
                name=f["name"],
                type=sql_type(f["type"]),
                nullable=str(not f.get("required", False)),
            )
        )
    content = MODEL_TEMPLATE.format(
        ModelName=pascal(name),
        table=table,
        fields="\n".join(fields_src),
    )
    models_dir = BACKEND_APP / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    (models_dir / f"{table}.py").write_text(content, encoding="utf-8")
    print(f"✔ Model: {table}.py")

# ---------- 2) CRUD generator ----------
CRUD_TEMPLATE = """from sqlalchemy.orm import Session
from app.models.{table} import {ModelName}

def get_{table_plural}(db: Session):
    return db.query({ModelName}).all()

def get_{table}(db: Session, id: int):
    return db.query({ModelName}).filter({ModelName}.id == id).first()

def create_{table}(db: Session, data: dict):
    obj = {ModelName}(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def delete_{table}(db: Session, id: int):
    obj = get_{table}(db, id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj
"""

def generate_crud(model: dict):
    name = model["name"]
    table = snake(name)
    table_plural = p.plural(table)
    content = CRUD_TEMPLATE.format(
        table=table,
        table_plural=table_plural,
        ModelName=pascal(name),
    )
    crud_dir = BACKEND_APP / "crud"
    crud_dir.mkdir(parents=True, exist_ok=True)
    (crud_dir / f"{table}_crud.py").write_text(content, encoding="utf-8")
    print(f"✔ CRUD: {table}_crud.py")

# ---------- 3) Route generator ----------
ROUTE_TEMPLATE = """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud.{table}_crud import (
    get_{table_plural},
    create_{table},
    delete_{table},
)

router = APIRouter(prefix="/{table}", tags=["{ModelName}"])

@router.get("/")
def list_{table_plural}(db: Session = Depends(get_db)):
    return get_{table_plural}(db)

@router.post("/")
def add_{table}(data: dict, db: Session = Depends(get_db)):
    return create_{table}(db, data)

@router.delete("/{id}")
def remove_{table}(id: int, db: Session = Depends(get_db)):
    return delete_{table}(db, id)
"""

def generate_route(model: dict):
    name = model["name"]
    table = snake(name)
    table_plural = p.plural(table)
    content = ROUTE_TEMPLATE.format(
        table=table,
        table_plural=table_plural,
        ModelName=pascal(name),
    )
    routes_dir = BACKEND_APP / "routes"
    routes_dir.mkdir(parents=True, exist_ok=True)
    (routes_dir / f"{table}.py").write_text(content, encoding="utf-8")
    print(f"✔ Route: {table}.py")

# ---------- 4) Frontend service generator ----------
SERVICE_TEMPLATE = """import { api } from "./api";

export const fetch{ModelNamePlural} = () => api.get("/{table}");
export const create{ModelName} = (data) => api.post("/{table}", data);
export const delete{ModelName} = (id) => api.delete(`/{table}/${id}`);
"""

def generate_frontend_service(model: dict):
    name = model["name"]
    table = snake(name)
    ModelName = pascal(name)
    ModelNamePlural = p.plural(ModelName)
    content = SERVICE_TEMPLATE.format(
        ModelName=ModelName,
        ModelNamePlural=ModelNamePlural,
        table=table,
    )
    services_dir = FRONTEND / "src" / "services"
    services_dir.mkdir(parents=True, exist_ok=True)
    (services_dir / f"{table}.ts").write_text(content, encoding="utf-8")
    print(f"✔ Service: {table}.ts")

# ---------- 5) UI generator (simple list page) ----------
LIST_PAGE_TEMPLATE = """import { useEffect, useState } from \"react\";
import { fetch{ModelNamePlural}, delete{ModelName} } from \"../services/{table}\";

export default function {ModelName}List() {{
  const [items, setItems] = useState([]);

  useEffect(() => {{
    fetch{ModelNamePlural}().then(res => setItems(res.data));
  }}, []);

  const handleDelete = async (id: number) => {{
    await delete{ModelName}(id);
    setItems(items.filter(i => i.id !== id));
  }};

  return (
    <div>
      <h1>{ModelNamePlural}</h1>
      <table>
        <thead>
          <tr>
{headers}
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {{items.map((i: any) => (
            <tr key={i.id}>
{cells}
              <td>
                <button onClick={() => handleDelete(i.id)}>Delete</button>
              </td>
            </tr>
          ))}}
        </tbody>
      </table>
    </div>
  );
}}
"""

def generate_ui_list_page(model: dict):
    name = model["name"]
    table = snake(name)
    ModelName = pascal(name)
    ModelNamePlural = p.plural(ModelName)
    headers = []
    cells = []
    for f in model["fields"]:
        if f["name"] in ["id", "created_at", "updated_at"]:
            continue
        headers.append(f'            <th>{f["name"]}</th>')
        cells.append(f'              <td>{{i.{f["name"]}}}</td>')
    content = LIST_PAGE_TEMPLATE.format(
        ModelName=ModelName,
        ModelNamePlural=ModelNamePlural,
        table=table,
        headers="\n".join(headers),
        cells="\n".join(cells),
    )
    pages_dir = FRONTEND / "src" / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    (pages_dir / f"{ModelName}List.tsx").write_text(content, encoding="utf-8")
    print(f"✔ UI page: {ModelName}List.tsx")

# ---------- 6) Main generator entry ----------
def generate_app(spec_path: str):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    for model in spec["models"]:
        generate_model(model)
        generate_crud(model)
        generate_route(model)
        generate_frontend_service(model)
        generate_ui_list_page(model)
        generate_typescript_type(model)
        generate_zod_schema(model)
        generate_create_form(model)
        generate_edit_form(model)
        generate_table_component(model)

    update_navigation_and_routes(spec)
    print("\n🎉 App generation complete.")
def update_navigation_and_routes(app_spec):
    pages_dir = FRONTEND / "src" / "pages"
    routes_file = FRONTEND / "src" / "routes.tsx"
    app_file = FRONTEND / "src" / "App.tsx"

    imports = []
    routes = []
    nav_links = []

    for model in app_spec["models"]:
        name = model["name"]
        ModelName = pascal(name)
        table = snake(name)

        imports.append(f'import {ModelName}List from "./pages/{ModelName}List";')
        routes.append(f'<Route path="/{table}" element={{<{ModelName}List />}} />')
        nav_links.append(f'{{ path: "/{table}", label: "{ModelName}s" }}')

    routes_file.write_text(
        f"""import {{ Routes, Route }} from \"react-router-dom\";\n"
        + "\n".join(imports)
        + "\n\nexport default function AppRoutes() {\n  return (\n    <Routes>\n      "
        + "\n      ".join(routes)
        + "\n    </Routes>\n  );\n}\n",
        encoding="utf-8",
    )

    app_file.write_text(
        f"""import {{ BrowserRouter }} from \"react-router-dom\";\nimport Nav from \"./components/Nav\";\nimport AppRoutes from \"./routes\";\n\nconst links = [\n  "
        + "\n  ".join(nav_links)
        + "\n];\n\nexport default function App() {\n  return (\n    <BrowserRouter>\n      <Nav links={{links}} />\n      <div style={{ padding: \"1rem\" }}>\n        <AppRoutes />\n      </div>\n    </BrowserRouter>\n  );\n}\n",
        encoding="utf-8",
    )

    print("✔ Navigation + routing updated")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python generate_app.py app_spec.json")
        sys.exit(1)
    generate_app(sys.argv[1])
