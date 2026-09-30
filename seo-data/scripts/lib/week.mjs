/**
 * Понедельник ISO-недели для даты (локальная календарная дата YYYY-MM-DD).
 * @param {string} isoDate
 */
export function mondayOf(isoDate) {
  const [y, m, d] = isoDate.split("-").map(Number);
  const dt = new Date(Date.UTC(y, m - 1, d));
  const day = dt.getUTCDay(); // 0 Sun .. 6 Sat
  const diff = day === 0 ? -6 : 1 - day;
  dt.setUTCDate(dt.getUTCDate() + diff);
  return dt.toISOString().slice(0, 10);
}

/**
 * ISO week label YYYY-Www for a Monday date.
 * @param {string} mondayIso
 */
export function isoWeekLabel(mondayIso) {
  const [y, m, d] = mondayIso.split("-").map(Number);
  const date = new Date(Date.UTC(y, m - 1, d));
  // ISO week: Thursday of this week determines year
  const thursday = new Date(date);
  thursday.setUTCDate(date.getUTCDate() + 3);
  const isoYear = thursday.getUTCFullYear();
  const jan4 = new Date(Date.UTC(isoYear, 0, 4));
  const jan4Day = jan4.getUTCDay() || 7;
  const week1Monday = new Date(jan4);
  week1Monday.setUTCDate(jan4.getUTCDate() - (jan4Day - 1));
  const week =
    1 + Math.round((date.getTime() - week1Monday.getTime()) / 604800000);
  return `${isoYear}-W${String(week).padStart(2, "0")}`;
}
