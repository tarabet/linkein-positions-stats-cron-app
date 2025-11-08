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
