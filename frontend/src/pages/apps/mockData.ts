import { BarChart3, Code, Database, Gauge, PanelRight, Play, Terminal, Timer } from 'lucide-react';

export interface User {
  id: string;
  name: string;
  email: string;
  avatar: string;
}

export interface Application {
  id: string;
  name: string;
  description: string;
  icon: string;
  usageLimit: number;
  currentUsage: number;
}

export interface UsageData {
  date: string;
  apiCalls: number;
  appId: string;
}

export interface BillingDetails {
  plan: string;
  price: number;
  billingCycle: string;
  nextBillingDate: string;
  applications: {
    appId: string;
    appName: string;
    usage: number;
    cost: number;
  }[];
}

// Mock authenticated user
export const currentUser: User = {
  id: '1',
  name: 'Alex Johnson',
  email: 'alex.johnson@example.com',
  avatar: 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2'
};

// Mock applications
export const applications: Application[] = [
  {
    id: '1',
    name: 'Data Analytics',
    description: 'Powerful data analytics and visualization tools',
    icon: BarChart3.name,
    usageLimit: 10000,
    currentUsage: 7500
  },
  {
    id: '2',
    name: 'API Gateway',
    description: 'Secure API management and monitoring system',
    icon: Code.name,
    usageLimit: 5000,
    currentUsage: 2300
  },
  {
    id: '3',
    name: 'Database Manager',
    description: 'Database management and optimization tools',
    icon: Database.name,
    usageLimit: 8000,
    currentUsage: 4200
  },
  {
    id: '4',
    name: 'Performance Monitor',
    description: 'Real-time performance monitoring and alerts',
    icon: Gauge.name,
    usageLimit: 12000,
    currentUsage: 9800
  },
  {
    id: '5',
    name: 'Dev Console',
    description: 'Advanced developer console and debugging tools',
    icon: Terminal.name,
    usageLimit: 3000,
    currentUsage: 1200
  },
  {
    id: '6',
    name: 'Workflow Automation',
    description: 'Automate tasks and integrate with other services',
    icon: Play.name,
    usageLimit: 7000,
    currentUsage: 4600
  }
];

// Mock usage data for charts
export const usageData: UsageData[] = [
  { date: 'Mon', apiCalls: 1200, appId: '1' },
  { date: 'Tue', apiCalls: 1900, appId: '1' },
  { date: 'Wed', apiCalls: 1500, appId: '1' },
  { date: 'Thu', apiCalls: 2100, appId: '1' },
  { date: 'Fri', apiCalls: 1800, appId: '1' },
  { date: 'Sat', apiCalls: 800, appId: '1' },
  { date: 'Sun', apiCalls: 1100, appId: '1' },
  { date: 'Mon', apiCalls: 300, appId: '2' },
  { date: 'Tue', apiCalls: 450, appId: '2' },
  { date: 'Wed', apiCalls: 520, appId: '2' },
  { date: 'Thu', apiCalls: 380, appId: '2' },
  { date: 'Fri', apiCalls: 650, appId: '2' },
  { date: 'Sat', apiCalls: 210, appId: '2' },
  { date: 'Sun', apiCalls: 320, appId: '2' },
  { date: 'Mon', apiCalls: 780, appId: '3' },
  { date: 'Tue', apiCalls: 890, appId: '3' },
  { date: 'Wed', apiCalls: 1010, appId: '3' },
  { date: 'Thu', apiCalls: 950, appId: '3' },
  { date: 'Fri', apiCalls: 720, appId: '3' },
  { date: 'Sat', apiCalls: 450, appId: '3' },
  { date: 'Sun', apiCalls: 600, appId: '3' }
];

// Mock billing details
export const billingDetails: BillingDetails = {
  plan: 'Business Pro',
  price: 99,
  billingCycle: 'Monthly',
  nextBillingDate: '2025-02-15',
  applications: [
    {
      appId: '1',
      appName: 'Data Analytics',
      usage: 7500,
      cost: 37.50
    },
    {
      appId: '2',
      appName: 'API Gateway',
      usage: 2300,
      cost: 11.50
    },
    {
      appId: '3',
      appName: 'Database Manager',
      usage: 4200,
      cost: 21.00
    },
    {
      appId: '4',
      appName: 'Performance Monitor',
      usage: 9800,
      cost: 49.00
    },
    {
      appId: '5',
      appName: 'Dev Console',
      usage: 1200,
      cost: 6.00
    },
    {
      appId: '6',
      appName: 'Workflow Automation',
      usage: 4600,
      cost: 23.00
    }
  ]
};