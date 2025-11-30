import React, { useState } from 'react'
import { analyze } from '../api'

export default function Analysis() {
  const [fio, setFio] = useState('')
  const [group, setGroup] = useState('')
  const [analyzeAll, setAnalyzeAll] = useState(false)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  async function handleAnalyze(e) {
    e?.preventDefault()
    setError(null)
    setResult(null)
    setLoading(true)
    try {
      const res = await analyze({ fio: fio || null, group: group || null, analyze_all: analyzeAll })
      setResult(res)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-3xl">
        <form onSubmit={handleAnalyze} className="bg-white p-6 rounded shadow">
          <h2 className="text-lg font-medium mb-4">Анализ состояния здоровья</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div>
              <label className="block text-sm">ФИО (для индивидуального анализа)</label>
              <input value={fio} onChange={e => setFio(e.target.value)} className="mt-1 block w-full border rounded px-3 py-2" />
            </div>
            <div>
              <label className="block text-sm">Номер группы (для группового анализа)</label>
              <input value={group} onChange={e => setGroup(e.target.value)} className="mt-1 block w-full border rounded px-3 py-2" />
            </div>
            <div className="flex items-center">
              <input id="all" type="checkbox" checked={analyzeAll} onChange={e => setAnalyzeAll(e.target.checked)} />
              <label htmlFor="all" className="ml-2">Проанализировать всех студентов</label>
            </div>
          </div>

          <div className="mt-4">
            <button disabled={loading} type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">{loading ? 'Идёт анализ...' : 'Анализировать'}</button>
          </div>

          {error && <div className="mt-4 text-red-600">{error}</div>}
        </form>

        {result && (
          <div className="mt-6 bg-white p-6 rounded shadow">
            <h3 className="text-md font-semibold">Результат — {result.subject}</h3>
            {result.summary && <p className="text-sm text-gray-600">{result.summary}</p>}

            <ul className="mt-4 space-y-4">
              {result.causes.map((c, i) => (
                <li key={i} className="border rounded p-3">
                  <div className="flex items-center justify-between">
                    <strong>{c.name}</strong>
                    <span className="text-sm text-gray-700">Уверенность: <span className="font-medium">{c.confidence}%</span></span>
                  </div>
                  <p className="mt-2 text-sm">{c.recommendation}</p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}