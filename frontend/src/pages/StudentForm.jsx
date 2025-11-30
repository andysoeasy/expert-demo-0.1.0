import React, { useState } from 'react'
import { createStudent } from '../api'

export default function StudentForm({ onDone = () => {} }) {
  const [form, setForm] = useState({
    fio: '',
    group: '',
    diseases: {
      respiratory: false,
      musculoskeletal: false,
      vision: false,
      gi: false,
      derm: false,
      mental: false,
      allergic: false,
      chronic: false
    },
    additional: {
      missed_lesson: 0,
      avg_miss_duration: 0.0,
      dorm: false,
      smoking: false,
      screen_time: 0.0,
      physical_activity: 0.0
    }
  })

  const diseasesToRu = {
    respiratory: 'Респираторные',
    musculoskeletal: 'Опорно-двигательного аппарата',
    vision: 'Зрения',
    gi: 'Желудочно-кишечного тракта',
    derm: 'Дерматовенерологические',
    mental: 'Психические',
    allergic: 'Аллергические',
    chronic: 'Хронические'
  };

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  function setField(path, value) {
    const parts = path.split('.')
    setForm(prev => {
      const copy = JSON.parse(JSON.stringify(prev))
      let cur = copy
      for (let i = 0; i < parts.length - 1; i++) cur = cur[parts[i]]
      cur[parts[parts.length - 1]] = value
      return copy
    })
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setSuccess(null)
    setLoading(true)
    try {
      await createStudent(form)
      setSuccess('Студент успешно добавлен')
      setForm({
        fio: '',
        group: '',
        diseases: {
          respiratory: false,
          musculoskeletal: false,
          vision: false,
          gi: false,
          derm: false,
          mental: false,
          allergic: false,
          chronic: false
        },
        additional: {
          missed_lesson: 0,
          avg_miss_duration: 0.0,
          dorm: false,
          smoking: false,
          screen_time: 0.0,
          physical_activity: 0.0
        }
      })
      onDone()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <form className="max-w-3xl bg-white p-6 rounded shadow" onSubmit={handleSubmit}>
        <h2 className="text-lg font-medium mb-4">Добавить студента</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium">ФИО</label>
            <input required value={form.fio} onChange={e => setField('fio', e.target.value)} className="mt-1 block w-full border rounded px-3 py-2" />
          </div>
          <div>
            <label className="block text-sm font-medium">Группа</label>
            <input required value={form.group} onChange={e => setField('group', e.target.value)} className="mt-1 block w-full border rounded px-3 py-2" />
          </div>

          <div>
            <label className="block text-sm font-medium">Число пропусков (кол-во пар)</label>
            <input type="number" min="0" value={form.additional.missed_lesson} onChange={e => setField('additional.missed_lesson', Number(e.target.value))} className="mt-1 block w-full border rounded px-3 py-2" />
          </div>
          <div>
            <label className="block text-sm font-medium">Средняя длительность пропусков (дни)</label>
            <input type="number" step="0.1" min="0" value={form.additional.avg_miss_duration} onChange={e => setField('additional.avg_miss_duration', Number(e.target.value))} className="mt-1 block w-full border rounded px-3 py-2" />
          </div>

          <div>
            <label className="block text-sm font-medium">Время за монитором (ч/день)</label>
            <input type="number" step="0.1" min="0" value={form.additional.screen_time} onChange={e => setField('additional.screen_time', Number(e.target.value))} className="mt-1 block w-full border rounded px-3 py-2" />
          </div>
          <div>
            <label className="block text-sm font-medium">Физическая активность (ч/неделя)</label>
            <input type="number" step="0.1" min="0" value={form.additional.physical_activity} onChange={e => setField('additional.physical_activity', Number(e.target.value))} className="mt-1 block w-full border rounded px-3 py-2" />
          </div>

          <div className="flex items-center space-x-3">
            <input id="dorm" type="checkbox" checked={form.additional.dorm} onChange={e => setField('additional.dorm', e.target.checked)} />
            <label htmlFor="dorm">Проживает в общежитии</label>
          </div>
          <div className="flex items-center space-x-3">
            <input id="smoking" type="checkbox" checked={form.additional.smoking} onChange={e => setField('additional.smoking', e.target.checked)} />
            <label htmlFor="smoking">Курение</label>
          </div>
        </div>

        <fieldset className="mt-6 border-t pt-4">
          <legend className="text-sm font-medium mb-2 pr-3">Заболевания</legend>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {Object.keys(form.diseases).map(key => (
              <label key={key} className="flex items-center space-x-2">
                <input type="checkbox" checked={form.diseases[key]} onChange={e => setField(`diseases.${key}`, e.target.checked)} />
                {/* <span className="capitalize">{key.replace('_', ' ')}</span> */}
                <span className="capitalize">{diseasesToRu[key]}</span>
              </label>
            ))}
          </div>
        </fieldset>

        <div className="mt-6 flex items-center space-x-3">
          <button disabled={loading} type="submit" className="bg-green-600 text-white px-4 py-2 rounded">{loading ? 'Сохраняю...' : 'Сохранить'}</button>
          <button type="button" onClick={() => { setForm(prev => ({ ...prev, fio: '', group: '' })) }} className="border px-4 py-2 rounded">Очистить</button>
        </div>

        {error && <div className="mt-4 text-red-600">{error}</div>}
        {success && <div className="mt-4 text-green-700">{success}</div>}
      </form>
    </div>
  )
}