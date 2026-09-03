# Push to github.com/SamOHON0/rscbus

Run these from this folder in your own terminal (VS Code) — the sandbox
here is blocked from pushing to this repo.

    git init -b main
    git add -A
    git commit -m "Initial build: RSC Buses static site"
    git remote add origin https://github.com/SamOHON0/rscbus.git
    git push -u origin main

## Vercel

Import the repo in Vercel and use:

- Framework preset: **Other**
- Build command: *(leave empty)*
- Output directory: *(leave empty / root)*
- Install command: *(leave empty)*

`vercel.json` already sets `trailingSlash: true`, which the directory-style
URLs (`/services/`, `/golf-trips/`) depend on.

Then point `rscbuses.ie` at it once the client is happy with the draft.
