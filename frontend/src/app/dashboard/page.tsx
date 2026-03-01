'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

interface User {
  id: number
  email: string
  username: string
  full_name: string
  certification_level: string
  total_dives: number
  created_at: string
}

interface Trip {
  id: number
  name: string
  description: string
  start_date: string
  end_date: string
  total_cost_estimate: number
  status: string
  is_public: boolean
  created_at: string
}

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null)
  const [trips, setTrips] = useState<Trip[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/auth/login')
      return
    }

    const fetchData = async () => {
      try {
        // Fetch user data
        const userResponse = await fetch('http://localhost:8000/api/auth/me', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        })

        if (!userResponse.ok) {
          throw new Error('Failed to fetch user data')
        }

        const userData = await userResponse.json()
        setUser(userData)

        // Fetch trips
        const tripsResponse = await fetch('http://localhost:8000/api/trips/', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        })

        if (tripsResponse.ok) {
          const tripsData = await tripsResponse.json()
          setTrips(tripsData)
        }
      } catch (error) {
        console.error('Error fetching data:', error)
        localStorage.removeItem('token')
        router.push('/auth/login')
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('token')
    router.push('/auth/login')
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-white text-xl">Loading dashboard...</div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-2xl font-bold text-white">DecoRoute Dashboard</h1>
              <p className="text-gray-400">Welcome back, {user.full_name}</p>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                href="/planner"
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Plan New Trip
              </Link>
              <button
                onClick={handleLogout}
                className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* User Profile Card */}
        <div className="bg-gray-800 rounded-lg p-6 mb-8">
          <h2 className="text-xl font-semibold text-white mb-4">Your Profile</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <p className="text-gray-400 text-sm">Certification Level</p>
              <p className="text-white font-medium">{user.certification_level}</p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Total Dives</p>
              <p className="text-white font-medium">{user.total_dives}</p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Member Since</p>
              <p className="text-white font-medium">{new Date(user.created_at).toLocaleDateString()}</p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Email</p>
              <p className="text-white font-medium">{user.email}</p>
            </div>
          </div>
        </div>

        {/* Saved Trips */}
        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-white">Your Saved Trips</h2>
            <Link
              href="/planner"
              className="text-blue-400 hover:text-blue-300 text-sm font-medium"
            >
              + Create New Trip
            </Link>
          </div>

          {trips.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-400 mb-4">No trips planned yet</p>
              <Link
                href="/planner"
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-md text-sm font-medium inline-block"
              >
                Plan Your First Trip
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {trips.map((trip) => (
                <div key={trip.id} className="bg-gray-700 rounded-lg p-4 hover:bg-gray-600 transition-colors">
                  <h3 className="text-white font-semibold mb-2">{trip.name}</h3>
                  <p className="text-gray-400 text-sm mb-3 line-clamp-2">{trip.description}</p>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-400">Start:</span>
                      <span className="text-white">{new Date(trip.start_date).toLocaleDateString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">End:</span>
                      <span className="text-white">{new Date(trip.end_date).toLocaleDateString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Status:</span>
                      <span className="text-green-400 capitalize">{trip.status}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
