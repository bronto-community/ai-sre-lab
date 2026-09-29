// Seal lab secrets into a secret gist; the deck only ever sees the ciphertext,
// and only when opened with the link this prints.
//
//   GH_TOKEN=<gist-capable token> node seal.mjs ../.env.gist
//
// The input is KEY=VALUE lines. Output: a secret gist holding sealed.json
// (AES-256-GCM) and the link to hand out in the room:
//   https://aisre-lab.vercel.app/#s=<gist-id>.<key>
// Delete the gist after the event and nothing is left to decrypt.
import { readFileSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { webcrypto as crypto } from 'node:crypto'

const DECK = process.env.DECK_URL ?? 'https://aisre-lab.vercel.app'
const b64u = (buf) => Buffer.from(buf).toString('base64url')

const vars = Object.fromEntries(
  readFileSync(process.argv[2], 'utf8').split('\n')
    .map((l) => l.trim()).filter((l) => l && !l.startsWith('#'))
    .map((l) => [l.slice(0, l.indexOf('=')), l.slice(l.indexOf('=') + 1)]),
)

const raw = crypto.getRandomValues(new Uint8Array(32))
const key = await crypto.subtle.importKey('raw', raw, 'AES-GCM', false, ['encrypt'])
const iv = crypto.getRandomValues(new Uint8Array(12))
const ct = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, new TextEncoder().encode(JSON.stringify(vars)))
const sealed = JSON.stringify({ v: 1, iv: b64u(iv), ct: b64u(ct) })

const gist = JSON.parse(execFileSync('gh', ['api', 'gists', '--input', '-'], {
  input: JSON.stringify({ public: false, description: 'lab', files: { 'sealed.json': { content: sealed } } }),
}))
console.error(`sealed ${Object.keys(vars).join(', ')} into gist ${gist.id} (${gist.owner.login})`)
console.log(`${DECK}/#s=${gist.owner.login}/${gist.id}.${b64u(raw)}`)
