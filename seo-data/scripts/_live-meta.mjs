import https from "node:https";

function fetch(url) {
  return new Promise((resolve, reject) => {
    https
      .get(url, { headers: { "User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache" } }, (res) => {
        const chunks = [];
        res.on("data", (c) => chunks.push(c));
        res.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
      })
      .on("error", reject);
  });
}

function one(html, re) {
  const m = html.match(re);
  return m ? m[1].replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim() : "";
}

const urls = [
  "https://alsn.ru/casemarketplace",
  "https://alsn.ru/ecom",
  "https://alsn.ru/etm-ipro",
  "https://alsn.ru/development1c",
  "https://alsn.ru/kompleksnaya_avtomatizaciya",
  "https://alsn.ru/erp-time-price",
  "https://alsn.ru/support1c",
];

for (const url of urls) {
  const html = await fetch(url);
  const title = one(html, /<title[^>]*>([\s\S]*?)<\/title>/i);
  const desc =
    one(html, /name=["']description["'][^>]*content=["']([^"']+)["']/i) ||
    one(html, /content=["']([^"']+)["'][^>]*name=["']description["']/i);
  const h1 = one(html, /<h1[^>]*>([\s\S]*?)<\/h1>/i);
  const hasOrg = /Organization/.test(html);
  const hasService = /"@type"\s*:\s*"Service"/.test(html) || /@type":"Service"/.test(html);
  const tgFloat = /Телеграм-бот 1С\. Протестируй!|rec331642749/.test(html);
  console.log(
    JSON.stringify({
      url,
      title: title.slice(0, 110),
      desc: desc.slice(0, 150),
      h1: h1.slice(0, 110),
      hasOrg,
      hasService,
      tgFloat,
    }),
  );
}
