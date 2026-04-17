# TASK: Deploy hodeia-auth to Railway to fix OAuth

## Role Override
bee

## Priority
P0

## Model Assignment
haiku

## Intent
Deploy hodeia-auth to Railway so `_migrate_schema()` runs and adds missing columns (`github_id`, `provider`, `provider_id`) to the `users` table. This fixes the GitHub OAuth ProgrammingError.

## Steps — Execute ALL of them. Do NOT ask for permission.

1. Link to the hodeia-auth Railway service:
   ```
   MSYS_NO_PATHCONV=1 railway link -s beneficial-cooperation -p peaceful-integrity -e production
   ```

2. Deploy:
   ```
   MSYS_NO_PATHCONV=1 railway up
   ```

3. Wait 60 seconds, then check logs:
   ```
   MSYS_NO_PATHCONV=1 railway logs -n 100
   ```

4. Look for "Migration:" lines in the logs confirming columns were added.

5. Write a response file to `.deia/hive/responses/` with the deploy result.

## Constraints
- You are a BEE. Execute every step. Do NOT ask "Shall I proceed?" — just do it.
- ALWAYS use `MSYS_NO_PATHCONV=1` prefix for ALL Railway CLI commands.
- Do NOT modify any code. This is a deploy-only task.
- If `railway up` fails, report the error in your response file and stop.
- If `railway link` asks for interactive input, use the flags shown above — they should not prompt.
