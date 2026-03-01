'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

interface DiveSite {
  id: number
  name: string
  description: string
  location: string
  country: string
  latitude: number
  longitude: number
  max_depth: number
  water_type: string
  difficulty_level: string
  marine_life_highlights: string
  best_season: string
  certification_required: string
  average_visibility: number
  current_strength: string
}

interface DivePlan {
  dive_site_id: number
  dive_datetime: string
  max_depth: number
  bottom_time: number
}

interface TransitResponse {
  is_safe: boolean
  violation_type: string
  recommended_wait_time: number
  details: string
}

interface TripFormData {
  name: string
  description: string
  start_date: string
  end_date: string
}

export default function TripPlannerPage() {
  const [diveSites, setDiveSites] = useState<DiveSite[]>([])
  const [selectedDives, setSelectedDives] = useState<DivePlan[]>([])
  const [flightDateTime, setFlightDateTime] = useState('')
  const [transitResult, setTransitResult] = useState<TransitResponse | null>(null)
  const [isLoadingSites, setIsLoadingSites] = useState(true)
  const [isLoadingTransit, setIsLoadingTransit] = useState(false)
  const [tripForm, setTripForm] = useState<TripFormData>({
    name: '',
    description: '',
    start_date: '',
    end_date: ''
  })
  const [showTripForm, setShowTripForm] = useState(false)
  const [isSavingTrip, setIsSavingTrip] = useState(false)
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/auth/login')
      return
    }

    const fetchDiveSites = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/dive-sites/', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        })

        if (response.ok) {
          const data = await response.json()
          setDiveSites(data)
        }
      } catch (error) {
        console.error('Error fetching dive sites:', error)
      } finally {
        setIsLoadingSites(false)
      }
    }

    fetchDiveSites()
  }, [router])

  const addDive = (site: DiveSite) => {
    const newDive: DivePlan = {
      dive_site_id: site.id,
      dive_datetime: `${tripForm.start_date}T10:00:00`,
      max_depth: site.max_depth || 20,
      bottom_time: 45
    }
    setSelectedDives([...selectedDives, newDive])
  }

  const removeDive = (index: number) => {
    setSelectedDives(selectedDives.filter((_, i) => i !== index))
  }

  const updateDive = (index: number, field: keyof DivePlan, value: string | number) => {
    const updatedDives = [...selectedDives]
    updatedDives[index] = { ...updatedDives[index], [field]: value }
    setSelectedDives(updatedDives)
  }

  const checkTransitSafety = async () => {
    if (selectedDives.length === 0 || !flightDateTime) {
      return
    }

    setIsLoadingTransit(true)
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8000/api/transit/check-safety', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          dives: selectedDives,
          flight_datetime: flightDateTime
        }),
      })

      if (response.ok) {
        const result = await response.json()
        setTransitResult(result)
      }
    } catch (error) {
      console.error('Error checking transit safety:', error)
    } finally {
      setIsLoadingTransit(false)
    }
  }

  const saveTrip = async () => {
    if (!tripForm.name || !tripForm.start_date || !tripForm.end_date) {
      return
    }

    setIsSavingTrip(true)
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8000/api/trips/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(tripForm),
      })

      if (response.ok) {
        router.push('/dashboard')
      }
    } catch (error) {
      console.error('Error saving trip:', error)
    } finally {
      setIsSavingTrip(false)
    }
  }

  const getDiveSiteName = (siteId: number) => {
    const site = diveSites.find(s => s.id === siteId)
    return site?.name || 'Unknown Site'
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-2xl font-bold text-white">Trip Planner</h1>
              <p className="text-gray-400">Plan your safe diving adventure</p>
            </div>
            <Link
              href="/dashboard"
              className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              Back to Dashboard
            </Link>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Dive Sites Selection */}
          <div className="lg:col-span-1">
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-xl font-semibold text-white mb-4">Dive Sites</h2>
              
              {isLoadingSites ? (
                <div className="text-gray-400">Loading dive sites...</div>
              ) : (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {diveSites.map((site) => (
                    <div key={site.id} className="bg-gray-700 rounded-lg p-4">
                      <h3 className="text-white font-medium mb-1">{site.name}</h3>
                      <p className="text-gray-400 text-sm mb-2">{site.location}, {site.country}</p>
                      <div className="text-xs text-gray-500 space-y-1">
                        <div>Max Depth: {site.max_depth}m</div>
                        <div>Difficulty: {site.difficulty_level}</div>
                        <div>Visibility: {site.average_visibility}m</div>
                      </div>
                      <button
                        onClick={() => addDive(site)}
                        className="mt-3 w-full bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm"
                      >
                        Add to Trip
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Trip Planning */}
          <div className="lg:col-span-2">
            {/* Trip Details */}
            <div className="bg-gray-800 rounded-lg p-6 mb-6">
              <h2 className="text-xl font-semibold text-white mb-4">Trip Details</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">
                    Trip Name
                  </label>
                  <input
                    type="text"
                    value={tripForm.name}
                    onChange={(e) => setTripForm({...tripForm, name: e.target.value})}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-blue-500 focus:border-blue-500"
                    placeholder="My Diving Adventure"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">
                    Description
                  </label>
                  <input
                    type="text"
                    value={tripForm.description}
                    onChange={(e) => setTripForm({...tripForm, description: e.target.value})}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Amazing diving experience"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">
                    Start Date
                  </label>
                  <input
                    type="date"
                    value={tripForm.start_date}
                    onChange={(e) => setTripForm({...tripForm, start_date: e.target.value})}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">
                    End Date
                  </label>
                  <input
                    type="date"
                    value={tripForm.end_date}
                    onChange={(e) => setTripForm({...tripForm, end_date: e.target.value})}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            </div>

            {/* Planned Dives */}
            <div className="bg-gray-800 rounded-lg p-6 mb-6">
              <h2 className="text-xl font-semibold text-white mb-4">Planned Dives</h2>
              
              {selectedDives.length === 0 ? (
                <div className="text-center py-8 text-gray-400">
                  No dives added yet. Select dive sites from the left panel.
                </div>
              ) : (
                <div className="space-y-4">
                  {selectedDives.map((dive, index) => (
                    <div key={index} className="bg-gray-700 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-3">
                        <h3 className="text-white font-medium">
                          {getDiveSiteName(dive.dive_site_id)}
                        </h3>
                        <button
                          onClick={() => removeDive(index)}
                          className="text-red-400 hover:text-red-300 text-sm"
                        >
                          Remove
                        </button>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                        <div>
                          <label className="block text-xs text-gray-400 mb-1">Date & Time</label>
                          <input
                            type="datetime-local"
                            value={dive.dive_datetime}
                            onChange={(e) => updateDive(index, 'dive_datetime', e.target.value)}
                            className="w-full px-2 py-1 bg-gray-600 border border-gray-500 rounded text-white text-sm"
                          />
                        </div>
                        <div>
                          <label className="block text-xs text-gray-400 mb-1">Max Depth (m)</label>
                          <input
                            type="number"
                            value={dive.max_depth}
                            onChange={(e) => updateDive(index, 'max_depth', parseFloat(e.target.value))}
                            className="w-full px-2 py-1 bg-gray-600 border border-gray-500 rounded text-white text-sm"
                          />
                        </div>
                        <div>
                          <label className="block text-xs text-gray-400 mb-1">Bottom Time (min)</label>
                          <input
                            type="number"
                            value={dive.bottom_time}
                            onChange={(e) => updateDive(index, 'bottom_time', parseInt(e.target.value))}
                            className="w-full px-2 py-1 bg-gray-600 border border-gray-500 rounded text-white text-sm"
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Safe Transit Check */}
            <div className="bg-gray-800 rounded-lg p-6 mb-6">
              <h2 className="text-xl font-semibold text-white mb-4">Safe Transit Check</h2>
              
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Flight Date & Time
                </label>
                <input
                  type="datetime-local"
                  value={flightDateTime}
                  onChange={(e) => setFlightDateTime(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <button
                onClick={checkTransitSafety}
                disabled={selectedDives.length === 0 || !flightDateTime || isLoadingTransit}
                className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white px-4 py-2 rounded-md font-medium"
              >
                {isLoadingTransit ? 'Checking Safety...' : 'Check Transit Safety'}
              </button>

              {transitResult && (
                <div className={`mt-4 p-4 rounded-lg ${
                  transitResult.is_safe 
                    ? 'bg-green-900 border border-green-700' 
                    : 'bg-red-900 border border-red-700'
                }`}>
                  <div className="flex items-center mb-2">
                    <span className={`text-lg font-bold ${
                      transitResult.is_safe ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {transitResult.is_safe ? '✓ SAFE FOR FLIGHT' : '✗ UNSAFE FOR FLIGHT'}
                    </span>
                  </div>
                  <p className="text-white text-sm mb-2">{transitResult.details}</p>
                  {!transitResult.is_safe && transitResult.recommended_wait_time > 0 && (
                    <p className="text-yellow-400 text-sm">
                      Recommended wait time: {transitResult.recommended_wait_time} hours
                    </p>
                  )}
                </div>
              )}
            </div>

            {/* Save Trip */}
            <div className="flex justify-end space-x-4">
              <Link
                href="/dashboard"
                className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-2 rounded-md font-medium"
              >
                Cancel
              </Link>
              <button
                onClick={saveTrip}
                disabled={!tripForm.name || !tripForm.start_date || !tripForm.end_date || isSavingTrip}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white px-6 py-2 rounded-md font-medium"
              >
                {isSavingTrip ? 'Saving...' : 'Save Trip'}
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
