# Frontend Testing Guide

## Current Status

The frontend test infrastructure is not yet fully set up. Placeholder test files have been created for future implementation.

## Setting Up Tests

To enable testing, follow these steps:

### 1. Install Testing Dependencies

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event axios-mock-adapter jsdom
```

### 2. Create Vitest Configuration

Create `vitest.config.ts`:

```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
  },
});
```

### 3. Create Test Setup File

Create `src/test/setup.ts`:

```typescript
import '@testing-library/jest-dom';
```

### 4. Add Test Scripts to package.json

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

### 5. Run Tests

```bash
npm test
```

## Test Files

- `src/components/__tests__/CompanyLogoSelector.test.tsx` - Component tests
- `src/services/__tests__/api.test.ts` - API service tests

## Testing Checklist

### CompanyLogoSelector Component

- [ ] Renders loading state while fetching companies
- [ ] Displays error message on fetch failure
- [ ] Renders all companies after successful fetch
- [ ] Calls onCompanySelect when company is clicked
- [ ] Shows checkmark on selected company
- [ ] Applies company-specific styling to selected card
- [ ] Supports keyboard navigation
- [ ] Has proper ARIA labels

### API Service

- [ ] fetchCompanies calls correct endpoint
- [ ] Returns proper data structure
- [ ] Handles errors gracefully
- [ ] Includes correct headers
- [ ] uploadResume works with FormData
- [ ] Progress tracking works
- [ ] checkHealth calls correct endpoint

## Manual Testing

Until automated tests are implemented, manually verify:

1. **Company Selection UI**
   - Companies load and display correctly
   - Clicking a company selects it
   - Selected company shows checkmark
   - Company colors apply correctly
   - Responsive on mobile and desktop

2. **API Integration**
   - /api/companies endpoint returns data
   - Error handling displays user-friendly messages
   - Loading states show appropriately

3. **Accessibility**
   - Keyboard navigation works
   - Screen reader announces selections
   - Focus indicators are visible
   - Color contrast is sufficient
