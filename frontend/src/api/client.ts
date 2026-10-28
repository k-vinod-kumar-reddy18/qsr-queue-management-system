export const API = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1'
export function token() { return localStorage.getItem('qsr_token') || '' }
export async function api<T=any>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers || {})
  if (token()) headers.set('Authorization', `Bearer ${token()}`)
  if (options.body && !(options.body instanceof FormData)) headers.set('Content-Type','application/json')
  const response = await fetch(`${API}${path}`, {...options, headers})
  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || `Request failed: ${response.status}`)
  }
  if (response.status === 204) return undefined as T
  return response.json()
}
export async function login(username:string,password:string) {
  const body = new URLSearchParams({username,password})
  const response = await fetch(`${API}/auth/login`, {method:'POST', headers:{'Content-Type':'application/x-www-form-urlencoded'}, body})
  if (!response.ok) throw new Error('Invalid username or password')
  const data = await response.json()
  localStorage.setItem('qsr_token', data.access_token)
  return data
}

export async function apiBlob(path: string): Promise<string> {
  const headers = new Headers()
  if (token()) headers.set('Authorization', `Bearer ${token()}`)
  const response = await fetch(`${API}${path}`, { headers })
  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || `Video request failed: ${response.status}`)
  }
  return URL.createObjectURL(await response.blob())
}
