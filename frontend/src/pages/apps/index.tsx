import { Layout } from "@/components/layout/Layout";
import { useState } from "react";
import { Application, applications } from "./mockData";
import AppCard from "@/components/apps/AppCard";
import { Clock, Database, Settings, Upload } from "lucide-react";

export default function Page() {
  const [searchTerm, setSearchTerm] = useState('');

  // Filter applications based on search term
  const filteredApps = applications.filter(app =>
    app.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    app.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const recentActivity = [
    {
      icon: Upload,
      iconBg: 'bg-blue-100',
      iconColor: 'text-blue-600',
      message: 'Data Analytics - 250 new API calls',
      time: '2 minutes ago'
    },
    {
      icon: Settings,
      iconBg: 'bg-purple-100',
      iconColor: 'text-purple-600',
      message: 'API Gateway - Configuration updated',
      time: '1 hour ago'
    },
    {
      icon: Database,
      iconBg: 'bg-green-100',
      iconColor: 'text-green-600',
      message: 'Database Manager - Backup completed',
      time: '3 hours ago'
    },
    {
      icon: Clock,
      iconBg: 'bg-yellow-100',
      iconColor: 'text-yellow-600',
      message: 'Performance Monitor - Weekly report generated',
      time: '1 day ago'
    }
  ];

  const handleAppClick = (appId: string) => {
    console.log(`Opening app with ID: ${appId}`);
    // In a real app, this would navigate to the specific app
  };

  return (
    <Layout>
      <div className="w-full max-w-7xl space-y-12">

        <div className="min-h-screen bg-gray-50 p-0 m-0">
          <div className="container mx-auto px-4 py-8">
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-gray-800 mb-2">Your Applications</h1>
              <p className="text-gray-600">Access all your available applications from one place</p>
            </div>

            <div className="mb-8">
              <div className="relative max-w-md">
                <input
                  type="text"
                  placeholder="Search applications..."
                  className="w-full px-4 py-2 pl-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <svg
                  className="absolute left-3 top-2.5 h-5 w-5 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  ></path>
                </svg>
              </div>
            </div>

            {filteredApps.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredApps.map((app: Application) => (
                  <AppCard key={app.id} app={app} onClick={handleAppClick} />
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <h3 className="text-lg font-medium text-gray-700 mb-2">No applications found</h3>
                <p className="text-gray-500">
                  Try adjusting your search or check back later for new applications
                </p>
              </div>
            )}

            <div className="mt-12 bg-white rounded-lg p-6 shadow-md">
              <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
              <div className="space-y-4">
                {recentActivity.map((activity, index) => (
                  <div key={index} className="flex items-start pb-4 border-b border-gray-100">
                    <div className={`p-2 rounded-full mr-3 ${activity.iconBg}`}>
                      <activity.icon size={16} className={activity.iconColor} />
                    </div>
                    <div>
                      <p className="text-gray-800">{activity.message}</p>
                      <p className="text-sm text-gray-500">{activity.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

      </div>
    </Layout>
  );
}
