## Feature Spec: Scheduling & Dispatch

**Feature Name**: Truckster Scheduling & Dispatch

### 1. Problem Statement
Site supervisors need a fast, reliable way to schedule dump trucks for job sites on a day-to-day basis. Current processes involve manual phone calls, inconsistent updates, and little visibility into load requirements or truck availability.

### 2. User Stories & Roles
**Primary User**: Site Supervisor
- *As a site supervisor*, I want to schedule trucks for a job site on a specific day, so I can ensure work proceeds without delays.
- *As a site supervisor*, I want to specify job details like location, load type, and truck requirements to avoid miscommunication.
- *As a dispatcher*, I want to see all incoming requests clearly categorized by job and date.

### 3. Core Functionality
- Single-day truck scheduling UI
- Inputs: date, job location, load type (e.g., gravel, fill, debris), gate entrance, truck type (e.g., quad, pup)
- Add/remove time slots for arrivals
- Ability to request multiple trucks per time slot
- Confirmation receipt upon scheduling

### 4. Edge Cases & Constraints
- Must validate gate entrance details match the job location
- Should support both early-morning and late-afternoon shifts
- Prevents double-booking trucks if availability is known

### 5. Dependencies & Integration Points
- Job location data (pre-filled from existing projects)
- Truck type taxonomy (standardized list)
- Notification system for confirming bookings

### 6. Acceptance Criteria
- [ ] Supervisor can schedule for a job within 3 minutes
- [ ] Supervisor can specify all 4 constraints (load type, job location, gate entrance, truck type)
- [ ] Dispatcher view shows all scheduled jobs and truck requirements
- [ ] Booking is confirmed via email or SMS
- [ ] System prevents incomplete requests (missing constraints)

---

**Next steps:** Define wireframes and backend service endpoints to support scheduling flow.