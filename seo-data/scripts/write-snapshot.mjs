#!/usr/bin/env node
/**
 * Запись недельного снимка из уже скачанного JSON (ответ MCP / API).
 *
 * node write-snapshot.mjs --engine yandex --from-json raw.json --date-from 2026-08-18 --date-to 2026-08-24
 */

import fs from "node:fs";
import path from "node:path";
import {
  normalizeGscQueries,
  normalizeYandexTop,
  writeWeeklySnapshot,
} from "./lib/io.mjs";

function arg(name, fallback = null) {
  const i = process.argv.indexOf(name);
  if (i === -1) return fallback;
  return process.argv[i + 1] ?? fallback;
}

function flag(name) {
  return process.argv.includes(name);
}

async function main() {
  const engine = arg("--engine", "yandex");
  const fromJson = arg("--from-json");
  const dateFrom = arg("--date-from");
  const dateTo = arg("--date-to");

  if (!fromJson || !dateFrom || !dateTo) {
    console.error(
      "Usage: node write-snapshot.mjs --engine yandex|google --from-json <file> --date-from YYYY-MM-DD --date-to YYYY-MM-DD",
    );
    process.exit(1);
  }

  const abs = path.resolve(fromJson);
  const raw = JSON.parse(fs.readFileSync(abs, "utf8"));
  const rows =
    engine === "google" ? normalizeGscQueries(raw) : normalizeYandexTop(raw);

  if (rows.length === 0) {
    console.error("No query rows found in JSON.");
    process.exit(2);
  }

  const meta = await writeWeeklySnapshot({
    engine,
    dateFrom,
    dateTo,
    rows,
    extraMeta: {
      source: "from-json",
      source_file: abs,
    },
  });

  console.log(JSON.stringify(meta, null, 2));
  if (flag("--quiet")) return;
  console.error(
    `Wrote ${meta.row_count} rows → ${meta.files.csv} + ${meta.files.parquet}`,
  );
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
