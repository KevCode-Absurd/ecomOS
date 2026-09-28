# Share the dashboard with the team (Render)

The team gets a link. Each person signs in with their own invite code.
Your OpenAI and Anthropic keys stay in Render's secret settings. The browser never gets them.

## What it costs

- Render Starter: about $7 a month, plus about $0.25 a month for the 1 GB disk.
- Images and AI text calls bill to your OpenAI and Anthropic accounts.
- Caps: 50 images per person per day, 1,500 images for the whole team per month, 200 AI text calls per person per day.

## Before you start

1. Keep the GitHub repo private. It holds sales and ad data.
2. Push the latest commit: `git push`.

## Set up (about 15 minutes, once)

1. Make invite codes on your laptop, 1 per person:
   ```
   python -m meta_gallery.team new kevin
   python -m meta_gallery.team new asha
   ```
   Each prints a code (send it to that person privately) and a `name:hash` line.
   Join the `name:hash` lines with commas. That is `TEAM_CODES`.
2. Go to render.com, sign in with GitHub, click New, then Blueprint, and pick the ecomOS repo.
   Render reads `render.yaml` and creates the `ecomos-dashboard` service.
3. When Render asks for the secret values, fill in:
   - `TEAM_CODES`: the joined `name:hash` lines from step 1
   - `TEAM_OWNERS`: `kevin` (only owners can change targets, approve catalog images or run the stock check)
   - `OPENAI_API_KEY`: your OpenAI key (images)
   - `ANTHROPIC_API_KEY`: your Anthropic key (breakdowns and copy). Optional.
   `TEAM_SECRET` is made by Render. Leave it.
4. Click Apply. After the deploy, open the `.onrender.com` link and sign in with your code.
5. Share the link and each person's code.

## Day to day

- New data: refresh as usual, commit, `git push`. Render redeploys by itself in about 2 minutes.
- Add a person: make a code, add their `name:hash` to `TEAM_CODES` in Render, then save.
- Remove a person: delete their `name:hash` from `TEAM_CODES`. Their sessions stop at once.
- Change caps: edit `TEAM_DAILY_IMAGES` or `TEAM_MONTHLY_IMAGES` in Render.
- See who used what: `/var/data/team/usage_log.jsonl` on the Render disk (Render Shell tab).
- Set a monthly spend limit in your OpenAI and Anthropic billing pages too. It is a second safety net.

## What people can and cannot do

- Can: see every tab, make image variants, product ads and stories, ask AI, leave notes, edit the playbook, packs and tests.
- Cannot: see or download your keys, change targets or settings, approve catalog images, run the stock check.
- Made images, notes and usage counts are kept on the Render disk across deploys.
