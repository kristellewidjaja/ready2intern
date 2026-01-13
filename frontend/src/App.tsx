import { ThemeProvider } from './contexts/ThemeContext';
import { MainLayout } from './components/MainLayout';
import { Dashboard } from './pages/Dashboard';

function App() {
  return (
    <ThemeProvider>
      <MainLayout>
        <Dashboard />
      </MainLayout>
    </ThemeProvider>
  );
}

export default App;
