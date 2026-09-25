# How to Define Your Ideal Customer Profile (ICP)

source_id: 1OEHklP3jiDou-x66ly42HjXB-o_s4T3U  |  folder: 02-AVT-avatars  |  cards: 8  |  words: 4,179  |  type: talk (podcast transcript, "Fieldnotes")
credibility: Two HubSpot Media practitioners (Kyle Denhoff and Andrew Frost) discussing their own team's process on their own show. Evidence is a mix of internal practice (their persona "Growth Gabby," their "Loop" marketing framework), one HubSpot-run survey ("over 300 marketers," 48% had a documented ICP) with no methodology given, and unsupported opinion/banter (the closing "last word" segment). They work for and plug HubSpot (CRM, portal features), so treat HubSpot-specific claims as vendor-favorable, not independently verified.
date signals: No year stated. References ChatGPT and Claude "projects"/knowledge bases as current, everyday tools for building and querying a persona, and AI-generated call transcripts as routine. This places the advice in the LLM-tooling era; no platform version numbers are given.

## 1. What this source is for

Helps an operator build a documented ideal customer profile (ICP) from scratch, using a three-layer taxonomy (TAM, ICP, persona) to decide who to target, what to say to them, and how deep to make content for them. It gives a concrete data-sourcing and interview method for teams with little or no CRM data, and a method for turning that raw data into a usable, queryable profile with an LLM instead of a static document.

## 2. Principles

