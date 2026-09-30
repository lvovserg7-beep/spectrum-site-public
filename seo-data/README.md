# SEO: еженедельные срезы позиций

Хранение показов, кликов и средней позиции по запросам **понедельно**.

## Структура

```
seo-data/
  yandex/     — Яндекс.Вебмастер (основной источник)
  google/     — Google Search Console (когда появятся данные)
  scripts/    — выгрузка и запись CSV + Parquet
```

Имена файлов: `YYYY-Www` (ISO-неделя, понедельник = начало).

Пример: `yandex/2026-W34.csv` + `yandex/2026-W34.parquet` + `yandex/2026-W34.meta.json`

## Колонки CSV / Parquet

| Колонка | Описание |
|---|---|
| week_start | Понедельник недели (YYYY-MM-DD) |
| week | ISO-неделя (YYYY-Www) |
| engine | `yandex` или `google` |
| date_from / date_to | Период метрик в API |
| query | Поисковый запрос |
| shows | Показы |
| clicks | Клики |
| avg_position | Средняя позиция показа |
| ctr | Клики / показы |
| cluster | Кластер продукта (эвристика) |

## Как снять неделю

### Вариант A — через агента (MCP Яндекса)

1. Агент вызывает `search_queries` за нужные 7 дней.
2. Сохраняет сырой JSON и запускает:

```bash
cd seo-data/scripts
npm install
node write-snapshot.mjs --engine yandex --from-json path/to/raw.json --date-from 2026-08-18 --date-to 2026-08-24
```

### Вариант B — напрямую по API (токен)

В `.env` проекта или окружении:

```
YANDEX_WEBMASTER_TOKEN=...
YANDEX_WEBMASTER_HOST_ID=https:alsn.ru:443
```

```bash
cd seo-data/scripts
npm install
node snapshot-yandex.mjs --date-from 2026-08-18 --date-to 2026-08-24
```

Период лучше фиксировать как **прошлый полный понедельник–воскресенье**.

## Google

Пока Search Analytics пустой. Когда появятся данные — тот же формат в `google/YYYY-Www.*`.
