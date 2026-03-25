# 🔮 TRENDRADAR — МЕГАПРОМПТ v2.0

**AI-платформа предсказания трендов | Signal Intelligence Architecture | Template D (Vibe Coding Bible v3.3)**

---

Ты — senior full-stack developer и AI/ML engineer с 10+ годами опыта в построении real-time data platforms, predictive analytics систем и SaaS-продуктов уровня production. Ты эксперт в: Next.js, Python, FastAPI, PostgreSQL, Redis, WebSocket, LLM API integration, time-series analysis, data aggregation pipelines, Stripe billing, и создании виральных consumer-facing продуктов.

---

## 📋 ПРОЕКТ: TrendRadar

### Что это
AI-платформа предсказания трендов. НЕ Google Trends (показывает что УЖЕ трендит). TrendRadar ПРЕДСКАЗЫВАЕТ что станет трендом через 24-72 часа.

**Ключевой value proposition:**
> "Эта тема вырастет на 400% через 3 дня, вот почему, вот контент который нужно создать прямо сейчас."

### Ключевой архитектурный принцип: SIGNAL INTELLIGENCE

TrendRadar НЕ сканирует миллионы постов напрямую с соцсетей. Вместо этого мы используем подход **Signal Intelligence** — агрегация уже агрегированных данных из 15+ бесплатных и дешёвых источников.

**Почему это лучше чем прямые API:**

