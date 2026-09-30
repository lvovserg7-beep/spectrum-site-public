import { writeFileSync } from "node:fs";
import { fetchWordstatFrequency } from "../../../Торговля/dashboard/lib/wordstat.mjs";

const PHRASES = [
  "модуль маркетплейсов 1с",
  "модуль 1с для маркетплейсов",
  "модули маркетплейсов для 1с",
  "1с ут интеграция с маркетплейсами",
  "интеграция 1с с ozon",
  "интеграция 1с с wildberries",
  "мерлион b2b",
  "ocs b2b",
  "втт b2b",
  "интеграция 1с с поставщиками",
  "внедрение 1с комплексная автоматизация",
  "1с внедрение ка",
  "стоимость внедрения 1с erp",
  "техподдержка 1с",
  "сопровождение 1с",
  "купить лицензию 1с",
  "1с кп",
  "аллсан",
];

const out = {};
for (const p of PHRASES) {
  try {
    out[p] = (await fetchWordstatFrequency(p)).frequency;
  } catch (e) {
    out[p] = `ERR ${e.message}`;
  }
}
writeFileSync(new URL("./_wordstat-2026-09-29.json", import.meta.url), JSON.stringify(out, null, 2), "utf8");
console.log(JSON.stringify(out, null, 2));
