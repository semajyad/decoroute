import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="max-w-4xl mx-auto text-center px-4">
        <h1 className="text-5xl font-bold text-white mb-6">
          DecoRoute
        </h1>
        <p className="text-xl text-gray-300 mb-8">
          Enterprise-grade scuba diving trip planner with the Safe Transit Engine
        </p>
        <p className="text-gray-400 mb-12 max-w-2xl mx-auto">
          Plan your diving adventures with confidence. Our advanced transit safety engine 
          ensures you never violate critical no-fly rules between dives and flights.
        </p>
        
        <div className="space-y-4 sm:space-y-0 sm:space-x-4 sm:flex sm:justify-center">
          <Link
            href="/auth/register"
            className="block bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors"
          >
            Get Started
          </Link>
          <Link
            href="/auth/login"
            className="block bg-gray-700 hover:bg-gray-600 text-white px-8 py-3 rounded-lg font-semibold transition-colors"
          >
            Sign In
          </Link>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-2">Safe Transit Engine</h3>
            <p className="text-gray-400 text-sm">
              Advanced algorithms calculate mandatory surface intervals and prevent unsafe 
              flight bookings after diving.
            </p>
          </div>
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-2">Enterprise Scale</h3>
            <p className="text-gray-400 text-sm">
              Built to handle 10,000+ concurrent users with robust security and 
              performance testing.
            </p>
          </div>
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-2">Global Dive Sites</h3>
            <p className="text-gray-400 text-sm">
              Access comprehensive dive site information and plan multi-location 
              diving adventures safely.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
