# Mutual Fund Brokerage API

A FastAPI-based backend application for a mutual fund brokerage firm. This application allows users to register, login, fetch mutual fund data via RapidAPI, and manage their investment portfolio.

## Features
- User registration and login with JWT authentication
- Fetch mutual fund data from RapidAPI
- Create and view investment portfolios
- Hourly portfolio value updates using a background scheduler

## Prerequisites
- Python 3.9+
- SQLite (included with Python, no separate installation needed)
- Git (for cloning the repository)
- A RapidAPI key from [mutual-fund API](https://rapidapi.com/suneetk92/api/latest-mutual-fund-nav)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/mutual-fund-api.git
cd mutual-fund-api