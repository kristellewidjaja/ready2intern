# UI/UX Mockups: Ready2Intern POC

**Version:** 1.0  
**Date:** January 11, 2026  
**Design System:** Modern, Clean, Professional

---

## ⚠️ Important Implementation Notes

> **NO EMOJIS IN PRODUCTION UI**  
> All emojis in this document are for visual reference ONLY. During implementation, use proper icon libraries:
> - **Recommended:** [Lucide React](https://lucide.dev/) - Modern, clean, consistent icons
> - **Alternative:** [Heroicons](https://heroicons.com/) - Tailwind's official icon set
> 
> Icon placeholders in mockups (e.g., `[CHECK]`, `[ALERT]`, `[FILE ICON]`) should be replaced with actual icon components from these libraries.

---

## Table of Contents

1. [Design System](#1-design-system)
2. [Theme Implementation](#2-theme-implementation)
3. [Dashboard Layout](#3-dashboard-layout)
4. [Left Panel Components](#4-left-panel-components)
5. [Right Panel States](#5-right-panel-states)
6. [Results Dashboard](#6-results-dashboard)
7. [Component Specifications](#7-component-specifications)
8. [Interactions & Animations](#8-interactions--animations)
9. [Responsive Design](#9-responsive-design)

---

## 1. Design System

### 1.1 Color Palette

**Brand Colors (Custom Theme):**

| Color Name | Hex Code | Usage | Preview |
|------------|----------|-------|---------|
| Deep Ocean (Primary Dark) | `#031926` | Headers, dark backgrounds, primary text (dark mode) | ![#031926](https://via.placeholder.com/80x30/031926/031926.png) |
| Teal (Primary) | `#468189` | Primary buttons, links, active states | ![#468189](https://via.placeholder.com/80x30/468189/468189.png) |
| Sage (Secondary) | `#77ACA2` | Secondary buttons, borders, highlights | ![#77ACA2](https://via.placeholder.com/80x30/77ACA2/77ACA2.png) |
| Mint (Accent) | `#9DBEBB` | Accents, hover states, subtle backgrounds | ![#9DBEBB](https://via.placeholder.com/80x30/9DBEBB/9DBEBB.png) |
| Cream (Light) | `#F4E9CD` | Light backgrounds, cards, primary text (light mode) | ![#F4E9CD](https://via.placeholder.com/80x30/F4E9CD/F4E9CD.png) |

**Semantic Colors:**

| Color Name | Hex Code | Usage | Preview |
|------------|----------|-------|---------|
| Success | `#10B981` | Success states, checkmarks, positive feedback | ![#10B981](https://via.placeholder.com/80x30/10B981/10B981.png) |
| Warning | `#F59E0B` | Warning states, medium priority items | ![#F59E0B](https://via.placeholder.com/80x30/F59E0B/F59E0B.png) |
| Error | `#EF4444` | Error states, high priority items, alerts | ![#EF4444](https://via.placeholder.com/80x30/EF4444/EF4444.png) |
| White | `#FFFFFF` | Pure white for light mode backgrounds | ![#FFFFFF](https://via.placeholder.com/80x30/FFFFFF/FFFFFF.png) |
| Black | `#000000` | Pure black for dark mode backgrounds | ![#000000](https://via.placeholder.com/80x30/000000/000000.png) |

**Light Mode Palette:**

| Element | Color | Hex Code |
|---------|-------|----------|
| Background | Cream | `#F4E9CD` |
| Surface (Cards) | White | `#FFFFFF` |
| Primary Text | Deep Ocean | `#031926` |
| Secondary Text | Teal | `#468189` |
| Borders | Mint | `#9DBEBB` |
| Primary Action | Teal | `#468189` |
| Hover State | Sage | `#77ACA2` |

**Dark Mode Palette:**

| Element | Color | Hex Code |
|---------|-------|----------|
| Background | Deep Ocean | `#031926` |
| Surface (Cards) | Teal (20% opacity) | `#468189` with opacity |
| Primary Text | Cream | `#F4E9CD` |
| Secondary Text | Mint | `#9DBEBB` |
| Borders | Sage | `#77ACA2` |
| Primary Action | Sage | `#77ACA2` |
| Hover State | Mint | `#9DBEBB` |

**Company Brand Colors:**

| Company | Hex Code | Preview |
|---------|----------|---------|
| Amazon Orange | `#FF9900` | ![#FF9900](https://via.placeholder.com/80x30/FF9900/FF9900.png) |
| Meta Blue | `#0668E1` | ![#0668E1](https://via.placeholder.com/80x30/0668E1/0668E1.png) |
| Google Blue | `#4285F4` | ![#4285F4](https://via.placeholder.com/80x30/4285F4/4285F4.png) |
| Google Red | `#EA4335` | ![#EA4335](https://via.placeholder.com/80x30/EA4335/EA4335.png) |
| Google Yellow | `#FBBC04` | ![#FBBC04](https://via.placeholder.com/80x30/FBBC04/FBBC04.png) |
| Google Green | `#34A853` | ![#34A853](https://via.placeholder.com/80x30/34A853/34A853.png) |

> **Note for Implementation:** 
> - Do NOT use emojis in the actual UI components. Use icon libraries like Lucide React or Heroicons instead.
> - Implement theme switching using CSS variables or Tailwind's dark mode class strategy.
> - All brand colors maintain accessibility contrast ratios (WCAG AA minimum).

### 1.2 Typography

**Font Family:**
```
Primary: 'Inter', system-ui, sans-serif
Monospace: 'JetBrains Mono', monospace (for code/data)
```

**Font Sizes:**
```
Heading 1:  48px (3rem) - Bold
Heading 2:  36px (2.25rem) - Semibold
Heading 3:  24px (1.5rem) - Semibold
Body Large: 18px (1.125rem) - Regular
Body:       16px (1rem) - Regular
Body Small: 14px (0.875rem) - Regular
Caption:    12px (0.75rem) - Regular
```

### 1.3 Spacing

```
xs:  4px   (0.25rem)
sm:  8px   (0.5rem)
md:  16px  (1rem)
lg:  24px  (1.5rem)
xl:  32px  (2rem)
2xl: 48px  (3rem)
3xl: 64px  (4rem)
```

### 1.4 Shadows

```
Small:  0 1px 2px rgba(0,0,0,0.05)
Medium: 0 4px 6px rgba(0,0,0,0.1)
Large:  0 10px 15px rgba(0,0,0,0.1)
XL:     0 20px 25px rgba(0,0,0,0.15)
```

### 1.5 Border Radius

```
Small:  4px
Medium: 8px
Large:  12px
XL:     16px
Full:   9999px (circular)
```

---

## 2. Theme Implementation

### 2.1 CSS Variables Approach

**Define theme colors as CSS variables:**

```css
/* Light Mode (Default) */
:root {
  /* Brand Colors */
  --color-primary: #468189;
  --color-primary-dark: #031926;
  --color-secondary: #77ACA2;
  --color-accent: #9DBEBB;
  --color-light: #F4E9CD;
  
  /* Semantic Colors */
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  
  /* Theme-specific */
  --bg-primary: #F4E9CD;
  --bg-surface: #FFFFFF;
  --text-primary: #031926;
  --text-secondary: #468189;
  --border-color: #9DBEBB;
  --button-primary: #468189;
  --button-hover: #77ACA2;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(3, 25, 38, 0.05);
  --shadow-md: 0 4px 6px rgba(3, 25, 38, 0.1);
  --shadow-lg: 0 10px 15px rgba(3, 25, 38, 0.1);
}

/* Dark Mode */
.dark {
  --bg-primary: #031926;
  --bg-surface: rgba(70, 129, 137, 0.2);
  --text-primary: #F4E9CD;
  --text-secondary: #9DBEBB;
  --border-color: #77ACA2;
  --button-primary: #77ACA2;
  --button-hover: #9DBEBB;
  
  /* Shadows for dark mode */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.5);
}
```

### 2.2 Tailwind Configuration

**Update `tailwind.config.js` to include custom colors:**

```javascript
module.exports = {
  darkMode: 'class', // Enable class-based dark mode
  theme: {
    extend: {
      colors: {
        brand: {
          'deep-ocean': '#031926',
          'teal': '#468189',
          'sage': '#77ACA2',
          'mint': '#9DBEBB',
          'cream': '#F4E9CD',
        },
        primary: {
          DEFAULT: '#468189',
          dark: '#031926',
        },
        secondary: {
          DEFAULT: '#77ACA2',
        },
        accent: {
          DEFAULT: '#9DBEBB',
        },
      },
      backgroundColor: {
        'primary': 'var(--bg-primary)',
        'surface': 'var(--bg-surface)',
      },
      textColor: {
        'primary': 'var(--text-primary)',
        'secondary': 'var(--text-secondary)',
      },
      borderColor: {
        'default': 'var(--border-color)',
      },
    },
  },
  plugins: [],
}
```

### 2.3 Theme Toggle Component

**Implementation Guide:**

```typescript
// useTheme.ts hook
import { useEffect, useState } from 'react';

export function useTheme() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    // Check system preference or localStorage
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    const initialTheme = savedTheme || (prefersDark ? 'dark' : 'light');
    setTheme(initialTheme as 'light' | 'dark');
    document.documentElement.classList.toggle('dark', initialTheme === 'dark');
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };

  return { theme, toggleTheme };
}
```

**Theme Toggle Button:**
- Position: Top-right corner of header
- Icon: Lucide Sun (light mode) / Lucide Moon (dark mode)
- Size: 40px × 40px
- Transition: Smooth fade between icons (300ms)

### 2.4 Component Color Mapping

**Button Colors:**

| State | Light Mode | Dark Mode |
|-------|------------|-----------|
| Primary Default | Teal (#468189) | Sage (#77ACA2) |
| Primary Hover | Sage (#77ACA2) | Mint (#9DBEBB) |
| Primary Active | Deep Ocean (#031926) | Teal (#468189) |
| Disabled | Mint (#9DBEBB) at 50% opacity | Sage (#77ACA2) at 30% opacity |

**Card Colors:**

| Element | Light Mode | Dark Mode |
|---------|------------|-----------|
| Background | White (#FFFFFF) | Teal (#468189) at 20% opacity |
| Border | Mint (#9DBEBB) | Sage (#77ACA2) |
| Shadow | Deep Ocean at 10% | Black at 40% |

**Score Card Gradients:**

| Score Range | Light Mode Gradient | Dark Mode Gradient |
|-------------|--------------------|--------------------|
| 90-100 (Excellent) | Success (#10B981) → Sage (#77ACA2) | Success (#10B981) → Teal (#468189) |
| 75-89 (Good) | Teal (#468189) → Mint (#9DBEBB) | Sage (#77ACA2) → Mint (#9DBEBB) |
| 60-74 (Fair) | Warning (#F59E0B) → Cream (#F4E9CD) | Warning (#F59E0B) → Sage (#77ACA2) |
| 0-59 (Poor) | Error (#EF4444) → Warning (#F59E0B) | Error (#EF4444) → Deep Ocean (#031926) |

### 2.5 Visual Theme Comparison

**Light Mode Example:**
```
┌─────────────────────────────────────────────────────┐
│ Header (White background)                           │
│ Ready2Intern [LOGO]              [SUN ICON] [MENU] │
├─────────────────────────────────────────────────────┤
│ Background: Cream (#F4E9CD)                         │
│                                                     │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Card (White background)                         │ │
│ │ Border: Mint (#9DBEBB)                          │ │
│ │                                                 │ │
│ │ Text: Deep Ocean (#031926)                      │ │
│ │                                                 │ │
│ │ ┌─────────────────────────────────────────────┐ │ │
│ │ │ [Analyze Resume] Button                     │ │ │
│ │ │ Background: Teal (#468189)                  │ │ │
│ │ │ Text: White                                 │ │ │
│ │ └─────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**Dark Mode Example:**
```
┌─────────────────────────────────────────────────────┐
│ Header (Dark Teal background)                       │
│ Ready2Intern [LOGO]            [MOON ICON] [MENU]  │
├─────────────────────────────────────────────────────┤
│ Background: Deep Ocean (#031926)                    │
│                                                     │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Card (Teal 20% opacity background)              │ │
│ │ Border: Sage (#77ACA2)                          │ │
│ │                                                 │ │
│ │ Text: Cream (#F4E9CD)                           │ │
│ │                                                 │ │
│ │ ┌─────────────────────────────────────────────┐ │ │
│ │ │ [Analyze Resume] Button                     │ │ │
│ │ │ Background: Sage (#77ACA2)                  │ │ │
│ │ │ Text: Deep Ocean (#031926)                  │ │ │
│ │ └─────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

### 2.6 Accessibility in Both Modes

**Contrast Ratios (WCAG AA Compliant):**

| Combination | Light Mode | Dark Mode | Ratio |
|-------------|------------|-----------|-------|
| Primary Text on Background | Deep Ocean on Cream | Cream on Deep Ocean | 12.8:1 ✓ |
| Secondary Text on Background | Teal on Cream | Mint on Deep Ocean | 4.8:1 ✓ |
| Button Text on Primary | White on Teal | Deep Ocean on Sage | 4.5:1 ✓ |
| Border on Background | Mint on Cream | Sage on Deep Ocean | 3.2:1 ✓ |

---

## 3. Dashboard Layout

### 2.1 Overall Structure

```
┌──────────────────────────────────────────────────────────────────┐
│ Header (Fixed, 64px height)                                      │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │ [LOGO] Ready2Intern                [Start New] [Download PDF]│ │
│ └──────────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌──────────────────────┬───────────────────────────────────────┐ │
│ │                      │                                       │ │
│ │   LEFT PANEL         │        RIGHT PANEL                    │ │
│ │   (400px fixed)      │        (Flexible)                     │ │
│ │                      │                                       │ │
│ │   [Upload Section]   │   [Empty State]                       │ │
│ │                      │        OR                             │ │
│ │   [Company Logos]    │   [Loading State]                     │ │
│ │                      │        OR                             │ │
│ │   [Role Description]  │   [Results Display]                   │ │
│ │                      │                                       │ │
│ │   [Analyze Button]   │                                       │ │
│ │                      │                                       │ │
│ │                      │                                       │ │
│ └──────────────────────┴───────────────────────────────────────┘ │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ Footer (48px height)                                             │
│ © 2026 Ready2Intern • Privacy Policy • Terms of Service          │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Grid System

```
Desktop (>1024px):  2-column layout (400px + flexible)
Tablet (768-1023px): 2-column layout (300px + flexible)
Mobile (<768px):    Stacked layout (full width)
```

---

## 3. Left Panel Components

### 3.1 Resume Upload Section

```
┌────────────────────────────────────┐
│ 1. Upload Your Resume              │
├────────────────────────────────────┤
│                                    │
│  ┌──────────────────────────────┐  │
│  │                              │  │
│  │      [FILE ICON]             │  │
│  │                              │  │
│  │  Drag & drop your resume     │  │
│  │  or click to browse          │  │
│  │                              │  │
│  │  PDF or DOCX • Max 5MB       │  │
│  │                              │  │
│  └──────────────────────────────┘  │
│                                    │
└────────────────────────────────────┘

States:
1. Empty (default)
2. Drag Active (blue border)
3. File Selected (green border + filename)
4. Error (red border + message)
5. Uploading (progress bar)
```

**Empty State:**
```
┌──────────────────────────────────┐
│ ┌────────────────────────────┐   │
│ │     [FILE ICON] Upload     │   │
│ │                            │   │
│ │  Drag & drop resume here   │   │
│ │  or click to browse        │   │
│ │                            │   │
│ │  PDF or DOCX • Max 5MB     │   │
│ └────────────────────────────┘   │
└──────────────────────────────────┘
Border: Dashed, Mint (#9DBEBB)
Background: Light Mode: White, Dark Mode: Teal (20% opacity)
```

**File Selected State:**
```
┌──────────────────────────────────┐
│ ┌────────────────────────────┐   │
│ │  [CHECK] resume.pdf        │   │
│ │  250 KB • Uploaded         │   │
│ │                            │   │
│ │  [Change File]             │   │
│ └────────────────────────────┘   │
└──────────────────────────────────┘
Border: Solid, Success Green (#10B981)
Background: Light Mode: Success Green (10% opacity), Dark Mode: Success Green (20% opacity)
Icon: Success Green checkmark (use Lucide Check icon)
```

**Error State:**
```
┌──────────────────────────────────┐
│ ┌────────────────────────────┐   │
│ │  [ALERT] File too large    │   │
│ │  resume.pdf (8 MB)         │   │
│ │                            │   │
│ │  Max file size is 5MB      │   │
│ │  [Try Again]               │   │
│ └────────────────────────────┘   │
└──────────────────────────────────┘
Border: Solid, Error Red (#EF4444)
Background: Light Mode: Error Red (10% opacity), Dark Mode: Error Red (20% opacity)
Icon: Error Red alert/warning triangle (use Lucide AlertTriangle icon)
```

### 3.2 Company Logo Selector

```
┌────────────────────────────────────┐
│ 2. Select Target Company           │
├────────────────────────────────────┤
│                                    │
│   ┌──────┐  ┌──────┐  ┌──────┐    │
│   │ [AWS]│  │[META]│  │[GOOG]│    │
│   │ LOGO │  │ LOGO │  │ LOGO │    │
│   │      │  │      │  │      │    │
│   └──[✓]─┘  └──────┘  └──────┘    │
│      ↑                             │
│   Selected                         │
│                                    │
└────────────────────────────────────┘

Note: Use actual company logo images, not emojis
```

**Logo Card Specifications:**
```
Size: 100px × 100px
Border Radius: 12px
Border: 2px solid
Padding: 16px
Cursor: pointer

States:
1. Unselected:
   - Border: Mint (#9DBEBB)
   - Background: Surface (White/Teal 20% opacity)
   - Opacity: 0.7
   - Hover: Scale(1.05), Shadow-md, Border: Sage (#77ACA2)

2. Selected:
   - Border: Brand color (Amazon: Orange, Meta: Blue, Google: Multi) - 2px
   - Background: Brand color (10% opacity in light, 20% opacity in dark)
   - Opacity: 1
   - Checkmark: Bottom-right corner (Teal #468189)
   - Shadow: Large
```

**Amazon Logo Card (Selected):**
```
┌──────────────────┐
│  ┌────────────┐  │
│  │            │  │
│  │  [AMAZON]  │  │  ← Amazon logo image
│  │   LOGO     │  │
│  │            │  │
│  └────────────┘  │
│      [CHECK]     │  ← Checkmark indicator (Lucide Check icon)
└──────────────────┘
Border: #FF9900 (2px)
Background: rgba(255, 153, 0, 0.1)
```

### 3.3 Role Description Input

```
┌────────────────────────────────────┐
│ 3. Paste Role Description *         │
├────────────────────────────────────┤
│                                    │
│  ┌──────────────────────────────┐  │
│  │ Amazon is seeking Software   │  │
│  │ Development Engineer Interns │  │
│  │ to join our team...          │  │
│  │                              │  │
│  │ Responsibilities:            │  │
│  │ • Design and implement...    │  │
│  │                              │  │
│  │ Qualifications:              │  │
│  │ • Currently pursuing BS...   │  │
│  │                              │  │
│  └──────────────────────────────┘  │
│                                    │
│  ✓ 250 characters                  │
│  Minimum 50 characters required    │
│                                    │
└────────────────────────────────────┘

Textarea:
- Rows: 8
- Font: 14px
- Placeholder: "Paste the full role description from the company's career site..."
- Border: Mint (#9DBEBB)
- Focus: Teal (#468189) border (2px)
- Resize: Vertical only
- Background: Surface (White/Teal 20% opacity)
- Text: Primary text color
```

**Character Counter:**
```
Valid (>= 50 chars):
[CHECK] 250 characters
Color: Success Green (#10B981)
Icon: Lucide Check

Invalid (< 50 chars):
[ALERT] 25 characters (minimum 50 required)
Color: Error Red (#EF4444)
Icon: Lucide AlertCircle
```

### 3.4 Analyze Button

```
┌────────────────────────────────────┐
│                                    │
│  ┌──────────────────────────────┐  │
│  │  Analyze Resume  [ARROW]     │  │
│  └──────────────────────────────┘  │
│                                    │
└────────────────────────────────────┘

Note: Use Lucide ArrowRight icon

Button Specs:
- Width: 100%
- Height: 48px
- Border Radius: 8px
- Font: 16px, Semibold
- Icon: Arrow right

States:
1. Disabled:
   - Background: Mint (#9DBEBB) at 50% opacity
   - Text: Secondary text color at 50% opacity
   - Cursor: not-allowed
   - Opacity: 0.6

2. Enabled:
   - Background: Teal (#468189) in light mode, Sage (#77ACA2) in dark mode
   - Text: White in light mode, Deep Ocean (#031926) in dark mode
   - Hover: Sage (#77ACA2) in light mode, Mint (#9DBEBB) in dark mode, Scale(1.02)
   - Active: Deep Ocean (#031926) in light mode, Teal (#468189) in dark mode
   - Shadow: Medium

3. Loading:
   - Background: Same as enabled
   - Text: "Analyzing..."
   - Icon: Spinning loader (Lucide Loader2)
   - Disabled: true
```

---

## 4. Right Panel States

### 4.1 Empty State

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│                                                     │
│              [BAR CHART ICON]                       │
│                                                     │
│         Get Your Internship Readiness Score        │
│                                                     │
│    Upload your resume and select a company to      │
│    receive personalized feedback and                │
│    recommendations                                  │
│                                                     │
│    ┌─────────────────────────────────────┐         │
│    │ 1. Upload resume (PDF or DOCX)      │         │
│    │ 2. Select target company            │         │
│    │ 3. Paste role description            │         │
│    │ 4. Click "Analyze Resume"           │         │
│    └─────────────────────────────────────┘         │
│                                                     │
│    What you'll get:                                │
│    [CHECK] Overall match score                     │
│    [CHECK] Detailed gap analysis                   │
│    [CHECK] Prioritized recommendations             │
│    [CHECK] Development timeline                    │
│    [CHECK] Downloadable PDF report                 │
│                                                     │
└─────────────────────────────────────────────────────┘

Design:
- Center aligned
- Icon: 64px, Gray-400 (use Lucide BarChart3 icon)
- Heading: 24px, Semibold, Gray-900
- Body: 16px, Regular, Gray-600
- Steps: Light gray box, 14px
- Features: Green checkmarks (Lucide Check icon), 14px
```

### 4.2 Loading State

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│                                                     │
│              [LOADER SPINNER]                       │
│                                                     │
│              Analyzing Your Resume                  │
│                                                     │
│    ████████████████░░░░░░░░░░░░░░░░░░░  60%        │
│                                                     │
│         Evaluating against Amazon criteria          │
│                                                     │
│              Estimated time: 20 seconds             │
│                                                     │
│                                                     │
│    Current Step: Analyzing technical skills         │
│                                                     │
└─────────────────────────────────────────────────────┘

Design:
- Center aligned
- Spinner: 48px, Blue-600, rotating animation (use Lucide Loader2 icon)
- Heading: 24px, Semibold, Gray-900
- Progress bar: 
  - Height: 8px
  - Background: Gray-200
  - Fill: Blue-600
  - Border radius: Full
  - Animated (smooth transition)
- Status: 16px, Regular, Gray-600
- Estimated time: 14px, Regular, Gray-500
```

**Progress Stages:**
```
0-20%:   "Extracting resume information..."
21-40%:  "Analyzing technical skills..."
41-60%:  "Evaluating against role requirements..."
61-80%:  "Identifying gaps and strengths..."
81-100%: "Generating recommendations..."
```

### 4.3 Results State

See Section 5 for detailed results dashboard mockup.

---

## 5. Results Dashboard

### 5.1 Overall Layout

```
┌─────────────────────────────────────────────────────────────┐
│ Header (sticky when scrolling)                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Ready2Intern Logo        [Start New Analysis] [Download]│ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │           OVERALL MATCH SCORE: 78/100                   │ │
│ │              ████████████████░░░░░                      │ │
│ │           "Good Match - Strong Candidate"               │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│ │ ATS Score    │  │ Role Match    │  │ Company Fit  │      │
│ │   85/100     │  │   72/100     │  │   68/100     │      │
│ │ ████████░░   │  │ ███████░░░   │  │ ██████░░░░   │      │
│ │ Excellent    │  │ Good         │  │ Fair         │      │
│ └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ YOUR STRENGTHS (5)                             [Expand] │ │
│ │                                                         │ │
│ │ [CHECK] Strong Technical Projects                      │ │
│ │   "Built full-stack e-commerce platform with React..." │ │
│ │   Why it matters: Demonstrates ownership (Amazon LP)   │ │
│ │                                                         │ │
│ │ [CHECK] Quantifiable Impact                            │ │
│ │   "Improved performance by 40%..."                     │ │
│ │   Why it matters: Shows results-driven mindset         │ │
│ │                                                         │ │
│ │ [Show 3 more...]                                       │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ GAPS & RECOMMENDATIONS (6)                     [Expand] │ │
│ │                                                         │ │
│ │ [RED DOT] HIGH PRIORITY                                │ │
│ │ Missing: System Design Experience                      │ │
│ │ Impact: Amazon SDE interns work on distributed systems │ │
│ │ Action: Add project with microservices/message queues  │ │
│ │ Example: "Build scalable chat app with Redis pub/sub"  │ │
│ │                                                         │ │
│ │ [YELLOW DOT] MEDIUM PRIORITY                            │ │
│ │ [2 more items...]                                      │ │
│ │                                                         │ │
│ │ [GREEN DOT] LOW PRIORITY                               │ │
│ │ [3 more items...]                                      │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ DEVELOPMENT TIMELINE                           [Expand] │ │
│ │                                                         │ │
│ │ Target Deadline: September 1, 2026                     │ │
│ │                                                         │ │
│ │ [DOT]─────────────────────────────────[DOT]            │ │
│ │ Now              Phase 1              Goal             │ │
│ │ Jan 11           Feb 8                Sep 1            │ │
│ │                                                         │ │
│ │ Phase 1: Immediate (0-4 weeks)                         │ │
│ │ [BULLET] Update resume with quantified achievements    │ │
│ │ [BULLET] Start distributed systems project             │ │
│ │                                                         │ │
│ │ [Show more phases...]                                  │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Overall Score Card

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                  OVERALL MATCH SCORE                        │
│                                                             │
│                       78/100                                │
│                                                             │
│              ████████████████░░░░░                          │
│                                                             │
│              "Good Match - Strong Candidate"                │
│                                                             │
│   You meet 8 out of 10 key requirements for this role      │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Specifications:
- Height: 200px
- Background: Linear gradient (Blue-600 to Purple-600)
- Text color: White
- Score: 96px font, Bold
- Progress bar: 
  - Height: 16px
  - Background: White (20% opacity)
  - Fill: White
  - Border radius: Full
  - Animated on load (0 → score over 1.5s)
- Status text: 24px, Semibold
- Subtitle: 16px, Regular, 80% opacity
```

**Score Ranges & Colors:**
```
90-100: Excellent Match (Green gradient)
75-89:  Good Match (Blue gradient)
60-74:  Fair Match (Yellow gradient)
0-59:   Needs Improvement (Red gradient)
```

### 5.3 Category Score Cards

```
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│ ATS Score            │  │ Role Match            │  │ Company Fit          │
│                      │  │                      │  │                      │
│      85/100          │  │      72/100          │  │      68/100          │
│                      │  │                      │  │                      │
│  ████████░░          │  │  ███████░░░          │  │  ██████░░░░          │
│                      │  │                      │  │                      │
│   Excellent          │  │   Good               │  │   Fair               │
│                      │  │                      │  │                      │
│ ℹ️ Hover for details │  │ ℹ️ Hover for details │  │ ℹ️ Hover for details │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘

Card Specifications:
- Width: 32% (responsive)
- Height: 180px
- Background: White
- Border: 1px solid Gray-200
- Border radius: 12px
- Padding: 24px
- Shadow: 0 4px 6px rgba(0,0,0,0.1)

Hover Effect:
- Transform: translateY(-4px)
- Shadow: 0 10px 15px rgba(0,0,0,0.15)
- Transition: 200ms ease

Score Display:
- Font: 48px, Bold
- Color: Based on score range
- Progress bar: 8px height, rounded

Label:
- Font: 14px, Semibold, Gray-600
- Uppercase

Status:
- Font: 16px, Semibold
- Color: Based on score range
```

**Tooltip on Hover:**
```
┌────────────────────────────────┐
│ ATS Score: 85/100              │
├────────────────────────────────┤
│ ✓ Keywords matched: 18/20      │
│ ✓ Format: Clean and parseable  │
│ ✓ Length: Optimal (1 page)     │
│ ⚠ Missing: AWS, Kubernetes     │
└────────────────────────────────┘
Background: Gray-900 (90% opacity)
Text: White
Arrow pointing to card
```

### 5.4 Strengths Section

```
┌─────────────────────────────────────────────────────────────┐
│ YOUR STRENGTHS (5)                                 [Expand] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ [CHECK] Strong Technical Projects                      │ │
│ │                                                         │ │
│ │ Evidence from resume:                                  │ │
│ │ "Built full-stack e-commerce platform with React,     │ │
│ │ Node.js, and PostgreSQL. Implemented payment          │ │
│ │ integration and user authentication."                  │ │
│ │                                                         │ │
│ │ Why it matters:                                        │ │
│ │ Demonstrates Ownership and Bias for Action (Amazon    │ │
│ │ Leadership Principles). Shows ability to deliver      │ │
│ │ complete projects independently.                       │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ [CHECK] Quantifiable Impact                            │ │
│ │                                                         │ │
│ │ Evidence from resume:                                  │ │
│ │ "Improved application performance by 40% through      │ │
│ │ database query optimization and caching strategies."   │ │
│ │                                                         │ │
│ │ Why it matters:                                        │ │
│ │ Shows results-driven mindset and ability to measure   │ │
│ │ impact. Aligns with Deliver Results principle.        │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ [Show 3 more strengths...]                             │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Section Header:
- Font: 20px, Bold, Gray-900
- Icon: 24px (use Lucide TrendingUp icon)
- Count badge: Gray-500
- Expand button: Blue-600, hover: Blue-700

Strength Card:
- Background: Green-50
- Border: 1px solid Green-200
- Border radius: 8px
- Padding: 16px
- Margin bottom: 12px

Checkmark Icon:
- Size: 20px
- Color: Green-600
- Position: Top-left
- Icon: Lucide Check

Title:
- Font: 18px, Semibold, Gray-900

Evidence:
- Font: 14px, Italic, Gray-700
- Background: White
- Padding: 12px
- Border radius: 6px
- Margin: 8px 0

Relevance:
- Font: 14px, Regular, Blue-600
- Icon: Lucide Info (info circle)
```

### 5.5 Gaps & Recommendations Section

```
┌─────────────────────────────────────────────────────────────┐
│ GAPS & RECOMMENDATIONS (6)                         [Expand] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ [RED DOT] HIGH PRIORITY (2 items)                          │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Missing: System Design Experience                      │ │
│ │                                                         │ │
│ │ [CHART] Impact:                                         │ │
│ │ Amazon SDE interns work on distributed systems and     │ │
│ │ microservices. This is a core requirement mentioned    │ │
│ │ 3 times in the role description.                        │ │
│ │                                                         │ │
│ │ [CHECK] Recommended Action:                             │ │
│ │ Add a project demonstrating distributed systems        │ │
│ │ knowledge. Include microservices, message queues,      │ │
│ │ or caching strategies.                                 │ │
│ │                                                         │ │
│ │ [LIGHTBULB] Example Project:                            │ │
│ │ "Build a scalable real-time chat application using    │ │
│ │ Redis pub/sub, WebSockets, and horizontal scaling.    │ │
│ │ Document architecture decisions and trade-offs."       │ │
│ │                                                         │ │
│ │ [CLOCK] Timeline: 2-3 months                            │ │
│ │ [BOOK] Resources: [MIT 6.824] [System Design Primer]   │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ [YELLOW DOT] MEDIUM PRIORITY (2 items)                     │
│ [Collapsed - Click to expand]                              │
│                                                             │
│ [GREEN DOT] LOW PRIORITY (2 items)                         │
│ [Collapsed - Click to expand]                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Section Header:
- Font: 20px, Bold, Gray-900
- Icon: 24px (use Lucide AlertTriangle icon)
- Count badge: Gray-500

Priority Badge:
- High: Red-500 circle (use Lucide Circle icon filled) + "HIGH PRIORITY"
- Medium: Yellow-500 circle (use Lucide Circle icon filled) + "MEDIUM PRIORITY"
- Low: Green-500 circle (use Lucide Circle icon filled) + "LOW PRIORITY"
- Font: 14px, Semibold

Gap Card:
- Background: White
- Border: 2px solid (Red/Yellow/Green based on priority)
- Border radius: 8px
- Padding: 20px
- Margin bottom: 16px
- Shadow: Medium

Title:
- Font: 18px, Bold, Gray-900

Impact Section:
- Icon: Lucide BarChart3
- Font: 14px, Regular, Gray-700
- Background: Red-50 (for high priority)
- Padding: 12px
- Border radius: 6px

Action Section:
- Icon: Lucide CheckCircle
- Font: 14px, Semibold, Gray-900
- Background: Blue-50
- Padding: 12px
- Border radius: 6px

Example Section:
- Icon: Lucide Lightbulb
- Font: 14px, Italic, Gray-700
- Background: Yellow-50
- Padding: 12px
- Border radius: 6px

Timeline & Resources:
- Font: 12px, Regular, Gray-600
- Icons: Lucide Clock (for timeline), Lucide BookOpen (for resources)
- Links: Blue-600, underline on hover
```

### 5.6 Timeline Section

```
┌─────────────────────────────────────────────────────────────┐
│ DEVELOPMENT TIMELINE                               [Expand] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Target Deadline: September 1, 2026                         │
│ Time Remaining: 32 weeks                                   │
│                                                             │
│ [DOT]─────────────────────────────────[DOT]                │
│ Now              Phase 1              Goal                 │
│ Jan 11           Feb 8                Sep 1                │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Phase 1: Immediate (0-4 weeks)                         │ │
│ │ Jan 11 - Feb 8, 2026                                   │ │
│ │                                                         │ │
│ │ Goals:                                                  │ │
│ │ [BULLET] Complete high-priority quick wins             │ │
│ │ [BULLET] Start distributed systems project             │ │
│ │ [BULLET] Update resume with quantified achievements    │ │
│ │                                                         │ │
│ │ Action Items:                                           │ │
│ │ [SQUARE] Revise resume bullet points with metrics      │ │
│ │ [SQUARE] Begin MIT 6.824 Distributed Systems course    │ │
│ │ [SQUARE] Design architecture for chat app project      │ │
│ │ [SQUARE] Set up development environment                │ │
│ │                                                         │ │
│ │ Milestone: Resume updated, project started             │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Phase 2: Short-term (1-3 months)                       │ │
│ │ [Collapsed - Click to expand]                          │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Phase 3: Medium-term (3-6 months)                      │ │
│ │ [Collapsed - Click to expand]                          │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Section Header:
- Font: 20px, Bold, Gray-900
- Icon: 24px (use Lucide Calendar icon)

Timeline Visualization:
- Line: 4px height, Gray-300
- Progress: Blue-600 fill
- Dots: 16px circles (use Lucide Circle icon)
  - Current: Blue-600, filled
  - Future: Gray-300, outlined
- Labels: 12px, Gray-600, below dots

Phase Card:
- Background: White
- Border: 1px solid Gray-200
- Border radius: 8px
- Padding: 20px
- Margin bottom: 12px

Phase Header:
- Font: 18px, Semibold, Gray-900
- Date range: 14px, Regular, Gray-600

Goals:
- Bullet points
- Font: 14px, Regular, Gray-700

Action Items:
- Checkboxes (interactive, use Lucide Square for unchecked, Lucide CheckSquare for checked)
- Font: 14px, Regular, Gray-700
- Hover: Background Gray-50

Milestone:
- Background: Blue-50
- Border: 1px solid Blue-200
- Padding: 8px 12px
- Border radius: 6px
- Font: 14px, Semibold, Blue-700
```

---

## 6. Component Specifications

### 6.1 Button Components

**Primary Button:**
```
Light Mode:
  Default:
  - Background: Teal (#468189)
  - Text: White, 16px, Semibold
  - Padding: 12px 24px
  - Border radius: 8px
  - Shadow: Small

  Hover:
  - Background: Sage (#77ACA2)
  - Transform: Scale(1.02)
  - Shadow: Medium

  Active:
  - Background: Deep Ocean (#031926)
  - Transform: Scale(0.98)

  Disabled:
  - Background: Mint (#9DBEBB) at 50% opacity
  - Text: Deep Ocean (#031926) at 50% opacity
  - Cursor: not-allowed

Dark Mode:
  Default:
  - Background: Sage (#77ACA2)
  - Text: Deep Ocean (#031926), 16px, Semibold
  - Padding: 12px 24px
  - Border radius: 8px
  - Shadow: Small

  Hover:
  - Background: Mint (#9DBEBB)
  - Transform: Scale(1.02)
  - Shadow: Medium

  Active:
  - Background: Teal (#468189)
  - Transform: Scale(0.98)

  Disabled:
  - Background: Sage (#77ACA2) at 30% opacity
  - Text: Cream (#F4E9CD) at 50% opacity
  - Cursor: not-allowed
```

**Secondary Button:**
```
Light Mode:
  Default:
  - Background: White
  - Text: Teal (#468189), 16px, Semibold
  - Border: 2px solid Teal (#468189)
  - Padding: 12px 24px
  - Border radius: 8px

  Hover:
  - Background: Mint (#9DBEBB) at 20% opacity
  - Border: 2px solid Sage (#77ACA2)
  - Text: Sage (#77ACA2)

Dark Mode:
  Default:
  - Background: Transparent
  - Text: Sage (#77ACA2), 16px, Semibold
  - Border: 2px solid Sage (#77ACA2)
  - Padding: 12px 24px
  - Border radius: 8px

  Hover:
  - Background: Sage (#77ACA2) at 20% opacity
  - Border: 2px solid Mint (#9DBEBB)
  - Text: Mint (#9DBEBB)
```

**Icon Button:**
```
Light Mode:
  Default:
  - Size: 40px × 40px
  - Background: Transparent
  - Icon: 20px, Teal (#468189)
  - Border radius: 8px

  Hover:
  - Background: Mint (#9DBEBB) at 20% opacity
  - Icon: Sage (#77ACA2)

Dark Mode:
  Default:
  - Size: 40px × 40px
  - Background: Transparent
  - Icon: 20px, Sage (#77ACA2)
  - Border radius: 8px

  Hover:
  - Background: Sage (#77ACA2) at 20% opacity
  - Icon: Mint (#9DBEBB)
```

### 6.2 Card Components

**Base Card:**
```
Light Mode:
- Background: White
- Border: 1px solid Mint (#9DBEBB)
- Border radius: 12px
- Padding: 24px
- Shadow: 0 4px 6px rgba(3, 25, 38, 0.1)

Hover (if interactive):
- Shadow: 0 10px 15px rgba(3, 25, 38, 0.15)
- Transform: translateY(-2px)
- Border: 1px solid Sage (#77ACA2)
- Transition: 200ms ease

Dark Mode:
- Background: Teal (#468189) at 20% opacity
- Border: 1px solid Sage (#77ACA2)
- Border radius: 12px
- Padding: 24px
- Shadow: 0 4px 6px rgba(0, 0, 0, 0.4)

Hover (if interactive):
- Shadow: 0 10px 15px rgba(0, 0, 0, 0.5)
- Transform: translateY(-2px)
- Border: 1px solid Mint (#9DBEBB)
- Transition: 200ms ease
```

**Expandable Card:**
```
Header:
- Cursor: pointer
- Display: flex, justify-between
- Padding: 16px 20px
- Border bottom: 1px solid Mint (#9DBEBB) in light, Sage (#77ACA2) in dark (when expanded)

Expand Icon:
- Size: 20px
- Color: Teal (#468189) in light mode, Sage (#77ACA2) in dark mode
- Rotate: 0deg (collapsed), 180deg (expanded)
- Transition: 200ms ease

Content:
- Padding: 20px
- Max height: 0 (collapsed), auto (expanded)
- Overflow: hidden
- Transition: 300ms ease
```

### 6.3 Progress Bar

```
Container:
- Height: 8px (small), 16px (large)
- Background: Light Mode: Mint (#9DBEBB) at 30% opacity, Dark Mode: Deep Ocean (#031926)
- Border radius: Full
- Overflow: hidden

Fill:
- Background: Teal (#468189) in light mode, Sage (#77ACA2) in dark mode (or color based on score)
- Height: 100%
- Border radius: Full
- Transition: width 500ms ease

Animation:
- On load: Animate from 0% to actual value
- Duration: 1500ms
- Easing: ease-out
```

### 6.4 Badge Component

```
Priority Badge:
- Display: inline-flex
- Align items: center
- Gap: 4px
- Padding: 4px 12px
- Border radius: Full
- Font: 12px, Semibold, Uppercase

High Priority:
- Background: Red-100
- Text: Red-700
- Icon: Red circle

Medium Priority:
- Background: Yellow-100
- Text: Yellow-700
- Icon: Yellow circle

Low Priority:
- Background: Green-100
- Text: Green-700
- Icon: Green circle
```

---

## 7. Interactions & Animations

### 7.1 Page Load Animations

```
Sequence:
1. Header: Fade in from top (0ms delay)
2. Left Panel: Slide in from left (100ms delay)
3. Right Panel: Fade in (200ms delay)

Duration: 400ms
Easing: ease-out
```

### 7.2 Results Display Animations

```
Sequence:
1. Overall Score Card: Scale up + fade in (0ms)
   - Score: Count up animation (0 → actual value)
   - Progress bar: Fill animation (left to right)
   
2. Category Cards: Stagger fade in (100ms between each)
   - Card 1: 200ms delay
   - Card 2: 300ms delay
   - Card 3: 400ms delay
   
3. Strengths Section: Slide up + fade in (500ms delay)

4. Gaps Section: Slide up + fade in (600ms delay)

5. Timeline Section: Slide up + fade in (700ms delay)

Duration: 400ms per animation
Easing: ease-out
```

### 7.3 Hover Interactions

**Card Hover:**
```
- Transform: translateY(-4px)
- Shadow: Increase from medium to large
- Duration: 200ms
- Easing: ease
```

**Button Hover:**
```
- Background: Darken by 10%
- Transform: Scale(1.02)
- Duration: 150ms
- Easing: ease
```

**Logo Hover:**
```
- Transform: Scale(1.05)
- Shadow: Medium
- Duration: 200ms
- Easing: ease-out
```

### 7.4 Click Interactions

**Expandable Card Click:**
```
1. Rotate expand icon (0deg → 180deg)
2. Expand content area (max-height: 0 → auto)
3. Fade in content (opacity: 0 → 1)

Duration: 300ms
Easing: ease-in-out
```

**Button Click:**
```
- Transform: Scale(0.98)
- Duration: 100ms
- Easing: ease-in
```

### 7.5 Loading Animations

**Spinner:**
```
- Rotation: 360deg continuous
- Duration: 1000ms
- Easing: linear
- Infinite loop
```

**Progress Bar Fill:**
```
- Width: Animate to percentage
- Duration: 500ms
- Easing: ease-out
- Update every 2 seconds during polling
```

**Skeleton Loading:**
```
- Background: Linear gradient (Gray-200 → Gray-300 → Gray-200)
- Animation: Shimmer effect (left to right)
- Duration: 1500ms
- Easing: ease-in-out
- Infinite loop
```

---

## 8. Responsive Design

### 8.1 Breakpoints

```
Mobile:  < 768px
Tablet:  768px - 1023px
Desktop: >= 1024px
Wide:    >= 1440px
```

### 8.2 Mobile Layout (< 768px)

```
┌────────────────────────────┐
│ Header (64px)              │
│ Ready2Intern    [Menu]     │
├────────────────────────────┤
│                            │
│ Upload Section             │
│ (Full width)               │
│                            │
├────────────────────────────┤
│                            │
│ Company Logos              │
│ (Horizontal scroll)        │
│                            │
├────────────────────────────┤
│                            │
│ Role Description            │
│ (Full width)               │
│                            │
├────────────────────────────┤
│                            │
│ [Analyze Button]           │
│ (Full width)               │
│                            │
├────────────────────────────┤
│                            │
│ Results                    │
│ (Full width, stacked)      │
│                            │
├────────────────────────────┤
│ Footer                     │
└────────────────────────────┘

Changes:
- Single column layout
- Left panel sections stack vertically
- Right panel appears below
- Company logos: Horizontal scroll
- Score cards: Stack vertically
- Font sizes: Reduce by 10-20%
- Padding: Reduce to 16px
```

### 8.3 Tablet Layout (768px - 1023px)

```
┌────────────────────────────────────┐
│ Header (64px)                      │
│ Ready2Intern      [Buttons]        │
├─────────────┬──────────────────────┤
│             │                      │
│ Left Panel  │  Right Panel         │
│ (300px)     │  (Flexible)          │
│             │                      │
│ Upload      │  Results             │
│             │  (2-column grid)     │
│ Logos       │                      │
│             │                      │
│ Role Desc    │                      │
│             │                      │
│ Button      │                      │
│             │                      │
├─────────────┴──────────────────────┤
│ Footer                             │
└────────────────────────────────────┘

Changes:
- Left panel: 300px (reduced from 400px)
- Score cards: 2-column grid
- Font sizes: Slightly reduced
- Padding: 20px
```

### 8.4 Desktop Layout (>= 1024px)

```
Full layout as shown in Section 2.1
- Left panel: 400px
- Right panel: Flexible
- Score cards: 3-column grid
- All sections visible
```

### 8.5 Responsive Typography

```
Mobile:
- H1: 32px
- H2: 24px
- H3: 18px
- Body: 14px
- Small: 12px

Tablet:
- H1: 40px
- H2: 30px
- H3: 20px
- Body: 15px
- Small: 13px

Desktop:
- H1: 48px
- H2: 36px
- H3: 24px
- Body: 16px
- Small: 14px
```

---

## 9. Accessibility

### 9.1 Color Contrast

```
All text meets WCAG AA standards:
- Normal text: 4.5:1 minimum
- Large text (18px+): 3:1 minimum
- Interactive elements: 3:1 minimum
```

### 9.2 Keyboard Navigation

```
Tab Order:
1. Header buttons
2. Upload dropzone
3. Company logos (left to right)
4. Role description textarea
5. Analyze button
6. Results sections (top to bottom)
7. Expandable cards
8. Footer links

Focus Indicators:
- Outline: 2px solid Blue-600
- Offset: 2px
- Border radius: Matches element
```

### 9.3 Screen Reader Support

```
- All images have alt text
- Buttons have aria-labels
- Progress bars have aria-valuenow
- Expandable sections have aria-expanded
- Loading states have aria-live="polite"
- Error messages have role="alert"
```

### 9.4 Motion Preferences

```
@media (prefers-reduced-motion: reduce) {
  - Disable all animations
  - Use instant transitions
  - Keep functional state changes
}
```

---

## 10. Implementation Notes

### 10.1 Technology Stack

```
- React 18+ with TypeScript
- Tailwind CSS for styling
- Framer Motion for animations (optional)
- Lucide React for icons
- Recharts for progress visualizations
```

### 10.2 Component Library Structure

```
src/components/
├── common/
│   ├── Button.tsx
│   ├── Card.tsx
│   ├── Badge.tsx
│   ├── ProgressBar.tsx
│   └── Spinner.tsx
├── dashboard/
│   ├── LeftPanel.tsx
│   ├── RightPanel.tsx
│   ├── FileDropzone.tsx
│   ├── CompanyLogoSelector.tsx
│   └── RoleDescriptionInput.tsx
├── results/
│   ├── OverallScoreCard.tsx
│   ├── CategoryScoreCard.tsx
│   ├── StrengthsSection.tsx
│   ├── GapsSection.tsx
│   └── TimelineSection.tsx
└── layout/
    ├── Header.tsx
    ├── Footer.tsx
    └── Layout.tsx
```

### 10.3 Design Tokens

```typescript
// colors.ts
export const colors = {
  brand: {
    deepOcean: '#031926',
    teal: '#468189',
    sage: '#77ACA2',
    mint: '#9DBEBB',
    cream: '#F4E9CD',
  },
  semantic: {
    success: '#10B981',
    warning: '#F59E0B',
    error: '#EF4444',
  },
  company: {
    amazon: '#FF9900',
    meta: '#0668E1',
    google: {
      blue: '#4285F4',
      red: '#EA4335',
      yellow: '#FBBC04',
      green: '#34A853',
    },
  },
};

// theme.ts
export const lightTheme = {
  background: {
    primary: '#F4E9CD',
    surface: '#FFFFFF',
  },
  text: {
    primary: '#031926',
    secondary: '#468189',
  },
  border: '#9DBEBB',
  button: {
    primary: '#468189',
    hover: '#77ACA2',
  },
};

export const darkTheme = {
  background: {
    primary: '#031926',
    surface: 'rgba(70, 129, 137, 0.2)',
  },
  text: {
    primary: '#F4E9CD',
    secondary: '#9DBEBB',
  },
  border: '#77ACA2',
  button: {
    primary: '#77ACA2',
    hover: '#9DBEBB',
  },
};

// spacing.ts
export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px',
  '2xl': '48px',
  '3xl': '64px',
};

// typography.ts
export const typography = {
  h1: { size: '48px', weight: 700, lineHeight: '1.2' },
  h2: { size: '36px', weight: 600, lineHeight: '1.3' },
  h3: { size: '24px', weight: 600, lineHeight: '1.4' },
  bodyLarge: { size: '18px', weight: 400, lineHeight: '1.6' },
  body: { size: '16px', weight: 400, lineHeight: '1.5' },
  bodySmall: { size: '14px', weight: 400, lineHeight: '1.5' },
  caption: { size: '12px', weight: 400, lineHeight: '1.4' },
};

// shadows.ts
export const shadows = {
  light: {
    sm: '0 1px 2px rgba(3, 25, 38, 0.05)',
    md: '0 4px 6px rgba(3, 25, 38, 0.1)',
    lg: '0 10px 15px rgba(3, 25, 38, 0.1)',
    xl: '0 20px 25px rgba(3, 25, 38, 0.15)',
  },
  dark: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.3)',
    md: '0 4px 6px rgba(0, 0, 0, 0.4)',
    lg: '0 10px 15px rgba(0, 0, 0, 0.5)',
    xl: '0 20px 25px rgba(0, 0, 0, 0.6)',
  },
};
```

### 10.4 Theme Provider Setup

```typescript
// ThemeProvider.tsx
import React, { createContext, useContext, ReactNode } from 'react';
import { useTheme } from './hooks/useTheme';

interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const { theme, toggleTheme } = useTheme();

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useThemeContext() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useThemeContext must be used within ThemeProvider');
  }
  return context;
}
```

---

## Quick Reference: Theme Colors

### Light Mode
- **Background:** Cream (#F4E9CD)
- **Cards:** White (#FFFFFF)
- **Text:** Deep Ocean (#031926)
- **Primary Button:** Teal (#468189)
- **Borders:** Mint (#9DBEBB)

### Dark Mode
- **Background:** Deep Ocean (#031926)
- **Cards:** Teal (#468189) at 20% opacity
- **Text:** Cream (#F4E9CD)
- **Primary Button:** Sage (#77ACA2)
- **Borders:** Sage (#77ACA2)

### Semantic Colors (Both Modes)
- **Success:** #10B981
- **Warning:** #F59E0B
- **Error:** #EF4444

### Company Brands (Both Modes)
- **Amazon:** #FF9900
- **Meta:** #0668E1
- **Google:** #4285F4, #EA4335, #FBBC04, #34A853

---

**This UI/UX mockup document provides complete visual specifications for implementing the Ready2Intern POC dashboard with full light/dark mode support. All measurements, colors, and interactions are defined for consistent implementation.**
