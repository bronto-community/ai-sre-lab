# Lab slides

Slidev, Bronto theme (same scaffold as [ai-sre-talk](https://github.com/bronto-community/ai-sre-talk)).

```bash
npm install
npm run dev -- --port 3031
npm run build       # -> dist/, deployed to Vercel
```

- Code slides import `agent/` through the `agent` symlink (`<<< @/agent/...`).
  `vite.config.ts` reloads the deck when those files change.
- `<Curl>` renders a copyable curl; `<PrettyToggle>` on the setup slide adds
  `| jq -r .result | glow -` to all of them.
- Lab keys: `SEAL_PASSPHRASE=… GH_TOKEN=… node seal.mjs ../.env.gist` seals `KEY=VALUE`
  lines into the lab's secret gist (address fixed in `components/secrets.ts`). Open the
  deck with `…/#s=<passphrase>` and `<EnvBlock>` fills the `.env` lines. Delete the gist
  after the event and they go dark.
