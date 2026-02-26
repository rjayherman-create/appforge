import os
import sys
import importlib
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent

def check_structure():
    required = [
        ROOT / "app",
        ROOT / "app" / "__init__.py",
        ROOT / "app" / "main.py",
        ROOT / "app" / "db.py",
        ROOT / "app" / "models" / "__init__.py",
        ROOT / "app" / "models" / "item.py",
        ROOT / "app" / "routes" / "__init__.py",
        ROOT / "app" / "routes" / "items.py",
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        print("❌ Missing required files:")
        for m in missing:
            print("   -", m)
        sys.exit(1)
    print("✔ Structure OK")

def check_imports():
    try:
        importlib.import_module("app.main")
        print("✔ Import OK")
    except Exception as e:
        print("❌ Import failed:", e)
        sys.exit(1)

def check_db_schema():
    try:
        from app.db import Base, engine
        Base.metadata.create_all(bind=engine)
        print("✔ DB schema OK")
    except Exception as e:
        print("❌ DB schema error:", e)
        sys.exit(1)

def check_database_file():
    db_path = ROOT / "app.db"
    if not db_path.exists():
        print("❌ Database file missing: app.db")
        sys.exit(1)
    print("✔ Database file OK")

if __name__ == "__main__":
    os.environ["PYTHONPATH"] = str(ROOT)
    check_structure()
    check_imports()
    check_db_schema()
    check_database_file()
    print("\n🎉 Backend is clean and ready to generate apps!")