import { createBrowserRouter, RouterProvider, Navigate, Outlet } from 'react-router-dom';
import AppLayout from './layouts/AppLayout';
import FullscreenLayout from './layouts/FullscreenLayout';
import { ToastProvider } from './components/Toast/Toast';

// Pages
import Landing from './pages/Landing/Landing';
import Register from './pages/Auth/Register';
import Login from './pages/Auth/Login';
import Onboarding from './pages/Onboarding/Onboarding';
import CVConfirm from './pages/CVConfirm/CVConfirm';
import AIProcessing from './pages/AIProcessing/AIProcessing';
import Dashboard from './pages/Dashboard/Dashboard';
import Profile from './pages/Profile/Profile';
import Interview from './pages/Interview/Interview';
import PerformanceAnalysis from './pages/PerformanceAnalysis/PerformanceAnalysis';
import DevelopmentPlan from './pages/DevelopmentPlan/DevelopmentPlan';
import InterviewHistory from './pages/InterviewHistory/InterviewHistory';
import PDFReport from './pages/PDFReport/PDFReport';
import Settings from './pages/Settings/Settings';

// ToastProvider wrapper — data router layout bileşenleri context sağlamaz,
// bu yüzden root layout'ta ToastProvider sarıyoruz.
function RootLayout() {
  return (
    <ToastProvider>
      <Outlet />
    </ToastProvider>
  );
}

// Bare layout: sadece Outlet — AI Processing kendi header/bg yönetiyor
function BareLayout() {
  return <Outlet />;
}

const router = createBrowserRouter([
  {
    element: <RootLayout />,
    children: [
      // AI Processing — kendi tam ekran arka planını yönetiyor, header yok
      {
        element: <BareLayout />,
        children: [
          { path: '/ai-processing', element: <AIProcessing /> },
        ],
      },
      // Fullscreen routes — auth + onboarding (logo header var)
      {
        element: <FullscreenLayout />,
        children: [
          { path: '/', element: <Landing /> },
          { path: '/login', element: <Login /> },
          { path: '/register', element: <Register /> },
          { path: '/onboarding', element: <Onboarding /> },
          { path: '/cv-confirm', element: <CVConfirm /> },
        ],
      },
      // App routes — authenticated
      {
        element: <AppLayout />,
        children: [
          { path: '/dashboard', element: <Dashboard /> },
          { path: '/profile', element: <Profile /> },
          { path: '/interview', element: <Interview /> },
          { path: '/performance', element: <PerformanceAnalysis /> },
          { path: '/development-plan', element: <DevelopmentPlan /> },
          { path: '/history', element: <InterviewHistory /> },
          { path: '/pdf-report', element: <PDFReport /> },
          { path: '/settings', element: <Settings /> },
        ],
      },
      // Fallback
      { path: '*', element: <Navigate to="/dashboard" replace /> },
    ],
  },
]);


export default function App() {
  return <RouterProvider router={router} />;
}
