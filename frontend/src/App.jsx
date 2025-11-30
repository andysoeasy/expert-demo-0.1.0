import React, { useState } from 'react'
import Home from './pages/Home'
import StudentForm from './pages/StudentForm'
import Analysis from './pages/Analysis'

export default function App() {
  const [page, setPage] = useState('home')

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800">
      <header className="bg-white shadow">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-semibold">Экспертная система: диагностика здоровья студентов</h1>
          <nav className="space-x-3">
            <button onClick={() => setPage('home')} className="px-3 py-1 rounded hover:bg-gray-100">Главная</button>
            <button onClick={() => setPage('form')} className="px-3 py-1 rounded hover:bg-gray-100">Добавить студента</button>
            <button onClick={() => setPage('analysis')} className="px-3 py-1 rounded hover:bg-gray-100">Анализ</button>
          </nav>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {page === 'home' && <Home onNavigate={setPage} />}
        {page === 'form' && <StudentForm onDone={() => setPage('analysis')} />}
        {page === 'analysis' && <Analysis />}
      </main>

      <footer className="bg-white border-t mt-8">
        <div className="container mx-auto px-4 py-4 text-sm text-gray-600">&copy; 2025 Экспертная система — Демонстрация</div>
      </footer>
    </div>
  )
}