/** Эвристика кластеров под канонические продукты ALLSUN. */

const BRAND_RE = /аллсан|allsun|allsan|алсан|алсн|\balsn\b/i;

/**
 * @param {string} text
 * @returns {string}
 */
export function classifyCluster(text) {
  const s = String(text || "").toLowerCase();
  if (BRAND_RE.test(s)) return "brand";
  if (
    (/маркетплейс|ozon|озон|wildberries|вайлдберр|\bwb\b|модуль/.test(s) &&
      /1с|1c|маркет/.test(s)) ||
    /ozon|озон|wildberries|вайлдберр/.test(s)
  ) {
    return "mp";
  }
  if (
    /мерлион|merlion|ocs|втт|vtt|treolan|треолан|ресурс медиа|auvix|аувикс|этм|netlab|cisco|телеком|b2b|б2б|3logic|дссл|dssl|elko|марвел|осиэс/.test(
      s,
    )
  ) {
    return "b2b";
  }
  if (/техподдержк|сопровожден|обслуживан|аутсорс/.test(s)) return "support";
  if (/доработк|программист 1с|разработк/.test(s)) return "dev";
  if (/внедрен|erp|ерп|\bут\b|ут8|ка 1с|комплексн|унф|документооборот/.test(s))
    return "impl";
  if (/лиценз|купить 1с|итс|кп проф|кп баз|fresh|фреш|комплект поддержки/.test(s))
    return "lic";
  if (/битрикс/.test(s)) return "bitrix";
  if (/телеграм|telegram|бот/.test(s)) return "tg";
  if (/сайт.*1с|1с.*сайт|интеграция сайта/.test(s)) return "site";
  return "other";
}
