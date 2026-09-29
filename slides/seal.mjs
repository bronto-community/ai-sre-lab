// Seal lab secrets into the lab's secret gist, locked with a passphrase that
// people can type: https://aisre-lab.vercel.app/#s=<passphrase>
//
//   SEAL_PASSPHRASE='…' GH_TOKEN=<ai-sre-lab token> node seal.mjs ../.env.gist
//
// The input is KEY=VALUE lines. The key is derived with PBKDF2 (600k rounds,
// random salt); the gist holds only salt, iv and ciphertext. The gist address
// is fixed in components/secrets.ts. Delete the gist after the event and
// nothing is left to decrypt or guess against.
import { readFileSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { webcrypto as crypto } from 'node:crypto'

const GIST = '321ed642983e8b88bcb71b4a07b66ddd'   // keep in sync with components/secrets.ts
const ROUNDS = 600_000
const b64u = (buf) => Buffer.from(buf).toString('base64url')

const pass = process.env.SEAL_PASSPHRASE
if (!pass) throw new Error('set SEAL_PASSPHRASE')
const vars = Object.fromEntries(
  readFileSync(process.argv[2], 'utf8').split('\n')
    .map((l) => l.trim()).filter((l) => l && !l.startsWith('#'))
    .map((l) => [l.slice(0, l.indexOf('=')), l.slice(l.indexOf('=') + 1)]),
)

const salt = crypto.getRandomValues(new Uint8Array(16))
const base = await crypto.subtle.importKey('raw', new TextEncoder().encode(pass), 'PBKDF2', false, ['deriveKey'])
const key = await crypto.subtle.deriveKey(
  { name: 'PBKDF2', salt, iterations: ROUNDS, hash: 'SHA-256' }, base,
  { name: 'AES-GCM', length: 256 }, false, ['encrypt'])
const iv = crypto.getRandomValues(new Uint8Array(12))
const ct = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, new TextEncoder().encode(JSON.stringify(vars)))
const sealed = JSON.stringify({ v: 2, kdf: 'PBKDF2-SHA256', rounds: ROUNDS, salt: b64u(salt), iv: b64u(iv), ct: b64u(ct) })

execFileSync('gh', ['api', '-X', 'PATCH', `gists/${GIST}`, '--input', '-'], {
  input: JSON.stringify({ files: { 'sealed.json': { content: sealed } } }), stdio: ['pipe', 'ignore', 'inherit'],
})
console.error(`sealed ${Object.keys(vars).join(', ')} into gist ${GIST}`)
