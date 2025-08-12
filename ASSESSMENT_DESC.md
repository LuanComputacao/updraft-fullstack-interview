# UpDraft Fullstack Interview - Take Home Test

## Overview

This is a simplified "snippet" of the architecture used at UpDraft, designed to showcase both the strengths and areas for improvement in our current system. This take-home test provides candidates with a realistic representation of our production environment, allowing you to experience the actual challenges and opportunities we face daily.

## Architecture Description

### Multi-Tenant Architecture
The entire application is built on a **Multi-Tenant architecture** where each tenant has its own logical database within a shared PostgreSQL instance. For simplification purposes, the tenant is determined by the hostname.

### Technology Stack

#### Frontend
- **Vite** - Modern build tool for fast development and optimized production builds
- **Vue.js 3** - Progressive JavaScript framework with Composition API
- **PrimeVue 3** - Rich UI component library for Vue.js
- **PrimeFlex** - CSS utility library for responsive layouts
- **TipTap** - Rich text editor for document editing capabilities

#### Backend
- **Python** - Core programming language
- **Flask** - Lightweight web framework
- **Cosmic Python Architecture** - Adapted implementation of the architecture patterns described in the book "Cosmic Python" by Harry Percival and Bob Gregory
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migration management
- **Pydantic** - Data validation and settings management

#### Infrastructure
- **PostgreSQL** - Primary database with multi-tenant logical separation
- **Nginx** - Reverse proxy for routing and load balancing
- **Docker** - Containerization for consistent deployment

## Access Information

Once the application is successfully running, it will be available at:

**http://localdev.localhost:8090**

Where `localdev` represents the tenant name in this simplified multi-tenant setup.

## Getting Started

The application requires all Docker containers to be running along with the Vite development server. The setup process involves:

1. Starting all required Docker containers
2. Running database migrations
3. Running the Vite development server

## What You'll Experience

This take-home test provides a realistic glimpse into UpDraft's architecture, including:

- **Real-world complexity** - Actual patterns and challenges from our production system
- **Multi-tenant considerations** - How we handle data isolation and tenant-specific logic
- **Modern frontend development** - Vue 3 with modern tooling and component libraries
- **Backend architecture patterns** - Domain-driven design principles in practice
- **Infrastructure decisions** - Containerization, reverse proxy, and database design choices

This environment represents both the good practices we've established and areas where we're actively working to improve, giving you insight into the real challenges and opportunities you'd encounter as part of our team.

## The Task

### Context
This task mirrors how real features are requested at UpDraft. You won't receive step-by-step instructions because, like in a startup environment, solutions aren't always straightforward. We value creativity and your ability to analyze ROI when making implementation decisions.

We're a startup - we don't always have time for the 100% perfect solution, but we can't ship a 10% solution either. Finding the right balance between UX quality and delivery time is crucial. We often discuss trade-offs between user experience and development velocity.

### Current State
The application has a fully functional **Documents** entity with CRUD operations implemented on both frontend and backend. You should find one pre-populated document with content to work with.

### Feature Request: Document Summarization

Users want a summary functionality for their documents. Since documents can be lengthy, they'd love a one-click solution to generate summaries. The implementation should:

- Use the existing **TipTap Rich Text Editor** for consistency
- **Stream responses** in the UI to avoid user waiting frustration
- Allow users to save summaries as the document's official summary
- Support editing and deleting saved summaries
- Enable re-summarization if users aren't satisfied

### User Stories

1. **As a user** I can create an AI-generated summary from a document
2. **As a user** I can save a summary so it becomes the document's summary
3. **As a user** I can edit the summary that was created
4. **As a user** I can delete the summary that was created
5. **As a user** I can see the response streaming in the UI while the summary is being created

### Implementation Considerations

- **AI Integration**: You'll need to choose and integrate an AI service for summarization
- **Streaming**: Consider how to implement real-time streaming of AI responses
- **Database Schema**: Plan how to store summaries and their relationship to documents
- **UX Design**: Think about where and how to present the summarization feature
- **Error Handling**: Consider edge cases and failure scenarios
- **Performance**: Balance feature richness with system performance

Remember: This is about finding the right balance between a polished user experience and practical implementation. We want to see your decision-making process and how you approach real-world constraints.

## Rules & Expectations

### AI Usage
**Use AI extensively!** This take-home test was designed with the expectation that you'll leverage AI to accelerate your work. We're not testing your ability to code from scratch - we're testing your ability to work efficiently with modern tools and understand the resulting code.

However, you must be able to:
- Understand the code you're working with
- Justify your implementation decisions in a code review
- Explain the architecture and design choices you made

### Deliverable
Your output should be a **Pull Request to the master branch** so we can conduct a proper code review and make future edits together.

### Development Practices
- **Commit frequently** with clear, descriptive commit messages
- We'll assess your task organization and workflow through your commit history

### Testing
- **Unit tests are not expected** at this stage
- Write tests only if you need them to verify functionality during development
- We'll cover comprehensive testing strategies in our follow-up discussion

### Time Management
- If you think the take-home is taking too long, you are not forced to continue
- Stop, make sure that what you submit is good, production ready, and we can talk about the missing features in the follow-up call
- Quality over quantity - focus on demonstrating good decision-making and clean implementation

### What We're Looking For
- **Problem-solving approach** - How you break down complex requirements
- **Technical decision-making** - Why you chose specific implementations
- **Code quality** - Clean, maintainable, well-structured code, following existing patterns
- **User experience** - Thoughtful UX decisions and implementation
- **Communication** - Ability to explain your work and take feedback

### Questions & Support
- If you encounter blockers or need clarification, document your questions and send me an email
- Feel free to include notes about trade-offs you considered or alternative approaches you explored

### Submission Instructions
When you've completed the task, email me the Pull Request link so I can review your work.

### Evaluation Timeline
You can expect feedback within **2 days** of submission.

### Follow-up Process
After reviewing your code, we'll schedule a **45-60 minute** live session where we'll:
- Conduct a detailed code review
- Discuss potential improvements and alternative approaches
- Chat about your implementation decisions and thought process 

