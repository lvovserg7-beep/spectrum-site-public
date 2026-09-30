import fs from "node:fs";

const before = JSON.parse(
  fs.readFileSync(
    "C:/Users/ALSN_LSA/.cursor/projects/c-Users-ALSN-LSA-Desktop-cursor/agent-tools/9cfbfb57-387a-4aff-9c48-60bbbf779603.txt",
    "utf8",
  ),
);
const after = JSON.parse(
  fs.readFileSync(
    "C:/Users/ALSN_LSA/.cursor/projects/c-Users-ALSN-LSA-Desktop-cursor/agent-tools/d377af94-8938-4999-89df-78354d4e7f06.txt",
    "utf8",
  ),
);

const BRAND = /аллсан|allsun|allsan|алсан|алсн|\balsn\b/i;

function classify(q) {
  const s = String(q).toLowerCase();
  if (BRAND.test(s)) return "brand";
  if (
    (/маркетплейс|ozon|озон|wildberries|вайлдберр|\bwb\b|модуль/.test(s) &&
      /1с|1c|маркет/.test(s)) ||
    /ozon|озон|wildberries|вайлдберр/.test(s)
  )
    return "mp";
  if (
    /мерлион|merlion|ocs|втт|vtt|treolan|треолан|ресурс медиа|auvix|аувикс|этм|netlab|cisco|телеком|b2b|б2б|3logic|дссл|dssl|elko|марвел|осиэс|русский свет|ipro|поставщик/.test(
      s,
    )
  )
    return "b2b";
  if (/техподдержк|сопровожден|обслуживан|аутсорс|программист 1с на час/.test(s))
    return "support";
  if (/доработк|кастом|печатн.*форм/.test(s)) return "dev";
  if (
    /внедрен|erp|комплексн.*автомат|1с внедрение|\bка\b.*внедр|стоимость внедрения|erp на производ/.test(
      s,
    )
  )
    return "impl";
  if (/битрикс|bitrix/.test(s)) return "bitrix";
  if (/лиценз|итс|\bкп\b|fresh|фреш|коробк|купить 1с|цена.*1с/.test(s))
    return "lic";
  if (/телеграм|telegram|бот/.test(s)) return "tg";
  return "other";
}

function agg(queries) {
  const out = {};
  for (const row of queries) {
    const c = classify(row.query_text);
    if (!out[c])
      out[c] = { shows: 0, clicks: 0, posSum: 0, n: 0, top: [] };
    out[c].shows += row.TOTAL_SHOWS || 0;
    out[c].clicks += row.TOTAL_CLICKS || 0;
    out[c].posSum += (row.AVG_SHOW_POSITION || 0) * (row.TOTAL_SHOWS || 0);
    out[c].n += 1;
    out[c].top.push(row);
  }
  for (const c of Object.keys(out)) {
    const o = out[c];
    o.ctr = o.shows ? (100 * o.clicks) / o.shows : 0;
    o.avgPos = o.shows ? o.posSum / o.shows : null;
    o.top = o.top
      .sort((a, b) => b.TOTAL_SHOWS - a.TOTAL_SHOWS)
      .slice(0, 8)
      .map((r) => ({
        q: r.query_text,
        shows: r.TOTAL_SHOWS,
        clicks: r.TOTAL_CLICKS,
        pos: Math.round(r.AVG_SHOW_POSITION * 10) / 10,
        ctr:
          r.TOTAL_SHOWS > 0
            ? Math.round((10000 * r.TOTAL_CLICKS) / r.TOTAL_SHOWS) / 100
            : 0,
      }));
  }
  return out;
}

const CONTROL = [
  "модуль маркетплейсов 1с",
  "модуль 1с для маркетплейсов",
  "модули маркетплейсов для 1с",
  "1с ут интеграция с маркетплейсами",
  "модуль интеграции 1с с маркетплейсами",
  "мерлион b2b",
  "ocs b2b",
  "интеграция с озон 1с ут",
  "внедрение 1с комплексная автоматизация",
  "1с внедрение ка",
  "стоимость внедрения 1с erp на производственном предприятии",
  "аллсан интеграция",
];

function indexByQuery(queries) {
  const m = {};
  for (const r of queries) m[r.query_text] = r;
  return m;
}

const bIdx = indexByQuery(before.queries || []);
const aIdx = indexByQuery(after.queries || []);

const controls = CONTROL.map((q) => {
  const b = bIdx[q];
  const a = aIdx[q];
  return {
    q,
    cluster: classify(q),
    before: b
      ? {
          shows: b.TOTAL_SHOWS,
          clicks: b.TOTAL_CLICKS,
          pos: Math.round(b.AVG_SHOW_POSITION * 10) / 10,
          ctr:
            b.TOTAL_SHOWS > 0
              ? Math.round((10000 * b.TOTAL_CLICKS) / b.TOTAL_SHOWS) / 100
              : 0,
        }
      : null,
    after: a
      ? {
          shows: a.TOTAL_SHOWS,
          clicks: a.TOTAL_CLICKS,
          pos: Math.round(a.AVG_SHOW_POSITION * 10) / 10,
          ctr:
            a.TOTAL_SHOWS > 0
              ? Math.round((10000 * a.TOTAL_CLICKS) / a.TOTAL_SHOWS) / 100
              : 0,
        }
      : null,
  };
});

const ba = agg(before.queries || []);
const aa = agg(after.queries || []);

function daysInRange(from, to) {
  const a = new Date(from);
  const b = new Date(to);
  return Math.max(1, Math.round((b - a) / 86400000) + 1);
}

const beforeDays = daysInRange(before.date_from, before.date_to);
const afterDays = daysInRange(after.date_from, after.date_to);

const clusters = [
  "mp",
  "b2b",
  "impl",
  "support",
  "lic",
  "bitrix",
  "brand",
  "tg",
  "dev",
  "other",
];

const clusterCompare = clusters.map((c) => {
  const b = ba[c] || { shows: 0, clicks: 0, avgPos: null, ctr: 0, n: 0, top: [] };
  const a = aa[c] || { shows: 0, clicks: 0, avgPos: null, ctr: 0, n: 0, top: [] };
  return {
    c,
    beforeDays,
    afterDays,
    bShows: b.shows,
    aShows: a.shows,
    bShowsDay: Math.round((10 * b.shows) / beforeDays) / 10,
    aShowsDay: Math.round((10 * a.shows) / afterDays) / 10,
    bClicks: b.clicks,
    aClicks: a.clicks,
    bClicksDay: Math.round((100 * b.clicks) / beforeDays) / 100,
    aClicksDay: Math.round((100 * a.clicks) / afterDays) / 100,
    bCtr: Math.round(b.ctr * 100) / 100,
    aCtr: Math.round(a.ctr * 100) / 100,
    bPos: b.avgPos ? Math.round(b.avgPos * 10) / 10 : null,
    aPos: a.avgPos ? Math.round(a.avgPos * 10) / 10 : null,
    bTop: b.top,
    aTop: a.top,
  };
});

console.log(
  JSON.stringify(
    {
      beforeMeta: {
        from: before.date_from,
        to: before.date_to,
        days: beforeDays,
        total: before.total_queries,
      },
      afterMeta: {
        from: after.date_from,
        to: after.date_to,
        days: afterDays,
        total: after.total_queries,
      },
      clusterCompare,
      controls,
    },
    null,
    2,
  ),
);
