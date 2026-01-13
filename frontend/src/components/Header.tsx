import { ThemeToggle } from './ThemeToggle';

export const Header = () => {
  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-blue-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">R2I</span>
            </div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Ready2Intern
            </h1>
          </div>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
};
