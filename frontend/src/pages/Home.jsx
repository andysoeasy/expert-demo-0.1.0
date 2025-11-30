import React from 'react'

export default function Home({ onNavigate = () => {} }) {
  return (
    <div className="prose max-w-none">
      <h2>О системе</h2>
      <p>
        Демоверсия экспертной системы для диагностирования возможных причин распространённых заболеваний среди студентов и выдачи рекомендаций.
      </p>

      <h3>Как пользоваться</h3>
      <ol>
        <li>Перейдите на "Добавить студента" и внесите данные (ФИО, группа, заболевания, дополнительные параметры).</li>
        <li>Перейдите на страницу "Анализ" и выберите анализ по ФИО, по группе или проанализируйте всех студентов.</li>
        <li>Получите список возможных причин с коэффициентом уверенности и рекомендациями.</li>
      </ol>

      <div className="mt-6">
        <button onClick={() => onNavigate('form')} className="bg-blue-600 text-white px-4 py-2 rounded">Добавить студента</button>
        <button onClick={() => onNavigate('analysis')} className="ml-3 border px-4 py-2 rounded">Перейти к анализу</button>
      </div>
    </div>
  )
}