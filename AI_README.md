# Docsie Landing Page

A modern, conversion-focused landing page for Docsie - an intelligent documentation platform. This project uses HTML, CSS, and vanilla JavaScript with Jinja templating for component organization.
 
## Project Structure


src/
├── new_home/
│ ├── index.html # Main landing page
│ ├── banner/ # Hero section
│ ├── solutions/ # Solutions showcase
│ │ ├── solutions.html
│ │ └── style.css
│ ├── ai/ # AI capabilities section
│ │ ├── ai.html
│ │ └── style.css
│ ├── industries/ # Industry solutions
│ │ ├── industries.html
│ │ └── style.css
│ ├── roles/ # Role-based features
│ │ ├── roles.html
│ │ └── style.css
│ ├── reviews/ # Customer testimonials
│ │ ├── reviews.html
│ │ ├── style.css
│ │ └── script.js
│ └── security/ # Security features
│ ├── security.html
│ └── style.css
└── assets/
└── new_home/
├── solutions/ # Solution icons and images
├── ai/ # AI section assets
├── industries/ # Industry images
└── reviews/ # Review section assets


## Component Overview

### 1. Solutions Section
- Horizontal card layout
- Four main solutions: Knowledge Base, Product Documentation, SOPs, User Manuals
- Interactive hover effects
- Responsive grid design

### 2. AI Section
- Dark, futuristic design theme
- Interactive feature showcase
- Cyan accent color (#00F0FF)
- Three main features: Chatbot, Video Transform, AI Writer

### 3. Industries Section
- Horizontal picker navigation
- Six industries: Manufacturing, IT Services, Energy, SaaS, Compliance, Government/Non-Profit
- Detailed feature descriptions
- Image + content layout

### 4. Roles Section
- Three main roles: Technical Writers, Product Managers, Developers
- Card-based layout
- Feature highlights for each role
- Icon-based visual elements

### 5. Reviews Section
- G2 reviews integration
- 4.8/5 rating display
- Carousel navigation
- Testimonial cards with user info

### 6. Security Section
- Three-column layout
- Feature highlights
- Icon-based design
- Enterprise security focus

## Design System

### Colors
- Primary: #B11111 (Red)
- Secondary: #00F0FF (Cyan, AI section)
- Text Primary: #101212
- Text Secondary: #39464E
- Background: #FFFFFF, #F8FAFC
- Borders: #ECF0F4

### Typography
- Headers: 'Arimo', sans-serif
- Body: 'Open Sans', sans-serif
- Font sizes: 12px - 48px

### Components
- Cards with hover effects
- Horizontal pickers
- Feature lists with icons
- Responsive grids
- Interactive carousels

## Responsive Breakpoints
- Desktop: > 968px
- Tablet: 768px - 968px
- Mobile: < 768px

## Key Features
- Modular component structure
- Jinja templating
- Lazy loading images
- Smooth animations
- Mobile-first approach
- SEO-friendly markup

## Development Notes
1. Use BEM naming convention for CSS
2. Maintain consistent spacing (8px grid)
3. Optimize images before deployment
4. Test across all breakpoints
5. Ensure accessibility compliance

## Future Enhancements
1. Add more interactive elements
2. Implement dark mode
3. Add more customer testimonials
4. Enhance mobile navigation
5. Add more industry-specific content

## Assets Required
- SVG icons for solutions
- Industry-specific images
- Customer testimonial photos
- AI section background patterns
- G2 review badges

## Performance Considerations
1. Lazy load images
2. Minimize CSS/JS
3. Optimize font loading
4. Use appropriate image formats
5. Implement caching strategies

This README provides a comprehensive overview of the project structure and components, making it easier for future development and maintenance.



