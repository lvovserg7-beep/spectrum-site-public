import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { classifyCluster } from "./cluster.mjs";
import { isoWeekLabel, mondayOf } from "./week.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const SEO_DATA_ROOT = path.resolve(__dirname, "../..");

/**
 * Нормализация ответа Яндекс search_queries (report=top) или уже плоского массива.
 * @param {unknown} raw
 */
export function normalizeYandexTop(raw) {
  const obj = typeof raw === "string" ? JSON.parse(raw) : raw;
  const queries = Array.isArray(obj)
    ? obj
    : Array.isArray(obj?.queries)
      ? obj.queries
      : [];
  return queries.map((q) => {
    const shows = Number(q.TOTAL_SHOWS ?? q.shows ?? 0);
    const clicks = Number(q.TOTAL_CLICKS ?? q.clicks ?? 0);
    const avgPos = Number(
      q.AVG_SHOW_POSITION ?? q.avg_position ?? q.position ?? 0,
    );
    const query = String(q.query_text ?? q.query ?? "");
    return {
      query,
      shows,
      clicks,
      avg_position: Number.isFinite(avgPos) ? avgPos : 0,
      ctr: shows > 0 ? clicks / shows : 0,
      cluster: classifyCluster(query),
    };
  });
}

/**
 * Нормализация строк GSC get_search_analytics (dimensions=query).
 * @param {unknown} raw
 */
export function normalizeGscQueries(raw) {
  const obj = typeof raw === "string" ? JSON.parse(raw) : raw;
  const rows = Array.isArray(obj)
    ? obj
    : Array.isArray(obj?.data)
      ? obj.data
      : Array.isArray(obj?.rows)
        ? obj.rows
        : [];
  return rows.map((r) => {
    const keys = r.keys ?? r.dimensions ?? [];
    const query = String(
      r.query ?? (Array.isArray(keys) ? keys[0] : "") ?? "",
    );
    const shows = Number(r.impressions ?? r.shows ?? 0);
    const clicks = Number(r.clicks ?? 0);
    const avgPos = Number(r.position ?? r.avg_position ?? 0);
    return {
      query,
      shows,
      clicks,
      avg_position: Number.isFinite(avgPos) ? avgPos : 0,
      ctr: shows > 0 ? clicks / shows : Number(r.ctr ?? 0),
      cluster: classifyCluster(query),
    };
  });
}

function csvEscape(value) {
  const s = String(value ?? "");
  if (/[",\n\r]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
  return s;
}

/**
 * @param {object} opts
 * @param {'yandex'|'google'} opts.engine
 * @param {string} opts.dateFrom
 * @param {string} opts.dateTo
 * @param {Array<{query:string,shows:number,clicks:number,avg_position:number,ctr:number,cluster:string}>} opts.rows
 * @param {object} [opts.extraMeta]
 */
export async function writeWeeklySnapshot(opts) {
  const { engine, dateFrom, dateTo, rows, extraMeta = {} } = opts;
  if (!["yandex", "google"].includes(engine)) {
    throw new Error(`engine must be yandex|google, got ${engine}`);
  }
  const week_start = mondayOf(dateFrom);
  const week = isoWeekLabel(week_start);
  const dir = path.join(SEO_DATA_ROOT, engine);
  fs.mkdirSync(dir, { recursive: true });

  const enriched = rows
    .filter((r) => r.query)
    .map((r) => ({
      week_start,
      week,
      engine,
      date_from: dateFrom,
      date_to: dateTo,
      query: r.query,
      shows: r.shows,
      clicks: r.clicks,
      avg_position: Math.round(r.avg_position * 1000) / 1000,
      ctr: Math.round(r.ctr * 100000) / 100000,
      cluster: r.cluster || classifyCluster(r.query),
    }))
    .sort((a, b) => b.shows - a.shows || a.query.localeCompare(b.query, "ru"));

  const headers = [
    "week_start",
    "week",
    "engine",
    "date_from",
    "date_to",
    "query",
    "shows",
    "clicks",
    "avg_position",
    "ctr",
    "cluster",
  ];

  const csvPath = path.join(dir, `${week}.csv`);
  const parquetPath = path.join(dir, `${week}.parquet`);
  const metaPath = path.join(dir, `${week}.meta.json`);

  const csvBody = [
    headers.join(","),
    ...enriched.map((row) => headers.map((h) => csvEscape(row[h])).join(",")),
  ].join("\n");
  fs.writeFileSync(csvPath, `\uFEFF${csvBody}\n`, "utf8");

  await writeParquet(parquetPath, enriched);

  const totalShows = enriched.reduce((s, r) => s + r.shows, 0);
  const totalClicks = enriched.reduce((s, r) => s + r.clicks, 0);
  const meta = {
    week,
    week_start,
    engine,
    date_from: dateFrom,
    date_to: dateTo,
    pulled_at: new Date().toISOString(),
    row_count: enriched.length,
    total_shows: totalShows,
    total_clicks: totalClicks,
    ctr: totalShows > 0 ? totalClicks / totalShows : 0,
    files: {
      csv: path.relative(SEO_DATA_ROOT, csvPath).replace(/\\/g, "/"),
      parquet: path.relative(SEO_DATA_ROOT, parquetPath).replace(/\\/g, "/"),
    },
    ...extraMeta,
  };
  fs.writeFileSync(metaPath, JSON.stringify(meta, null, 2), "utf8");

  return meta;
}

async function writeParquet(parquetPath, rows) {
  const arrow = await import("apache-arrow");
  const parquet = await import("parquet-wasm");

  // Node entry does not need wasmInit; ESM would.
  const { Table, writeParquet: wasmWrite, WriterPropertiesBuilder, Compression } =
    parquet;

  const table = arrow.tableFromArrays({
    week_start: rows.map((r) => r.week_start),
    week: rows.map((r) => r.week),
    engine: rows.map((r) => r.engine),
    date_from: rows.map((r) => r.date_from),
    date_to: rows.map((r) => r.date_to),
    query: rows.map((r) => r.query),
    shows: Int32Array.from(rows.map((r) => r.shows)),
    clicks: Int32Array.from(rows.map((r) => r.clicks)),
    avg_position: Float64Array.from(rows.map((r) => r.avg_position)),
    ctr: Float64Array.from(rows.map((r) => r.ctr)),
    cluster: rows.map((r) => r.cluster),
  });

  const wasmTable = Table.fromIPCStream(arrow.tableToIPC(table, "stream"));
  const props = new WriterPropertiesBuilder()
    .setCompression(Compression.ZSTD)
    .build();
  const parquetBytes = wasmWrite(wasmTable, props);
  fs.writeFileSync(parquetPath, Buffer.from(parquetBytes));
}
