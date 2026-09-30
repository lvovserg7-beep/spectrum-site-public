const HOSTS = ["demo.alsn.ru", "doc.alsn.ru", "ip.alsn.ru", "apps.alsn.ru", "lk.alsn.ru", "www.alsn.ru"];

async function get(url) {
  try {
    const r = await fetch(url, { redirect: "manual", signal: AbortSignal.timeout(10000) });
    const t = await r.text();
    return { status: r.status, loc: r.headers.get("location"), xrt: r.headers.get("x-robots-tag"), body: t.slice(0, 160).replace(/\s+/g, " ") };
  } catch (e) {
    return { err: e.cause?.code || e.message };
  }
}

for (const h of HOSTS) {
  for (const s of ["https", "http"]) {
    const root = await get(`${s}://${h}/`);
    const rob = await get(`${s}://${h}/robots.txt`);
    console.log(`${s}://${h}/`, JSON.stringify(root));
    console.log(`   robots`, JSON.stringify(rob));
  }
}
