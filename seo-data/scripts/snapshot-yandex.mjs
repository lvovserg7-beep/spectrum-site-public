#!/usr/bin/env node
/**
 * Прямая выгрузка топ-запросов Яндекс.Вебмастера за период → CSV + Parquet.
 *
 * Env:
 *   YANDEX_WEBMASTER_TOKEN   OAuth token
 *   YANDEX_WEBMASTER_HOST_ID default https:alsn.ru:443
 *   YANDEX_WEBMASTER_USER_ID optional; иначе берётся из /user
 *
 * node snapshot-yandex.mjs --date-from 2026-08-18 --date-to 2026-08-24
 * node snapshot-yandex.mjs --last-week
 */

import {
  normalizeYandexTop,
  writeWeeklySnapshot,
} from "./lib/io.mjs";
import { mondayOf } from "./lib/week.mjs";

const API = "https://api.webmaster.yandex.net/v4";

function arg(name, fallback = null) {
  const i = process.argv.indexOf(name);
  if (i === -1) return fallback;
  return process.argv[i + 1] ?? fallback;
}

function flag(name) {
  return process.argv.includes(name);
}

function ymd(d) {
  return d.toISOString().slice(0, 10);
}

/** Прошлая полная ISO-неделя (пн–вс). */
function lastFullWeek() {
  const today = new Date();
  const utc = new Date(
    Date.UTC(today.getFullYear(), today.getMonth(), today.getDate()),
  );
  const thisMonday = new Date(mondayOf(ymd(utc)) + "T00:00:00Z");
  const lastMonday = new Date(thisMonday);
  lastMonday.setUTCDate(thisMonday.getUTCDate() - 7);
  const lastSunday = new Date(lastMonday);
  lastSunday.setUTCDate(lastMonday.getUTCDate() + 6);
  return { dateFrom: ymd(lastMonday), dateTo: ymd(lastSunday) };
}

async function apiGet(token, urlPath) {
  const res = await fetch(`${API}${urlPath}`, {
    headers: { Authorization: `OAuth ${token}` },
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Yandex API ${res.status} ${urlPath}: ${body}`);
  }
  return res.json();
}

async function fetchAllQueries(token, userId, hostId, dateFrom, dateTo) {
  const limit = 500;
  let offset = 0;
  const all = [];
  // eslint-disable-next-line no-constant-condition
  while (true) {
    const qs = new URLSearchParams({
      date_from: dateFrom,
      date_to: dateTo,
      order_by: "TOTAL_SHOWS",
      limit: String(limit),
      offset: String(offset),
    });
    const data = await apiGet(
      token,
      `/user/${userId}/hosts/${encodeURIComponent(hostId)}/search-queries/popular?${qs}`,
    );
    const batch = data.queries ?? data ?? [];
    if (!Array.isArray(batch) || batch.length === 0) break;
    all.push(...batch);
    if (batch.length < limit) break;
    offset += limit;
  }
  return { queries: all };
}

async function main() {
  const token = process.env.YANDEX_WEBMASTER_TOKEN;
  if (!token) {
    console.error(
      "Set YANDEX_WEBMASTER_TOKEN (OAuth). Or use write-snapshot.mjs --from-json with MCP dump.",
    );
    process.exit(1);
  }

  let dateFrom = arg("--date-from");
  let dateTo = arg("--date-to");
  if (flag("--last-week") || (!dateFrom && !dateTo)) {
    ({ dateFrom, dateTo } = lastFullWeek());
  }
  if (!dateFrom || !dateTo) {
    console.error("Need --date-from/--date-to or --last-week");
    process.exit(1);
  }

  const hostId =
    arg("--host-id") ||
    process.env.YANDEX_WEBMASTER_HOST_ID ||
    "https:alsn.ru:443";

  let userId = process.env.YANDEX_WEBMASTER_USER_ID;
  if (!userId) {
    const user = await apiGet(token, "/user");
    userId = String(user.user_id ?? user.id);
  }

  console.error(`Fetching ${hostId} ${dateFrom}…${dateTo} …`);
  const raw = await fetchAllQueries(token, userId, hostId, dateFrom, dateTo);
  const rows = normalizeYandexTop(raw);
  console.error(`Got ${rows.length} queries`);

  const meta = await writeWeeklySnapshot({
    engine: "yandex",
    dateFrom,
    dateTo,
    rows,
    extraMeta: {
      source: "yandex-webmaster-api",
      host_id: hostId,
      user_id: userId,
    },
  });

  console.log(JSON.stringify(meta, null, 2));
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
