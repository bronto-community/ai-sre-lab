import { ref } from 'vue'

// Lab secrets, opened with the link from the room: #s=<owner>/<gist-id>.<key>
// The gist holds only ciphertext; the key never leaves the browser, and the
// fragment is never sent to any server. Delete the gist and this goes dark.
const STORE = 'ai-sre-lab:seal'
export const secrets = ref<Record<string, string>>({})

const b64u = (s: string) => Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/')), (c) => c.charCodeAt(0))

async function open(seal: string) {
  const [path, k] = seal.split('.')
  const res = await fetch(`https://gist.githubusercontent.com/${path}/raw/sealed.json`, { cache: 'no-store' })
  if (!res.ok) throw new Error(`gist ${res.status}`)
  const { iv, ct } = await res.json()
  const key = await crypto.subtle.importKey('raw', b64u(k), 'AES-GCM', false, ['decrypt'])
  const plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: b64u(iv) }, key, b64u(ct))
  secrets.value = JSON.parse(new TextDecoder().decode(plain))
}

if (typeof window !== 'undefined') {
  const m = location.hash.match(/[#&]s=([^&]+)/)
  if (m) {
    try { localStorage.setItem(STORE, m[1]) } catch {}
    // Don't leave the key in the address bar. Slidev's router restores the URL once
    // it starts, so strip it again after that.
    const strip = () => { if (location.hash.includes('s=')) history.replaceState(history.state, '', location.pathname + location.search) }
    strip(); setTimeout(strip, 500); setTimeout(strip, 1500)
  }
  let seal: string | null = null
  try { seal = localStorage.getItem(STORE) } catch {}
  if (seal) open(seal).catch(() => { try { localStorage.removeItem(STORE) } catch {} })
}
