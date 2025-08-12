import { useState } from 'react'

export default function App() {
  const [count, setCount] = useState(0)
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="p-6 rounded-xl shadow-md">
        <h1 className="text-2xl font-bold mb-4">JobFinderPro</h1>
        <p className="mb-4">Frontend scaffold is running.</p>
        <button className="px-4 py-2 bg-blue-600 text-white rounded" onClick={() => setCount(c => c + 1)}>Click {count}</button>
      </div>
    </div>
  )
}