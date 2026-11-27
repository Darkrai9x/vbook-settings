// Checks src/*/skin.json and template/skin.json against skin.schema.json.
// Once: (cd /tmp && npm i ajv@8); then: NODE_PATH=/tmp/node_modules node skins/tools/validate_schema.js skins

const Ajv2020 = require("ajv/dist/2020"); const fs = require("fs"); const path = require("path");
const ajv = new Ajv2020({ allErrors: true, strict: false });
const dir = process.argv[2];
const validate = ajv.compile(JSON.parse(fs.readFileSync(path.join(dir, "skin.schema.json"))));
let bad = 0;
for (const f of [...fs.readdirSync(path.join(dir, "src")).map(d => path.join(dir, "src", d, "skin.json")), path.join(dir, "template", "skin.json")]) {
  if (!fs.existsSync(f)) continue;
  if (!validate(JSON.parse(fs.readFileSync(f)))) { bad++; console.log(f, JSON.stringify(validate.errors.slice(0, 3))); }
}
console.log(bad ? `${bad} invalid` : "all valid");
