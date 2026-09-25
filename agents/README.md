# ecomOS agents: the catalogue

Date: 25 Sep 2026. Status: design, for Kevin's review. Companion to `ARCHITECTURE.md` and the Blueprint page (`reviews/blueprint/`).

This folder defines every agent that runs a brand inside ecomOS, what each one can do, how its prompt is built, which tools and skills it holds, and which sub-agents it spawns. The goal is a set of capabilities that is mutually exclusive and collectively exhaustive: everything a competent person could do for an e-commerce brand from a laptop is owned by exactly one agent, and the only thing the founder must do is decide.

## Layout

```
agents/
  README.md            this file: framework, prompt structure, skill system, tools, autonomy
  catalogue.json       every capability, one record each, machine readable
  CATALOGUE.md         the same catalogue as a readable index by agent
  SKILLS.md            index of every skill, its owner and when it is invoked
  loop/                the 7 agents that run and guard the loop
    ORCHESTRATOR.md  DIAGNOSE.md  PROPOSE.md  REGISTRAR.md  QA-GATE.md  BRAIN-KEEPER.md  REFERENCE-SCOUT.md
  specialists/         the 8 agents that do the work
    SITE.md  CREA.md  MEDIA.md  LIFE.md  ORG.md  PROD.md  MONEY.md  BRAND.md
  skills/              SKILL.md files for the shared skills every agent may call
```

Each agent file has the same shape: front matter, identity and scope, the system prompt skeleton, tools, skills, sub-agents, capability index, gaps.

## Capability record

Every capability is one JSON record in `catalogue.json`:

| Field | Meaning |
|---|---|
| `id` | `<AGENT>-C<nn>` |
| `name` | short verb phrase |
| `folders` | idea bank folders it draws on |
| `what` | 1 to 3 plain sentences, e-commerce specific |
| `encompasses` | the sub-tasks, in detail |
| `inputs` | brand brain sections, connectors, metric contract fields, the approved idea |
| `outputs` | artefact types: report, brief, draft, change list, registry entry, page, flow |
| `trigger` | daily, weekly, monthly, event, on demand, continuous |
| `autonomy` | `agent_does`, `founder_gate`, `human_assist` |
| `external_write` | whether it needs a write and on which surface |
| `tools`, `skills`, `subagent` | what it uses |
| `sources` | web URLs and idea ids it came from; `found_in` says web, bank or both |
| `founder_sees` | what the founder gets, in one sentence |

Two files sit beside the agents: `REVIEW.json`, the overlap and gap review applied by the builder (merges, reassignments, gap records, autonomy corrections; every change carries its reason and dropped ids stay visible as "merged in"), and `id_aliases.json`, which maps every dropped id to the id that absorbed it so rooms and workflows can keep referring to old ids. Cross-cutting records carry `LOOP-C` ids and an `agent` field naming the loop agent that owns them.

## Autonomy levels

- **agent_does**: safe, reversible, no external write. Runs on its trigger without asking. Examples: a weekly speed audit, tagging support tickets, drafting a report. The founder sees the output, not a request.
- **founder_gate**: needs a decision before it runs. Anything that spends money, changes what a customer sees, touches a brand red line, or writes to an external system. Arrives as a card with 3 buttons: let the agent do it, send to a person, not now.
- **human_assist**: the agent prepares everything and a person acts. Developer briefs, change lists for Ads Manager until writes are on, supplier calls, anything needing a card or an identity.

External writes are off per surface until the founder turns them on. When a surface is on, capabilities that needed `human_assist` only because of the write become `founder_gate`.

## How a prompt is built

Every agent prompt is assembled at run time from 6 parts, in this order. The agent file holds the fixed text; the Orchestrator fills the rest.

