import https from "node:https";

function fetch(url) {
  return new Promise((resolve, reject) => {
    https
      .get(
        url,
        {
          headers: {
            "User-Agent": "Mozilla/5.0",
            "Cache-Control": "no-cache",
          },
        },
        (res) => {
          const c = [];
          res.on("data", (d) => c.push(d));
          res.on("end", () => resolve(Buffer.concat(c).toString("utf8")));
        },
      )
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
  "https://alsn.ru/",
];

for (const url of urls) {
  try {
    const html = await fetch(url);
    const title = one(html, /<title[^>]*>([\s\S]*?)<\/title>/i);
    let desc = one(
      html,
      /<meta[^>]+name=["']description["'][^>]+content=["']([^"']*)["']/i,
    );
    if (!desc) {
      desc = one(
        html,
        /<meta[^>]+content=["']([^"']*)["'][^>]+name=["']description["']/i,
      );
    }
    const h1 = one(html, /<h1[^>]*>([\s\S]*?)<\/h1>/i);
    let og = one(
      html,
      /<meta[^>]+property=["']og:image["'][^>]+content=["']([^"']*)["']/i,
    );
    if (!og) {
      og = one(
        html,
        /<meta[^>]+content=["']([^"']*)["'][^>]+property=["']og:image["']/i,
      );
    }
    console.log(
      JSON.stringify({
        url,
        title: title.slice(0, 160),
        desc: desc.slice(0, 180),
        h1: h1.slice(0, 140),
        hasOg: Boolean(og),
      }),
    );
  } catch (e) {
    console.log(JSON.stringify({ url, error: String(e.message || e) }));
  }
}
