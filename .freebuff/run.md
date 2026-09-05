# Run doc — Persian edgetunnel workspace (static preview)

This workspace is a **static HTML frontend + a Cloudflare Worker**. There is no `package.json`/npm dev server and no runtime dependencies to install. The Preview tab serves the HTML files directly (no server process, no port).

## Reproduce the uncommitted artifacts

A fresh checkout needs nothing that is not in the repo:
- No `.env.local` is used by the local panel HTML pages.
- The Persian panel is built by `tools/build_fa_panel.py` from `tools/main.zip` (the pristine upstream `edt-pages` snapshot). If you ever rebuild the panel, run:
  - `python tools/build_fa_panel.py` — regenerates `panel/admin/index.html` (and any other translated pages) from the dictionary in `tools/fa_panel/fa_dict.py`.
- The worker is a single file, `_worker.js`. It is not served here; deploy it with Wrangler/Cloudflare separately. The local `panel/` folder is the static frontend it can point at via the `PANEL`/`ADMIN` binding.

No secrets are required to view the local panel pages in the Preview tab. Never copy secret values into this doc.

## How to run the server

Nothing to start. To preview in this thread:
- Register `panel/login/index.html` (or `panel/admin/index.html`) via `register_preview` with `htmlPath`. The desktop app serves it as a standalone page.
- If you instead want a live dev server from the repo root on a chosen port (e.g. 3000), use any static file server. One option that already matches this project's single-file nature:
  - `npx serve -l <port> panel` (no install needed for a one-off preview), or
  - a detached PowerShell launch if the run doc requires a long-lived process:
    ```powershell
    $log = "C:\Users\paya\Desktop\New folder (3)\.freebuff\preview-91a5a366-78cb-4b8d-be1c-5cbccb54488e.log"
    powershell -NoProfile -Command "(Start-Process -FilePath 'npx.cmd' -ArgumentList 'serve','-l','3000','-s','panel' -RedirectStandardOutput $log -RedirectStandardError \"$log.err\" -WindowStyle Hidden -PassThru).Id"
    ```
  - Adapt the port if 3000 is in use.
