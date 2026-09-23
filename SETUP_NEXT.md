# Next setup steps

No hosting purchase is needed for the initial local build. The complete Drive library is confirmed by the owner. Working API budget: USD160; absolute ceiling: USD200. Existing reported balances are USD20 at DeepSeek and approximately USD20 at OpenAI. These are available balances, not the full budget. No automatic top-ups or paid processing are enabled.

## Keys

Open the `.env` file in this project locally. Paste the DeepSeek key after DEEPSEEK_API_KEY= and the OpenAI key after OPENAI_API_KEY=. Save the file. Do not paste keys in chat. Do not put quotes or spaces around values. Do not upload the file. It is excluded by .gitignore, but that is not encryption: keep the local machine and backups private.

LIVE_INFERENCE_ENABLED remains false. Budget values currently express configuration intent; the application does not yet implement live providers or budget enforcement. Before paid work, implement cost reservation for in-flight requests, actual-usage reconciliation and durable spend tracking.

## GitHub

The connector returned 404 after the owner made ecomOS private. This does not establish deletion; private-repository access may need to be granted to the installed GitHub connection. In GitHub Settings > Applications > Installed GitHub Apps, locate the app used by the Codex/ChatGPT GitHub connection, choose Configure, and ensure ecomOS is included in selected repositories. Do not grant unrelated repositories. If no matching app appears, reconnect GitHub from Codex settings and select this repository. The user should perform the permission grant.

## Drive

No Google password is needed in chat. For local development, a desktop OAuth connection can avoid service-account credential handling: create an owned Google Cloud project, enable Drive API, configure consent/test user as needed, create a Desktop app OAuth client, and complete the browser sign-in. Store downloaded client configuration and resulting tokens only in ignored secrets/. Use a read-only scope. This scope can be broader than one folder; constrain the worker to the confirmed root, explain the actual consent scope, and do not claim folder-only authorization. A folder-shared service account is an alternative when narrower resource access is preferred. We will guide this setup before implementation requires it.

## Evaluation questions are optional input

They are examples of the decisions the finished service must help with, used to test retrieval and recommendations. No customer data is required. We can draft them from the categories and ask the owner to refine them later. Examples: how to diagnose high add-to-cart but low purchases; what evidence an avatar needs; what to change before scaling ads; how to design a creative test; how an offer differs for subscriptions versus one-time purchases. Missing business facts should produce targeted questions, not invented advice.