1. **Role and scope.** Who it is, what it produces, what it never does. Fixed text from the agent file. Under 300 lines, like a good CLAUDE.md.
2. **Brand context.** The brand brain sections this agent needs, quoted, with freshness stamps. Never the whole brain. Each agent file lists its sections.
3. **Numbers.** The metric contract fields this agent reads, computed in code, with windows and freshness. Missing fields say `unavailable`.
4. **The task.** The approved idea record (or the trigger for a scheduled run), the founder's reason if any, the registry context (what was tried before on this brand for this idea), and references from the Scout when relevant.
5. **Rules.** The global rules (below) plus the agent's own. Fixed text.
6. **Output contract.** The exact artefact shape expected, and the self-check list the agent runs before handing to the QA Gate.

Skills are not in the prompt. The agent loads a skill when a step calls for it, reads it, follows it, and drops it. This keeps the prompt lean.

## Global rules, in every prompt

- Ad accounts, the live site, the email platform and every other external system are read-only until the founder switches writes on for that surface. Until then, produce a brief, a draft, a change list or a pull request.
- Arithmetic in code, never in the model. Period ROAS is total value over total spend. Totals stay separate from breakdowns. Windows end on the last full day.
- Missing or unsupported data shows as unavailable, never as 0.
- Every claim traces to the brand record: approved, site-backed or forbidden. No invented claims or numbers.
- Public web research stays separate from private brand data. Every fetched fact carries its URL and date.
- Competitor material is signal only: layout and mood. Never their text, logos, products or faces.
- Writing for the founder: short sentences, digits, plain words, no jargon, below tenth-grade reading level.
- When in doubt about scope, stop and ask the founder with a specific question and a recommended answer.

## The skill system

A skill is a reusable procedure: a `SKILL.md` with purpose, inputs, steps, checks and the output shape. Skills are how a workflow becomes repeatable across agents, brands and runs.

- **Shared skills** live in `agents/skills/` and any agent may call them: `developer-brief`, `claim-check`, `plain-english-card`, `registry-entry`, `metric-read`, `web-research-budgeted`, `founder-question-round`, `surface-audit`, `rank-candidates`, `report-section`.
- **Agent skills** are listed in each agent file and live next to it. They are domain procedures: `speed-audit`, `welcome-flow-build`, `campaign-purpose-lines`, `landed-cost-model`.
- **Skill lifecycle.** An agent may draft a new skill when it has repeated a procedure 3 times in the registry. The draft goes to a person for review. Approved skills are versioned. A skill that produced a QA failure gets a note and a fix, never a silent edit. Founder feedback changes skills and brand records, never the idea bank.
- **Skill shape.** Front matter (name, owner agent, version, when to invoke, inputs, outputs). Steps as a numbered list, each with the tool it uses. Checks the agent must pass before returning. An example of a good output.

## Tools, in 4 kinds

| Kind | Examples | Access |
|---|---|---|
| Connectors (MCP or API) | Shopify, WooCommerce, Meta Ads, Google Ads, GA4, Search Console, Klaviyo, support desk, Metabase or the store database, Google Drive, Notion | Read by default. Write per surface when switched on. |
| Scripts (deterministic) | `speed_lab/*`, `scripts/ideas.py`, `intelligence/ideas.py`, metric contract computation, crawler and site diff, landed cost model, feed builder | Always preferred over the model for anything with a number. |
| Browser | Headless Chromium for crawls, speed, screenshots, checkout test orders | Read. Test orders only on a copy or with a test gateway. |
| Web | Search and fetch within a token budget per run | Public only, labelled, dated. |

## Model routing

- Small and mid models: collectors, extraction, signal matching, tagging, QA checks, registry work, drafting inside a fixed template.
- Top model: Diagnose narrative, Propose ranking rationale, specialist judgement and creative work, founder chat, anything that challenges a bank idea.
- Code: every sort, sum, ratio, threshold and window.

## MECE discipline

- One owner per capability. When two agents could do a thing, the one that owns the output type owns it, and the other hands off. Hand-offs are named in each agent file.
- The loop agents own process and cross-domain work. Specialists own domain work. The Orchestrator owns nothing a specialist can do.
- New capabilities enter through the catalogue with an owner, sources and an autonomy level. A capability without a trigger and an output is not a capability.