| Подход | Стоимость | Стабильность | Покрытие | Скорость запуска |
|--------|-----------|--------------|----------|-----------------|
| Прямые API (Twitter $5K/мес, TikTok закрыт, Instagram закрыт) | $5,000-10,000/мес | Низкая (API меняются, закрываются) | Зависит от бюджета | Месяцы |
| Data Providers (Brandwatch, Meltwater) | $500-5,000/мес | Средняя | Хорошее | Недели |
| **Signal Intelligence (наш подход)** | **$0-100/мес** | **Высокая (множество fallback'ов)** | **Отличное (15+ источников)** | **Дни** |

**Принцип:** Каждый источник (Reddit Rising, HN Front Page, YouTube Trending, GitHub Trending, Google Trends, Wikipedia Pageviews, npm downloads) уже сделал первичную фильтрацию за нас. Наша задача — обнаружить **cross-source correlations**: если тема одновременно растёт в Google Trends, поднимается на Reddit Rising и появляется на HN — это предиктивный сигнал, который ни один источник не даёт по отдельности.

**Уникальная ценность TrendRadar** — не в сборе данных (это commodity), а в:
1. **Cross-source correlation detection** — мульти-платформенное обнаружение
2. **AI prediction** — предсказание роста на основе паттернов
3. **Content brief generation** — actionable рекомендации для контент-креаторов
4. **Speed** — предсказание ДО того как тренд попадёт в мейнстрим

### Как работает (Signal Intelligence Pipeline)

```
Шаг 1: SIGNAL COLLECTION
┌─────────────────────────────────────────────────────────┐
│  15+ бесплатных Signal Sources                          │
│                                                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │ Google   │ │ Reddit   │ │ Hacker   │ │ YouTube  │   │
│  │ Trends   │ │ Rising   │ │ News     │ │ Trending │   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘   │
│       │            │            │            │          │
│  ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐   │
│  │ GitHub   │ │ Wikipedia│ │ npm/PyPI │ │ News RSS │   │
│  │ Trending │ │ Pageviews│ │ Stats    │ │ Feeds    │   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘   │
│       │            │            │            │          │
│  ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐   │
│  │ Product  │ │ ArXiv    │ │ CoinGecko│ │ Steam    │   │
│  │ Hunt     │ │ Papers   │ │ Crypto   │ │ Charts   │   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘   │
│       │            │            │            │          │
│  ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐                │
│  │ Dev.to   │ │ Lobsters │ │ Stack    │                │
│  │ Articles │ │ Stories  │ │ Overflow │                │
│  └──────────┘ └──────────┘ └──────────┘                │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
Шаг 2: SIGNAL NORMALIZATION
┌─────────────────────────────────────────────────────────┐
│  Topic Extraction → Deduplication → Normalization       │
│  "GPT-5", "GPT5", "gpt 5" → "GPT-5"                   │
│  Каждый сигнал → unified SignalEvent format             │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
Шаг 3: CROSS-SOURCE CORRELATION ENGINE (уникальная фича)
┌─────────────────────────────────────────────────────────┐
│  Тема X появилась в:                                    │
│    ✓ Google Trends (interest +200%)                     │
│    ✓ Reddit Rising (3 subreddits)                       │
│    ✓ Hacker News Front Page (score 450)                 │
│    ✗ YouTube Trending                                   │
│    ✓ GitHub Trending (new repo 2.5K stars)              │
│    ✓ Wikipedia Pageviews (+500%)                        │
│                                                         │
│  → 5/6 sources firing = HIGH CORRELATION                │
│  → Cross-source velocity accelerating                   │
│  → PREDICTION: +380% growth in 72 hours                 │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
Шаг 4: AI PREDICTION ENGINE
┌─────────────────────────────────────────────────────────┐
│  ML Features + Claude Reasoning                         │
│  → Growth prediction (% and timeframe)                  │
│  → Confidence score (0-100%)                            │
│  → Factor breakdown (why)                               │
│  → Peak timing (when)                                   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
Шаг 5: CONTENT BRIEF GENERATION
┌─────────────────────────────────────────────────────────┐
│  AI generates actionable content briefs:                │
│  → Hook, key points, structure                          │
│  → SEO keywords, hashtags                               │
│  → Best platforms to publish                            │
│  → Optimal timing                                       │
└─────────────────────────────────────────────────────────┘
```

### 3 режима работы

| Режим | Описание | Аналогия |
|-------|----------|----------|
| **EXPLORE** | Лента трендов в реальном времени | Twitter Trending, но умнее — без мусора, с AI-скорингом |
| **PREDICT** | AI предсказания на 24-72 часа вперёд | Уникальная фича. Нет аналогов на рынке |
| **ALERT** | Push-уведомления когда тема в твоей нише растёт | Как Google Alerts, но предиктивные |

### Ключевое отличие от конкурентов

| Продукт | Проблема |
|---------|----------|
| Google Trends | Запаздывает на дни, нет предсказаний, нет контента |
| Exploding Topics | $299/мес, обновляется раз в неделю, нет real-time |
| SparkToro | Аудитории, не тренды |
| Twitter Trending | Мусор, политика, боты, нерелевантно |
| **TrendRadar** | **15+ signal sources + cross-source AI prediction + content briefs + $0 data cost** |

### Целевая аудитория

| Сегмент | Потребность | Как TrendRadar помогает |
|---------|------------|------------------------|
| Контент-креаторы (YouTube, TikTok, Twitter) | Поймать тренд первыми | Предсказание + content brief |
| Маркетологи | Реактивный контент-маркетинг | Real-time мониторинг + recommendations |
| Журналисты | Первыми написать о теме | Алерты + source analysis |
| Трейдеры | Sentiment signals для крипто/акций | Prediction confidence + category filters |
| Product Managers | Понять что хочет рынок | Cross-source analysis + trend velocity |
| Агентства | Trend reports для клиентов | Export + historical data + branded reports |

### Виральный потенциал
- **Free tier** + shareable trend cards = органический рост
- **"TrendRadar predicted this 3 days ago"** watermark на shared карточках
- Weekly **"TrendRadar called it"** Twitter thread (build in public)
- Embeddable trend widgets для блогов и newsletters
- **Browser extension** (Phase 8) — показывает trending overlay, в обмен собирает анонимизированные сигналы

### Бизнес-модель

| Тариф | Цена | Включает |
|-------|------|----------|
| **Free** | $0 | 3 тренда/день, без предсказаний, без алертов (виральный хук) |
| **Creator** | $19/мес | Unlimited тренды, базовые предсказания (24h), 3 алерта, 5 content briefs/день |
| **Pro** | $79/мес | Full предсказания (72h), unlimited алертов, unlimited briefs, API access, export |
| **Business** | $299/мес | Team (5 seats), custom categories, export, integrations, historical data (90 дней), priority support |
| **Enterprise** | Custom | Unlimited seats, premium data sources (Twitter, data providers), SLA, dedicated support, white-label |

### Стратегия расширения источников данных

```
MVP (Фаза 0-3, $0/мес):
├── 15+ бесплатных signal sources (см. Signal Source Registry ниже)
├── Достаточно для real predictions и cross-source correlation
└── Нулевая стоимость данных

Growth ($5-10K MRR):
├── + Twitter/X Basic API ($100/мес) — прямые tweets
├── + NewsAPI Business ($449/мес) — расширенный news coverage
└── + Browser extension data (бесплатно, от пользователей)

Scale ($50K+ MRR):
├── + Data provider (Brandwatch/Meltwater) — полный social coverage
├── + Twitter Enterprise — firehose data
├── + SocialRadar integration (если доступен)
└── + Custom scrapers для niche sources

Enterprise:
├── + Customer-provided data sources
├── + On-premise deployment
└── + Custom signal adapters per client
```

---

## 📡 SIGNAL SOURCE REGISTRY

### Полный реестр источников (все бесплатные или дешёвые)

#### Tier 1: Core Sources (обязательные, бесплатные, стабильные)

| # | Source | API/Method | Cost | Rate Limit | Signal Type | Best For |
|---|--------|-----------|------|------------|-------------|----------|
| 1 | **Google Trends** | pytrends (unofficial) | $0 | ~10 req/min | Search interest over time, related queries, rising queries | General trends, search-driven topics |
| 2 | **Reddit** | PRAW (official API) | $0 | 100 req/min | Rising posts, hot posts, subreddit growth, comment velocity | Tech, culture, memes, discussions |
| 3 | **Hacker News** | Firebase API (official) | $0 | Unlimited | Top stories, new stories, score velocity, comment count | Tech, startups, programming, AI |
| 4 | **YouTube Trending** | Data API v3 (official) | $0 | 10K units/day | Trending videos, view velocity, category trends | Culture, entertainment, tech, how-to |
| 5 | **GitHub Trending** | Scrape + API | $0 | 5K req/hr | Trending repos, stars velocity, language trends | Developer tools, open source, libraries |
| 6 | **Wikipedia Pageviews** | REST API (official) | $0 | 200 req/s | Pageview spikes, article creation | Breaking news, people, events |
| 7 | **Google News RSS** | RSS feeds | $0 | Unlimited | Top stories, category news, topic clusters | News, politics, business, world events |

#### Tier 2: Vertical Sources (бесплатные, нишевые)

| # | Source | API/Method | Cost | Rate Limit | Signal Type | Best For |
|---|--------|-----------|------|------------|-------------|----------|
| 8 | **Product Hunt** | GraphQL API (official) | $0 | 450 req/day | Daily top products, upvotes, comments | Products, startups, tech launches |
| 9 | **npm Registry** | Registry API (official) | $0 | Generous | Download stats, new packages, version activity | JavaScript ecosystem, developer tools |
| 10 | **PyPI Stats** | pypistats API | $0 | Generous | Download trends, new packages | Python ecosystem, ML/AI libraries |
| 11 | **ArXiv** | REST API (official) | $0 | Generous | New papers, citation velocity, category trends | AI research, science, academia |
| 12 | **CoinGecko** | Free API | $0 | 10-30 req/min | Price movements, volume spikes, new listings | Crypto, DeFi, Web3 |
| 13 | **Steam Charts** | Scrape steamcharts.com | $0 | Gentle scraping | Player count changes, new game spikes | Gaming trends |
| 14 | **Dev.to** | Forem API (official) | $0 | 30 req/min | Top articles, tag trends, comment activity | Developer content, tutorials |
| 15 | **Lobste.rs** | RSS + JSON | $0 | Unlimited | Top stories, tag trends | Niche tech, programming |
| 16 | **Stack Overflow** | API v2.3 (official) | $0 | 300 req/day | Trending tags, question velocity, new tags | Programming, technical trends |

#### Tier 3: Supplementary Sources (дешёвые, добавляем по мере роста)

| # | Source | API/Method | Cost | Signal Type | Best For |
|---|--------|-----------|------|-------------|----------|
| 17 | **Subreddit Stats** | Reddit API | $0 | Subscriber growth rate | Emerging communities |
| 18 | **Twitter/X** | Basic API | $100/мес | Tweets, trending topics | General, when budget allows |
| 19 | **NewsAPI** | Business tier | $449/мес | Full news articles | Extended news coverage |
| 20 | **Crates.io** | API (official) | $0 | Downloads, new crates | Rust ecosystem |
| 21 | **Docker Hub** | API | $0 | Pull stats, new images | DevOps, containers |
| 22 | **App Store / Play Store** | Scrape | $0 | App rankings, reviews | Mobile app trends |
| 23 | **Telegram Channel Stats** | TGStat API | $0-49/мес | Channel growth, view spikes | Russian market, crypto communities |

#### Future: User-Powered Sources (Phase 8+)

| # | Source | Method | Cost | Signal Type |
|---|--------|--------|------|-------------|
| 24 | **Browser Extension** | User opt-in data | $0 | Anonymized browsing patterns, trending pages |
| 25 | **SocialRadar** | API integration | Variable | Full social media coverage |
| 26 | **Data Providers** | Brandwatch, etc. | $500-5K/мес | Twitter, Instagram, TikTok data |

### Source Quality Weights

Не все источники одинаково ценны для предсказаний. Веса используются в Correlation Engine:

```python
SOURCE_WEIGHTS = {
    # Tier 1: High-quality, real-time signals
    "google_trends":     0.90,   # Massive user base, search-driven
    "reddit":            0.85,   # Early trend incubator, organic
    "hackernews":        0.85,   # Tech authority, high signal-to-noise
    "youtube_trending":  0.80,   # Massive reach, culture indicator
    "github_trending":   0.80,   # Developer ecosystem, code adoption
    "wikipedia":         0.75,   # Breaking news indicator, factual
    "google_news":       0.70,   # News aggregation, editorial filter
    
    # Tier 2: Vertical signals
    "producthunt":       0.70,   # Product launches, startup ecosystem
    "npm_registry":      0.65,   # JS ecosystem adoption
    "pypi_stats":        0.65,   # Python ecosystem adoption
    "arxiv":             0.60,   # Academic research, slow but impactful
    "coingecko":         0.75,   # Crypto-specific, high volatility
    "steam_charts":      0.60,   # Gaming-specific
    "devto":             0.55,   # Developer content, derivative
    "lobsters":          0.55,   # Niche tech
    "stackoverflow":     0.60,   # Developer problems/adoption
    
    # Tier 3: Supplementary
    "subreddit_stats":   0.50,   # Growth signals
    "twitter":           0.85,   # When available (paid)
    "newsapi":           0.70,   # When available (paid)
}
```

### Cross-Source Correlation Multipliers

Определённые комбинации источников дают особо сильные предсказательные сигналы:

```python
CORRELATION_MULTIPLIERS = {
    # Tech trend patterns
    frozenset(["hackernews", "github_trending", "reddit"]): 1.8,
    frozenset(["hackernews", "github_trending", "npm_registry"]): 1.7,
    frozenset(["hackernews", "reddit", "google_trends"]): 1.6,
    frozenset(["arxiv", "hackernews", "github_trending"]): 1.9,  # AI research → adoption
    
    # Product/startup patterns
    frozenset(["producthunt", "hackernews", "github_trending"]): 1.7,
    frozenset(["producthunt", "reddit", "google_trends"]): 1.5,
    
    # Mainstream breakout patterns
    frozenset(["google_trends", "youtube_trending", "reddit"]): 1.8,
    frozenset(["google_trends", "wikipedia", "google_news"]): 1.7,
    frozenset(["google_trends", "youtube_trending", "google_news"]): 1.9,  # Full mainstream
    
    # Crypto patterns
    frozenset(["coingecko", "reddit", "google_trends"]): 1.6,
    frozenset(["coingecko", "hackernews", "reddit"]): 1.5,
    
    # Gaming patterns
    frozenset(["steam_charts", "reddit", "youtube_trending"]): 1.7,
    
    # Developer ecosystem patterns
    frozenset(["npm_registry", "stackoverflow", "github_trending"]): 1.6,
    frozenset(["pypi_stats", "arxiv", "github_trending"]): 1.7,
    
    # Breaking news patterns
    frozenset(["wikipedia", "google_news", "google_trends"]): 2.0,  # Strongest
    frozenset(["wikipedia", "google_news", "reddit"]): 1.8,
    
    # 5+ sources = massive signal regardless of combination
    # handled separately in correlation engine: 5 sources = 2.0x, 6+ = 2.5x
}
```

---

## 🛠️ СТЕК

### Frontend
```
Next.js 14.2          — App Router, RSC, Server Actions
React 18.3            — UI framework
TypeScript 5.4        — type safety
Tailwind CSS 3.4      — utility-first styling
shadcn/ui             — component library (как Linear/Vercel aesthetic)
Framer Motion 11      — animations (trend cards, charts)
Recharts 2.12         — trend velocity charts, prediction graphs
D3.js 7               — cross-source correlation maps, network graphs
Lucide React          — icons
next-themes           — dark/light mode
nuqs                  — URL state management
react-hot-toast       — notifications
date-fns 3            — date formatting
swr 2                 — data fetching + caching
zustand 4             — state management
```

### Backend
```
Python 3.12           — primary backend language
FastAPI 0.111         — async API framework
Uvicorn               — ASGI server
Celery 5.4            — distributed task queue (scanning, analysis)
Redis 7.2             — caching, pub/sub, rate limiting, Celery broker
PostgreSQL 16         — primary database
SQLAlchemy 2.0        — ORM + async
Alembic 1.13          — database migrations
Pydantic 2.7          — data validation
httpx                 — async HTTP client
BeautifulSoup4        — HTML parsing (GitHub Trending, Steam Charts scraping)
feedparser            — RSS feed parsing (Google News, Lobsters)
pytrends              — Google Trends unofficial API
praw                  — Reddit API wrapper
```

### AI/ML
```
Anthropic Claude API (claude-sonnet-4-20250514) — prediction, classification, content briefs
OpenAI Embeddings (text-embedding-3-small)       — semantic similarity, topic clustering
scikit-learn 1.5       — velocity calculations, trend scoring algorithms
numpy / pandas         — data processing
```

### Infrastructure
```
Supabase               — PostgreSQL hosting, Auth (email + OAuth), RLS, Realtime
Redis Cloud             — managed Redis
Vercel                  — frontend hosting, edge functions, OG image generation
Railway / Render        — backend hosting (FastAPI + Celery workers)
Cloudflare R2           — image storage (OG images, trend cards)
Resend                  — transactional emails
Stripe                  — billing & subscriptions
Upstash                 — rate limiting (serverless Redis)
```

### DevOps & Monitoring
```
GitHub Actions          — CI/CD
Semgrep                 — SAST security scanning
Snyk                    — dependency vulnerability scanning
Sentry                  — error tracking
PostHog                 — product analytics
Telegram Bot API        — server monitoring alerts
Docker                  — containerization
pytest                  — backend testing
Playwright              — E2E testing
```

### External Data Sources (Signal Sources)
```
## Tier 1: Core (бесплатные, стабильные)
pytrends                — Google Trends (unofficial, $0)
Reddit API (PRAW)       — posts, subreddits ($0, 100 req/min)
Hacker News API         — Firebase-based ($0, unlimited)
YouTube Data API v3     — trending, search ($0, 10K units/day)
GitHub REST API v3      — trending scrape + API ($0, 5K req/hr)
Wikipedia Pageviews API — pageview stats ($0, 200 req/s)
Google News RSS         — RSS feeds ($0, unlimited)

## Tier 2: Vertical (бесплатные, нишевые)
Product Hunt GraphQL    — daily products ($0, 450 req/day)
npm Registry API        — download stats ($0)
PyPI Stats API          — download stats ($0)
ArXiv API               — papers ($0)
CoinGecko API           — crypto data ($0, 10-30 req/min)
Steam Charts            — scrape ($0)
Dev.to Forem API        — articles ($0, 30 req/min)
Lobste.rs               — RSS/JSON ($0)
Stack Overflow API      — tags, questions ($0, 300 req/day)

## Tier 3: Paid (добавляем при росте revenue)
Twitter/X API v2        — ($100-5K/мес, когда есть MRR)
NewsAPI                 — ($449/мес, расширенные новости)
```

---

## 📂 ФАЙЛОВАЯ СТРУКТУРА ПРОЕКТА

```
trendradar/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                          # Lint + test + security scan
│   │   ├── cd-frontend.yml                 # Vercel deployment
│   │   ├── cd-backend.yml                  # Railway/Render deployment
│   │   └── security-scan.yml               # Semgrep + Snyk weekly
│   └── CODEOWNERS
│
├── frontend/                               # Next.js 14 App
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   ├── .env.example                        # НЕ реальные значения
│   ├── .env.local                          # .gitignore'd
│   │
│   ├── public/
│   │   ├── favicon.ico
│   │   ├── logo.svg
│   │   ├── og-default.png                  # Default OG image
│   │   └── fonts/
│   │       ├── inter-var.woff2
│   │       └── jetbrains-mono.woff2
│   │
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx                  # Root layout: fonts, theme, providers
│   │   │   ├── page.tsx                    # Landing page (marketing)
│   │   │   ├── globals.css                 # Tailwind base + custom vars
│   │   │   ├── not-found.tsx
│   │   │   ├── error.tsx
│   │   │   │
│   │   │   ├── (auth)/
│   │   │   │   ├── login/page.tsx          # Login (email + OAuth)
│   │   │   │   ├── signup/page.tsx         # Registration
│   │   │   │   ├── forgot-password/page.tsx
│   │   │   │   ├── reset-password/page.tsx
│   │   │   │   ├── verify-email/page.tsx
│   │   │   │   └── layout.tsx              # Auth layout (centered card)
│   │   │   │
│   │   │   ├── (marketing)/
│   │   │   │   ├── pricing/page.tsx        # Pricing page with plan comparison
│   │   │   │   ├── about/page.tsx
│   │   │   │   ├── blog/
│   │   │   │   │   ├── page.tsx            # Blog listing
│   │   │   │   │   └── [slug]/page.tsx     # Blog post
│   │   │   │   ├── changelog/page.tsx
│   │   │   │   └── layout.tsx              # Marketing layout (nav + footer)
│   │   │   │
│   │   │   ├── (dashboard)/
│   │   │   │   ├── layout.tsx              # Dashboard layout (sidebar + topbar)
│   │   │   │   │
│   │   │   │   ├── explore/
│   │   │   │   │   ├── page.tsx            # EXPLORE mode: real-time trend feed
│   │   │   │   │   └── loading.tsx
│   │   │   │   │
│   │   │   │   ├── predict/
│   │   │   │   │   ├── page.tsx            # PREDICT mode: AI predictions
│   │   │   │   │   ├── [trendId]/page.tsx  # Prediction detail page
│   │   │   │   │   └── loading.tsx
│   │   │   │   │
│   │   │   │   ├── alerts/
│   │   │   │   │   ├── page.tsx            # ALERT mode: manage alerts
│   │   │   │   │   ├── new/page.tsx        # Create new alert
│   │   │   │   │   └── [alertId]/page.tsx  # Edit alert
│   │   │   │   │
│   │   │   │   ├── trend/
│   │   │   │   │   └── [trendId]/
│   │   │   │   │       ├── page.tsx        # Trend detail: signals, velocity, prediction
│   │   │   │   │       ├── brief/page.tsx  # Content brief for trend
│   │   │   │   │       └── share/page.tsx  # Share/embed trend card
│   │   │   │   │
│   │   │   │   ├── categories/
│   │   │   │   │   ├── page.tsx            # Category explorer
│   │   │   │   │   └── [categorySlug]/page.tsx
│   │   │   │   │
│   │   │   │   ├── search/page.tsx         # Search across all trends
│   │   │   │   ├── history/page.tsx        # Historical trend data (Business+)
│   │   │   │   │
│   │   │   │   ├── settings/
│   │   │   │   │   ├── page.tsx            # General settings
│   │   │   │   │   ├── profile/page.tsx
│   │   │   │   │   ├── billing/page.tsx    # Subscription management
│   │   │   │   │   ├── team/page.tsx       # Team management (Business+)
│   │   │   │   │   ├── api-keys/page.tsx   # API key management (Pro+)
│   │   │   │   │   ├── notifications/page.tsx
│   │   │   │   │   ├── categories/page.tsx # Custom categories (Business+)
│   │   │   │   │   └── integrations/page.tsx
│   │   │   │   │
│   │   │   │   └── admin/                  # Admin panel (internal only)
│   │   │   │       ├── page.tsx
│   │   │   │       ├── users/page.tsx
│   │   │   │       ├── trends/page.tsx
│   │   │   │       ├── sources/page.tsx    # Signal source health dashboard
│   │   │   │       └── analytics/page.tsx
│   │   │   │
│   │   │   ├── api/
│   │   │   │   ├── auth/callback/route.ts  # Supabase OAuth callback
│   │   │   │   ├── webhooks/stripe/route.ts # Stripe webhook handler
│   │   │   │   ├── og/[trendId]/route.tsx  # Dynamic OG image generation
│   │   │   │   └── embed/[trendId]/route.ts # Embeddable widget endpoint
│   │   │   │
│   │   │   └── share/
│   │   │       └── [trendId]/page.tsx      # Public shareable trend page
│   │   │
│   │   ├── components/
│   │   │   ├── ui/                         # shadcn/ui components (button, card, dialog, etc.)
│   │   │   │
│   │   │   ├── layout/
│   │   │   │   ├── sidebar.tsx             # Dashboard sidebar navigation
│   │   │   │   ├── topbar.tsx              # Dashboard top bar (search, user menu)
│   │   │   │   ├── mobile-nav.tsx
│   │   │   │   ├── marketing-nav.tsx
│   │   │   │   ├── footer.tsx
│   │   │   │   ├── breadcrumb.tsx
│   │   │   │   └── page-header.tsx
│   │   │   │
│   │   │   ├── trends/
│   │   │   │   ├── trend-card.tsx           # Individual trend card (feed item)
│   │   │   │   ├── trend-feed.tsx           # Scrollable trend feed (EXPLORE)
│   │   │   │   ├── trend-detail.tsx         # Full trend detail view
│   │   │   │   ├── trend-velocity-chart.tsx # Velocity over time (Recharts)
│   │   │   │   ├── trend-signal-list.tsx    # Signal sources where trend detected
│   │   │   │   ├── trend-source-badge.tsx   # Signal source icon + label
│   │   │   │   ├── trend-category-badge.tsx
│   │   │   │   ├── trend-score-ring.tsx     # Circular score indicator
│   │   │   │   ├── trend-skeleton.tsx
│   │   │   │   ├── trend-filters.tsx        # Category, source, time filters
│   │   │   │   ├── trend-sort.tsx
│   │   │   │   ├── trend-empty-state.tsx
│   │   │   │   └── trend-share-button.tsx
│   │   │   │
│   │   │   ├── predictions/
│   │   │   │   ├── prediction-card.tsx
│   │   │   │   ├── prediction-feed.tsx
│   │   │   │   ├── prediction-detail.tsx
│   │   │   │   ├── prediction-timeline.tsx
│   │   │   │   ├── prediction-confidence.tsx
│   │   │   │   ├── prediction-factors.tsx
│   │   │   │   ├── prediction-history.tsx
│   │   │   │   └── prediction-skeleton.tsx
│   │   │   │
│   │   │   ├── alerts/
│   │   │   │   ├── alert-card.tsx
│   │   │   │   ├── alert-form.tsx
│   │   │   │   ├── alert-list.tsx
│   │   │   │   ├── alert-history.tsx
│   │   │   │   ├── alert-category-picker.tsx
│   │   │   │   ├── alert-threshold-slider.tsx
│   │   │   │   └── alert-channel-select.tsx
│   │   │   │
│   │   │   ├── content-briefs/
│   │   │   │   ├── brief-card.tsx
│   │   │   │   ├── brief-detail.tsx
│   │   │   │   ├── brief-format-tabs.tsx
│   │   │   │   ├── brief-copy-button.tsx
│   │   │   │   └── brief-skeleton.tsx
│   │   │   │
│   │   │   ├── categories/
│   │   │   │   ├── category-grid.tsx
│   │   │   │   ├── category-card.tsx
│   │   │   │   ├── category-trend-count.tsx
│   │   │   │   └── category-icon.tsx
│   │   │   │
│   │   │   ├── visualizations/
│   │   │   │   ├── velocity-chart.tsx        # Velocity over time (Recharts)
│   │   │   │   ├── cross-source-map.tsx      # Signal source correlation map (D3)
│   │   │   │   ├── prediction-graph.tsx      # Prediction confidence over time
│   │   │   │   ├── category-heatmap.tsx      # Category activity heatmap
│   │   │   │   ├── source-network.tsx        # Source relationship network (D3)
│   │   │   │   ├── signal-radar-chart.tsx    # Radar chart: which sources firing
│   │   │   │   ├── sparkline.tsx             # Mini inline chart for cards
│   │   │   │   ├── live-counter.tsx          # Animated count-up numbers
│   │   │   │   ├── signal-strength-bar.tsx   # Signal strength indicator
│   │   │   │   └── mini-bar-chart.tsx
│   │   │   │
│   │   │   ├── share/
│   │   │   │   ├── share-card.tsx
│   │   │   │   ├── share-modal.tsx
│   │   │   │   ├── embed-code.tsx
│   │   │   │   ├── twitter-share.tsx
│   │   │   │   └── watermark.tsx
│   │   │   │
│   │   │   ├── billing/
│   │   │   │   ├── pricing-table.tsx
│   │   │   │   ├── plan-card.tsx
│   │   │   │   ├── usage-meter.tsx
│   │   │   │   ├── invoice-list.tsx
│   │   │   │   ├── payment-method.tsx
│   │   │   │   └── upgrade-banner.tsx
│   │   │   │
│   │   │   ├── settings/
│   │   │   │   ├── profile-form.tsx
│   │   │   │   ├── notification-settings.tsx
│   │   │   │   ├── api-key-manager.tsx
│   │   │   │   ├── team-member-list.tsx
│   │   │   │   ├── team-invite-form.tsx
│   │   │   │   ├── integration-card.tsx
│   │   │   │   └── danger-zone.tsx
│   │   │   │
│   │   │   ├── search/
│   │   │   │   ├── search-bar.tsx
│   │   │   │   ├── search-results.tsx
│   │   │   │   ├── search-filters.tsx
│   │   │   │   └── search-empty.tsx
│   │   │   │
│   │   │   ├── common/
│   │   │   │   ├── loading-spinner.tsx
│   │   │   │   ├── error-boundary.tsx
│   │   │   │   ├── empty-state.tsx
│   │   │   │   ├── confirm-dialog.tsx
│   │   │   │   ├── copy-button.tsx
│   │   │   │   ├── relative-time.tsx
│   │   │   │   ├── source-icon.tsx           # Google, Reddit, HN, etc icons
│   │   │   │   ├── trend-direction-arrow.tsx
│   │   │   │   ├── percentage-badge.tsx
│   │   │   │   ├── dot-pulse.tsx
│   │   │   │   ├── count-animation.tsx
│   │   │   │   └── logo.tsx
│   │   │   │
│   │   │   └── landing/
│   │   │       ├── hero.tsx
│   │   │       ├── features.tsx
│   │   │       ├── how-it-works.tsx          # Signal Intelligence pipeline visual
│   │   │       ├── social-proof.tsx
│   │   │       ├── comparison-table.tsx
│   │   │       ├── cta-section.tsx
│   │   │       ├── live-demo.tsx             # Live trend feed preview
│   │   │       ├── prediction-showcase.tsx
│   │   │       ├── source-logos.tsx           # "Powered by 15+ signal sources"
│   │   │       └── faq.tsx
│   │   │
│   │   ├── lib/
│   │   │   ├── supabase/
│   │   │   │   ├── client.ts
│   │   │   │   ├── server.ts
│   │   │   │   ├── middleware.ts
│   │   │   │   └── admin.ts
│   │   │   │
│   │   │   ├── api/
│   │   │   │   ├── client.ts               # API client wrapper
│   │   │   │   ├── trends.ts
│   │   │   │   ├── predictions.ts
│   │   │   │   ├── alerts.ts
│   │   │   │   ├── briefs.ts
│   │   │   │   ├── categories.ts
│   │   │   │   ├── search.ts
│   │   │   │   ├── billing.ts
│   │   │   │   ├── user.ts
│   │   │   │   ├── team.ts
│   │   │   │   └── admin.ts
│   │   │   │
│   │   │   ├── hooks/
│   │   │   │   ├── use-trends.ts
│   │   │   │   ├── use-predictions.ts
│   │   │   │   ├── use-alerts.ts
│   │   │   │   ├── use-realtime.ts         # WebSocket/SSE for live data
│   │   │   │   ├── use-subscription.ts
│   │   │   │   ├── use-user.ts
│   │   │   │   ├── use-debounce.ts
│   │   │   │   ├── use-local-storage.ts
│   │   │   │   ├── use-media-query.ts
│   │   │   │   └── use-infinite-scroll.ts
│   │   │   │
│   │   │   ├── utils/
│   │   │   │   ├── cn.ts
│   │   │   │   ├── formatters.ts
│   │   │   │   ├── constants.ts
│   │   │   │   ├── validators.ts           # Zod schemas
│   │   │   │   ├── colors.ts
│   │   │   │   ├── sources.ts              # Signal source metadata
│   │   │   │   └── url.ts
│   │   │   │
│   │   │   ├── store/
│   │   │   │   ├── filters.ts              # Zustand: filter state
│   │   │   │   ├── preferences.ts
│   │   │   │   └── realtime.ts
│   │   │   │
│   │   │   └── types/
│   │   │       ├── trend.ts
│   │   │       ├── prediction.ts
│   │   │       ├── alert.ts
│   │   │       ├── brief.ts
│   │   │       ├── category.ts
│   │   │       ├── user.ts
│   │   │       ├── billing.ts
│   │   │       ├── api.ts
│   │   │       ├── signal.ts               # Signal source types
│   │   │       └── source.ts               # Source enum + types
│   │   │
│   │   └── middleware.ts                   # Next.js middleware (auth check)
│   │
│   └── tests/
│       ├── e2e/
│       │   ├── auth.spec.ts
│       │   ├── explore.spec.ts
│       │   ├── predict.spec.ts
│       │   ├── alerts.spec.ts
│       │   └── billing.spec.ts
│       └── components/
│           ├── trend-card.test.tsx
│           ├── prediction-card.test.tsx
│           └── velocity-chart.test.tsx
│
├── backend/                                # FastAPI Backend
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── .env.example
│   ├── .env                                # .gitignore'd
│   ├── Dockerfile
│   ├── docker-compose.yml
│   │
│   ├── alembic/
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   └── versions/
│   │       ├── 001_initial_schema.py
│   │       ├── 002_add_predictions.py
│   │       ├── 003_add_alerts.py
│   │       ├── 004_add_billing.py
│   │       ├── 005_add_content_briefs.py
│   │       ├── 006_add_teams.py
│   │       ├── 007_add_api_keys.py
│   │       └── 008_add_share_cards.py
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                         # FastAPI app entry point
│   │   ├── config.py                       # Settings (Pydantic BaseSettings)
│   │   ├── database.py                     # Async SQLAlchemy setup
│   │   ├── dependencies.py                 # Dependency injection
│   │   │
│   │   ├── models/                         # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── user.py
│   │   │   ├── trend.py
│   │   │   ├── signal_event.py             # SignalEvent model (was TrendMention)
│   │   │   ├── trend_velocity.py
│   │   │   ├── prediction.py
│   │   │   ├── prediction_factor.py
│   │   │   ├── alert.py
│   │   │   ├── alert_trigger.py
│   │   │   ├── content_brief.py
│   │   │   ├── category.py
│   │   │   ├── subscription.py
│   │   │   ├── api_key.py
│   │   │   ├── team.py
│   │   │   ├── team_member.py
│   │   │   ├── share_card.py
│   │   │   ├── usage_log.py
│   │   │   ├── scan_log.py
│   │   │   └── source_health.py            # Signal source health tracking
│   │   │
│   │   ├── schemas/                        # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── trend.py
│   │   │   ├── prediction.py
│   │   │   ├── alert.py
│   │   │   ├── content_brief.py
│   │   │   ├── category.py
│   │   │   ├── user.py
│   │   │   ├── billing.py
│   │   │   ├── team.py
│   │   │   ├── api_key.py
│   │   │   ├── search.py
│   │   │   ├── signal.py                   # Signal event schemas
│   │   │   └── common.py
│   │   │
│   │   ├── api/                            # API routes
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── trends.py
│   │   │   │   ├── predictions.py
│   │   │   │   ├── alerts.py
│   │   │   │   ├── briefs.py
│   │   │   │   ├── categories.py
│   │   │   │   ├── search.py
│   │   │   │   ├── billing.py
│   │   │   │   ├── user.py
│   │   │   │   ├── team.py
│   │   │   │   ├── api_keys.py
│   │   │   │   ├── share.py
│   │   │   │   ├── webhooks.py
│   │   │   │   ├── health.py
│   │   │   │   ├── sources.py              # Signal source status endpoint
│   │   │   │   └── admin.py
│   │   │   │
│   │   │   └── public/
│   │   │       ├── __init__.py
│   │   │       ├── trends.py
│   │   │       └── share.py
│   │   │
│   │   ├── services/                       # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── trend_service.py
│   │   │   ├── prediction_service.py
│   │   │   ├── alert_service.py
│   │   │   ├── brief_service.py
│   │   │   ├── category_service.py
│   │   │   ├── search_service.py
│   │   │   ├── billing_service.py
│   │   │   ├── user_service.py
│   │   │   ├── team_service.py
│   │   │   ├── usage_service.py
│   │   │   ├── share_service.py
│   │   │   └── notification_service.py
│   │   │
│   │   ├── core/                           # Core engine modules
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── signals/                    # 📡 SIGNAL COLLECTION ENGINE
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py                 # BaseSignalAdapter (abstract)
│   │   │   │   ├── manager.py              # SignalManager (orchestrator)
│   │   │   │   ├── registry.py             # Signal Source Registry
│   │   │   │   ├── adapters/               # Signal source adapters
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── google_trends.py    # Google Trends via pytrends
│   │   │   │   │   ├── reddit.py           # Reddit Rising/Hot via PRAW
│   │   │   │   │   ├── hackernews.py       # HN Firebase API
│   │   │   │   │   ├── youtube.py          # YouTube Data API trending
│   │   │   │   │   ├── github.py           # GitHub Trending scrape + API
│   │   │   │   │   ├── wikipedia.py        # Wikipedia Pageviews API
│   │   │   │   │   ├── google_news.py      # Google News RSS
│   │   │   │   │   ├── producthunt.py      # Product Hunt GraphQL
│   │   │   │   │   ├── npm_registry.py     # npm download stats
│   │   │   │   │   ├── pypi_stats.py       # PyPI download stats
│   │   │   │   │   ├── arxiv.py            # ArXiv papers
│   │   │   │   │   ├── coingecko.py        # CoinGecko crypto data
│   │   │   │   │   ├── steam_charts.py     # Steam player stats
│   │   │   │   │   ├── devto.py            # Dev.to articles
│   │   │   │   │   ├── lobsters.py         # Lobste.rs stories
│   │   │   │   │   ├── stackoverflow.py    # Stack Overflow tags/questions
│   │   │   │   │   └── twitter.py          # Twitter (optional, paid)
│   │   │   │   │
│   │   │   │   ├── normalizer.py           # Topic normalization
│   │   │   │   ├── deduplicator.py         # Cross-source deduplication
│   │   │   │   └── topic_extractor.py      # Extract topic from signals
│   │   │   │
│   │   │   ├── correlation/                # 🔗 CROSS-SOURCE CORRELATION ENGINE
│   │   │   │   ├── __init__.py
│   │   │   │   ├── engine.py               # CorrelationEngine main class
│   │   │   │   ├── detector.py             # Cross-source signal detector
│   │   │   │   ├── scorer.py               # Correlation scoring
│   │   │   │   ├── patterns.py             # Known correlation patterns
│   │   │   │   └── timeline.py             # Spread timeline construction
│   │   │   │
│   │   │   ├── velocity/                   # 📈 VELOCITY ANALYZER ENGINE
│   │   │   │   ├── __init__.py
│   │   │   │   ├── analyzer.py
│   │   │   │   ├── calculator.py
│   │   │   │   ├── scorer.py
│   │   │   │   ├── time_series.py
│   │   │   │   └── thresholds.py
│   │   │   │
│   │   │   ├── predictor/                  # 🔮 PREDICTION ENGINE
│   │   │   │   ├── __init__.py
│   │   │   │   ├── engine.py
│   │   │   │   ├── features.py
│   │   │   │   ├── model.py
│   │   │   │   ├── confidence.py
│   │   │   │   ├── timing.py
│   │   │   │   ├── calibrator.py
│   │   │   │   └── evaluator.py
│   │   │   │
│   │   │   ├── classifier/                 # 🏷️ CATEGORY CLASSIFIER
│   │   │   │   ├── __init__.py
│   │   │   │   ├── engine.py
│   │   │   │   ├── categories.py
│   │   │   │   ├── prompts.py
│   │   │   │   └── embeddings.py
│   │   │   │
│   │   │   └── brief_generator/            # 📝 CONTENT BRIEF GENERATOR
│   │   │       ├── __init__.py
│   │   │       ├── engine.py
│   │   │       ├── prompts.py
│   │   │       ├── formats.py
│   │   │       └── templates.py
│   │   │
│   │   ├── ai/                             # AI/LLM integration
│   │   │   ├── __init__.py
│   │   │   ├── client.py                   # Claude API client wrapper
│   │   │   ├── prompts/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── prediction.py
│   │   │   │   ├── classification.py
│   │   │   │   ├── content_brief.py
│   │   │   │   ├── trend_summary.py
│   │   │   │   └── topic_extraction.py     # Extract topics from raw signals
│   │   │   │
│   │   │   ├── guardrails.py
│   │   │   └── rate_limiter.py
│   │   │
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── supabase.py
│   │   │   ├── jwt.py
│   │   │   ├── permissions.py
│   │   │   ├── api_key_auth.py
│   │   │   └── middleware.py
│   │   │
│   │   ├── billing/
│   │   │   ├── __init__.py
│   │   │   ├── stripe_client.py
│   │   │   ├── plans.py
│   │   │   ├── webhooks.py
│   │   │   └── usage_tracker.py
│   │   │
│   │   ├── tasks/                          # Celery tasks
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py
│   │   │   ├── signal_collection.py        # Scheduled signal collection
│   │   │   ├── correlation.py              # Cross-source correlation
│   │   │   ├── velocity.py                 # Velocity recalculation
│   │   │   ├── predictions.py              # Prediction generation
│   │   │   ├── alerts.py                   # Alert checking
│   │   │   ├── briefs.py                   # Content brief generation
│   │   │   ├── cleanup.py                  # Data cleanup
│   │   │   ├── share_cards.py              # OG image generation
│   │   │   ├── source_health.py            # Signal source health checks
│   │   │   └── analytics.py
│   │   │
│   │   ├── realtime/
│   │   │   ├── __init__.py
│   │   │   ├── websocket.py
│   │   │   ├── sse.py
│   │   │   └── channels.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── security.py
│   │       ├── encryption.py
│   │       ├── rate_limiter.py
│   │       ├── pagination.py
│   │       ├── cache.py
│   │       └── logging.py
│   │
│   └── tests/
│       ├── conftest.py
│       ├── test_signals/
│       │   ├── test_google_trends.py
│       │   ├── test_reddit.py
│       │   ├── test_hackernews.py
│       │   ├── test_github.py
│       │   ├── test_wikipedia.py
│       │   └── test_signal_manager.py
│       ├── test_correlation.py
│       ├── test_velocity.py
│       ├── test_predictions.py
│       ├── test_alerts.py
│       ├── test_billing.py
│       ├── test_auth.py
│       └── test_share.py
│
├── AGENTS.md
├── plan.md
├── .gitignore
├── .claudecodeignore
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## 🗄️ БАЗА ДАННЫХ (PostgreSQL 16 + Supabase)

### Принципы
- **RLS (Row Level Security) на КАЖДОЙ таблице** — даже если AI генерит кривой SQL, база НЕ отдаст чужие данные
- **UUID v7 для primary keys** — сортируемые по времени
- **Все timestamps в UTC**
- **Soft delete** — `deleted_at` вместо DELETE
- **Аудит** — `created_at`, `updated_at` на каждой таблице
- **Индексы** — на все foreign keys + часто запрашиваемые поля
- **Partitioning** — `signal_events` партиционируется по месяцам

### Общие функции

```sql
-- Trigger для автоматического updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Таблица: `users`
```sql
CREATE TABLE public.users (
    id              UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email           TEXT NOT NULL UNIQUE,
    full_name       TEXT,
    avatar_url      TEXT,
    username        TEXT UNIQUE,
    bio             TEXT,
    timezone        TEXT DEFAULT 'UTC',
    locale          TEXT DEFAULT 'en',
    
    -- Subscription
    plan            TEXT NOT NULL DEFAULT 'free' CHECK (plan IN ('free', 'creator', 'pro', 'business', 'enterprise')),
    stripe_customer_id    TEXT UNIQUE,
    stripe_subscription_id TEXT UNIQUE,
    subscription_status   TEXT DEFAULT 'active' CHECK (subscription_status IN ('active', 'canceled', 'past_due', 'trialing', 'paused')),
    trial_ends_at         TIMESTAMPTZ,
    current_period_end    TIMESTAMPTZ,
    
    -- Preferences
    preferred_categories  TEXT[] DEFAULT '{}',
    preferred_sources     TEXT[] DEFAULT '{}',
    email_notifications   BOOLEAN DEFAULT true,
    push_notifications    BOOLEAN DEFAULT false,
    weekly_digest         BOOLEAN DEFAULT true,
    
    -- Usage tracking
    daily_trend_views     INTEGER DEFAULT 0,
    daily_brief_count     INTEGER DEFAULT 0,
    last_trend_reset      DATE DEFAULT CURRENT_DATE,
    last_brief_reset      DATE DEFAULT CURRENT_DATE,
    
    -- Metadata
    onboarding_completed  BOOLEAN DEFAULT false,
    last_seen_at          TIMESTAMPTZ,
    created_at            TIMESTAMPTZ DEFAULT NOW(),
    updated_at            TIMESTAMPTZ DEFAULT NOW(),
    deleted_at            TIMESTAMPTZ
);

CREATE INDEX idx_users_plan ON public.users(plan);
CREATE INDEX idx_users_stripe_customer ON public.users(stripe_customer_id) WHERE stripe_customer_id IS NOT NULL;
CREATE INDEX idx_users_email ON public.users(email);

ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile" ON public.users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON public.users FOR UPDATE USING (auth.uid() = id) WITH CHECK (auth.uid() = id);
CREATE POLICY "Users can insert own profile" ON public.users FOR INSERT WITH CHECK (auth.uid() = id);

CREATE TRIGGER users_updated_at BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Таблица: `categories`
```sql
CREATE TABLE public.categories (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug            TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    description     TEXT,
    icon            TEXT,
    color           TEXT NOT NULL DEFAULT '#6366f1',
    parent_id       UUID REFERENCES public.categories(id),
    sort_order      INTEGER DEFAULT 0,
    is_default      BOOLEAN DEFAULT false,
    is_active       BOOLEAN DEFAULT true,
    trend_count_24h INTEGER DEFAULT 0,
    trend_count_7d  INTEGER DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_categories_slug ON public.categories(slug);
ALTER TABLE public.categories ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can view active categories" ON public.categories FOR SELECT USING (is_active = true);

INSERT INTO public.categories (slug, name, icon, color, is_default, sort_order) VALUES
    ('tech', 'Technology', 'Cpu', '#6366f1', true, 1),
    ('ai', 'Artificial Intelligence', 'Brain', '#8b5cf6', true, 2),
    ('crypto', 'Crypto & Web3', 'Bitcoin', '#f59e0b', true, 3),
    ('business', 'Business', 'Briefcase', '#10b981', true, 4),
    ('science', 'Science', 'Atom', '#06b6d4', true, 5),
    ('health', 'Health & Wellness', 'Heart', '#ef4444', true, 6),
    ('culture', 'Culture & Entertainment', 'Music', '#ec4899', true, 7),
    ('politics', 'Politics', 'Landmark', '#64748b', true, 8),
    ('gaming', 'Gaming', 'Gamepad2', '#84cc16', true, 9),
    ('finance', 'Finance & Markets', 'TrendingUp', '#0ea5e9', true, 10),
    ('sports', 'Sports', 'Trophy', '#f97316', true, 11),
    ('design', 'Design & UX', 'Palette', '#d946ef', true, 12),
    ('devtools', 'Developer Tools', 'Code', '#22d3ee', true, 13),
    ('opensource', 'Open Source', 'GitBranch', '#a3e635', true, 14);
```

### Таблица: `trends`
```sql
CREATE TABLE public.trends (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Core
    topic           TEXT NOT NULL,
    topic_slug      TEXT NOT NULL,
    description     TEXT,
    summary         TEXT,
    
    -- Classification
    category_id     UUID REFERENCES public.categories(id),
    subcategory     TEXT,
    tags            TEXT[] DEFAULT '{}',
    
    -- Scoring
    trend_score     FLOAT NOT NULL DEFAULT 0,         -- composite 0-100
    velocity_score  FLOAT DEFAULT 0,
    correlation_score FLOAT DEFAULT 0,                -- cross-source correlation (0-100)
    signal_strength FLOAT DEFAULT 0,                  -- overall signal strength (0-100)
    sentiment_score FLOAT DEFAULT 0,                  -- -1 to 1
    
    -- Signal data
    signal_count_1h  INTEGER DEFAULT 0,               -- signals received in last hour
    signal_count_6h  INTEGER DEFAULT 0,
    signal_count_24h INTEGER DEFAULT 0,
    signal_count_7d  INTEGER DEFAULT 0,
    velocity_1h      FLOAT DEFAULT 0,                 -- signal velocity
    velocity_6h      FLOAT DEFAULT 0,
    velocity_24h     FLOAT DEFAULT 0,
    acceleration     FLOAT DEFAULT 0,
    
    -- Source presence
    active_sources   TEXT[] DEFAULT '{}',              -- ['google_trends', 'reddit', 'hackernews']
    source_count     INTEGER DEFAULT 0,               -- how many sources detect this
    first_source     TEXT,                             -- where first detected
    first_seen_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Status
    status          TEXT DEFAULT 'active' CHECK (status IN ('emerging', 'active', 'peaking', 'declining', 'dead')),
    peak_at         TIMESTAMPTZ,
    is_viral        BOOLEAN DEFAULT false,
    is_breaking     BOOLEAN DEFAULT false,
    
    -- AI analysis
    ai_analysis     JSONB DEFAULT '{}',
    last_ai_update  TIMESTAMPTZ,
    
    -- Engagement
    view_count      INTEGER DEFAULT 0,
    share_count     INTEGER DEFAULT 0,
    bookmark_count  INTEGER DEFAULT 0,
    
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);

CREATE INDEX idx_trends_score ON public.trends(trend_score DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_trends_velocity ON public.trends(velocity_24h DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_trends_category ON public.trends(category_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_trends_status ON public.trends(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_trends_sources ON public.trends USING GIN(active_sources) WHERE deleted_at IS NULL;
CREATE INDEX idx_trends_tags ON public.trends USING GIN(tags) WHERE deleted_at IS NULL;
CREATE INDEX idx_trends_created ON public.trends(created_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_trends_topic_slug ON public.trends(topic_slug);
CREATE INDEX idx_trends_topic_search ON public.trends USING GIN(to_tsvector('english', topic || ' ' || COALESCE(description, '')));

ALTER TABLE public.trends ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can view active trends" ON public.trends FOR SELECT USING (deleted_at IS NULL);
CREATE TRIGGER trends_updated_at BEFORE UPDATE ON public.trends FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Таблица: `signal_events` (заменяет trend_mentions)
```sql
-- Ключевая таблица: каждый сигнал от каждого источника
-- Партиционирование по месяцам (будет расти быстро)

CREATE TABLE public.signal_events (
    id              UUID DEFAULT gen_random_uuid(),
    trend_id        UUID REFERENCES public.trends(id) ON DELETE CASCADE,
    
    -- Source identification
    source          TEXT NOT NULL CHECK (source IN (
        'google_trends', 'reddit', 'hackernews', 'youtube_trending',
        'github_trending', 'wikipedia', 'google_news',
        'producthunt', 'npm_registry', 'pypi_stats', 'arxiv',
        'coingecko', 'steam_charts', 'devto', 'lobsters',
        'stackoverflow', 'subreddit_stats', 'twitter', 'newsapi'
    )),
    
    -- Signal data (varies by source type)
    signal_type     TEXT NOT NULL CHECK (signal_type IN (
        'trending',           -- appeared in trending/rising list
        'velocity_spike',     -- sudden increase in metric
        'new_entry',          -- new item appeared (new repo, new paper, new product)
        'score_spike',        -- score/upvotes/stars exceeded threshold
        'search_interest',    -- Google Trends interest rise
        'pageview_spike',     -- Wikipedia pageview spike
        'download_spike',     -- npm/PyPI download spike
        'price_movement',     -- crypto price movement
        'player_spike',       -- Steam player count spike
        'ranking_change'      -- ranking position change
    )),
    
    -- Signal details
    signal_title    TEXT,                               -- что именно (repo name, article title, etc.)
    signal_url      TEXT,                               -- URL источника
    signal_value    FLOAT DEFAULT 0,                    -- числовое значение (score, stars, downloads)
    signal_delta    FLOAT DEFAULT 0,                    -- изменение (%, абсолютное)
    signal_rank     INTEGER,                            -- позиция в списке (если применимо)
    
    -- Extracted topic (normalized)
    extracted_topic TEXT,                               -- topic extracted from this signal
    
    -- Context
    context_data    JSONB DEFAULT '{}',                 -- source-specific raw data
    -- Examples:
    -- Google Trends:  {"interest": 85, "related_queries": [...], "region": "US"}
    -- Reddit:         {"subreddit": "r/technology", "score": 4500, "comments": 320, "author": "u/..."}
    -- HN:             {"hn_score": 450, "comments": 120, "by": "dang"}
    -- GitHub:         {"stars": 2500, "stars_today": 800, "language": "Python", "description": "..."}
    -- Wikipedia:      {"pageviews_today": 50000, "pageviews_avg": 2000, "spike_ratio": 25.0}
    -- YouTube:        {"view_count": 1500000, "like_count": 45000, "channel": "..."}
    -- npm:            {"downloads_week": 500000, "downloads_prev_week": 50000, "growth": 900}
    -- CoinGecko:      {"price_change_24h": 15.5, "volume_24h": 5000000, "market_cap_rank": 42}
    -- Steam:          {"current_players": 150000, "peak_today": 200000, "avg_30d": 50000}
    
    -- Quality
    signal_weight   FLOAT DEFAULT 0.5,                  -- computed quality/importance (0-1)
    is_noise        BOOLEAN DEFAULT false,               -- flagged as noise by deduplicator
    
    -- Timing
    detected_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),  -- when we detected the signal
    source_timestamp TIMESTAMPTZ,                        -- when the signal originated (if known)
    
    PRIMARY KEY (id, detected_at)
) PARTITION BY RANGE (detected_at);

-- Партиции на 12 месяцев
CREATE TABLE signal_events_2026_01 PARTITION OF signal_events FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE signal_events_2026_02 PARTITION OF signal_events FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE signal_events_2026_03 PARTITION OF signal_events FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE signal_events_2026_04 PARTITION OF signal_events FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE signal_events_2026_05 PARTITION OF signal_events FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
CREATE TABLE signal_events_2026_06 PARTITION OF signal_events FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
CREATE TABLE signal_events_2026_07 PARTITION OF signal_events FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');
CREATE TABLE signal_events_2026_08 PARTITION OF signal_events FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');
CREATE TABLE signal_events_2026_09 PARTITION OF signal_events FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');
CREATE TABLE signal_events_2026_10 PARTITION OF signal_events FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
CREATE TABLE signal_events_2026_11 PARTITION OF signal_events FOR VALUES FROM ('2026-11-01') TO ('2026-12-01');
CREATE TABLE signal_events_2026_12 PARTITION OF signal_events FOR VALUES FROM ('2026-12-01') TO ('2027-01-01');

CREATE INDEX idx_signals_trend ON public.signal_events(trend_id);
CREATE INDEX idx_signals_source ON public.signal_events(source);
CREATE INDEX idx_signals_detected ON public.signal_events(detected_at DESC);
CREATE INDEX idx_signals_type ON public.signal_events(signal_type);
CREATE INDEX idx_signals_topic ON public.signal_events(extracted_topic);

ALTER TABLE public.signal_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can view signals" ON public.signal_events FOR SELECT USING (true);
```

### Таблица: `source_health` (отслеживание здоровья источников)
```sql
CREATE TABLE public.source_health (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source          TEXT NOT NULL,
    
    -- Health metrics
    is_healthy      BOOLEAN DEFAULT true,
    last_success    TIMESTAMPTZ,
    last_failure    TIMESTAMPTZ,
    consecutive_failures INTEGER DEFAULT 0,
    
    -- Performance
    avg_response_ms INTEGER DEFAULT 0,
    signals_collected_24h INTEGER DEFAULT 0,
    api_calls_24h   INTEGER DEFAULT 0,
    
    -- Rate limiting
    rate_limit_remaining INTEGER,
    rate_limit_reset     TIMESTAMPTZ,
    
    -- Errors
    last_error      TEXT,
    error_count_24h INTEGER DEFAULT 0,
    
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_source_health_source ON public.source_health(source);
ALTER TABLE public.source_health ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can view source health" ON public.source_health FOR SELECT USING (true);
```

### Таблица: `trend_velocity_snapshots`
```sql
CREATE TABLE public.trend_velocity_snapshots (
    id              UUID DEFAULT gen_random_uuid(),
    trend_id        UUID NOT NULL REFERENCES public.trends(id) ON DELETE CASCADE,
    
    signals_total   INTEGER DEFAULT 0,
    signals_delta   INTEGER DEFAULT 0,
    velocity        FLOAT DEFAULT 0,
    acceleration    FLOAT DEFAULT 0,
    
    -- Per-source breakdown
    source_data     JSONB DEFAULT '{}',  -- {"google_trends": 85, "reddit": 45, "hackernews": 320, ...}
    
    -- Correlation at this time
    correlation_score FLOAT DEFAULT 0,
    active_sources    INTEGER DEFAULT 0,
    
    -- Prediction at this time
    predicted_peak  TIMESTAMPTZ,
    prediction_confidence FLOAT,
    
    snapshot_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id, snapshot_at)
) PARTITION BY RANGE (snapshot_at);

CREATE TABLE velocity_snapshots_2026_01 PARTITION OF trend_velocity_snapshots FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE velocity_snapshots_2026_02 PARTITION OF trend_velocity_snapshots FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE velocity_snapshots_2026_03 PARTITION OF trend_velocity_snapshots FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
-- ... остальные месяцы аналогично

CREATE INDEX idx_velocity_trend ON public.trend_velocity_snapshots(trend_id, snapshot_at DESC);
ALTER TABLE public.trend_velocity_snapshots ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can view velocity" ON public.trend_velocity_snapshots FOR SELECT USING (true);
```

### Таблица: `predictions`
```sql
CREATE TABLE public.predictions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trend_id        UUID NOT NULL REFERENCES public.trends(id) ON DELETE CASCADE,
    
    predicted_growth    FLOAT NOT NULL,
    predicted_peak_at   TIMESTAMPTZ NOT NULL,
    predicted_peak_score FLOAT,
    confidence          FLOAT NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    timeframe_hours     INTEGER NOT NULL DEFAULT 72,
    
    -- What signals drove this prediction
    source_signals      JSONB DEFAULT '[]',  -- which sources were firing when prediction was made
    -- Example: [
    --   {"source": "google_trends", "signal_type": "search_interest", "value": 85, "weight": 0.9},
    --   {"source": "reddit", "signal_type": "trending", "value": 4500, "weight": 0.85},
    --   {"source": "hackernews", "signal_type": "score_spike", "value": 450, "weight": 0.85},
    -- ]
    
    -- Correlation data
    correlation_data    JSONB DEFAULT '{}',
    -- {"sources_firing": 5, "correlation_multiplier": 1.8, "pattern": "tech_breakout"}
    
    -- Factor breakdown
    factors             JSONB DEFAULT '[]',
    
    -- AI analysis
    ai_reasoning        TEXT,
    ai_model_version    TEXT,
    
    -- Status
    status              TEXT DEFAULT 'active' CHECK (status IN ('active', 'expired', 'validated', 'invalidated')),
    
    -- Outcome tracking
    actual_growth       FLOAT,
    actual_peak_at      TIMESTAMPTZ,
    accuracy_score      FLOAT,
    validated_at        TIMESTAMPTZ,
    
    -- Plan gating
    prediction_tier     TEXT DEFAULT 'basic' CHECK (prediction_tier IN ('basic', 'full')),
    
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW(),
    expires_at          TIMESTAMPTZ
);

CREATE INDEX idx_predictions_trend ON public.predictions(trend_id);
CREATE INDEX idx_predictions_confidence ON public.predictions(confidence DESC) WHERE status = 'active';
CREATE INDEX idx_predictions_status ON public.predictions(status);
CREATE INDEX idx_predictions_created ON public.predictions(created_at DESC);

ALTER TABLE public.predictions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view predictions based on plan" ON public.predictions FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.users u
            WHERE u.id = auth.uid()
            AND (
                u.plan IN ('pro', 'business', 'enterprise')
                OR (u.plan = 'creator' AND prediction_tier = 'basic')
            )
        )
    );

CREATE TRIGGER predictions_updated_at BEFORE UPDATE ON public.predictions FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Таблицы: `alerts`, `alert_triggers`, `content_briefs`, `subscriptions`, `api_keys`, `teams`, `team_members`, `share_cards`, `usage_logs`, `user_bookmarks`, `user_custom_categories`

### Таблица: `alerts`
```sql
CREATE TABLE public.alerts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    name            TEXT NOT NULL,
    description     TEXT,
    categories      TEXT[] DEFAULT '{}',
    keywords        TEXT[] DEFAULT '{}',
    exclude_keywords TEXT[] DEFAULT '{}',
    sources         TEXT[] DEFAULT '{}',              -- signal sources filter (empty = all)
    min_velocity    FLOAT DEFAULT 50,
    min_correlation FLOAT DEFAULT 30,                 -- minimum correlation_score
    min_confidence  FLOAT DEFAULT 0.5,
    notify_email    BOOLEAN DEFAULT true,
    notify_push     BOOLEAN DEFAULT false,
    notify_webhook  BOOLEAN DEFAULT false,
    webhook_url     TEXT,
    is_active       BOOLEAN DEFAULT true,
    frequency       TEXT DEFAULT 'instant' CHECK (frequency IN ('instant', 'hourly', 'daily', 'weekly')),
    quiet_hours_start TEXT,
    quiet_hours_end   TEXT,
    trigger_count   INTEGER DEFAULT 0,
    last_triggered  TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);

CREATE INDEX idx_alerts_user ON public.alerts(user_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_alerts_active ON public.alerts(is_active) WHERE deleted_at IS NULL AND is_active = true;
CREATE INDEX idx_alerts_categories ON public.alerts USING GIN(categories);
CREATE INDEX idx_alerts_keywords ON public.alerts USING GIN(keywords);

ALTER TABLE public.alerts ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can manage own alerts" ON public.alerts FOR ALL
    USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE TRIGGER alerts_updated_at BEFORE UPDATE ON public.alerts FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Таблица: `alert_triggers`
```sql
CREATE TABLE public.alert_triggers (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    alert_id        UUID NOT NULL REFERENCES public.alerts(id) ON DELETE CASCADE,
    trend_id        UUID NOT NULL REFERENCES public.trends(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    trigger_reason  TEXT,
    velocity_at_trigger FLOAT,
    correlation_at_trigger FLOAT,
    notified_email  BOOLEAN DEFAULT false,
    notified_push   BOOLEAN DEFAULT false,
    notified_webhook BOOLEAN DEFAULT false,
    notification_sent_at TIMESTAMPTZ,
    is_read         BOOLEAN DEFAULT false,
    read_at         TIMESTAMPTZ,
    is_dismissed    BOOLEAN DEFAULT false,
    triggered_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_alert_triggers_user ON public.alert_triggers(user_id, triggered_at DESC);
CREATE INDEX idx_alert_triggers_unread ON public.alert_triggers(user_id) WHERE is_read = false;

ALTER TABLE public.alert_triggers ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own triggers" ON public.alert_triggers FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update own triggers" ON public.alert_triggers FOR UPDATE USING (auth.uid() = user_id);
```

### Таблица: `content_briefs`
```sql
CREATE TABLE public.content_briefs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trend_id        UUID NOT NULL REFERENCES public.trends(id) ON DELETE CASCADE,
    user_id         UUID REFERENCES public.users(id) ON DELETE SET NULL,
    title           TEXT NOT NULL,
    format          TEXT NOT NULL CHECK (format IN ('article', 'video', 'thread', 'short_post', 'newsletter', 'podcast')),
    hook            TEXT,
    key_points      JSONB DEFAULT '[]',
    target_audience TEXT,
    tone            TEXT,
    estimated_length TEXT,
    suggested_hashtags TEXT[] DEFAULT '{}',
    seo_keywords    TEXT[] DEFAULT '{}',
    best_platforms  TEXT[] DEFAULT '{}',
    optimal_publish_time TEXT,
    full_brief      TEXT NOT NULL,
    ai_model_version TEXT,
    generation_tokens INTEGER,
    is_premium      BOOLEAN DEFAULT false,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_briefs_trend ON public.content_briefs(trend_id);
CREATE INDEX idx_briefs_user ON public.content_briefs(user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_briefs_created ON public.content_briefs(created_at DESC);

ALTER TABLE public.content_briefs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view briefs based on plan" ON public.content_briefs FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.users WHERE id = auth.uid()
            AND plan IN ('creator', 'pro', 'business', 'enterprise')
        )
    );
CREATE TRIGGER briefs_updated_at BEFORE UPDATE ON public.content_briefs FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Таблица: `subscriptions`
```sql
CREATE TABLE public.subscriptions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    stripe_subscription_id TEXT NOT NULL UNIQUE,
    stripe_price_id     TEXT NOT NULL,
    stripe_customer_id  TEXT NOT NULL,
    plan                TEXT NOT NULL CHECK (plan IN ('creator', 'pro', 'business', 'enterprise')),
    billing_interval    TEXT NOT NULL CHECK (billing_interval IN ('month', 'year')),
    status              TEXT NOT NULL DEFAULT 'active' CHECK (status IN (
        'active', 'canceled', 'past_due', 'trialing', 'paused', 'incomplete', 'incomplete_expired'
    )),
    current_period_start TIMESTAMPTZ,
    current_period_end   TIMESTAMPTZ,
    cancel_at           TIMESTAMPTZ,
    canceled_at         TIMESTAMPTZ,
    trial_start         TIMESTAMPTZ,
    trial_end           TIMESTAMPTZ,
    seats_total         INTEGER DEFAULT 1,
    seats_used          INTEGER DEFAULT 1,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_user ON public.subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe ON public.subscriptions(stripe_subscription_id);

ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own subscriptions" ON public.subscriptions FOR SELECT USING (auth.uid() = user_id);
CREATE TRIGGER subscriptions_updated_at BEFORE UPDATE ON public.subscriptions FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Таблица: `api_keys`
```sql
CREATE TABLE public.api_keys (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    name            TEXT NOT NULL DEFAULT 'Default',
    key_prefix      TEXT NOT NULL,                    -- "tr_live_aBcD..."
    key_hash        TEXT NOT NULL,                    -- SHA-256
    scopes          TEXT[] DEFAULT '{read}',
    last_used_at    TIMESTAMPTZ,
    usage_count     INTEGER DEFAULT 0,
    rate_limit_rpm  INTEGER DEFAULT 60,
    is_active       BOOLEAN DEFAULT true,
    expires_at      TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    revoked_at      TIMESTAMPTZ
);

CREATE INDEX idx_api_keys_user ON public.api_keys(user_id) WHERE revoked_at IS NULL;
CREATE INDEX idx_api_keys_hash ON public.api_keys(key_hash) WHERE is_active = true;

ALTER TABLE public.api_keys ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can manage own API keys" ON public.api_keys FOR ALL
    USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
```

### Таблица: `teams`
```sql
CREATE TABLE public.teams (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            TEXT NOT NULL,
    slug            TEXT NOT NULL UNIQUE,
    owner_id        UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    logo_url        TEXT,
    max_seats       INTEGER DEFAULT 5,
    custom_categories JSONB DEFAULT '[]',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);

CREATE INDEX idx_teams_owner ON public.teams(owner_id);
ALTER TABLE public.teams ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Team members can view team" ON public.teams FOR SELECT
    USING (EXISTS (SELECT 1 FROM public.team_members WHERE team_id = id AND user_id = auth.uid() AND status = 'active'));
CREATE POLICY "Team owner can manage" ON public.teams FOR ALL
    USING (auth.uid() = owner_id) WITH CHECK (auth.uid() = owner_id);
```

### Таблица: `team_members`
```sql
CREATE TABLE public.team_members (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id         UUID NOT NULL REFERENCES public.teams(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    role            TEXT NOT NULL DEFAULT 'member' CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
    status          TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('active', 'pending', 'removed')),
    invited_by      UUID REFERENCES public.users(id),
    invited_email   TEXT,
    joined_at       TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(team_id, user_id)
);

CREATE INDEX idx_team_members_team ON public.team_members(team_id) WHERE status = 'active';
CREATE INDEX idx_team_members_user ON public.team_members(user_id) WHERE status = 'active';

ALTER TABLE public.team_members ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Team members can view" ON public.team_members FOR SELECT
    USING (EXISTS (SELECT 1 FROM public.team_members tm WHERE tm.team_id = team_id AND tm.user_id = auth.uid() AND tm.status = 'active'));
```

### Таблица: `share_cards`
```sql
CREATE TABLE public.share_cards (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trend_id        UUID NOT NULL REFERENCES public.trends(id) ON DELETE CASCADE,
    card_type       TEXT NOT NULL DEFAULT 'trend' CHECK (card_type IN ('trend', 'prediction', 'comparison')),
    og_image_url    TEXT,
    og_image_hash   TEXT,
    card_data       JSONB NOT NULL DEFAULT '{}',
    share_token     TEXT NOT NULL UNIQUE,
    view_count      INTEGER DEFAULT 0,
    allow_embed     BOOLEAN DEFAULT true,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    expires_at      TIMESTAMPTZ
);

CREATE INDEX idx_share_cards_token ON public.share_cards(share_token);
ALTER TABLE public.share_cards ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can view share cards" ON public.share_cards FOR SELECT USING (true);
```

### Таблица: `usage_logs`
```sql
CREATE TABLE public.usage_logs (
    id              UUID DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    action          TEXT NOT NULL CHECK (action IN (
        'trend_view', 'prediction_view', 'brief_generate',
        'alert_create', 'api_call', 'export', 'share_card_create'
    )),
    resource_id     UUID,
    resource_type   TEXT,
    metadata        JSONB DEFAULT '{}',
    ip_address      INET,
    user_agent      TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

CREATE TABLE usage_logs_2026_01 PARTITION OF usage_logs FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE usage_logs_2026_02 PARTITION OF usage_logs FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE usage_logs_2026_03 PARTITION OF usage_logs FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE usage_logs_2026_04 PARTITION OF usage_logs FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE usage_logs_2026_05 PARTITION OF usage_logs FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
CREATE TABLE usage_logs_2026_06 PARTITION OF usage_logs FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
CREATE TABLE usage_logs_2026_07 PARTITION OF usage_logs FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');
CREATE TABLE usage_logs_2026_08 PARTITION OF usage_logs FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');
CREATE TABLE usage_logs_2026_09 PARTITION OF usage_logs FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');
CREATE TABLE usage_logs_2026_10 PARTITION OF usage_logs FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
CREATE TABLE usage_logs_2026_11 PARTITION OF usage_logs FOR VALUES FROM ('2026-11-01') TO ('2026-12-01');
CREATE TABLE usage_logs_2026_12 PARTITION OF usage_logs FOR VALUES FROM ('2026-12-01') TO ('2027-01-01');

CREATE INDEX idx_usage_user_action ON public.usage_logs(user_id, action, created_at DESC);
ALTER TABLE public.usage_logs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own usage" ON public.usage_logs FOR SELECT USING (auth.uid() = user_id);
```

### Таблица: `user_bookmarks`
```sql
CREATE TABLE public.user_bookmarks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    trend_id        UUID NOT NULL REFERENCES public.trends(id) ON DELETE CASCADE,
    note            TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, trend_id)
);

CREATE INDEX idx_bookmarks_user ON public.user_bookmarks(user_id, created_at DESC);
ALTER TABLE public.user_bookmarks ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can manage own bookmarks" ON public.user_bookmarks FOR ALL
    USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
```

### Таблица: `user_custom_categories` (Business+)
```sql
CREATE TABLE public.user_custom_categories (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    team_id         UUID REFERENCES public.teams(id) ON DELETE CASCADE,
    name            TEXT NOT NULL,
    slug            TEXT NOT NULL,
    keywords        TEXT[] NOT NULL DEFAULT '{}',
    exclude_keywords TEXT[] DEFAULT '{}',
    color           TEXT DEFAULT '#6366f1',
    icon            TEXT DEFAULT 'Tag',
    is_active       BOOLEAN DEFAULT true,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, slug)
);

ALTER TABLE public.user_custom_categories ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can manage own" ON public.user_custom_categories FOR ALL
    USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
```

### Redis Schema

```
# Signal data cache
signal:latest:{source}              → JSON (last signal batch from source, TTL: 5 min)
signal:queue:{source}               → List (pending signals to process)

# Trend cache
trend:{trend_id}                    → JSON (full trend object, TTL: 5 min)
trend:feed:explore                  → Sorted Set (trend_ids by score)
trend:feed:category:{slug}          → Sorted Set
trend:velocity:{trend_id}           → Time Series (last 72h)

# Cross-source correlation
correlation:topic:{topic_hash}      → Set (source names that detected this topic)
correlation:active                  → Sorted Set (topics by correlation score)

# Rate limiting
rate:user:{user_id}:trends          → Counter (TTL: 24h)
rate:user:{user_id}:briefs          → Counter (TTL: 24h)
rate:user:{user_id}:api             → Counter (TTL: 60s)
rate:ip:{ip}:global                 → Counter (TTL: 60s)
rate:source:{source}:api            → Counter (per-source rate limit tracking)

# Source health
source:health:{source}              → JSON (health status, TTL: 1 min)
source:lock:{source}                → Lock (prevent duplicate scans, TTL: 5 min)
source:last:{source}                → Timestamp (last successful collection)

# Topic deduplication
topic:hash:{hash}                   → trend_id (TTL: 7 days)
topic:embedding:{trend_id}          → Binary (embedding vector, TTL: 24h)

# Prediction cache
prediction:active                   → Sorted Set (prediction_ids by confidence)
prediction:{prediction_id}          → JSON (TTL: 1h)

# User/session
user:prefs:{user_id}                → JSON (TTL: 1h)
user:plan:{user_id}                 → String (TTL: 5 min)

# Pub/Sub
channel:trends:new                  → Pub/Sub
channel:trends:update               → Pub/Sub
channel:predictions:new             → Pub/Sub
channel:alerts:{user_id}            → Pub/Sub
```

---

## 🔌 API СПЕЦИФИКАЦИЯ

*(API endpoints идентичны v1.0 с следующими изменениями:)*

### Изменения в API по сравнению с v1.0

**1. `GET /api/v1/trends` — поле `platforms` → `active_sources`**
```json
{
    "active_sources": ["google_trends", "reddit", "hackernews", "youtube_trending", "github_trending"],
    "source_count": 5,
    "first_source": "hackernews",
    "correlation_score": 85.2
}
```

**2. `GET /api/v1/trends/:trendId` — расширенная detail page**
```json
{
    "signal_breakdown": {
        "google_trends": {
            "interest": 85,
            "related_queries": ["openai", "ai release"],
            "signal_type": "search_interest",
            "first_detected": "2026-03-24T08:00:00Z",
            "current_value": 85,
            "delta": "+340%"
        },
        "reddit": {
            "subreddits": ["r/technology", "r/artificial", "r/MachineLearning"],
            "top_post_score": 4500,
            "signal_type": "trending",
            "first_detected": "2026-03-24T07:30:00Z"
        },
        "hackernews": {
            "score": 450,
            "comments": 120,
            "position": 3,
            "signal_type": "score_spike",
            "first_detected": "2026-03-24T06:45:00Z"
        },
        "github_trending": {
            "repo": "openai/gpt-5-api",
            "stars": 2500,
            "stars_today": 800,
            "signal_type": "new_entry",
            "first_detected": "2026-03-24T09:00:00Z"
        },
        "wikipedia": {
            "pageviews_today": 50000,
            "pageviews_avg": 2000,
            "spike_ratio": 25.0,
            "signal_type": "pageview_spike",
            "first_detected": "2026-03-24T10:00:00Z"
        }
    },
    "correlation": {
        "score": 85.2,
        "sources_firing": 5,
        "pattern_match": "tech_breakout",
        "pattern_multiplier": 1.8,
        "spread_timeline": [
            {"source": "hackernews", "detected_at": "2026-03-24T06:45:00Z"},
            {"source": "reddit", "detected_at": "2026-03-24T07:30:00Z"},
            {"source": "google_trends", "detected_at": "2026-03-24T08:00:00Z"},
            {"source": "github_trending", "detected_at": "2026-03-24T09:00:00Z"},
            {"source": "wikipedia", "detected_at": "2026-03-24T10:00:00Z"}
        ]
    }
}
```

**3. Новый endpoint: `GET /api/v1/sources/status`**
```json
{
    "success": true,
    "data": {
        "total_sources": 16,
        "healthy": 14,
        "degraded": 1,
        "down": 1,
        "sources": [
            {
                "name": "google_trends",
                "status": "healthy",
                "last_success": "2026-03-24T14:55:00Z",
                "signals_24h": 342,
                "avg_response_ms": 1200,
                "rate_limit_remaining": null
            },
            {
                "name": "reddit",
                "status": "healthy",
                "last_success": "2026-03-24T14:58:00Z",
                "signals_24h": 890,
                "avg_response_ms": 450,
                "rate_limit_remaining": 85
            }
        ]
    }
}
```

*(Все остальные endpoints ниже — полные спецификации.)*

#### 🔔 Alerts

**GET /api/v1/alerts** — список алертов пользователя.
**POST /api/v1/alerts** — создать алерт. Body: `{name, categories[], keywords[], exclude_keywords[], sources[], min_velocity, min_correlation, notify_email, notify_push, notify_webhook, webhook_url, frequency}`. Validation: name required (max 100), categories min 1, keywords max 20, webhook_url must be HTTPS.
**PUT /api/v1/alerts/:alertId** — обновить алерт.
**DELETE /api/v1/alerts/:alertId** — удалить (soft delete).
**GET /api/v1/alerts/triggers** — история срабатываний. Query: alert_id, is_read, page, per_page.
**PUT /api/v1/alerts/triggers/:triggerId/read** — пометить как прочитанное.
Auth: Creator+. Plan Limits: Creator = 3 alerts, Pro+ = unlimited.

#### 📝 Content Briefs

**POST /api/v1/briefs/generate** — сгенерировать brief. Body: `{trend_id, format, target_audience, tone, language}`. Response: full brief object with title, hook, key_points, seo_keywords, hashtags, structure, full_brief text.
**GET /api/v1/briefs** — список сгенерированных briefs.
**GET /api/v1/briefs/:briefId** — конкретный brief.
Auth: Creator+. Plan Limits: Creator = 5/day, Pro+ = unlimited.

#### 💳 Billing

**GET /api/v1/billing/subscription** — текущая подписка.
**POST /api/v1/billing/checkout** — создать Stripe Checkout. Body: `{plan, billing_interval, success_url, cancel_url}`. Returns checkout_url.
**POST /api/v1/billing/portal** — Stripe Customer Portal session.
**GET /api/v1/billing/usage** — текущее использование (trend_views, briefs, alerts, api_calls with limits).
**GET /api/v1/billing/invoices** — история счетов.
Auth: Required.

#### 👤 User

**GET /api/v1/user/profile** — профиль текущего пользователя.
**PUT /api/v1/user/profile** — обновить профиль.
**PUT /api/v1/user/preferences** — обновить настройки (categories, sources, notifications).
**DELETE /api/v1/user/account** — удалить аккаунт (soft delete, cancel subscription).
Auth: Required.

#### 🔑 API Keys (Pro+)

**GET /api/v1/api-keys** — список ключей.
**POST /api/v1/api-keys** — создать ключ. Body: `{name, scopes[]}`. Returns key (shown ONCE), prefix, id.
**DELETE /api/v1/api-keys/:keyId** — отозвать ключ.
**PUT /api/v1/api-keys/:keyId/rotate** — ротация ключа. Returns new key.
Auth: Pro+.

#### 👥 Team (Business+)

**GET /api/v1/team** — информация о team.
**POST /api/v1/team/invite** — пригласить участника. Body: `{email, role}`.
**PUT /api/v1/team/members/:memberId/role** — изменить роль.
**DELETE /api/v1/team/members/:memberId** — удалить участника.
Auth: Business+ (owner/admin for write).

#### 🔗 Share

**POST /api/v1/share/card** — создать shareable карточку. Body: `{trend_id, card_type}`. Returns share_url, og_image_url, embed_code, twitter_share_url, share_token.
**GET /api/v1/share/:token** — получить данные карточки (public, no auth).
Auth: Creator+ for creation. Public for viewing.

#### 🏥 Health

**GET /api/v1/health** — `{"status": "ok"}`. No auth. МИНИМУМ информации наружу.
**GET /api/v1/health/detailed** — полная диагностика. Admin only. Включает: database, redis, celery workers, source health, queue size, uptime.

#### 📡 Sources

**GET /api/v1/sources/status** — статус всех signal sources. Includes: total, healthy, degraded, down counts + per-source details.
Auth: Required.

#### 🔒 Webhooks

**POST /api/v1/webhooks/stripe** — Stripe webhook с signature verification. Handled events: checkout.session.completed, customer.subscription.created/updated/deleted, invoice.payment_failed/succeeded.
Auth: Stripe signature (NOT user auth).

---

## 🧠 CORE ENGINES

### Engine 1: Signal Collection Engine (core/signals/)

#### BaseSignalAdapter (abstract)

```python
# backend/app/core/signals/base.py

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class SignalType(str, Enum):
    TRENDING = "trending"
    VELOCITY_SPIKE = "velocity_spike"
    NEW_ENTRY = "new_entry"
    SCORE_SPIKE = "score_spike"
    SEARCH_INTEREST = "search_interest"
    PAGEVIEW_SPIKE = "pageview_spike"
    DOWNLOAD_SPIKE = "download_spike"
    PRICE_MOVEMENT = "price_movement"
    PLAYER_SPIKE = "player_spike"
    RANKING_CHANGE = "ranking_change"


class SignalEvent(BaseModel):
    """Universal signal event from any source.
    
    Ключевое отличие от v1.0 (RawMention):
    - Это не "упоминание" а "сигнал" — конкретный факт о тренде
    - Каждый адаптер извлекает СИГНАЛЫ, а не сырые посты
    - Сигнал = "тема X выросла на Y% в источнике Z"
    """
    source: str                          # "google_trends", "reddit", "hackernews"
    signal_type: SignalType
    
    # What
    title: str                           # Human-readable signal title
    url: Optional[str] = None            # Source URL
    extracted_topic: str                 # Normalized topic extracted from signal
    
    # How much
    value: float = 0                     # Numeric value (score, interest, stars, etc.)
    delta: float = 0                     # Change (%, absolute depends on source)
    rank: Optional[int] = None           # Position if in a ranked list
    
    # Context
    context: Dict = {}                   # Source-specific raw data
    
    # Quality
    weight: float = 0.5                  # Computed importance (0-1)
    
    # When
    detected_at: datetime = None         # When we detected it
    source_timestamp: Optional[datetime] = None  # When it originated


class CollectionResult(BaseModel):
    """Result of a signal collection run."""
    source: str
    signals: List[SignalEvent]
    duration_ms: int
    api_calls: int
    errors: List[str] = []
    is_healthy: bool = True


class BaseSignalAdapter(ABC):
    """Abstract base for all signal source adapters.
    
    Принцип: адаптер извлекает СИГНАЛЫ (факты о трендах),
    а не сырые данные. Каждый адаптер знает как интерпретировать
    свой источник и выдаёт нормализованные SignalEvent.
    
    Все адаптеры:
    - Бесплатные (или дешёвые, опциональные)
    - Изолированные (свой rate limiter, error handling)
    - Resilient (если падает — остальные работают)
    - Stateless (каждый вызов независим)
    """
    
    source_name: str
    source_weight: float              # Default quality weight for this source
    
    @abstractmethod
    async def collect(self) -> CollectionResult:
        """Collect current signals from this source.
        Returns trending/rising items as SignalEvents.
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if this source is reachable."""
        pass
    
    def extract_topics(self, raw_title: str) -> str:
        """Extract normalized topic from signal title.
        Override in subclass for source-specific logic.
        """
        import re
        topic = raw_title.strip()
        topic = re.sub(r'\[.*?\]', '', topic)       # Remove [tags]
        topic = re.sub(r'\(.*?\)', '', topic)        # Remove (notes)
        topic = re.sub(r'https?://\S+', '', topic)   # Remove URLs
        topic = re.sub(r'\s+', ' ', topic).strip()
        return topic[:200]  # Limit length
```

#### Пример: Google Trends Adapter

```python
# backend/app/core/signals/adapters/google_trends.py

import asyncio
from typing import List
from datetime import datetime
import logging

from pytrends.request import TrendReq
from app.core.signals.base import BaseSignalAdapter, SignalEvent, SignalType, CollectionResult

logger = logging.getLogger(__name__)


class GoogleTrendsAdapter(BaseSignalAdapter):
    """Google Trends signal adapter via pytrends.
    
    Что даёт:
    - Real-time trending searches (что ищут прямо сейчас)
    - Interest over time (рост интереса к теме)
    - Related queries (связанные запросы — помогают обнаружить связи)
    - Rising queries (быстро растущие запросы — ранний сигнал!)
    
    Limitations pytrends:
    - Unofficial API (может сломаться, но работает годами)
    - ~10 req/min без бана
    - Данные с задержкой ~4-24 часа (не real-time)
    - Но Rising queries — это РАННИЙ сигнал
    
    Стратегия: 
    - Каждые 30 минут запрашиваем trending searches
    - Каждый час запрашиваем interest для отслеживаемых категорий
    - Rising queries с breakout (>5000%) — сильнейший сигнал
    
    Стоимость: $0
    Rate limit: ~10 req/min (self-imposed, pytrends)
    """
    
    source_name = "google_trends"
    source_weight = 0.90
    
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
    
    async def collect(self) -> CollectionResult:
        """Collect signals from Google Trends."""
        import time
        start = time.time()
        signals: List[SignalEvent] = []
        api_calls = 0
        errors: List[str] = []
        
        try:
            # 1. Get real-time trending searches
            trending = await asyncio.to_thread(
                self.pytrends.trending_searches, pn='united_states'
            )
            api_calls += 1
            
            if trending is not None and not trending.empty:
                for idx, row in trending.head(20).iterrows():
                    topic = str(row[0])
                    signals.append(SignalEvent(
                        source=self.source_name,
                        signal_type=SignalType.TRENDING,
                        title=f"Trending on Google: {topic}",
                        extracted_topic=self.extract_topics(topic),
                        value=20 - idx,  # Higher value for higher rank
                        rank=idx + 1,
                        weight=self.source_weight,
                        detected_at=datetime.utcnow(),
                        context={"region": "US", "rank": idx + 1}
                    ))
            
            # 2. Get rising related queries for key categories
            category_keywords = {
                "tech": ["AI", "software", "startup"],
                "crypto": ["bitcoin", "ethereum", "crypto"],
                "science": ["research", "NASA", "climate"],
            }
            
            for category, keywords in category_keywords.items():
                try:
                    self.pytrends.build_payload(keywords, timeframe='now 7-d')
                    related = await asyncio.to_thread(
                        self.pytrends.related_queries
                    )
                    api_calls += 1
                    
                    for keyword, data in related.items():
                        if data is None:
                            continue
                        rising = data.get('rising')
                        if rising is not None and not rising.empty:
                            for _, row in rising.head(5).iterrows():
                                query = str(row.get('query', ''))
                                value = row.get('value', 0)
                                
                                # Breakout (5000%+) = strongest signal
                                is_breakout = str(value) == 'Breakout' or (isinstance(value, (int, float)) and value > 5000)
                                
                                signals.append(SignalEvent(
                                    source=self.source_name,
                                    signal_type=SignalType.SEARCH_INTEREST,
                                    title=f"Rising search: {query} (+{value}%)",
                                    extracted_topic=self.extract_topics(query),
                                    value=float(value) if isinstance(value, (int, float)) else 5000,
                                    delta=float(value) if isinstance(value, (int, float)) else 5000,
                                    weight=self.source_weight * (1.5 if is_breakout else 1.0),
                                    detected_at=datetime.utcnow(),
                                    context={
                                        "category": category,
                                        "parent_keyword": keyword,
                                        "is_breakout": is_breakout,
                                        "growth_pct": value
                                    }
                                ))
                    
                    # Small delay to avoid rate limiting
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    errors.append(f"Related queries for {category}: {e}")
        
        except Exception as e:
            errors.append(f"Google Trends collection failed: {e}")
        
        return CollectionResult(
            source=self.source_name,
            signals=signals,
            duration_ms=int((time.time() - start) * 1000),
            api_calls=api_calls,
            errors=errors,
            is_healthy=len(errors) == 0
        )
    
    async def health_check(self) -> bool:
        try:
            await asyncio.to_thread(
                self.pytrends.trending_searches, pn='united_states'
            )
            return True
        except Exception:
            return False
```

#### Пример: Reddit Adapter

```python
# backend/app/core/signals/adapters/reddit.py

import asyncio
from typing import List
from datetime import datetime
import logging

import praw
from app.core.signals.base import BaseSignalAdapter, SignalEvent, SignalType, CollectionResult
from app.config import settings

logger = logging.getLogger(__name__)


class RedditAdapter(BaseSignalAdapter):
    """Reddit signal adapter via PRAW.
    
    Что даёт:
    - Rising posts (раннний индикатор — появляется ДО hot)
    - Hot posts (уже набрали трекцию)
    - Subreddit subscriber growth (growing community = growing topic)
    - Cross-subreddit presence (одна тема в нескольких сабреддитах)
    
    Стратегия:
    - Каждые 10 минут: rising posts из целевых subreddits
    - Каждые 30 минут: hot posts из r/all + целевых
    - Ежечасно: subscriber counts для отслеживания роста
    
    Целевые subreddits (по категориям):
    - Tech: technology, programming, webdev, devops, sysadmin
    - AI: MachineLearning, artificial, LocalLLaMA, ChatGPT, singularity
    - Crypto: CryptoCurrency, Bitcoin, ethereum, defi
    - Science: science, space, Futurology
    - Business: business, Entrepreneur, startups
    - Gaming: gaming, pcgaming, Games, IndieGaming
    - Culture: entertainment, movies, music, television
    
    Стоимость: $0
    Rate limit: 100 req/min (PRAW handles automatically)
    """
    
    source_name = "reddit"
    source_weight = 0.85
    
    # Target subreddits grouped by category
    SUBREDDITS = {
        "tech": ["technology", "programming", "webdev", "devops", "sysadmin", "netsec", "linux"],
        "ai": ["MachineLearning", "artificial", "LocalLLaMA", "ChatGPT", "singularity", "StableDiffusion"],
        "crypto": ["CryptoCurrency", "Bitcoin", "ethereum", "defi", "solana"],
        "science": ["science", "space", "Futurology", "askscience"],
        "business": ["business", "Entrepreneur", "startups", "smallbusiness"],
        "gaming": ["gaming", "pcgaming", "Games", "IndieGaming", "gamedev"],
        "culture": ["entertainment", "movies", "music", "television", "books"],
        "finance": ["wallstreetbets", "stocks", "investing", "personalfinance"],
        "devtools": ["opensource", "selfhosted", "rust", "golang", "Python"],
    }
    
    # Thresholds for signal detection
    RISING_MIN_SCORE = 50        # Minimum score to count as signal
    HOT_MIN_SCORE = 500          # Minimum score for hot posts
    VELOCITY_THRESHOLD = 100     # Score gained per hour = velocity spike
    
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            user_agent="TrendRadar/1.0 signal collector"
        )
    
    async def collect(self) -> CollectionResult:
        """Collect signals from Reddit."""
        import time
        start = time.time()
        signals: List[SignalEvent] = []
        api_calls = 0
        errors: List[str] = []
        
        # 1. Scan rising posts from target subreddits
        all_subs = []
        for subs in self.SUBREDDITS.values():
            all_subs.extend(subs)
        
        for sub_name in all_subs:
            try:
                subreddit = await asyncio.to_thread(
                    lambda: self.reddit.subreddit(sub_name)
                )
                
                # Get rising posts
                rising_posts = await asyncio.to_thread(
                    lambda: list(subreddit.rising(limit=10))
                )
                api_calls += 1
                
                for post in rising_posts:
                    if post.score < self.RISING_MIN_SCORE:
                        continue
                    
                    # Calculate velocity (score per hour since creation)
                    age_hours = max(
                        (datetime.utcnow() - datetime.utcfromtimestamp(post.created_utc)).total_seconds() / 3600,
                        0.1
                    )
                    velocity = post.score / age_hours
                    
                    signal_type = SignalType.VELOCITY_SPIKE if velocity > self.VELOCITY_THRESHOLD else SignalType.TRENDING
                    
                    signals.append(SignalEvent(
                        source=self.source_name,
                        signal_type=signal_type,
                        title=post.title,
                        url=f"https://reddit.com{post.permalink}",
                        extracted_topic=self.extract_topics(post.title),
                        value=float(post.score),
                        delta=velocity,
                        weight=self.source_weight * min(velocity / 200, 1.5),
                        detected_at=datetime.utcnow(),
                        source_timestamp=datetime.utcfromtimestamp(post.created_utc),
                        context={
                            "subreddit": sub_name,
                            "score": post.score,
                            "num_comments": post.num_comments,
                            "upvote_ratio": post.upvote_ratio,
                            "velocity_per_hour": round(velocity, 1),
                            "author": str(post.author),
                            "is_self": post.is_self,
                            "category": self._get_category(sub_name)
                        }
                    ))
                
            except Exception as e:
                errors.append(f"Reddit r/{sub_name}: {e}")
        
        # 2. Scan r/all hot for breakout topics
        try:
            all_hot = await asyncio.to_thread(
                lambda: list(self.reddit.subreddit("all").hot(limit=25))
            )
            api_calls += 1
            
            for post in all_hot:
                if post.score < self.HOT_MIN_SCORE:
                    continue
                
                signals.append(SignalEvent(
                    source=self.source_name,
                    signal_type=SignalType.TRENDING,
                    title=post.title,
                    url=f"https://reddit.com{post.permalink}",
                    extracted_topic=self.extract_topics(post.title),
                    value=float(post.score),
                    rank=None,
                    weight=self.source_weight,
                    detected_at=datetime.utcnow(),
                    source_timestamp=datetime.utcfromtimestamp(post.created_utc),
                    context={
                        "subreddit": str(post.subreddit),
                        "score": post.score,
                        "num_comments": post.num_comments,
                        "is_r_all": True
                    }
                ))
        except Exception as e:
            errors.append(f"Reddit r/all: {e}")
        
        return CollectionResult(
            source=self.source_name,
            signals=signals,
            duration_ms=int((time.time() - start) * 1000),
            api_calls=api_calls,
            errors=errors,
            is_healthy=len(errors) < len(all_subs) // 2  # Healthy if <50% failed
        )
    
    def _get_category(self, subreddit: str) -> str:
        for category, subs in self.SUBREDDITS.items():
            if subreddit in subs:
                return category
        return "general"
    
    async def health_check(self) -> bool:
        try:
            await asyncio.to_thread(
                lambda: list(self.reddit.subreddit("all").hot(limit=1))
            )
            return True
        except Exception:
            return False
```

#### Пример: Hacker News Adapter

```python
# backend/app/core/signals/adapters/hackernews.py

import httpx
import asyncio
from typing import List, Optional
from datetime import datetime
import logging

from app.core.signals.base import BaseSignalAdapter, SignalEvent, SignalType, CollectionResult

logger = logging.getLogger(__name__)


class HackerNewsAdapter(BaseSignalAdapter):
    """Hacker News signal adapter via Firebase API.
    
    Что даёт:
    - Top stories (высший рейтинг = confirmed trend)
    - New stories (ранний обнаружатель — высокий score на свежем = сильный сигнал)
    - Best stories (стабильно хорошие — sustained interest)
    - Score velocity (быстро набирающие очки = accelerating trend)
    
    Стратегия:
    - Каждые 5 минут: top stories (first 30)
    - Каждые 15 минут: new stories с score > 50 (ранний сигнал)
    - Отслеживаем score velocity: если story набирает >100 points/hour — сигнал
    
    Стоимость: $0 (Firebase API, полностью бесплатный)
    Rate limit: Нет (Firebase handles scaling)
    """
    
    source_name = "hackernews"
    source_weight = 0.85
    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    
    # Thresholds
    MIN_SCORE_TOP = 100          # Minimum score for top stories to count
    MIN_SCORE_NEW = 30           # Minimum score for new stories (early signal)
    VELOCITY_THRESHOLD = 50      # Points/hour = velocity spike
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def collect(self) -> CollectionResult:
        import time
        start = time.time()
        signals: List[SignalEvent] = []
        api_calls = 0
        errors: List[str] = []
        
        try:
            # 1. Get top story IDs
            resp = await self.client.get(f"{self.BASE_URL}/topstories.json")
            api_calls += 1
            top_ids = resp.json()[:30]  # Top 30
            
            # 2. Fetch details for each story (parallel)
            tasks = [self._fetch_item(item_id) for item_id in top_ids]
            items = await asyncio.gather(*tasks, return_exceptions=True)
            api_calls += len(top_ids)
            
            for idx, item in enumerate(items):
                if isinstance(item, Exception) or item is None:
                    continue
                
                score = item.get("score", 0)
                if score < self.MIN_SCORE_TOP:
                    continue
                
                title = item.get("title", "")
                url = item.get("url", f"https://news.ycombinator.com/item?id={item.get('id')}")
                
                # Calculate velocity
                created_ts = item.get("time", 0)
                age_hours = max(
                    (datetime.utcnow() - datetime.utcfromtimestamp(created_ts)).total_seconds() / 3600,
                    0.1
                )
                velocity = score / age_hours
                
                signal_type = SignalType.SCORE_SPIKE if velocity > self.VELOCITY_THRESHOLD else SignalType.TRENDING
                
                signals.append(SignalEvent(
                    source=self.source_name,
                    signal_type=signal_type,
                    title=title,
                    url=url,
                    extracted_topic=self.extract_topics(title),
                    value=float(score),
                    delta=round(velocity, 1),
                    rank=idx + 1,
                    weight=self.source_weight * min(velocity / 100, 1.5),
                    detected_at=datetime.utcnow(),
                    source_timestamp=datetime.utcfromtimestamp(created_ts) if created_ts else None,
                    context={
                        "hn_id": item.get("id"),
                        "score": score,
                        "comments": item.get("descendants", 0),
                        "author": item.get("by", ""),
                        "velocity_per_hour": round(velocity, 1),
                        "position": idx + 1,
                        "type": item.get("type", "story"),
                        "domain": self._extract_domain(url)
                    }
                ))
            
            # 3. Get new stories for early detection
            resp = await self.client.get(f"{self.BASE_URL}/newstories.json")
            api_calls += 1
            new_ids = resp.json()[:50]
            
            new_tasks = [self._fetch_item(item_id) for item_id in new_ids]
            new_items = await asyncio.gather(*new_tasks, return_exceptions=True)
            api_calls += len(new_ids)
            
            for item in new_items:
                if isinstance(item, Exception) or item is None:
                    continue
                
                score = item.get("score", 0)
                if score < self.MIN_SCORE_NEW:
                    continue
                
                title = item.get("title", "")
                created_ts = item.get("time", 0)
                age_hours = max(
                    (datetime.utcnow() - datetime.utcfromtimestamp(created_ts)).total_seconds() / 3600,
                    0.1
                )
                velocity = score / age_hours
                
                # New story with high velocity = EARLY SIGNAL
                if velocity > self.VELOCITY_THRESHOLD * 0.5:
                    signals.append(SignalEvent(
                        source=self.source_name,
                        signal_type=SignalType.NEW_ENTRY,
                        title=title,
                        url=item.get("url", f"https://news.ycombinator.com/item?id={item.get('id')}"),
                        extracted_topic=self.extract_topics(title),
                        value=float(score),
                        delta=round(velocity, 1),
                        weight=self.source_weight * 1.2,  # Early signal bonus
                        detected_at=datetime.utcnow(),
                        source_timestamp=datetime.utcfromtimestamp(created_ts) if created_ts else None,
                        context={
                            "hn_id": item.get("id"),
                            "score": score,
                            "comments": item.get("descendants", 0),
                            "velocity_per_hour": round(velocity, 1),
                            "is_early_signal": True
                        }
                    ))
        
        except Exception as e:
            errors.append(f"HN collection error: {e}")
        
        return CollectionResult(
            source=self.source_name,
            signals=signals,
            duration_ms=int((time.time() - start) * 1000),
            api_calls=api_calls,
            errors=errors,
            is_healthy=len(errors) == 0
        )
    
    async def _fetch_item(self, item_id: int) -> Optional[dict]:
        try:
            resp = await self.client.get(f"{self.BASE_URL}/item/{item_id}.json")
            return resp.json()
        except Exception:
            return None
    
    def _extract_domain(self, url: str) -> str:
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc.replace("www.", "")
        except Exception:
            return ""
    
    async def health_check(self) -> bool:
        try:
            resp = await self.client.get(f"{self.BASE_URL}/topstories.json")
            return resp.status_code == 200
        except Exception:
            return False
```

#### Пример: GitHub Trending Adapter

```python
# backend/app/core/signals/adapters/github.py

import httpx
from bs4 import BeautifulSoup
import asyncio
from typing import List
from datetime import datetime
import logging

from app.core.signals.base import BaseSignalAdapter, SignalEvent, SignalType, CollectionResult

logger = logging.getLogger(__name__)


class GitHubTrendingAdapter(BaseSignalAdapter):
    """GitHub Trending signal adapter.
    
    Что даёт:
    - Trending repositories (новые repos набирающие stars)
    - Stars velocity (stars per day)
    - Language trends (какие языки растут)
    - New repo spikes (0 → 1000 stars за день = сильный сигнал)
    
    Подход: scrape github.com/trending + API для деталей
    
    Стратегия:
    - Каждые 30 минут: scrape trending page (daily/weekly)
    - API для star count деталей
    - Отслеживаем repos с >500 stars/day
    
    Стоимость: $0
    Rate limit: 5000 req/hr (authenticated), trending page — no limit
    """
    
    source_name = "github_trending"
    source_weight = 0.80
    TRENDING_URL = "https://github.com/trending"
    API_URL = "https://api.github.com"
    
    # Minimum stars today to count as signal
    MIN_STARS_TODAY = 100
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={"Accept": "text/html,application/json"}
        )
    
    async def collect(self) -> CollectionResult:
        import time
        start = time.time()
        signals: List[SignalEvent] = []
        api_calls = 0
        errors: List[str] = []
        
        try:
            # 1. Scrape trending page (daily)
            for period in ["daily", "weekly"]:
                try:
                    resp = await self.client.get(
                        f"{self.TRENDING_URL}?since={period}",
                        headers={"Accept": "text/html"}
                    )
                    api_calls += 1
                    
                    soup = BeautifulSoup(resp.text, "html.parser")
                    articles = soup.select("article.Box-row")
                    
                    for idx, article in enumerate(articles[:25]):
                        # Extract repo info
                        h2 = article.select_one("h2 a")
                        if not h2:
                            continue
                        
                        repo_path = h2.get("href", "").strip("/")
                        repo_name = repo_path.split("/")[-1] if "/" in repo_path else repo_path
                        
                        # Extract stars today
                        stars_today_el = article.select_one("span.d-inline-block.float-sm-right")
                        stars_today = 0
                        if stars_today_el:
                            stars_text = stars_today_el.get_text(strip=True).replace(",", "")
                            try:
                                stars_today = int(stars_text.split()[0])
                            except (ValueError, IndexError):
                                pass
                        
                        if stars_today < self.MIN_STARS_TODAY and period == "daily":
                            continue
                        
                        # Extract description
                        desc_el = article.select_one("p")
                        description = desc_el.get_text(strip=True) if desc_el else ""
                        
                        # Extract language
                        lang_el = article.select_one("span[itemprop='programmingLanguage']")
                        language = lang_el.get_text(strip=True) if lang_el else "Unknown"
                        
                        # Total stars
                        total_stars_el = article.select("a.Link--muted")
                        total_stars = 0
                        if total_stars_el:
                            for a in total_stars_el:
                                href = a.get("href", "")
                                if "/stargazers" in href:
                                    try:
                                        total_stars = int(a.get_text(strip=True).replace(",", ""))
                                    except ValueError:
                                        pass
                        
                        # New repo with lots of stars = strongest signal
                        is_new = total_stars < stars_today * 3  # Most stars are recent
                        
                        signals.append(SignalEvent(
                            source=self.source_name,
                            signal_type=SignalType.NEW_ENTRY if is_new else SignalType.VELOCITY_SPIKE,
                            title=f"{repo_path}: {description[:100]}",
                            url=f"https://github.com/{repo_path}",
                            extracted_topic=self._extract_topic(repo_name, description),
                            value=float(stars_today),
                            delta=float(stars_today),
                            rank=idx + 1,
                            weight=self.source_weight * (1.3 if is_new else 1.0),
                            detected_at=datetime.utcnow(),
                            context={
                                "repo": repo_path,
                                "stars_today": stars_today,
                                "total_stars": total_stars,
                                "language": language,
                                "description": description,
                                "period": period,
                                "is_new_repo": is_new,
                                "position": idx + 1
                            }
                        ))
                
                except Exception as e:
                    errors.append(f"GitHub trending ({period}): {e}")
        
        except Exception as e:
            errors.append(f"GitHub collection error: {e}")
        
        return CollectionResult(
            source=self.source_name,
            signals=signals,
            duration_ms=int((time.time() - start) * 1000),
            api_calls=api_calls,
            errors=errors,
            is_healthy=len(errors) == 0
        )
    
    def _extract_topic(self, repo_name: str, description: str) -> str:
        """Extract topic from repo name and description."""
        combined = f"{repo_name} {description}"
        return self.extract_topics(combined)
    
    async def health_check(self) -> bool:
        try:
            resp = await self.client.get(self.TRENDING_URL)
            return resp.status_code == 200
        except Exception:
            return False
```

#### Пример: Wikipedia Pageviews Adapter

```python
# backend/app/core/signals/adapters/wikipedia.py

import httpx
import asyncio
from typing import List
from datetime import datetime, timedelta
import logging

from app.core.signals.base import BaseSignalAdapter, SignalEvent, SignalType, CollectionResult

logger = logging.getLogger(__name__)


class WikipediaAdapter(BaseSignalAdapter):
    """Wikipedia Pageviews signal adapter.
    
    Что даёт:
    - Most viewed pages today (что читают)
    - Pageview spikes (резкий рост просмотров = что-то произошло)
    - New article creation (новая статья = новая тема)
    
    Почему это мощный сигнал:
    - Wikipedia pageview spike = подтверждение что тема "взорвалась"
    - Люди идут в Wikipedia когда хотят понять что происходит
    - Spike ratio (today/avg) > 10x = breaking news
    - Spike ratio > 5x = trending topic
    
    API: Wikimedia REST API (полностью бесплатный, официальный)
    Rate limit: 200 req/s (очень generous)
    Стоимость: $0
    """
    
    source_name = "wikipedia"
    source_weight = 0.75
    API_URL = "https://wikimedia.org/api/rest_v1"
    
    MIN_VIEWS_TODAY = 10000       # Minimum views to count
    MIN_SPIKE_RATIO = 3.0         # Today views / avg views
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={"User-Agent": "TrendRadar/1.0 (trend-detection; contact@trendradar.io)"}
        )
    
    async def collect(self) -> CollectionResult:
        import time
        start = time.time()
        signals: List[SignalEvent] = []
        api_calls = 0
        errors: List[str] = []
        
        try:
            # Get most viewed pages for today
            today = datetime.utcnow()
            yesterday = today - timedelta(days=1)
            date_str = yesterday.strftime("%Y/%m/%d")
            
            resp = await self.client.get(
                f"{self.API_URL}/metrics/pageviews/top/en.wikipedia/all-access/{date_str}"
            )
            api_calls += 1
            
            if resp.status_code == 200:
                data = resp.json()
                articles = data.get("items", [{}])[0].get("articles", [])
                
                # Filter out special pages
                skip_prefixes = ["Main_Page", "Special:", "Wikipedia:", "Portal:", "File:"]
                
                for article in articles[:50]:
                    title = article.get("article", "")
                    views = article.get("views", 0)
                    rank = article.get("rank", 999)
                    
                    # Skip special pages
                    if any(title.startswith(p) for p in skip_prefixes):
                        continue
                    
                    if views < self.MIN_VIEWS_TODAY:
                        continue
                    
                    # Get average pageviews for comparison
                    avg_views = await self._get_avg_pageviews(title, days=30)
                    api_calls += 1
                    
                    if avg_views > 0:
                        spike_ratio = views / avg_views
                    else:
                        spike_ratio = 0
                    
                    # Only signal if there's a meaningful spike
                    if spike_ratio < self.MIN_SPIKE_RATIO:
                        continue
                    
                    clean_title = title.replace("_", " ")
                    
                    signal_type = SignalType.PAGEVIEW_SPIKE
                    
                    signals.append(SignalEvent(
                        source=self.source_name,
                        signal_type=signal_type,
                        title=f"Wikipedia spike: {clean_title} ({spike_ratio:.0f}x normal)",
                        url=f"https://en.wikipedia.org/wiki/{title}",
                        extracted_topic=clean_title,
                        value=float(views),
                        delta=spike_ratio,
                        rank=rank,
                        weight=self.source_weight * min(spike_ratio / 10, 2.0),
                        detected_at=datetime.utcnow(),
                        context={
                            "pageviews_today": views,
                            "pageviews_avg": round(avg_views),
                            "spike_ratio": round(spike_ratio, 1),
                            "rank": rank,
                            "article_title": clean_title
                        }
                    ))
                    
                    # Rate limiting
                    await asyncio.sleep(0.1)
        
        except Exception as e:
            errors.append(f"Wikipedia collection error: {e}")
        
        return CollectionResult(
            source=self.source_name,
            signals=signals,
            duration_ms=int((time.time() - start) * 1000),
            api_calls=api_calls,
            errors=errors,
            is_healthy=len(errors) == 0
        )
    
    async def _get_avg_pageviews(self, title: str, days: int = 30) -> float:
        """Get average daily pageviews for an article over last N days."""
        try:
            end = datetime.utcnow() - timedelta(days=1)
            start = end - timedelta(days=days)
            
            resp = await self.client.get(
                f"{self.API_URL}/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents"
                f"/{title}/daily/{start.strftime('%Y%m%d')}/{end.strftime('%Y%m%d')}"
            )
            
            if resp.status_code != 200:
                return 0
            
            data = resp.json()
            items = data.get("items", [])
            
            if not items:
                return 0
            
            total = sum(item.get("views", 0) for item in items)
            return total / max(len(items), 1)
        
        except Exception:
            return 0
    
    async def health_check(self) -> bool:
        try:
            resp = await self.client.get(f"{self.API_URL}/metrics/pageviews/top/en.wikipedia/all-access/2026/03/20")
            return resp.status_code == 200
        except Exception:
            return False
```

#### Краткие описания остальных адаптеров

```python
# Остальные адаптеры следуют тому же паттерну BaseSignalAdapter.
# Ниже — ключевые детали реализации для каждого:

# --- npm Registry Adapter ---
# backend/app/core/signals/adapters/npm_registry.py
# API: https://api.npmjs.org/downloads/point/last-week/{package}
# Стратегия: отслеживаем топ-100 пакетов + новые пакеты с >1000 downloads/week
# Сигнал: download_spike (>200% рост за неделю)
# Стоимость: $0, rate limit: generous

# --- PyPI Stats Adapter ---
# backend/app/core/signals/adapters/pypi_stats.py
# API: https://pypistats.org/api/packages/{package}/recent
# Стратегия: аналогично npm — отслеживаем рост downloads
# Сигнал: download_spike
# Стоимость: $0

# --- YouTube Trending Adapter ---
# backend/app/core/signals/adapters/youtube.py
# API: YouTube Data API v3 (videos.list, chart=mostPopular)
# Стратегия: trending videos + search для горячих топиков
# 10K units/day quota (одна выборка = ~100 units)
# Сигнал: trending + view velocity
# Стоимость: $0

# --- Product Hunt Adapter ---
# backend/app/core/signals/adapters/producthunt.py
# API: GraphQL (api.producthunt.com/v2/api/graphql)
# Стратегия: daily top products, upvotes > 200
# Сигнал: new_entry (new product), score_spike (high upvotes)
# Стоимость: $0, rate limit: 450 req/day

# --- ArXiv Adapter ---
# backend/app/core/signals/adapters/arxiv.py
# API: http://export.arxiv.org/api/query
# Стратегия: новые papers в cs.AI, cs.LG, cs.CL + отслеживание цитирований
# Сигнал: new_entry (new paper), velocity_spike (citations/day)
# Стоимость: $0

# --- CoinGecko Adapter ---
# backend/app/core/signals/adapters/coingecko.py
# API: https://api.coingecko.com/api/v3/
# Стратегия: trending coins, price movers (>10% 24h), new listings
# Сигнал: trending, price_movement, new_entry
# Стоимость: $0, rate limit: 10-30 req/min

# --- Steam Charts Adapter ---
# backend/app/core/signals/adapters/steam_charts.py
# Scrape: steamcharts.com/top
# Стратегия: player count spikes (>200% vs avg)
# Сигнал: player_spike
# Стоимость: $0 (gentle scraping)

# --- Dev.to Adapter ---
# backend/app/core/signals/adapters/devto.py
# API: https://dev.to/api/articles (Forem API)
# Стратегия: top articles by reactions, tag trends
# Сигнал: trending (high reactions), new_entry
# Стоимость: $0, rate limit: 30 req/min

# --- Lobste.rs Adapter ---
# backend/app/core/signals/adapters/lobsters.py
# API: https://lobste.rs/hottest.json
# Стратегия: hottest stories, score > 30
# Сигнал: trending, score_spike
# Стоимость: $0

# --- Stack Overflow Adapter ---
# backend/app/core/signals/adapters/stackoverflow.py
# API: https://api.stackexchange.com/2.3/
# Стратегия: trending tags (most questions this week), hot questions
# Сигнал: trending (new tags), velocity_spike (question volume)
# Стоимость: $0, rate limit: 300 req/day

# --- Google News RSS Adapter ---
# backend/app/core/signals/adapters/google_news.py
# RSS: https://news.google.com/rss/topics/{topic}?hl=en-US
# Стратегия: parse RSS feeds для top stories, topic sections
# Сигнал: trending (top stories), new_entry
# Стоимость: $0, rate limit: нет

# --- Twitter Adapter (optional, paid) ---
# backend/app/core/signals/adapters/twitter.py
# API: Twitter/X v2 Basic ($100/мес)
# Стратегия: trending topics, keyword search
# Активируется ТОЛЬКО если TWITTER_BEARER_TOKEN настроен в .env
# Сигнал: trending, velocity_spike
# Стоимость: $100/мес (опционально)
```

#### SignalManager (orchestrator)

```python
# backend/app/core/signals/manager.py

import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import logging

from app.core.signals.base import BaseSignalAdapter, CollectionResult, SignalEvent
from app.core.signals.registry import SignalSourceRegistry
from app.core.signals.normalizer import TopicNormalizer
from app.core.signals.deduplicator import SignalDeduplicator
from app.core.signals.topic_extractor import AITopicExtractor
from app.utils.cache import RedisCache


logger = logging.getLogger(__name__)


class SignalManager:
    """Orchestrates signal collection from all sources.
    
    Цикл сбора сигналов:
    1. Запустить все адаптеры параллельно (с таймаутами)
    2. Нормализовать extracted_topics ("GPT-5", "GPT5" → "GPT-5")
    3. Дедуплицировать сигналы (один тренд из разных источников → один trend_id)
    4. AI topic extraction для сложных случаев
    5. Записать signal_events в БД
    6. Обновить source_health
    7. Передать в CorrelationEngine для cross-source detection
    
    Resilience:
    - Каждый адаптер имеет таймаут (30 секунд)
    - Если адаптер падает — остальные продолжают
    - Consecutive failures трекаются в source_health
    - При 5 consecutive failures — адаптер автоматически disabled на 1 час
    - Health check восстанавливает адаптер
    
    Scheduling:
    - Tier 1 sources: каждые 5 минут
    - Tier 2 sources: каждые 15-30 минут
    - Tier 3 sources: каждые 30-60 минут
    """
    
    ADAPTER_TIMEOUT = 30  # seconds per adapter
    MAX_CONSECUTIVE_FAILURES = 5
    COOLDOWN_SECONDS = 3600  # 1 hour cooldown after max failures
    
    def __init__(
        self,
        registry: SignalSourceRegistry,
        normalizer: TopicNormalizer,
        deduplicator: SignalDeduplicator,
        topic_extractor: AITopicExtractor,
        cache: RedisCache,
    ):
        self.registry = registry
        self.normalizer = normalizer
        self.deduplicator = deduplicator
        self.topic_extractor = topic_extractor
        self.cache = cache
    
    async def collect_all(self, tier: Optional[str] = None) -> Dict[str, CollectionResult]:
        """Run signal collection across all (or specific tier) sources.
        
        Args:
            tier: "tier1", "tier2", "tier3" or None for all
        """
        adapters = self.registry.get_adapters(tier=tier)
        results: Dict[str, CollectionResult] = {}
        
        # Filter out adapters in cooldown
        active_adapters = {}
        for name, adapter in adapters.items():
            if await self._is_in_cooldown(name):
                logger.info(f"Skipping {name} — in cooldown")
                continue
            
            lock_key = f"source:lock:{name}"
            if await self.cache.exists(lock_key):
                logger.info(f"Skipping {name} — collection in progress")
                continue
            
            await self.cache.set(lock_key, "1", ttl=300)
            active_adapters[name] = adapter
        
        # Run all adapters in parallel with timeouts
        tasks = {
            name: asyncio.create_task(
                asyncio.wait_for(adapter.collect(), timeout=self.ADAPTER_TIMEOUT)
            )
            for name, adapter in active_adapters.items()
        }
        
        for name, task in tasks.items():
            try:
                result = await task
                results[name] = result
                
                # Update health
                await self._update_health(name, result)
                
                # Reset failure count on success
                if result.is_healthy:
                    await self.cache.delete(f"source:failures:{name}")
                
                logger.info(
                    f"Collected {len(result.signals)} signals from {name} "
                    f"in {result.duration_ms}ms ({result.api_calls} API calls)"
                )
            
            except asyncio.TimeoutError:
                logger.warning(f"Timeout collecting from {name}")
                await self._increment_failures(name)
                results[name] = CollectionResult(
                    source=name, signals=[], duration_ms=self.ADAPTER_TIMEOUT * 1000,
                    api_calls=0, errors=["Timeout"], is_healthy=False
                )
            except Exception as e:
                logger.error(f"Error collecting from {name}: {e}")
                await self._increment_failures(name)
                results[name] = CollectionResult(
                    source=name, signals=[], duration_ms=0,
                    api_calls=0, errors=[str(e)], is_healthy=False
                )
            finally:
                await self.cache.delete(f"source:lock:{name}")
        
        return results
    
    async def process_signals(
        self, results: Dict[str, CollectionResult]
    ) -> List[SignalEvent]:
        """Process collected signals: normalize, deduplicate, extract topics.
        
        Pipeline:
        1. Flatten all signals
        2. Normalize topic names
        3. AI topic extraction for ambiguous signals
        4. Deduplicate (same topic from different sources = 1 trend)
        5. Return clean signals ready for CorrelationEngine
        """
        # 1. Flatten
        all_signals: List[SignalEvent] = []
        for source, result in results.items():
            all_signals.extend(result.signals)
        
        total = len(all_signals)
        logger.info(f"Processing {total} raw signals from {len(results)} sources")
        
        # 2. Normalize topics
        normalized = await self.normalizer.normalize_batch(all_signals)
        
        # 3. AI topic extraction for complex/ambiguous signals
        enriched = await self.topic_extractor.enrich_batch(normalized)
        
        # 4. Deduplicate
        unique = await self.deduplicator.deduplicate(enriched)
        logger.info(f"After processing: {len(unique)} unique signals (from {total} raw)")
        
        return unique
    
    async def _is_in_cooldown(self, source: str) -> bool:
        failures = await self.cache.get(f"source:failures:{source}")
        if failures and int(failures) >= self.MAX_CONSECUTIVE_FAILURES:
            cooldown_key = f"source:cooldown:{source}"
            return await self.cache.exists(cooldown_key)
        return False
    
    async def _increment_failures(self, source: str) -> None:
        key = f"source:failures:{source}"
        failures = await self.cache.increment(key)
        if failures >= self.MAX_CONSECUTIVE_FAILURES:
            await self.cache.set(f"source:cooldown:{source}", "1", ttl=self.COOLDOWN_SECONDS)
            logger.warning(f"Source {source} disabled for {self.COOLDOWN_SECONDS}s after {failures} failures")
    
    async def _update_health(self, source: str, result: CollectionResult) -> None:
        health_data = {
            "source": source,
            "is_healthy": result.is_healthy,
            "last_success": datetime.utcnow().isoformat() if result.is_healthy else None,
            "signals_collected": len(result.signals),
            "duration_ms": result.duration_ms,
            "api_calls": result.api_calls,
            "errors": result.errors,
        }
        await self.cache.set(f"source:health:{source}", health_data, ttl=300)
    
    async def get_all_health(self) -> Dict[str, Dict]:
        """Get health status for all sources."""
        health = {}
        for name in self.registry.get_all_names():
            cached = await self.cache.get(f"source:health:{name}")
            if cached:
                health[name] = cached
            else:
                health[name] = {"source": name, "is_healthy": None, "last_check": None}
        return health
```

### Engine 2: Cross-Source Correlation Engine (core/correlation/)

**ЭТО УНИКАЛЬНАЯ ФИЧА TRENDRADAR.**

```python
# backend/app/core/correlation/engine.py

from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

from app.core.signals.base import SignalEvent
from app.core.correlation.scorer import CorrelationScorer
from app.core.correlation.patterns import PatternMatcher
from app.core.correlation.timeline import SpreadTimelineBuilder


logger = logging.getLogger(__name__)


@dataclass
class CorrelationResult:
    """Result of cross-source correlation analysis."""
    topic: str
    sources_firing: List[str]          # which sources detected this topic
    source_count: int                   # how many sources
    correlation_score: float            # 0-100
    pattern_match: Optional[str]        # matched pattern name
    pattern_multiplier: float           # multiplier from pattern
    
    # Spread timeline
    first_source: str
    first_detected: datetime
    spread_timeline: List[Dict]         # [{source, detected_at, signal_type, value}]
    spread_velocity: float              # sources per hour
    
    # Per-source data
    source_signals: Dict[str, Dict]     # {source: {signal_type, value, delta, context}}
    
    # Combined signal strength
    signal_strength: float              # weighted sum of all source signals (0-100)
    
    # Prediction hint
    is_high_confidence: bool            # correlation_score > 70 and source_count >= 3


class CorrelationEngine:
    """Detects cross-source topic correlations.
    
    ЭТО ЯДРО TRENDRADAR.
    
    Логика:
    1. Получаем signals от SignalManager (все источники за последний цикл)
    2. Группируем по extracted_topic (нормализованному)
    3. Для каждого topic — считаем в скольких sources он появился
    4. Применяем pattern matching (определённые комбинации = сильнее)
    5. Вычисляем correlation_score
    6. Строим spread timeline (хронология появления по источникам)
    7. Определяем signal_strength (weighted sum)
    
    Формула correlation_score:
    
    correlation_score = min(100,
        source_diversity * 0.30 +        # кол-во sources (normalized 0-100)
        spread_velocity * 0.25 +         # скорость распространения
        signal_strength * 0.25 +         # взвешенная сила сигналов
        pattern_bonus * 0.20             # бонус за matching pattern
    ) * pattern_multiplier
    
    Ключевые pattern'ы:
    - Tech breakout: HN + GitHub + Reddit → multiplier 1.8x
    - Mainstream breakout: Google Trends + YouTube + News → multiplier 1.9x
    - AI research → adoption: ArXiv + HN + GitHub → multiplier 1.9x
    - Breaking news: Wikipedia spike + News + Google Trends → multiplier 2.0x
    - 5+ sources simultaneously → multiplier 2.0x
    - 6+ sources → multiplier 2.5x
    """
    
    def __init__(
        self,
        scorer: CorrelationScorer,
        pattern_matcher: PatternMatcher,
        timeline_builder: SpreadTimelineBuilder,
    ):
        self.scorer = scorer
        self.patterns = pattern_matcher
        self.timeline = timeline_builder
    
    async def analyze(
        self,
        signals: List[SignalEvent],
        existing_trends: Dict[str, Dict] = None,
    ) -> List[CorrelationResult]:
        """Analyze cross-source correlations in collected signals.
        
        Args:
            signals: All signals from latest collection cycle
            existing_trends: Known trends (to update, not just create new)
        
        Returns:
            List of CorrelationResult for topics with significant correlation
        """
        # 1. Group signals by topic
        topic_groups: Dict[str, List[SignalEvent]] = {}
        for signal in signals:
            topic = signal.extracted_topic.lower().strip()
            if not topic:
                continue
            if topic not in topic_groups:
                topic_groups[topic] = []
            topic_groups[topic].append(signal)
        
        logger.info(f"Grouped {len(signals)} signals into {len(topic_groups)} topics")
        
        # 2. Analyze each topic for cross-source correlation
        results: List[CorrelationResult] = []
        
        for topic, topic_signals in topic_groups.items():
            # Get unique sources for this topic
            sources: Set[str] = set(s.source for s in topic_signals)
            source_count = len(sources)
            
            # Single-source topics can still be interesting if signal is strong
            # But multi-source = much stronger
            if source_count < 1:
                continue
            
            # 3. Build per-source data
            source_data: Dict[str, Dict] = {}
            for signal in topic_signals:
                if signal.source not in source_data:
                    source_data[signal.source] = {
                        "signal_type": signal.signal_type.value,
                        "value": signal.value,
                        "delta": signal.delta,
                        "weight": signal.weight,
                        "detected_at": signal.detected_at.isoformat() if signal.detected_at else None,
                        "url": signal.url,
                        "title": signal.title,
                        "context": signal.context
                    }
                else:
                    # Multiple signals from same source — take the strongest
                    if signal.value > source_data[signal.source]["value"]:
                        source_data[signal.source] = {
                            "signal_type": signal.signal_type.value,
                            "value": signal.value,
                            "delta": signal.delta,
                            "weight": signal.weight,
                            "detected_at": signal.detected_at.isoformat() if signal.detected_at else None,
                            "url": signal.url,
                            "title": signal.title,
                            "context": signal.context
                        }
            
            # 4. Pattern matching
            pattern_match, pattern_multiplier = self.patterns.match(sources)
            
            # 5+ sources override
            if source_count >= 6:
                pattern_multiplier = max(pattern_multiplier, 2.5)
            elif source_count >= 5:
                pattern_multiplier = max(pattern_multiplier, 2.0)
            
            # 5. Calculate scores
            source_diversity = min(100, (source_count / 16) * 100)  # 16 = max sources
            
            spread_velocity = self.timeline.calculate_spread_velocity(topic_signals)
            
            signal_strength = self.scorer.calculate_signal_strength(
                topic_signals, source_data
            )
            
            pattern_bonus = (pattern_multiplier - 1.0) * 100
            
            # 6. Composite correlation score
            base_score = (
                source_diversity * 0.30 +
                min(100, spread_velocity * 20) * 0.25 +
                signal_strength * 0.25 +
                min(100, pattern_bonus) * 0.20
            )
            
            correlation_score = min(100, base_score * pattern_multiplier)
            
            # 7. Build spread timeline
            spread_timeline = self.timeline.build(topic_signals)
            first_signal = min(topic_signals, key=lambda s: s.detected_at or datetime.max)
            
            # 8. Create result
            result = CorrelationResult(
                topic=topic,
                sources_firing=sorted(sources),
                source_count=source_count,
                correlation_score=round(correlation_score, 1),
                pattern_match=pattern_match,
                pattern_multiplier=pattern_multiplier,
                first_source=first_signal.source,
                first_detected=first_signal.detected_at or datetime.utcnow(),
                spread_timeline=spread_timeline,
                spread_velocity=round(spread_velocity, 2),
                source_signals=source_data,
                signal_strength=round(signal_strength, 1),
                is_high_confidence=(correlation_score > 70 and source_count >= 3)
            )
            
            results.append(result)
        
        # Sort by correlation score
        results.sort(key=lambda r: r.correlation_score, reverse=True)
        
        logger.info(
            f"Correlation analysis: {len(results)} topics, "
            f"{sum(1 for r in results if r.is_high_confidence)} high-confidence"
        )
        
        return results
```

### Engine 3: Velocity Analyzer (core/velocity/)

```python
# backend/app/core/velocity/analyzer.py

from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import numpy as np


@dataclass
class VelocitySnapshot:
    timestamp: datetime
    signals_total: int
    signals_delta: int
    velocity: float
    acceleration: float
    source_breakdown: Dict[str, int]
    correlation_score: float
    active_sources: int


@dataclass
class TrendAnalysis:
    trend_id: str
    topic: str
    trend_score: float
    velocity_score: float
    correlation_score: float
    signal_strength: float
    velocity_1h: float
    velocity_6h: float
    velocity_24h: float
    acceleration: float
    signal_count_1h: int
    signal_count_6h: int
    signal_count_24h: int
    signal_count_7d: int
    status: str
    is_viral: bool
    is_breaking: bool
    sparkline: List[int]


class VelocityAnalyzer:
    """Analyzes signal velocity and determines trend status.
    
    Формулы:
    
    1. Velocity (signals per hour):
       v = Δsignals / Δtime_hours
    
    2. Acceleration:
       a = Δvelocity / Δtime
       Positive = trend accelerating
       Negative = trend decelerating
    
    3. Velocity Score (0-100):
       Normalized velocity relative to category baseline.
       v_score = min(100, (velocity / category_baseline) * 50)
    
    4. Trend Score (composite, 0-100):
       trend_score = (
           velocity_score * 0.25 +
           correlation_score * 0.30 +   # КЛЮЧЕВОЙ: cross-source корреляция
           signal_strength * 0.20 +
           engagement_score * 0.10 +
           novelty_score * 0.10 +
           source_diversity * 0.05
       )
    
    5. Status determination:
       - emerging:  velocity > 0 AND acceleration > 0 AND signal_count_24h < 50
       - active:    velocity > 0 AND signal_count_24h >= 50
       - peaking:   velocity > 0 AND acceleration < 0
       - declining: velocity < 0
       - dead:      signal_count_1h == 0 AND velocity_24h < 2
    
    6. Viral: acceleration > 3.0 AND correlation_score > 80 AND velocity_24h > 100
    7. Breaking: velocity_1h > 50 AND source_count >= 4 AND correlation_score > 70
    """
    
    def __init__(self):
        self.viral_acceleration = 3.0
        self.viral_velocity = 100
        self.breaking_velocity = 50
        self.breaking_sources = 4
    
    async def analyze_trend(
        self,
        trend_id: str,
        signals: List[Dict],
        history: List[VelocitySnapshot],
        correlation_score: float,
        source_count: int,
        signal_weights: List[float],
    ) -> TrendAnalysis:
        now = datetime.utcnow()
        
        # Count signals by window
        s_1h = self._count_since(signals, now - timedelta(hours=1))
        s_6h = self._count_since(signals, now - timedelta(hours=6))
        s_24h = self._count_since(signals, now - timedelta(hours=24))
        s_7d = self._count_since(signals, now - timedelta(days=7))
        
        # Velocity
        v_1h = self._velocity(signals, hours=1)
        v_6h = self._velocity(signals, hours=6)
        v_24h = self._velocity(signals, hours=24)
        
        # Acceleration
        acceleration = self._acceleration(history)
        
        # Scores
        velocity_score = min(100, v_24h * 2)
        signal_strength = self._signal_strength(signal_weights)
        engagement = min(100, sum(s.get("value", 0) for s in signals[:100]) / 100)
        novelty = 100 if s_24h > 0 and s_7d < s_24h * 3 else 50
        diversity = min(100, (source_count / 16) * 100)
        
        trend_score = (
            velocity_score * 0.25 +
            correlation_score * 0.30 +
            signal_strength * 0.20 +
            engagement * 0.10 +
            novelty * 0.10 +
            diversity * 0.05
        )
        
        status = self._status(v_1h, v_24h, acceleration, s_1h, s_24h)
        is_viral = (acceleration > self.viral_acceleration and
                    correlation_score > 80 and v_24h > self.viral_velocity)
        is_breaking = (v_1h > self.breaking_velocity and
                      source_count >= self.breaking_sources and
                      correlation_score > 70)
        sparkline = self._sparkline(history, 48)
        
        return TrendAnalysis(
            trend_id=trend_id, topic="",
            trend_score=round(trend_score, 1),
            velocity_score=round(velocity_score, 1),
            correlation_score=round(correlation_score, 1),
            signal_strength=round(signal_strength, 1),
            velocity_1h=round(v_1h, 1), velocity_6h=round(v_6h, 1),
            velocity_24h=round(v_24h, 1), acceleration=round(acceleration, 2),
            signal_count_1h=s_1h, signal_count_6h=s_6h,
            signal_count_24h=s_24h, signal_count_7d=s_7d,
            status=status, is_viral=is_viral, is_breaking=is_breaking,
            sparkline=sparkline,
        )
    
    def _count_since(self, signals, since):
        return sum(1 for s in signals if s.get("detected_at", datetime.min) >= since)
    
    def _velocity(self, signals, hours):
        now = datetime.utcnow()
        cutoff = now - timedelta(hours=hours)
        count = sum(1 for s in signals if s.get("detected_at", datetime.min) >= cutoff)
        return count / max(hours, 1)
    
    def _acceleration(self, history, window=6):
        if len(history) < 2:
            return 0.0
        recent = sorted(history, key=lambda h: h.timestamp)[-window:]
        if len(recent) < 2:
            return 0.0
        velocities = [s.velocity for s in recent]
        x = np.arange(len(velocities))
        return float(np.polyfit(x, velocities, 1)[0])
    
    def _signal_strength(self, weights):
        if not weights:
            return 0.0
        return min(100, (sum(weights) / max(len(weights), 1)) * 100)
    
    def _status(self, v_1h, v_24h, accel, s_1h, s_24h):
        if s_1h == 0 and v_24h < 2:
            return "dead"
        if v_24h < 0:
            return "declining"
        if v_24h > 0 and accel < 0:
            return "peaking"
        if v_24h > 0 and s_24h < 50:
            return "emerging"
        return "active"
    
    def _sparkline(self, history, periods=48):
        if not history:
            return [0] * periods
        recent = sorted(history, key=lambda h: h.timestamp)[-periods:]
        return [s.signals_delta for s in recent]
```

### Engine 4: Prediction Engine (core/predictor/)
*(Аналогичен v1.0 с ключевым изменением: вместо cross_platform_spread используем cross_source_correlation. Features обновлены:)*

```python
# Обновлённые feature weights для Signal Intelligence
FEATURE_WEIGHTS = {
    "cross_source_correlation": 0.25,   # ГЛАВНЫЙ фактор: сколько sources firing
    "velocity_acceleration": 0.18,      # скорость роста скорости
    "signal_strength": 0.15,            # взвешенная сила сигналов
    "pattern_match": 0.12,              # совпадение с known patterns
    "volume_spike": 0.10,               # резкий рост объёма
    "source_diversity": 0.08,           # разнообразие источников (tier mix)
    "topic_novelty": 0.05,              # новизна темы
    "historical_pattern": 0.04,         # совпадение с историческими трендами
    "sentiment_shift": 0.03,            # изменение тональности
}
```

### Engine 5: Content Brief Generator (core/brief_generator/)

```python
# backend/app/core/brief_generator/engine.py

from typing import Dict
from app.ai.client import ClaudeClient


class BriefGenerator:
    """AI-powered content brief generator.
    
    Генерирует actionable briefs на основе:
    - Данных тренда (topic, velocity, sources, prediction)
    - Формата контента (article, video, thread, etc.)
    - Целевой аудитории и тональности
    
    Brief включает:
    1. Hook — attention-grabbing opening (< 280 chars)
    2. Key Points — что осветить (3-7 пунктов)
    3. Structure — структура контента по формату
    4. SEO — ключевые слова, хэштеги
    5. Distribution — где и когда публиковать
    6. CTA — что должен сделать читатель
    """
    
    def __init__(self, ai_client: ClaudeClient):
        self.ai = ai_client
    
    async def generate(
        self,
        trend_data: Dict,
        format: str,
        target_audience: str = "general",
        tone: str = "informative",
        language: str = "en"
    ) -> Dict:
        sources_text = "\n".join([
            f"  [{s.get('source', '?')}] {s.get('title', '')[:100]}"
            for s in trend_data.get("source_signals", {}).values()
        ][:10])
        
        prediction = trend_data.get("prediction", {})
        prediction_text = ""
        if prediction:
            prediction_text = f"\nPREDICTION: +{prediction.get('predicted_growth', 0):.0f}%, peak {prediction.get('predicted_peak_at', '?')}, confidence {prediction.get('confidence', 0):.0f}%"
        
        prompt = f"""Generate content brief for trending topic.

TOPIC: {trend_data.get('topic', '')}
DESCRIPTION: {trend_data.get('description', '')}
CATEGORY: {trend_data.get('category', '')}
VELOCITY: {trend_data.get('velocity_24h', 0):.1f} signals/hour
CORRELATION: {trend_data.get('correlation_score', 0):.1f}% ({trend_data.get('source_count', 0)} sources)
{prediction_text}

SIGNAL SOURCES:
{sources_text}

FORMAT: {format}
TARGET AUDIENCE: {target_audience}
TONE: {tone}
LANGUAGE: {language}

Generate complete, actionable brief as JSON."""
        
        response = await self.ai.complete(
            system_prompt=CONTENT_BRIEF_SYSTEM_PROMPT,
            user_prompt=prompt,
            max_tokens=2000,
            temperature=0.7
        )
        
        import json
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"title": "Brief", "full_brief": response, "format": format}
```

### AI Client + Guardrails

```python
# backend/app/ai/client.py

import httpx
import logging
from app.config import settings
from app.ai.guardrails import AIGuardrails

logger = logging.getLogger(__name__)


class ClaudeClient:
    """Claude API wrapper with guardrails.
    
    БЕЗОПАСНОСТЬ (Bible 12.7, 12.8):
    - system/user/assistant РАЗДЕЛЕНИЕ (НЕ конкатенация)
    - Input validation через AIGuardrails
    - Output validation через AIGuardrails
    - Retry с exponential backoff
    - НИКОГДА user input в system prompt
    """
    
    API_URL = "https://api.anthropic.com/v1/messages"
    MODEL = "claude-sonnet-4-20250514"
    
    def __init__(self):
        self.guardrails = AIGuardrails()
        self.client = httpx.AsyncClient(
            headers={
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            timeout=60.0
        )
    
    async def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.5,
    ) -> str:
        sanitized = self.guardrails.sanitize_input(user_prompt)
        
        payload = {
            "model": self.MODEL,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system_prompt,
            "messages": [{"role": "user", "content": sanitized}]
        }
        
        try:
            response = await self.client.post(self.API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            content = data.get("content", [{}])[0].get("text", "")
            return self.guardrails.validate_output(content)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                logger.warning("Claude API rate limit")
                raise RateLimitError("AI rate limit exceeded")
            raise


class RateLimitError(Exception):
    pass
```

```python
# backend/app/ai/guardrails.py

import re
import logging

logger = logging.getLogger(__name__)


class AIGuardrails:
    """Input/Output validation for AI interactions.
    
    - Санитизация input ПЕРЕД отправкой
    - Валидация output ПЕРЕД использованием
    - Injection pattern detection + logging
    """
    
    INJECTION_PATTERNS = [
        r"ignore (?:all )?(?:previous )?instructions",
        r"you are now", r"new persona", r"override",
        r"pretend (?:you|to be)", r"forget (?:everything|all)",
        r"system prompt", r"jailbreak", r"DAN mode",
    ]
    
    MAX_INPUT = 5000
    MAX_OUTPUT = 10000
    
    def sanitize_input(self, text: str) -> str:
        text = text[:self.MAX_INPUT]
        text_lower = text.lower()
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, text_lower):
                logger.warning(f"Injection detected: {pattern}")
                text = re.sub(pattern, "[FILTERED]", text, flags=re.IGNORECASE)
        return text
    
    def validate_output(self, text: str) -> str:
        text = text[:self.MAX_OUTPUT]
        text = re.sub(r"(?i)(system prompt|instructions?:).*?\n", "", text)
        return text
```

### Celery Tasks Pipeline

```python
# backend/app/tasks/celery_app.py

from celery import Celery
from celery.schedules import crontab
from app.config import settings

celery_app = Celery(
    "trendradar",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,      # 5 min max per task
    task_soft_time_limit=240,
    worker_max_tasks_per_child=100,  # Restart worker after 100 tasks (memory leak prevention)
)

# Scheduled tasks
celery_app.conf.beat_schedule = {
    # Signal collection
    "collect-tier1-signals": {
        "task": "app.tasks.signal_collection.collect_tier1",
        "schedule": 300.0,  # Every 5 minutes
    },
    "collect-tier2-signals": {
        "task": "app.tasks.signal_collection.collect_tier2",
        "schedule": 900.0,  # Every 15 minutes
    },
    
    # Processing
    "run-correlation-engine": {
        "task": "app.tasks.correlation.run_correlation",
        "schedule": 600.0,  # Every 10 minutes (after signals collected)
    },
    "update-velocity-snapshots": {
        "task": "app.tasks.velocity.update_snapshots",
        "schedule": 900.0,  # Every 15 minutes
    },
    
    # Predictions
    "generate-predictions": {
        "task": "app.tasks.predictions.generate_predictions",
        "schedule": 1800.0,  # Every 30 minutes
    },
    "validate-past-predictions": {
        "task": "app.tasks.predictions.validate_predictions",
        "schedule": crontab(hour=0, minute=0),  # Daily at midnight
    },
    
    # Alerts
    "check-alerts": {
        "task": "app.tasks.alerts.check_all_alerts",
        "schedule": 300.0,  # Every 5 minutes
    },
    
    # Maintenance
    "source-health-check": {
        "task": "app.tasks.source_health.check_all_sources",
        "schedule": 600.0,  # Every 10 minutes
    },
    "cleanup-old-signals": {
        "task": "app.tasks.cleanup.cleanup_old_data",
        "schedule": crontab(hour=3, minute=0),  # Daily at 3 AM
    },
    "reset-daily-counters": {
        "task": "app.tasks.cleanup.reset_daily_counters",
        "schedule": crontab(hour=0, minute=0),  # Daily at midnight
    },
    "update-category-counts": {
        "task": "app.tasks.analytics.update_category_counts",
        "schedule": 3600.0,  # Every hour
    },
}
```

```python
# backend/app/tasks/signal_collection.py

from app.tasks.celery_app import celery_app
from app.core.signals.manager import SignalManager
from app.core.signals.registry import SignalSourceRegistry
import logging

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.signal_collection.collect_tier1")
def collect_tier1():
    """Collect signals from Tier 1 sources (every 5 min).
    
    Tier 1: Google Trends, Reddit, HN, YouTube, GitHub, Wikipedia, Google News
    """
    import asyncio
    
    async def _collect():
        registry = SignalSourceRegistry()
        manager = SignalManager(registry=registry, ...)
        
        # Collect signals
        results = await manager.collect_all(tier="tier1")
        
        # Process: normalize, deduplicate, extract topics
        clean_signals = await manager.process_signals(results)
        
        # Save to database
        saved = await _save_signals(clean_signals)
        
        logger.info(
            f"Tier 1 collection: {sum(len(r.signals) for r in results.values())} raw → "
            f"{len(clean_signals)} processed → {saved} saved"
        )
        
        return {"raw": sum(len(r.signals) for r in results.values()),
                "processed": len(clean_signals), "saved": saved}
    
    return asyncio.run(_collect())


@celery_app.task(name="app.tasks.signal_collection.collect_tier2")
def collect_tier2():
    """Collect signals from Tier 2 sources (every 15 min).
    
    Tier 2: ProductHunt, npm, PyPI, ArXiv, CoinGecko, Steam, Dev.to, Lobsters, StackOverflow
    """
    import asyncio
    
    async def _collect():
        registry = SignalSourceRegistry()
        manager = SignalManager(registry=registry, ...)
        results = await manager.collect_all(tier="tier2")
        clean_signals = await manager.process_signals(results)
        saved = await _save_signals(clean_signals)
        logger.info(f"Tier 2: {len(clean_signals)} processed, {saved} saved")
        return {"processed": len(clean_signals), "saved": saved}
    
    return asyncio.run(_collect())
```

```python
# backend/app/tasks/correlation.py

from app.tasks.celery_app import celery_app
from app.core.correlation.engine import CorrelationEngine
import logging

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.correlation.run_correlation")
def run_correlation():
    """Run cross-source correlation analysis (every 10 min).
    
    Pipeline:
    1. Load recent signals (last 6 hours)
    2. Run CorrelationEngine.analyze()
    3. Update trend scores based on correlation
    4. Create/update trends in database
    5. Push updates to real-time channel
    """
    import asyncio
    
    async def _correlate():
        engine = CorrelationEngine(...)
        
        # Load recent signals
        recent_signals = await _load_recent_signals(hours=6)
        
        # Run correlation
        results = await engine.analyze(recent_signals)
        
        # Process results
        new_trends = 0
        updated_trends = 0
        
        for result in results:
            if result.correlation_score < 20:  # Below threshold
                continue
            
            # Find or create trend
            existing = await _find_trend(result.topic)
            
            if existing:
                # Update existing trend
                await _update_trend(existing.id, result)
                updated_trends += 1
            else:
                # Create new trend
                await _create_trend(result)
                new_trends += 1
            
            # Trigger alerts if applicable
            if result.is_high_confidence:
                await _check_alerts_for_trend(result)
        
        logger.info(
            f"Correlation: {len(results)} topics analyzed, "
            f"{new_trends} new trends, {updated_trends} updated, "
            f"{sum(1 for r in results if r.is_high_confidence)} high-confidence"
        )
        
        return {"analyzed": len(results), "new": new_trends, "updated": updated_trends}
    
    return asyncio.run(_correlate())
```

```python
# backend/app/tasks/source_health.py

from app.tasks.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.source_health.check_all_sources")
def check_all_sources():
    """Check health of all signal sources (every 10 min).
    
    - Runs health_check() on each adapter
    - Updates source_health table
    - Alerts admin if critical sources are down
    - Manages cooldown for failing sources
    """
    import asyncio
    
    async def _check():
        from app.core.signals.registry import SignalSourceRegistry
        
        registry = SignalSourceRegistry()
        results = {}
        
        for name, adapter in registry.get_all_adapters().items():
            try:
                healthy = await adapter.health_check()
                results[name] = {
                    "healthy": healthy,
                    "checked_at": datetime.utcnow().isoformat()
                }
                
                if not healthy:
                    logger.warning(f"Source {name} health check FAILED")
                    # Check if we should alert admin
                    await _maybe_alert_admin(name)
                    
            except Exception as e:
                results[name] = {"healthy": False, "error": str(e)}
                logger.error(f"Source {name} health check error: {e}")
        
        healthy_count = sum(1 for r in results.values() if r.get("healthy"))
        total = len(results)
        
        logger.info(f"Source health: {healthy_count}/{total} healthy")
        
        # Alert if more than 30% sources are down
        if healthy_count < total * 0.7:
            await _alert_admin_critical(f"Only {healthy_count}/{total} sources healthy!")
        
        return results
    
    from datetime import datetime
    return asyncio.run(_check())
```

---

## 🤖 AI ПРОМПТЫ

### System Prompt: Topic Extraction (НОВЫЙ)

```python
# backend/app/ai/prompts/topic_extraction.py

class TopicExtractionPromptBuilder:
    
    SYSTEM_PROMPT = """You are TrendRadar's Topic Extraction AI.
Your job is to extract the main TOPIC or TREND from a raw signal title.

A signal might be:
- A Hacker News story title
- A GitHub repo name + description
- A Reddit post title
- A Google Trends rising query
- A Wikipedia article title
- A news headline

You must extract the UNDERLYING TREND or TOPIC, not the specific instance.

Examples:
- "Show HN: I built a GPT-5 API wrapper in Rust" → "GPT-5"
- "openai/gpt-5-sdk: Official SDK for GPT-5 API" → "GPT-5"
- "GPT-5 benchmark results leak shows 40% improvement" → "GPT-5"
- "Apple Vision Pro 2 spotted in FCC filings" → "Apple Vision Pro 2"
- "visionpro-dev/spatial-ui: Framework for Vision Pro apps" → "Apple Vision Pro"
- "Bitcoin crosses $150K as institutional buying surges" → "Bitcoin price rally"
- "Rust overtakes Java in TIOBE index for first time" → "Rust programming language growth"

RULES:
- Extract the TOPIC, not the full title
- Normalize names: "GPT5", "GPT-5", "gpt 5" → "GPT-5"
- Group related signals under the same topic
- Keep topics concise (2-6 words)
- Return ONLY JSON

OUTPUT FORMAT:
{
    "topic": "GPT-5",
    "confidence": 0.95,
    "category_hint": "ai",
    "related_topics": ["OpenAI", "Large Language Models"],
    "is_specific_event": true,
    "event_type": "product_launch"
}"""
```

### System Prompt: Prediction (обновлённый для Signal Intelligence)

```python
# Обновлённый prediction prompt (отличие от v1.0):
# Вместо "platform breakdown" показываем "source signals"

PREDICTION_USER_PROMPT = """Analyze this trend and provide a prediction.

TREND DATA:
- Topic: {topic}
- Description: {description}
- Category: {category}

CROSS-SOURCE CORRELATION:
  Sources firing: {source_count} / 16
  Correlation score: {correlation_score}
  Pattern match: {pattern_match} (multiplier {pattern_multiplier}x)
  
SIGNAL BREAKDOWN:
{signal_breakdown}
  Example:
  google_trends:  interest=85, type=search_interest, rising +340%
  reddit:         score=4500, type=trending, r/technology, r/artificial
  hackernews:     score=450, position=#3, type=score_spike
  github:         stars_today=800, repo=openai/gpt-5-sdk, type=new_entry
  wikipedia:      pageviews=50000, spike_ratio=25x, type=pageview_spike

VELOCITY:
  Signals/hour: {velocity}
  Acceleration: {acceleration}

SPREAD TIMELINE:
{spread_timeline}
  Example:
  06:45 - hackernews (score_spike, score=450)
  07:30 - reddit (trending, r/technology)
  08:00 - google_trends (search_interest, +340%)
  09:00 - github (new_entry, 800 stars today)
  10:00 - wikipedia (pageview_spike, 25x normal)

Based on this data, provide your analysis as JSON.
Focus on:
1. Is the cross-source correlation pattern genuine or coincidental?
2. Does the spread timeline suggest organic growth or coordinated?
3. Which source signals are strongest predictors?
4. What's the most likely growth trajectory?
5. Are there risk factors that could derail the trend?"""
```

### System Prompt: Classification

```python
CLASSIFICATION_SYSTEM_PROMPT = """You are TrendRadar's Classification AI.
Classify trending topics into categories.

CATEGORIES: tech, ai, crypto, business, science, health, culture, politics,
gaming, finance, sports, design, devtools, opensource

RULES:
- Choose SINGLE most relevant category
- If multi-category, pick PRIMARY: "OpenAI launches GPT-5" → "ai" (not "tech")
- "Apple stock drops" → "finance" (not "tech")
- Return ONLY JSON

OUTPUT: {"category": "ai", "confidence": 0.92, "secondary_category": "tech",
"tags": ["openai", "gpt-5"], "reasoning": "One sentence why"}"""
```

### System Prompt: Content Brief

```python
CONTENT_BRIEF_SYSTEM_PROMPT = """You are TrendRadar's Content Brief AI.
Generate actionable content briefs for trending topics.

PRINCIPLES:
- SPECIFIC and ACTIONABLE — not "write about AI" but specific angles and hooks
- TIMING-aware — if peak in 24h, content must be quick (thread, short video)
- Format-matched — structure for the requested format
- Hook must be under 280 chars (tweetable)
- Include SEO + distribution strategy

OUTPUT FORMAT (JSON only):
{
    "title": "Compelling title",
    "hook": "Attention-grabbing opening (< 280 chars)",
    "key_points": ["Point 1", "Point 2", "Point 3"],
    "target_audience": "Specific audience",
    "tone": "informative",
    "estimated_length": "1500-2000 words",
    "structure": "## Intro\\n## Section 1\\n## Conclusion",
    "suggested_hashtags": ["#tag1"],
    "seo_keywords": ["keyword 1"],
    "best_platforms": ["medium", "twitter"],
    "optimal_publish_time": "Within 6 hours",
    "call_to_action": "What readers should do",
    "full_brief": "Complete detailed brief..."
}

FORMAT GUIDELINES:
- article: 1500-3000 words, Hook→Context→Analysis→Points→Implications→CTA
- video: 5-12 min, Hook(0-15s)→Problem→Content→Summary→CTA
- thread: 8-15 tweets, Hook tweet→Context→Points(1/tweet)→Summary→CTA
- short_post: 100-280 chars, Hook+insight+CTA
- newsletter: 800-1500 words, Subject→Hook→Analysis→Links
- podcast: 15-30 min, Intro→What→Why→Discussion→Outro"""
```

---

## 🎨 UI SPECS

*(Основа идентична v1.0 с обновлениями ниже:)*

### Стиль: как Linear + Vercel
- **Тёмная тема по умолчанию** (light mode available)
- **Чистые линии**, минимум визуального шума
- **Монохромные акценты** + цветные категории
- **Micro-animations**: subtle transitions, hover states
- **Typography**: Inter для UI, JetBrains Mono для данных/чисел

### Цветовая палитра (CSS Variables)
```css
:root {
  --bg-primary: #0a0a0a;
  --bg-secondary: #141414;
  --bg-tertiary: #1a1a1a;
  --bg-card: #1c1c1c;
  --bg-hover: #252525;
  --text-primary: #fafafa;
  --text-secondary: #a1a1aa;
  --text-tertiary: #71717a;
  --border-default: #27272a;
  --border-hover: #3f3f46;
  --accent-primary: #6366f1;
  --accent-hover: #818cf8;
  --status-emerging: #22c55e;
  --status-active: #6366f1;
  --status-peaking: #f59e0b;
  --status-declining: #ef4444;
  --status-dead: #71717a;
  --velocity-hot: #ef4444;
  --velocity-warm: #f59e0b;
  --velocity-cool: #22c55e;
  --confidence-high: #22c55e;
  --confidence-medium: #f59e0b;
  --confidence-low: #ef4444;
  /* Category colors */
  --cat-tech: #6366f1; --cat-ai: #8b5cf6; --cat-crypto: #f59e0b;
  --cat-business: #10b981; --cat-science: #06b6d4; --cat-health: #ef4444;
  --cat-culture: #ec4899; --cat-politics: #64748b; --cat-gaming: #84cc16;
  --cat-finance: #0ea5e9; --cat-sports: #f97316; --cat-design: #d946ef;
  --cat-devtools: #22d3ee; --cat-opensource: #a3e635;
  /* Source colors */
  --src-google: #4285F4; --src-reddit: #FF4500; --src-hn: #FF6600;
  --src-youtube: #FF0000; --src-github: #6e5494; --src-wikipedia: #636466;
  --src-news: #1a73e8; --src-producthunt: #DA552F; --src-npm: #CB3837;
  --src-pypi: #3775A9; --src-arxiv: #B31B1B; --src-coingecko: #8DC63F;
  --src-steam: #171A21; --src-devto: #0A0A0A; --src-lobsters: #AC130D;
  --src-stackoverflow: #F48024;
}
```

### Layout Dashboard
```
┌──────────────────────────────────────────────────────┐
│ ┌─────────┐ ┌────────────────────────────────────┐   │
│ │ Sidebar │ │ Topbar: Search | [EXPLORE][PREDICT] │   │
│ │         │ │         [ALERTS] | 🔔 | 👤          │   │
│ │ Explore │ ├────────────────────────────────────┤   │
│ │ Predict │ │                                    │   │
│ │ Alerts  │ │  Trend Feed / Prediction Feed      │   │
│ │ Search  │ │                                    │   │
│ │         │ │  ┌────────────┐ ┌────────────┐     │   │
│ │ ──────  │ │  │ Trend Card │ │ Trend Card │     │   │
│ │ Tech    │ │  │ Sources:   │ │ Sources:   │     │   │
│ │ AI      │ │  │ GT RD HN  │ │ GT YT GH   │     │   │
│ │ Crypto  │ │  │ Score: 87  │ │ Score: 72  │     │   │
│ │ ...     │ │  │ Corr: 85%  │ │ Corr: 60%  │     │   │
│ │         │ │  └────────────┘ └────────────┘     │   │
│ │ ──────  │ │                                    │   │
│ │ Settings│ │  ┌────────────┐ ┌────────────┐     │   │
│ │ Billing │ │  │ Trend Card │ │ Trend Card │     │   │
│ └─────────┘ │  └────────────┘ └────────────┘     │   │
│             └────────────────────────────────────┘   │
└──────────────────────────────────────────────────────┘
```

### Visualizations

1. **Velocity Chart (Recharts)** — Area chart, gradient fill, 24-72h, 15-min intervals, hover tooltips, "prediction made here" annotation
2. **Cross-Source Correlation Map (D3.js)** — Network graph with source nodes, correlation edges, node size = signal strength, animated spread timeline
3. **Signal Radar Chart (Recharts)** — Radar with axes for each source, filled area shows which sources are active
4. **Prediction Confidence Gauge** — Half-circle gauge, red/yellow/green zones, animated needle
5. **Category Heatmap** — Calendar heatmap (like GitHub contributions), per category per day
6. **Trend Score Ring** — Apple Watch-style: Velocity (outer), Correlation (middle), Signal (inner)
7. **Signal Strength Bar** — Horizontal bar showing source contributions to trend
8. **Sparkline** — SVG path, 120x30px, green if up / red if down, no axes

### Обновлённые компоненты

**Trend Card: `platforms` → `active_sources`**
```
┌────────────────────────────────────────────────┐
│ [AI] 🟣  GPT-5 Release                   🔖   │
│                                                │
│ OpenAI reportedly preparing to launch GPT-5    │
│                                                │
│ ┌──────────────────────────────────────┐       │
│ │ ▁▂▃▄▅▆▇█ (sparkline velocity chart) │       │
│ └──────────────────────────────────────┘       │
│                                                │
│ Score: ██████████░░░ 87.5                      │
│ Velocity: +312% ↑    │   Signals: 3.4K        │
│                                                │
│ 🔍GT 📰Reddit 🔶HN 📺YT 🐙GH  │  3h ago     │
│ Correlation: 5/16 sources ████████░░ 85%       │
│                                                │
│ [🔮 Prediction: +380% in 72h (78% conf)]      │
└────────────────────────────────────────────────┘
```

**НОВЫЙ: Signal Source Map (вместо Cross-Platform Map)**
```
Визуализация (D3.js): какие sources firing для данного тренда.

    Google Trends  ●━━━━━━━━━━━━━━━━●  Reddit
           ╲                              ╱
            ╲          TOPIC             ╱
             ●━━━━━━━● GPT-5 ●━━━━━━━●
            ╱          Score: 87.5      ╲
           ╱                              ╲
    Hacker News  ●━━━━━━━━━━━━━━━━━●  GitHub
                                          │
                                    Wikipedia ●

● = источник активен (размер = сила сигнала)
━ = корреляция (толщина = сила)
Серые = источники которые НЕ детектируют этот тренд
```

**НОВЫЙ: Source Health Dashboard (Admin)**
```
┌────────────────────────────────────────────────────────┐
│ 📡 SIGNAL SOURCES                      14/16 healthy  │
│                                                        │
│ Tier 1 (Core):                                         │
│ ● Google Trends    healthy   342 signals/24h    1.2s   │
│ ● Reddit           healthy   890 signals/24h    0.5s   │
│ ● Hacker News      healthy   156 signals/24h    0.3s   │
│ ● YouTube          healthy    89 signals/24h    0.8s   │
│ ● GitHub           healthy   234 signals/24h    1.5s   │
│ ● Wikipedia        healthy   178 signals/24h    0.9s   │
│ ● Google News      healthy   445 signals/24h    0.4s   │
│                                                        │
│ Tier 2 (Vertical):                                     │
│ ● Product Hunt     healthy    45 signals/24h    0.6s   │
│ ● npm Registry     healthy    67 signals/24h    0.3s   │
│ ● PyPI Stats       healthy    34 signals/24h    0.4s   │
│ ● ArXiv            healthy    23 signals/24h    0.5s   │
│ ● CoinGecko        healthy    89 signals/24h    0.7s   │
│ ○ Steam Charts     degraded   12 signals/24h    3.2s   │
│ ● Dev.to           healthy    56 signals/24h    0.4s   │
│ ● Lobste.rs        healthy    34 signals/24h    0.2s   │
│ ✗ Stack Overflow   down        0 signals/24h    ---    │
│                                                        │
│ Tier 3 (Optional):                                     │
│ ○ Twitter          not configured                      │
│                                                        │
│ Total: 2,693 signals collected in last 24h             │
└────────────────────────────────────────────────────────┘
```

---

## 🔄 ФАЗЫ РЕАЛИЗАЦИИ

### Фаза 0: Инфраструктура и Auth (5-7 дней)

**Задачи:**

1. **Инициализация проектов**
   - Next.js 14 + TypeScript + Tailwind + shadcn/ui
   - FastAPI + async SQLAlchemy + Celery
   - Docker compose (PostgreSQL + Redis)
   - .env.example, .gitignore, .claudecodeignore
   → Покажи результат → жди OK

2. **Supabase Auth**
   - Email + password, Google OAuth, GitHub OAuth
   - Email verification, password reset
   - Supabase middleware для Next.js
   - JWT validation на FastAPI
   → Покажи результат → жди OK

3. **База данных**
   - Все таблицы: users, categories, trends, signal_events, predictions, alerts, etc.
   - RLS на КАЖДУЮ таблицу
   - Seed категории
   - Alembic migrations
   → Покажи результат → жди OK

4. **Auth UI + Dashboard layout**
   - Login/signup/forgot-password pages
   - Dashboard sidebar + topbar
   - Dark/light mode
   - Mobile responsive
   → Покажи результат → жди OK

**OK-gate**: Auth E2E. Dashboard renders. RLS confirmed.

---

### Фаза 1: Signal Collection Engine (7-10 дней)

**Задачи:**

1. **BaseSignalAdapter + SignalManager**
   - Abstract base class
   - Orchestrator with parallel execution
   - Source health tracking
   - Cooldown logic
   → Покажи результат → жди OK

2. **Tier 1 Adapters: Google Trends + Reddit + HN**
   - Google Trends (pytrends): trending + rising queries
   - Reddit (PRAW): rising + hot from target subreddits
   - Hacker News (Firebase): top + new stories
   - Test each independently
   → Покажи результат → жди OK

3. **Tier 1 Adapters: YouTube + GitHub + Wikipedia + Google News**
   - YouTube Data API: trending videos
   - GitHub: trending page scrape
   - Wikipedia: pageview spikes
   - Google News: RSS feed parsing
   → Покажи результат → жди OK

4. **Tier 2 Adapters: ProductHunt + npm + PyPI + ArXiv + CoinGecko + остальные**
   - Все Tier 2 адаптеры
   - Steam Charts, Dev.to, Lobsters, StackOverflow
   → Покажи результат → жди OK

5. **Topic Normalizer + Deduplicator + AI Topic Extractor**
   - Rule-based normalization
   - Cross-source deduplication (same topic from different sources)
   - Claude-based topic extraction для сложных случаев
   → Покажи результат → жди OK

6. **Celery Scheduled Tasks**
   - Tier 1 collection: каждые 5 минут
   - Tier 2 collection: каждые 15 минут
   - Source health check: каждые 10 минут
   - Error handling, retry logic, logging
   → Покажи результат → жди OK

**OK-gate**: 15+ adapters collecting signals. SignalManager orchestrates. Deduplication works. Health tracking works. Celery runs on schedule.

---

### Фаза 2: Correlation Engine + Velocity + Trends API + EXPLORE UI (7-10 дней)

**Задачи:**

1. **Cross-Source Correlation Engine**
   - CorrelationEngine: group by topic, count sources, apply patterns
   - PatternMatcher: known correlation patterns + multipliers
   - SpreadTimelineBuilder: chronological spread across sources
   - CorrelationScorer: compute correlation_score
   → Покажи результат → жди OK

2. **Velocity Analyzer**
   - Signal velocity, acceleration
   - TrendScorer (composite score with correlation)
   - Status determination (emerging/active/peaking/declining/dead)
   - Snapshot every 15 minutes
   → Покажи результат → жди OK

3. **Trends API**
   - GET /api/v1/trends (feed + filters + pagination)
   - GET /api/v1/trends/:id (detail with signal breakdown)
   - GET /api/v1/trends/:id/velocity
   - GET /api/v1/sources/status
   - Redis caching
   → Покажи результат → жди OK

4. **EXPLORE Mode UI**
   - Trend feed (infinite scroll, cards, skeletons)
   - Trend card with source icons + correlation bar
   - Filters (category, source, status, min score)
   - Trend detail page (velocity chart, signal breakdown, source map)
   - Category explorer
   - Search (Cmd+K)
   → Покажи результат → жди OK

**OK-gate**: Correlation engine detects multi-source trends. EXPLORE UI shows real data. Signal breakdown visible on detail page. Source status dashboard works.

---

### Фаза 3: Prediction Engine + PREDICT Mode (7-10 дней)

**Задачи:**

1. **Feature Extractor (Signal Intelligence версия)**
   - Extract features: cross_source_correlation, velocity_acceleration, signal_strength, pattern_match, volume_spike, source_diversity, topic_novelty, historical_pattern, sentiment_shift
   - Normalize all features to 0-1
   - Use correlation data as PRIMARY feature (weight 0.25)
   → Покажи результат → жди OK

2. **Prediction Engine**
   - ML-based confidence from feature weights
   - Claude integration: send signal breakdown + correlation data → get AI reasoning
   - Confidence calibration (historical accuracy feedback loop)
   - Peak timing prediction (based on spread velocity + source count patterns)
   - Growth estimation formula
   → Покажи результат → жди OK

3. **Prediction Validation System**
   - Daily task: compare past predictions (72h ago) with actual outcomes
   - Calculate accuracy_score per prediction
   - Update calibrator with new data
   - Track accuracy by category, confidence tier, source combination
   → Покажи результат → жди OK

4. **Predictions API**
   - GET /api/v1/predictions (feed + filters)
   - GET /api/v1/predictions/:id (detail with source signals)
   - GET /api/v1/predictions/accuracy
   - Celery task: generate predictions every 30 min
   - Celery task: validate past predictions daily
   → Покажи результат → жди OK

5. **PREDICT Mode UI**
   - Prediction feed (sorted by confidence)
   - Prediction card: confidence gauge, growth %, timeline, factors
   - Prediction detail page: full AI reasoning, source signal breakdown, spread timeline
   - Factor breakdown: which sources drove the prediction
   - Prediction accuracy dashboard
   - "Generate Content Brief" button on each prediction
   → Покажи результат → жди OK

**OK-gate**: Predictions generated from correlation + signal data. PREDICT UI shows predictions with source-based factors. Accuracy tracking works.

---

### Фаза 4: Alerts + Content Briefs (5-7 дней)

**Задачи:**

1. **Alert System Backend**
   - Alert CRUD API (with source filter support)
   - Alert trigger detection: Celery task every 5 min checks velocity + correlation against alert thresholds
   - Alert trigger history with read/unread tracking
   - Notification dispatch: email via Resend, webhook via httpx
   - Plan limits: Creator = 3, Pro+ = unlimited
   → Покажи результат → жди OK

2. **ALERT Mode UI**
   - Alert list with active/inactive toggle
   - Create/edit form: categories, keywords, sources (with source icons), velocity slider, correlation slider
   - Notification channel selection (email, push, webhook)
   - Alert trigger history with trend links
   - Unread badge on sidebar
   → Покажи результат → жди OK

3. **Content Brief Generator Backend**
   - BriefGenerator engine with Claude
   - Format-specific prompts (article, video, thread, short_post, newsletter, podcast)
   - POST /api/v1/briefs/generate endpoint
   - GET /api/v1/briefs for history
   - Plan limits: Creator = 5/day, Pro+ = unlimited
   → Покажи результат → жди OK

4. **Content Brief UI**
   - Generation modal: select format, audience, tone (with format previews)
   - Brief display card: title, hook, key points, hashtags, SEO, platforms, timing
   - Format-specific tabs
   - Copy to clipboard (full brief, hook only, hashtags only)
   - Brief history list
   → Покажи результат → жди OK

**OK-gate**: Alerts created, triggered, notifications sent. Content briefs generated for all formats. UI fully functional.

---

### Фаза 5: Billing + Plan Gating (5-7 дней)

**Задачи:**

1. **Stripe Integration**
   - Products + prices: Creator ($19/m, $190/y), Pro ($79/m, $790/y), Business ($299/m, $2990/y)
   - Checkout session creation
   - Customer portal (manage subscription, payment method, invoices)
   - Webhook handler: checkout.session.completed, subscription.created/updated/deleted, invoice.payment_failed/succeeded
   - Subscription sync → update users.plan
   → Покажи результат → жди OK

2. **Plan Gating (backend middleware)**
   - Usage tracking: Redis counters for daily limits
   - Check plan on EVERY protected endpoint
   - Free: 3 trend views/day, no predictions, no alerts, no briefs
   - Creator: unlimited trends, basic predictions (24h), 3 alerts, 5 briefs/day
   - Pro: full access, 60 API calls/min
   - Business: team + custom categories, 120 API calls/min
   - Rate limiting per plan
   - Reset daily counters at midnight UTC
   → Покажи результат → жди OK

3. **Billing UI**
   - Pricing page (marketing + dashboard versions)
   - Subscription management: current plan, usage meters, upgrade/downgrade
   - Usage meter component (visual progress bars)
   - Upgrade prompts: inline banners when hitting free tier limits
   - Invoice history
   - Plan comparison feature table
   → Покажи результат → жди OK

4. **Team Management (Business+)**
   - Team creation with slug
   - Member invitation by email
   - Role management (owner, admin, member, viewer)
   - Seat tracking (max 5 for Business)
   - Shared custom categories within team
   → Покажи результат → жди OK

**OK-gate**: Stripe checkout → subscription created. Plan gating enforced. Upgrade prompts shown. Team management works.

---

### Фаза 6: Share Cards + API Keys + Embeds (5-7 дней)

**Задачи:**

1. **Shareable Trend Cards**
   - POST /api/v1/share/card: create share card with frozen data snapshot
   - OG image generation (Next.js Edge API): trend topic, growth %, confidence, source icons, TrendRadar branding, "Predicted X days ago" watermark
   - Public share page (/share/:token): renders trend card without auth
   - Twitter share: pre-filled tweet with OG image
   - Copy link button
   → Покажи результат → жди OK

2. **Embeddable Widgets**
   - iframe embed code generator
   - Embed endpoint: serves standalone HTML card (dark + light themes)
   - Responsive (auto-resize with postMessage)
   - Brand attribution link "Powered by TrendRadar"
   - Allow/disallow embed per card
   → Покажи результат → жди OK

3. **API Key Management (Pro+)**
   - Key generation: `tr_live_` + 32 random chars
   - Store SHA-256 hash only (NEVER plain key)
   - Key prefix for display ("tr_live_aBcD...")
   - Key rotation (new key, old key revoked)
   - Scope management: read, write, predict
   - API key auth middleware: check hash, verify active, enforce rate limit
   - Usage tracking per key
   → Покажи результат → жди OK

4. **Public API Documentation**
   - API docs page (custom, NOT Swagger in production)
   - Interactive examples with real responses
   - Code samples: curl, Python, Node.js, Ruby
   - Authentication guide
   - Rate limit documentation
   - Error codes reference
   → Покажи результат → жди OK

**OK-gate**: Share cards with OG images. Public share page. Embeds. API keys authenticate and rate limit.

---

### Фаза 7: Landing Page + Deploy + Security (5-7 дней)

**Задачи:**

1. **Landing Page** (стиль: Vercel/Linear)
   - Hero: animated signal flow visualization, "Predict trends before they go viral"
   - "Powered by 15+ signal sources" logo wall (Google, Reddit, HN, GitHub, etc.)
   - Feature showcase: EXPLORE / PREDICT / ALERT with screenshots
   - How it works: Signal Intelligence pipeline visualization (animated)
   - Live demo: real trending topics (3 free trends visible)
   - "TrendRadar Called It": showcase of correct past predictions
   - Competitor comparison table (vs Google Trends, Exploding Topics, etc.)
   - Pricing section
   - FAQ
   - CTA: "Start free — 3 trends per day, no credit card"
   → Покажи результат → жди OK

2. **Email Templates (Resend)**
   - Welcome email (with onboarding steps)
   - Alert notification: trend name, velocity, sources, link to trend
   - Weekly digest: top 5 predictions, accuracy stats
   - Subscription confirmation
   - Payment failed
   - All templates: responsive HTML, dark theme, brand-consistent
   → Покажи результат → жди OK

3. **Performance Optimization**
   - Next.js: ISR for landing (revalidate 60s), CSR for dashboard
   - Redis caching: trend feed (5 min TTL), category counts (15 min)
   - Database: EXPLAIN ANALYZE on hot queries, add missing indexes
   - Image optimization: next/image, Cloudflare R2 CDN
   - Bundle analysis: remove unused imports, tree-shake
   - Lighthouse: target 90+ performance score
   → Покажи результат → жди OK

4. **CI/CD + Deployment**
   - GitHub Actions: lint → test → Semgrep → Snyk → deploy
   - Frontend: Vercel (auto-deploy on main)
   - Backend: Railway or Render (Docker deploy on main)
   - Environment variables: all secrets via platform config
   - SSL/TLS: automatic via Vercel + Railway
   - Domain: trendradar.io + api.trendradar.io
   → Покажи результат → жди OK

5. **Monitoring + Analytics**
   - Sentry: frontend + backend error tracking
   - PostHog: page views, feature usage, funnel analysis
   - Telegram bot: server alerts (errors, restarts, failed payments)
   - Uptime monitoring: UptimeRobot or Better Uptime
   - Signal source health dashboard (admin)
   → Покажи результат → жди OK

6. **Security Audit (полный чеклист из Bible 12.1-12.21)**
   - Semgrep SAST scan: 0 critical/high findings
   - Snyk dependency scan: 0 critical vulnerabilities
   - Manual review: RLS policies on ALL tables
   - Rate limiting: verified with curl loop (expect 429)
   - CORS: whitelist only trendradar.io domains (NOT *)
   - Security headers: HSTS, CSP, X-Frame-Options, X-Content-Type-Options
   - server_tokens off: nginx version hidden
   - Swagger/docs: disabled in production
   - Health endpoint: only {"status": "ok"} public
   - Console.log cleanup: no sensitive data in prod
   - Source maps: OFF in production
   - .env: not in git, .env.example has placeholders only
   - API keys: SHA-256 hashed, never stored plain
   - AI I/O: system/user separation, guardrails active
   - Port audit: nmap, close everything except 80/443/SSH
   - SQL: all parameterized (SQLAlchemy), no string concat
   - Auth: Supabase (bcrypt), MFA available
   - Frontend: no business logic, no isAdmin checks
   - Incident response protocol: documented
   → Покажи результат → жди OK

**OK-gate**: Landing page beautiful. CI/CD working. Monitoring active. Security audit passed. Production LIVE.

---

### Фаза 8: Growth + Premium Sources (ongoing)

**Задачи:**

1. **"TrendRadar Called It" weekly automation** — compare past predictions with outcomes
2. **Twitter adapter** ($100/мес when MRR > $5K) — прямые tweets
3. **Browser Extension** — бесплатный extension, пользователи дают анонимизированные данные
4. **Historical Data** (Business+) — 90/365 day archive
5. **Custom Categories** (Business+)
6. **Integrations** — Slack, Discord, Zapier, Notion
7. **SocialRadar integration** — когда/если доступен
8. **Data provider** (Brandwatch) — когда MRR > $50K

---

## 🔒 БЕЗОПАСНОСТЬ

### Полный Security Checklist (Bible 12.1-12.21)

```
КЛЮЧИ И СЕКРЕТЫ:
☐ Все API ключи в .env (Reddit, YouTube, Anthropic, OpenAI, Stripe, Resend)
☐ .env в .gitignore
☐ .env.example содержит ТОЛЬКО placeholders
☐ Production: AES-256-GCM encryption для хранимых ключей
☐ Pre-commit hook: проверка staged на секреты
☐ Короткоживущие токены (Supabase, Railway)
☐ git-secrets hook установлен

БАЗА ДАННЫХ:
☐ RLS включен на КАЖДОЙ таблице (users, trends, signal_events, predictions, alerts, alert_triggers, content_briefs, subscriptions, api_keys, teams, team_members, share_cards, usage_logs, user_bookmarks, user_custom_categories, source_health)
☐ Policies проверены для каждой роли
☐ SQL параметризация (SQLAlchemy, НЕ строковая подстановка)
☐ Индексы на все FK + часто запрашиваемые поля
☐ Партиционирование signal_events и usage_logs по месяцам

АУТЕНТИФИКАЦИЯ:
☐ Supabase Auth (bcrypt by default)
☐ MFA доступна (TOTP)
☐ Пароли НИКОГДА не логируются
☐ Login attempts logged (IP, timestamp, user agent)
☐ Session management через Supabase

АВТОРИЗАЦИЯ:
☐ RBAC: запрещено всё, кроме разрешённого
☐ Plan gating на КАЖДОМ endpoint
☐ Admin endpoints: role check
☐ Team role checks (owner/admin/member/viewer)
☐ API key scopes enforced

RATE LIMITING:
☐ AI endpoints: 10 req/min max
☐ API endpoints: per-plan limits (Free=3/day, Creator=unlimited, Pro=60/min, Business=120/min)
☐ Global rate limit по IP
☐ Per-signal-source rate limiting (respect platform limits)
☐ Brute-force protection на auth

INPUT VALIDATION:
☐ Pydantic schemas на ВСЁ
☐ Max length на text fields
☐ Enum validation для fixed values
☐ URL validation для webhook_url (HTTPS only)

AI I/O VALIDATION:
☐ system/user/assistant разделение
☐ AIGuardrails input sanitization
☐ AIGuardrails output validation
☐ Injection pattern detection
☐ Max length limits

ЗАВИСИМОСТИ:
☐ npm audit / pip audit passed
☐ Нет зависимостей с <1000 downloads
☐ depcheck: нет неиспользуемых
☐ socket.dev проверка

ФРОНТЕНД:
☐ Бизнес-логика на бэкенде
☐ isAdmin / plan checks — ТОЛЬКО бэкенд
☐ console.log cleanup
☐ Source maps OFF
☐ Нет API ключей в клиентском коде

ИНФРАСТРУКТУРА:
☐ Security headers: HSTS, CSP, X-Frame-Options, X-Content-Type-Options
☐ server_tokens off
☐ CORS: whitelist (НЕ *)
☐ Swagger/docs OFF в production
☐ Health: только {"status": "ok"} публично
☐ Аудит портов: nmap + ufw
☐ SSL/TLS everywhere

МОНИТОРИНГ:
☐ Sentry error tracking
☐ Telegram bot alerts
☐ Uptime monitoring
☐ Signal source health monitoring
☐ Failed payment alerts

INCIDENT RESPONSE:
☐ Протокол документирован
☐ Контакты определены
☐ Backup strategy протестирована
☐ Key rotation процедура готова

CI/CD:
☐ Semgrep SAST в pipeline
☐ Snyk dependency scan
☐ Tests pass before deploy

ПЕНТЕСТ:
☐ nmap -sV — порты
☐ Security headers verified
☐ CORS not *
☐ Swagger not in prod
☐ Health не сливает
☐ Rate limiting returns 429
☐ TLS: SSL Labs ≥ A
```

### Stripe Webhook Security
```python
# Signature verification ОБЯЗАТЕЛЬНА
# Endpoint НЕ требует user auth
# Все действия идемпотентны
@router.post("/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    if not sig_header:
        raise HTTPException(400, "Missing signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400, "Invalid signature")
    # Handle event...
    return {"status": "ok"}
```

### FastAPI Security Config
```python
app = FastAPI(
    docs_url=None if settings.ENVIRONMENT == "production" else "/docs",
    redoc_url=None if settings.ENVIRONMENT == "production" else "/redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # ["https://trendradar.io"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}  # МИНИМУМ наружу

@app.get("/api/v1/health/detailed")
@require_admin
async def health_detailed():
    return {"status": "ok", "database": "...", "redis": "...", "sources": {...}}
```

---

## 📤 SHAREABLE TREND CARDS

### OG Image Generation (Next.js Edge)
```typescript
// frontend/src/app/api/og/[trendId]/route.tsx
import { ImageResponse } from 'next/og'
export const runtime = 'edge'

export async function GET(request: Request, { params }: { params: { trendId: string } }) {
  const trend = await fetchTrend(params.trendId)
  if (!trend) return new Response('Not found', { status: 404 })
  
  // Source icons mapping
  const sourceEmojis: Record<string, string> = {
    google_trends: '🔍', reddit: '📰', hackernews: '🔶', youtube_trending: '📺',
    github_trending: '🐙', wikipedia: '📖', google_news: '📰', producthunt: '🚀',
    npm_registry: '📦', coingecko: '🪙', steam_charts: '🎮',
  }
  
  return new ImageResponse(
    (
      <div style={{
        width: '1200px', height: '630px', display: 'flex',
        flexDirection: 'column', justifyContent: 'space-between',
        padding: '60px',
        background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%)',
        fontFamily: 'Inter, sans-serif', color: '#fafafa',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ fontSize: '28px' }}>🔮</span>
          <span style={{ fontSize: '20px', color: '#a1a1aa' }}>
            TrendRadar predicted this {trend.daysAgo} days ago
          </span>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <h1 style={{ fontSize: '52px', fontWeight: 700, margin: 0, lineHeight: 1.2 }}>
            {trend.topic}
          </h1>
          <div style={{ display: 'flex', gap: '40px', fontSize: '24px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>📈</span>
              <span style={{ color: '#22c55e', fontWeight: 600 }}>
                +{trend.growth}% growth
              </span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>🎯</span>
              <span style={{ fontWeight: 600 }}>{trend.confidence}% confidence</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>📡</span>
              <span style={{ fontWeight: 600 }}>{trend.sourceCount} sources</span>
            </div>
          </div>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', gap: '12px', color: '#a1a1aa', fontSize: '18px' }}>
            {trend.activeSources.slice(0, 6).map((s: string) => (
              <span key={s}>{sourceEmojis[s] || '📡'}</span>
            ))}
          </div>
          <span style={{ color: '#6366f1', fontSize: '20px', fontWeight: 500 }}>
            trendradar.io
          </span>
        </div>
      </div>
    ),
    { width: 1200, height: 630 }
  )
}
```

### Embeddable Widget
```typescript
// frontend/src/app/api/embed/[trendId]/route.ts
export async function GET(request: Request, { params }: { params: { trendId: string } }) {
  const trend = await fetchTrend(params.trendId)
  // Returns standalone HTML card with trend data
  // Dark theme by default, responsive, TrendRadar branding
  // X-Frame-Options: ALLOWALL for embedding
  const html = `<!DOCTYPE html><html>
    <head><style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      body { font-family: -apple-system, 'Inter', sans-serif; }
      .card { background: #1c1c1c; border: 1px solid #27272a; border-radius: 12px;
        padding: 20px; color: #fafafa; max-width: 400px; }
      .topic { font-size: 18px; font-weight: 600; margin-bottom: 8px; }
      .stats { display: flex; gap: 16px; font-size: 14px; color: #a1a1aa; }
      .velocity { color: #22c55e; font-weight: 600; }
      .sources { display: flex; gap: 8px; font-size: 12px; color: #71717a; margin-top: 8px; }
      .footer { display: flex; justify-content: space-between; align-items: center;
        padding-top: 12px; border-top: 1px solid #27272a; font-size: 12px; color: #71717a; }
      .footer a { color: #6366f1; text-decoration: none; }
    </style></head>
    <body><div class="card">
      <div class="topic">${trend.topic}</div>
      <div class="stats">
        <span class="velocity">+${trend.velocity24h}% ↑</span>
        <span>Score: ${trend.trendScore}</span>
        <span>${trend.sourceCount} sources</span>
      </div>
      <div class="sources">${trend.activeSources.map((s: string) => s).join(' • ')}</div>
      <div class="footer">
        <span>🔮 TrendRadar</span>
        <a href="https://trendradar.io/trend/${trend.id}" target="_blank">View →</a>
      </div>
    </div></body></html>`
  return new Response(html, {
    headers: { 'Content-Type': 'text/html', 'X-Frame-Options': 'ALLOWALL' }
  })
}
```

---

## 📋 AGENTS.md

```markdown
# AGENTS.md — TrendRadar

## Project
TrendRadar: AI trend prediction platform using Signal Intelligence.
15+ free signal sources → cross-source correlation → AI predictions → content briefs.

## Stack
- Frontend: Next.js 14.2, TypeScript 5.4, Tailwind 3.4, shadcn/ui
- Backend: Python 3.12, FastAPI 0.111, SQLAlchemy 2.0 (async), Celery 5.4
- Database: PostgreSQL 16 (Supabase), Redis 7.2
- AI: Claude API (claude-sonnet-4-20250514), OpenAI Embeddings
- Auth: Supabase Auth
- Billing: Stripe
- Deploy: Vercel (frontend), Railway (backend)

## Architecture
Signal Intelligence: collect signals from 15+ free sources (Google Trends,
Reddit, HN, YouTube, GitHub, Wikipedia, Google News, ProductHunt, npm, PyPI,
ArXiv, CoinGecko, Steam, Dev.to, Lobsters, StackOverflow).
Cross-source correlation → velocity analysis → AI prediction.
NOT scraping social media posts. Aggregating already-aggregated signals.

## Commands
```
cd frontend && npm run dev
cd frontend && npm run build
cd backend && uvicorn app.main:app --reload
cd backend && celery -A app.tasks.celery_app worker -l info
cd backend && celery -A app.tasks.celery_app beat -l info
cd backend && pytest
cd backend && alembic upgrade head
docker-compose up -d
```

## Rules
- ONLY modify files related to the current task
- DO NOT refactor unrelated code
- DO NOT add dependencies without explicit approval
- All API keys in .env, NEVER in code
- RLS enabled on ALL database tables
- Input validation (Pydantic) on ALL endpoints
- AI prompts: system/user separation, NEVER concatenation
- Rate limiting on ALL AI endpoints
- Each signal adapter must be independent and resilient
- Self-audit after each change
- Commit after each completed task

## Forbidden
- DO NOT expose API keys or secrets
- DO NOT disable RLS
- DO NOT use Access-Control-Allow-Origin: *
- DO NOT enable Swagger/docs in production
- DO NOT log passwords or sensitive data
- DO NOT put business logic on frontend
- DO NOT use string concatenation for SQL or AI prompts
- DO NOT commit .env files
- DO NOT make one adapter's failure break others

## When compacting preserve
- Current phase and task number
- Last error and fix applied
- Files modified in current session
- Test results
- Signal source health status
- Database migration status
```

---

## ⚠️ КРИТИЧЕСКИЕ ПРАВИЛА (из Bible v3.3)

```
🔴 DRY RUN по дефолту — для ЛЮБОГО действия с реальными API, billing, email
🔴 Блокировка изменений — ONLY requested changes. Do NOT modify other code.
🔴 Self-audit каждой фазы — проверь работу, покажи что тестировать
🔴 OK-gates между фазами — НЕ ПЕРЕХОДИ К СЛЕДУЮЩЕМУ ШАГУ ПОКА Я НЕ ОДОБРЮ
🔴 Коммить после каждой задачи
🔴 ТОЛЬКО запрошенное, минимум сложности
🔴 Визуальная верификация — после каждого UI-изменения скриншот
🔴 Если не уверен — скажи прямо
🔴 Если ошибка не решается за 3 попытки — другой подход
🔴 Ключи .env + шифрование
🔴 RLS на всех таблицах
🔴 Input validation + AI I/O validation
🔴 Security headers, CORS whitelist, Swagger OFF
🔴 Каждый signal adapter — изолирован и resilient
🔴 Source health tracking — автоматический cooldown при failures
```

---

## 🚀 НАЧНИ С ФАЗЫ 0, ШАГ 1

Покажи план инициализации проектов (Next.js + FastAPI + Docker).
Жди OK.
