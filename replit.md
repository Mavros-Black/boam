# Overview

BOA ME Youth Empowerment is a nonprofit organization website built as a full-stack web application. The platform serves as both an informational site showcasing the organization's mission and programs, and an e-commerce platform for selling merchandise. The application focuses on empowering African youth through education, skills training, and community development programs, with integrated payment processing through Paystack for merchandise sales.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The client-side is built with React 18 using TypeScript and modern development practices:

- **Framework**: React with Vite as the build tool and development server
- **Routing**: Wouter for lightweight client-side routing
- **UI Framework**: Shadcn/ui components built on Radix UI primitives for accessibility
- **Styling**: Tailwind CSS with custom CSS variables for theming
- **State Management**: React Context for cart and theme management, TanStack React Query for server state
- **Form Handling**: React Hook Form with Zod validation for type-safe forms

## Backend Architecture
The server follows a REST API pattern with Express.js:

- **Runtime**: Node.js with Express.js framework
- **Database ORM**: Drizzle ORM with PostgreSQL dialect
- **Validation**: Zod schemas shared between client and server
- **Storage**: Abstracted storage interface with in-memory implementation for development
- **Build System**: ESBuild for production bundling, TSX for development

## Data Storage Architecture
The application uses a PostgreSQL database with the following schema design:

- **Users**: Authentication and user management
- **Products**: E-commerce catalog with categories, pricing, and inventory
- **Orders**: Shopping cart functionality with JSON storage for cart items and Paystack integration
- **Contact Inquiries**: Contact form submissions for community engagement

## Key Design Patterns
- **Repository Pattern**: Abstracted storage interface allows switching between in-memory and database implementations
- **Schema Sharing**: Zod schemas in the shared directory ensure type safety across client and server
- **Component Composition**: Modular UI components with clear separation of concerns
- **Context Providers**: Centralized state management for cart and theme functionality

# External Dependencies

## Payment Processing
- **Paystack**: Integrated payment gateway for handling merchandise transactions with Nigerian Naira support

## Database Infrastructure
- **Neon Database**: Serverless PostgreSQL database with connection pooling via @neondatabase/serverless

## UI and Design System
- **Radix UI**: Comprehensive set of unstyled, accessible UI primitives
- **Tailwind CSS**: Utility-first CSS framework with custom design tokens
- **Lucide React**: Icon library for consistent iconography
- **Font Awesome**: Additional icon support for specific use cases

## Development and Build Tools
- **Vite**: Fast development server and build tool with HMR support
- **TypeScript**: Type safety across the entire application
- **Drizzle Kit**: Database migration and schema management
- **React Hook Form**: Form state management with validation

## External Services Integration
- **Google Fonts**: Inter font family for typography
- **Unsplash**: Stock photography for program and hero imagery
- **Replit**: Development environment integration with error overlay and banner support

The architecture prioritizes developer experience with hot module replacement, type safety, and modular component design while maintaining production readiness with optimized builds and database integration.