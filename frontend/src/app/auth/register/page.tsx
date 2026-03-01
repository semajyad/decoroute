'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    full_name: '',
    certification_level: 'Open Water'
  })
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const response = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Registration failed')
      }

      router.push('/auth/login?message=Registration successful')
    } catch (err: any) {
      setError(err.message || 'Registration failed')
    } finally {
      setIsLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-white">
            Create your DecoRoute account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-400">
            Start planning safe diving adventures
          </p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-900 border border-red-700 text-red-100 px-4 py-3 rounded">
              {error}
            </div>
          )}
          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-300">
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-500 text-white bg-gray-800 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Enter your email"
                value={formData.email}
                onChange={handleChange}
              />
            </div>
            
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-300">
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-500 text-white bg-gray-800 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Choose a username"
                value={formData.username}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="full_name" className="block text-sm font-medium text-gray-300">
                Full name
              </label>
              <input
                id="full_name"
                name="full_name"
                type="text"
                required
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-500 text-white bg-gray-800 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Enter your full name"
                value={formData.full_name}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="certification_level" className="block text-sm font-medium text-gray-300">
                Certification Level
              </label>
              <select
                id="certification_level"
                name="certification_level"
                required
                className="mt-1 block w-full px-3 py-2 border border-gray-600 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                value={formData.certification_level}
                onChange={handleChange}
              >
                <option value="Open Water">Open Water</option>
                <option value="Advanced Open Water">Advanced Open Water</option>
                <option value="Rescue Diver">Rescue Diver</option>
                <option value="Divemaster">Divemaster</option>
                <option value="Assistant Instructor">Assistant Instructor</option>
                <option value="Instructor">Instructor</option>
                <option value="Master Instructor">Master Instructor</option>
                <option value="Course Director">Course Director</option>
              </select>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-500 text-white bg-gray-800 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Create a password"
                value={formData.password}
                onChange={handleChange}
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Creating account...' : 'Create account'}
            </button>
          </div>

          <div className="text-center">
            <span className="text-gray-400">Already have an account? </span>
            <Link 
              href="/auth/login" 
              className="font-medium text-blue-400 hover:text-blue-300"
            >
              Sign in
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}
