# LinkedIn Positions Stats Cron App

A Python application that collects and tracks statistics about LinkedIn job positions through automated scheduled runs.

## Description

This application runs as a cron job to gather statistics about job positions from LinkedIn, helping track trends and metrics over time.

## Configuration

### DB Config

Current implementation is set up to work with Posgres DB using SQLAlchemy. Feel free to change db_utils to work with other DB.

### Environment Variables

Create a `.env` file in the root directory with the following variables (template provided in `.env.template`):

```env
# Environment Configuration
ENV=prod
DEBUG=false

# Database Configuration
DB_URL='your db url'

# Telegram Notification Config
BOT_TOKEN=your_bot_token
BOT_USER=your_bot_user
BOT_NAME=your_bot_name
BOT_CHAT_ID=your_bot_chat_id
```

Fill in the Telegram bot configuration with data generated after bot creation.
Currently only `BOT_TOKEN` and `BOT_CHAT_ID` are used by the app; `BOT_USER` and `BOT_NAME` are optional metadata kept in `.env.template` for compatibility.

The app loads variables from `.env` and `.env.<ENV>` when running locally. On Railway, environment variables provided by the platform are used automatically.

## Deployment to Railway

- A Railway-friendly Dockerfile is available at `Dockerfile.railway` (no cron inside the container; the process exits after the job completes).
- GitHub Actions workflow: `Deploy to Railway` (`.github/workflows/deploy-railway.yml`) can be triggered manually via **workflow_dispatch**. Add the following repository secrets: `RAILWAY_TOKEN`, `RAILWAY_PROJECT_ID`, `RAILWAY_SERVICE_ID`. Optional input `environment` picks the Railway environment when provided.
- Railway admin steps:
  1. Create/choose a Railway project and service, and point deployments to this repository using `Dockerfile.railway`. The Dockerfile already sets `CMD ["python", "-u", "/app/main.py"]`; override only if you need a different entrypoint.
  2. In the service Variables panel, add required env vars (`ENV` defaults to `dev` if omitted, `DB_URL`, `BOT_TOKEN`, `BOT_CHAT_ID`). Optional metadata fields like `BOT_USER` and `BOT_NAME` can also be added for consistency with the template.
  3. Use Railway's Cron/Triggers feature to schedule runs for the service (the container stops after finishing the scrape).
  4. Obtain the Project ID, Service ID, and a Project Token from Railway and store them as GitHub secrets for the manual deployment workflow.
