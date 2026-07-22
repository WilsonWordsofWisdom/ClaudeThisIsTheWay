# DESIGN_GUIDE.md

**Stage:** Design — after the brief, before building any UI.
**Purpose:** Standards for designing interfaces that are clear, consistent, and accessible.

## Principles

1. **Default to Google Material Design.** Use [Material Design](https://m3.material.io) as the baseline reference for components, layout, spacing, elevation, and interaction patterns — unless a project specifies its own design system.
2. **Clarity over cleverness.** The user should never have to think about the interface.
3. **Consistency.** Same patterns, spacing, and language everywhere.
4. **Accessibility by default**, not as an afterthought.
5. **Reuse before invent.** Prefer existing components and patterns over new ones.

## Gate — always offer a mockup first

**Before building UI, ask the human operator whether they'd like to see a mockup or wireframe first.** Don't jump to production code on a visual change without offering this.

## The design doc lives at `docs/design.md`

Record final designs (layouts, key screens, component decisions, visual language) in `docs/design.md`. **Update it whenever the design changes or is refined** during the lifecycle, so it always reflects the current product.

## Checklist — every screen/component covers

- [ ] **Information hierarchy** — the most important thing is the most prominent.
- [ ] **Spacing / type / color system** — consistent scale, not ad-hoc values.
- [ ] **Contrast meets WCAG AA** — text and interactive elements are legible.
- [ ] **All states designed** — empty, loading, error, success, and populated.
- [ ] **Responsive** — works from mobile to desktop; no horizontal overflow.
- [ ] **Keyboard + screen-reader** — focus order, labels, roles, alt text.
- [ ] **Motion restraint** — animation aids understanding, never distracts.
- [ ] **Reuse check** — is there an existing component/pattern for this?

## Defers to

Use `impeccable` / `design-review` (and `design-consultation` / `design-shotgun`) for visual polish and critique; this SOP defines the baseline every design must meet and the artifacts to maintain.
