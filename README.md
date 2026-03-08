# github-contribution-generator
Because apparently green squares are now a career skill. This repo is a public demo of how easy it is to grow a very healthy-looking GitHub lawn with automation.

> *Because apparently green squares are now a career skill. This repo is a public demo of how easy it is to grow a very healthy-looking GitHub lawn with automation.*


A Python proof-of-concept that generates a fully populated GitHub contribution graph via automated, backdated Git commits. 

This repository exists to demonstrate what many developers already suspect: a GitHub contribution graph is an easily manipulated proxy metric, and a heavily green profile does not automatically equal engineering excellence.

---
I kept seeing how often GitHub profiles are used as a soft signal in job applications and tech recruitment. A dense, green contribution graph is often read as:
- Consistency
- Discipline
- Productivity
- Coding effort
- "Passion"

But a contribution graph is just a visual summary of timestamp data. It is a metric. And optimizing for a single, easily manipulated metric rarely yields an accurate picture of the underlying system. 

The goal is to **question how much weight we give to green squares** in the first place. This repo is meant to make that tension visible.

---

## How It Works

This project injects backdated timestamps directly into the Git commit metadata using environment variables (`GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE`). 

The script calculates every calendar day between your chosen `START_DATE` and `END_DATE`, randomizes a number of commits for that day, appends a line to a markdown log file, and commits the change to Git history.
