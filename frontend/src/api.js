const BASE = 'http://127.0.0.1:8000'

export async function createStudent(payload) {
  const res = await fetch(`${BASE}/students`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Ошибка: ${res.status} ${text}`)
  }
  return res.json()
}

export async function listStudents() {
  const res = await fetch(`${BASE}/students`)
  if (!res.ok) throw new Error(`Ошибка: ${res.status}`)
  return res.json()
}

export async function analyze({ fio, group, analyze_all }) {
  const params = new URLSearchParams()
  if (fio) params.set('fio', fio)
  if (group) params.set('group', group)
  if (analyze_all) params.set('analyze_all', 'true')

  const res = await fetch(`${BASE}/analyze?${params.toString()}`, { method: 'POST' })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Ошибка анализа: ${res.status} ${text}`)
  }
  return res.json()
}

