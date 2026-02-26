const fs = require("fs");
const path = require("path");

function checkExists(p) {
  if (!fs.existsSync(p)) {
    console.error("❌ Missing:", p);
    process.exit(1);
  }
}

function checkStructure() {
  const root = process.cwd();
  const required = [
    "src",
    "src/components",
    "src/services",
    "package.json",
  ];

  required.forEach((p) => checkExists(path.join(root, p)));
  console.log("✔ Structure OK");
}

function checkBuild() {
  const { execSync } = require("child_process");
  try {
    execSync("npm run build", { stdio: "ignore" });
    console.log("✔ Build OK");
  } catch (e) {
    console.error("❌ Build failed");
    process.exit(1);
  }
}

function checkLint() {
  const { execSync } = require("child_process");
  try {
    execSync("npm run lint", { stdio: "ignore" });
    console.log("✔ Lint OK");
  } catch (e) {
    console.error("❌ Lint errors");
    process.exit(1);
  }
}

checkStructure();
checkLint();
checkBuild();

console.log("\n🎉 Frontend is clean and ready to generate apps!");
