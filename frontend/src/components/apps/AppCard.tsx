import React from 'react';

import * as LucideIcons from 'lucide-react';
import { Application } from '@/pages/apps/mockData';

interface AppCardProps {
  app: Application;
  onClick: (appId: string) => void;
}

const AppCard: React.FC<AppCardProps> = ({ app, onClick }) => {
  // Dynamically get the icon component
  const IconComponent = (LucideIcons as Record<string, React.FC<{ size?: number }>>)[app.icon] || LucideIcons.Box;
  
  // Calculate usage percentage
  const usagePercentage = (app.currentUsage / app.usageLimit) * 100;
  
  // Determine the color based on usage percentage
  const getProgressColor = (percentage: number) => {
    if (percentage < 50) return 'bg-green-500';
    if (percentage < 75) return 'bg-yellow-500';
    return 'bg-red-500';
  };
  
  return (
    <div 
      className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300 cursor-pointer border border-gray-100"
      onClick={() => onClick(app.id)}
    >
      <div className="p-6">
        <div className="flex justify-between items-start mb-4">
          <div className="p-3 rounded-lg bg-blue-100 text-blue-600">
            <IconComponent size={24} />
          </div>
          <div className="text-xs font-medium px-2 py-1 rounded-full bg-blue-50 text-blue-600">
            {usagePercentage.toFixed(0)}% used
          </div>
        </div>
        <h3 className="text-lg font-semibold mb-1 text-gray-800">{app.name}</h3>
        <p className="text-gray-600 text-sm mb-4">{app.description}</p>
        
        <div className="mt-4">
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div 
              className={`h-full ${getProgressColor(usagePercentage)} rounded-full transition-all duration-500`}
              style={{ width: `${usagePercentage}%` }}
            ></div>
          </div>
          <div className="mt-2 flex justify-between text-xs text-gray-500">
            <span>{app.currentUsage.toLocaleString()} API calls</span>
            <span>Limit: {app.usageLimit.toLocaleString()}</span>
          </div>
        </div>
      </div>
      <div className="px-6 py-2 bg-gray-50 border-t border-gray-100">
        <button className="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors">
          Launch App
        </button>
      </div>
    </div>
  );
};

export default AppCard;