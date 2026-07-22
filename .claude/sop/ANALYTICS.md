# ANALYTICS.md

**Stage:** Measure — after the first release, then continuously.
**Purpose:** Instrument the product so we can tell whether it achieves the PRD's goals.

## Principles

1. **Measure what matters.** Track metrics tied to real outcomes, not vanity numbers.
2. **Close the loop with the brief.** Analytics exists to answer the PRD's success metrics.
3. **Privacy-respecting.** Collect the minimum; never put PII in events.

## Metrics framework

Default to **Google HEART** as the lens for product metrics — **H**appiness, **E**ngagement, **A**doption, **R**etention, **T**ask success — paired with the **Goals → Signals → Metrics** method to turn each dimension into concrete, trackable events. Complement with **Amplitude's North Star framework** (one north-star metric plus a few input metrics) to keep focus. Anchor both to the PRD's success metrics and north star.

## Recommend an analytics page after first release

**After the product's first release, recommend to the human operator that a product-analytics view/page be created.** Don't build it silently or prematurely — raise it as the natural next step once there are real users.

## Work with the operator on metrics

- **Identify the key metrics** to monitor, track, record, and analyse.
- **Refine metrics over time** as understanding of the product improves.
- **Reference `docs/PRD.md`** — the success metrics and **north star** are the primary inputs before building the analytics page (per project).

## Tooling

- **Chrome Lighthouse** to start — performance and quality baselines (Core Web Vitals, accessibility, best practices).
- **Amplitude** (or similar) for event-based product analytics and journey funnels.
- **In-app logging & event tracing** — instrument the app itself to derive analytics that off-the-shelf tools miss: time taken to complete key tasks, per-step timings, and journey progression. Build lightweight, privacy-safe instrumentation directly into the product.

## Dashboard & SLOs

The analytics / alerting dashboard should surface standard service-level objectives, with alerts when thresholds are breached:

- **Uptime / availability**
- **Error rate**
- **Latency** (p50 / p95 / p99)
- **Transaction completion rate**
- **Drop-off count** — by journey and step.

**Flag dropped or incomplete journeys** to the operator — highlight which user journeys or workflows are frequently abandoned or left incomplete, based on real usage, so they can be investigated and improved.

## Instrumentation checklist

- [ ] **Events tied to PRD metrics** — every tracked event maps to a success metric.
- [ ] **Consistent naming** — a clear, documented event-naming scheme.
- [ ] **No PII in events** — anonymize/aggregate; respect privacy.
- [ ] **Capture failures** — errors and drop-offs, not just happy paths.
- [ ] **Task timing** — capture time-to-complete for key tasks and journeys.
- [ ] **Journey completion & drop-off** — track step-by-step progression to spot abandonment.
- [ ] **Verify events actually fire** — confirm data lands before trusting it.
- [ ] **Review outcomes vs. success criteria** — feed learnings back into `docs/PRD.md`.
- [ ] **Privacy** — no PII in analytics; comply with `SECURITY_ASSESSMENT.md` (GDPR/PDPA) rules.

## Defers to

This is the loop-closing stage: findings here update the PRD (`PRODUCT_BRIEF.md`) and shape the next cycle.