1. Split audience thinking into three layers before planning any campaign or content: TAM (total addressable market), ICP (target account/company fit), and persona (the individual stakeholder). The source calls this foundational, "critically important" work to do up front, not an ongoing task. [a1faffe60195][834684cbb868]
2. ICP criteria in this source are firmographic and B2B: industry, company size, location, seniority, job profile, and which department/decision-maker to target. `[B2B-leaning: source frames ICP mainly as a target-company/firmographic concept; a consumer ecommerce brand has no company to profile this way — the source explicitly says B2C needs a different adaptation but does not say what it is]` [a1faffe60195][834684cbb868]
3. Persona is the individual inside a buying committee, not the account: each has distinct daily tasks, career goals, pain points, and success vocabulary (e.g., marketers say CPL/ROAS, sellers say quota/pipeline/president's club). `[B2B-leaning: "buying committee" assumes multiple stakeholders per purchase, which most consumer purchases do not have; source does not say how to model a persona for a single-decision-maker buyer]` [a1faffe60195][834684cbb868]
4. Combine three data streams to build the profile: external (customer surveys, direct conversations, social mining), internal (CRM firmographics), and call/support transcripts (recurring pain points, company types, who seeks information). [ff3969ab7ccb]
5. Qualitative customer interviews are framed as the fastest, easiest high-value data source, even though the idea of doing them "sounds long and hard" before you start. [6f9531c5c473]
6. An LLM can synthesize unstructured qualitative data (transcripts, surveys, firmographics, content performance) into a usable ICP/persona document, in a fraction of the time a team would take by hand ("hours, weeks... months"). [ba49787189ec]
7. The persona should live as an interactive, queryable LLM knowledge base used on every new project, not a static document ("It's not just like a PDF we're passing around"), so it functions as an ongoing messaging QA check. [d7c43255dc6e]
8. Content depth ("altitude": 101 vs. 301) should be set from the specific persona's actual experience level with the topic, not a generic content calendar. [8cf79dbd3fd4]
9. When there is no CRM and no call transcripts, start with social community mining (Reddit, LinkedIn, Instagram) as a temporary, lower-confidence data layer, then move to direct interviews as soon as possible. [e7cebf3b70d1]

## 3. Procedures

**A. Build initial data with no CRM and no transcripts**
1. Search Reddit and similar communities for people describing pain points in your industry, or post asking what they would want from a solution in your space.
2. Search LinkedIn for target companies and job profiles matching your market. `[B2B-leaning: LinkedIn company/job-title search does not translate directly to consumer audiences]`
3. Check Instagram and other platforms where your audience discusses the problem.
4. Ask an LLM (the source names Claude and ChatGPT) to summarize market trends and the most common personas/ICPs in your space, telling it whether you are B2B or B2C.
5. Treat this as a stopgap: the source's stated highest-quality layer is still "get on the phone with someone, get that transcript."

**B. Five-customer interview protocol**
1. Pick your top 5 customers.
2. Ask each for 30 minutes to talk through what is going on for them.
3. If they consent, use an AI tool to auto-generate a transcript of the call.
4. Keep it conversational, not a rigid survey — the goal is raw, unstructured language.
5. Collect all 5 transcripts as input for synthesis (step D).

**C. Assemble the full data layer (when CRM/transcripts exist)**
1. Pull CRM/database fields: industry, company size, location, seniority, job profile.
2. Mine sales and support call transcripts for recurring pain points, company types, and who on the buying side seeks information.
3. Run customer surveys and direct customer conversations.
4. Mine social platforms (LinkedIn, Reddit, Instagram) for pain-point language.
5. If there is no CRM, use LinkedIn to manually research target accounts, and use whatever sales/call transcripts already exist.
6. Package all of it into one place (document or LLM project) as the working data layer.

**D. LLM synthesis of the ICP/persona**
1. Collect inputs: the 5 call transcripts, survey results, CRM firmographics, and your own content-performance data (what is already resonating).
2. Also load information about your own company, products, features and pricing, so the model can connect what you offer to what the audience needs.
3. Upload everything into a dedicated LLM project/knowledge base (ChatGPT or Claude). `[verify UI: confirm the current project/knowledge-base feature, file limits and team-sharing behavior in whichever tool you use]`
4. Ask direct questions: who am I speaking to, what are their pain points, what do they care about most, what themes keep recurring.
5. Ask the model to define an ICP from the demographic and qualitative inputs and turn it into something tangible you can use or share with the team.
6. Review the model's output against the source transcripts before treating it as the documented ICP — the source frames this as compressing synthesis work, not replacing judgment on the raw data.

**E. Operationalize the persona as an on-demand focus group**
1. Keep the persona/ICP knowledge base as a live, dedicated LLM project, not a static document.
2. Have the team use that project for every new campaign, content piece or copy task.
3. Ask directional questions, not yes/no ones: would this resonate with this ICP, will she hate it, how should I position this, what words should I use, how can I make this more impactful.
4. If your publishing platform supports saving a persona for automatic QA checks against new content, use it. `[verify UI: source names HubSpot's own "save your persona to your portal" feature; confirm whether your CMS/publishing tool has an equivalent]`
5. Use the same project to align new hires and long-tenured staff on who the audience is and what they care about.

**F. Set content altitude per persona**
1. Identify the persona's current experience/skill level with the topic (e.g., already runs paid ads vs. has never set one up).
2. Decide 101 (introductory) vs. 301 (advanced) coverage for that topic, for that persona.
3. Feed the LLM your audience context plus content-performance data so the altitude call is grounded in what already works, not guesswork.
4. Covering a topic at multiple altitudes for different audiences is fine; the point is to decide on purpose, not default to one level.

## 4. Rules, thresholds and numbers

| Rule | Number/threshold | Condition | Source's basis | Card |
|---|---|---|---|---|
| Interview sample to start an ICP | 5 customers, 30 minutes each | Starting point when you lack a documented ICP or persona, especially with thin CRM data | Practitioner recommendation, not a statistical claim | 6f9531c5c473 |
| Share of marketers with a documented ICP | 48% of 300+ marketers surveyed had a clear, well-documented ICP (implying 52% did not) | Cited to show how common it is to operate without one | The source's own marketer survey; sample/methodology not given here | ff3969ab7ccb |
| Audience layers | 3 (TAM, ICP, persona) | Applied to any audience-definition task in this framework | The source's internal "Loop" marketing framework | a1faffe60195 |
| Content depth levels | 2 (101, 301) | When deciding how advanced a piece of content should be, per persona per topic | Practitioner framework from HubSpot Media's content team | 8cf79dbd3fd4 |

## 5. Diagnostics and checks

- Check: does the team have a documented ICP at all? How: ask whether marketing, sales and success can point to one shared reference. Good: yes, and it gets used before messaging decisions. Bad: no, or "we know it in our heads." Next: run procedure B (interviews), then D (LLM synthesis).
- Check: does the ICP include persona-level detail, or only company data? How: look for fields on daily tasks, goals and success vocabulary, not just industry/size. Good: firmographic ICP fields and separate per-role persona fields both exist. Bad: only company-level fields, or a persona built from demographics alone. Next: run procedure C, splitting fields per card 834684cbb868.
- Check: is content or copy tested against the persona before it ships? How: see if anyone actually opens the persona project and asks "would this resonate." Good: routine use before publishing. Bad: persona lives in a slide deck nobody reopens. Next: run procedure E.
- Check: is content altitude matched to what the persona already knows? How: compare the piece's assumed knowledge level to what you know that persona does day to day. Good: advanced (301) content for an experienced persona, introductory (101) for a novice one, chosen on purpose. Bad: one altitude applied everywhere regardless of who is reading. Next: run procedure F.

## 6. Tools, settings and named features

- HubSpot CRM: named as a place to store firmographic data if you have none. The speakers work for HubSpot and joke "get a HubSpot," so treat this specific recommendation as vendor-favorable, not a neutral comparison.
- LinkedIn: for researching target companies and job titles (B2B), and for general community mining. `[B2B-leaning]`
- Reddit: for mining pain-point discussions; framed as usable for either B2B or B2C.
- Instagram: named as another platform where an audience may discuss its problem; not elaborated beyond that.
- ChatGPT and Claude: named as the LLMs to build a "project"/knowledge base in, both for one-time ICP synthesis and for an ongoing, queryable persona. `[verify UI: current project/knowledge-base capabilities, upload limits and sharing controls in each tool]`
- HubSpot portal "save your persona" feature: lets saved content get automatic QA checks against the ICP on publish. `[verify UI: HubSpot-specific; confirm whether your own CMS/publishing stack has an equivalent before promising this to a team]`
- "Loop" framework: HubSpot Media's internal marketing framework; ICP/persona work sits in its "Express phase" alongside brand voice definition. Internal terminology, not a public standard.
- "Growth Gabby": HubSpot Media's own named persona (AI-forward, experimental, a marketing executive). An internal example, not a template to copy.
- "Project Teddy Bear": the hosts' joking name for turning the interactive LLM persona into a formal internal tool; references former HubSpot CEO Brian Halligan bringing a teddy bear named after the company persona into meetings and "asking" it for input on decisions.

## 7. Examples and case results

- Example: HubSpot's own survey of "over 300 marketers" found 48% had a clear, well-documented ICP. Presented as the source's own stat; no methodology, date or sample composition is given here, so treat it as an illustrative figure, not a benchmark to cite externally without checking the original report. [ff3969ab7ccb]
- Example: Growth Gabby, HubSpot Media's persona, is described as AI-forward, experimental, and an executive who has already set up several Facebook pages and is generating leads and revenue from Meta ads. Used to justify covering a topic at 301 instead of 101 for her, since a "how to set up a Facebook page" piece would be off-target. [8cf79dbd3fd4]
- Example (anecdote, not a recommended tool): former HubSpot CEO Brian Halligan reportedly kept a teddy bear named after the company's persona in meetings and turned to it for input at decision points, as a "cheesy but concrete" way to keep the customer present in decisions.
- Example: HubSpot Media's own data stack for ICP work is customer survey results, call transcripts and their own content-performance data, fed into an LLM knowledge base to extract insights.

## 8. Mistakes the source warns about

- Operating without a clear, documented ICP: the 48%/52% survey stat is used to show this is common across marketing teams, not rare.
- Building a persona as a static document that gets shared once and never reopened ("it's not just like a PDF we're passing around"), instead of a live, queryable project.
- Conflating TAM, ICP and persona: the hosts admit "we get tripped up on it internally," implying that even practitioners blur these terms when the layers are not kept separate.
- Skipping the upfront research work to save time: the source states plainly that doing this work up front is "critically important," implying that shortcutting it is a mistake, even though the reasoning behind that claim is not elaborated.
- Applying one content altitude to every persona and topic instead of deciding on purpose: the source is explicit that covering multiple altitudes is fine; the mistake is not doing the "who is this for" reasoning first, not the act of covering more than one level.

## 9. Caveats, conflicts and what is missing

- The source states its own limits: ICP/buying-committee framing is B2B, and it explicitly flags that B2C needs a different adaptation without saying what that adaptation is [a1faffe60195][834684cbb868]. For a consumer ecommerce brand: there is usually no company to profile and no multi-stakeholder buying committee, so the ICP layer (industry/size/seniority) and the persona-as-committee-member layer do not map directly onto individual shoppers. `[B2B-leaning: this gap is the source's own admission, not resolved here — do not substitute an invented consumer-ICP schema and call it this source's method]`
- Vendor bias: both speakers work for HubSpot and recommend HubSpot's CRM and HubSpot's portal "save persona" QA feature. Treat those two specific claims as promotional, and verify equivalents in your own stack before relying on them.
- The 48%-of-300-marketers stat comes from a HubSpot-run survey referenced only by number in this transcript; no link, date, or methodology is given here, so it should not be treated as an independently verified industry figure.
- No fixed template or field list is given for the final ICP/persona document beyond the firmographic-vs-persona field split in card 834684cbb868 (industry, location, size, seniority, job profile for ICP; daily tasks, career goals, pain points, vocabulary for persona). The source deliberately favors letting the LLM draft the document from data rather than filling a fixed template, so if a rigid schema is needed, this source is thin on that "how."
- Five interviews is explicitly framed as a fast starting point, not statistical validation; the source does not say when or whether to scale up interview volume.
- No treatment of quantitative/at-scale surveys as a method here beyond the one HubSpot marketer-survey example; the source's method is qualitative (interviews, transcripts, community mining) plus LLM synthesis, not large-sample research design.

## 10. Card index

- [a1faffe60195] Three-tier audience taxonomy: TAM, ICP and persona
- [6f9531c5c473] Run five 30-minute qualitative customer interviews
- [ff3969ab7ccb] Source data externally and pull CRM firmographics
- [ba49787189ec] Synthesize unstructured transcripts into an ICP with an LLM
- [d7c43255dc6e] Use a live LLM persona as an on-demand focus group
- [8cf79dbd3fd4] Set content altitude by persona seniority
- [834684cbb868] Separate ICP data layer from persona scope: firmographics vs committee roles
- [e7cebf3b70d1] Use social communities when CRM and transcripts are missing
