import { ref } from 'vue'

// Lab secrets, opened with the passphrase from the room: …/#s=<passphrase>
// The gist holds only ciphertext; the passphrase never leaves the browser (the
// URL fragment is never sent to a server). Delete the gist and this goes dark.
const GIST = 'ai-sre-lab/321ed642983e8b88bcb71b4a07b66ddd'
const STORE = 'ai-sre-lab:passphrase'
export const secrets = ref<Record<string, string>>({})

const b64u = (s: string) => Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/')), (c) => c.charCodeAt(0))

async function open(pass: string) {
  const res = await fetch(`https://gist.githubusercontent.com/${GIST}/raw/sealed.json`, { cache: 'no-store' })
  if (!res.ok) throw new Error(`gist ${res.status}`)
  const { salt, rounds, iv, ct } = await res.json()
  const base = await crypto.subtle.importKey('raw', new TextEncoder().encode(pass), 'PBKDF2', false, ['deriveKey'])
  const key = await crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt: b64u(salt), iterations: rounds, hash: 'SHA-256' }, base,
    { name: 'AES-GCM', length: 256 }, false, ['decrypt'])
  const plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: b64u(iv) }, key, b64u(ct))
  secrets.value = JSON.parse(new TextDecoder().decode(plain))
}

if (typeof window !== 'undefined') {
  const m = location.hash.match(/[#&]s=([^&]+)/)
  if (m) {
    try { localStorage.setItem(STORE, decodeURIComponent(m[1])) } catch {}
    // Don't leave the passphrase in the address bar. Slidev's router restores the
    // URL once it starts, so strip it again after that.
    const strip = () => { if (location.hash.includes('s=')) history.replaceState(history.state, '', location.pathname + location.search) }
    strip(); setTimeout(strip, 500); setTimeout(strip, 1500)
  }
  let pass: string | null = null
  try { pass = localStorage.getItem(STORE) } catch {}
  // Forget the phrase only if it's wrong (decryption fails), not on a network hiccup.
  if (pass) open(pass).catch((e) => { if (e?.name === 'OperationError') try { localStorage.removeItem(STORE) } catch {} })
}
