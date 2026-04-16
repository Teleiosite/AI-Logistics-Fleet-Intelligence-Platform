# AI Logistics & Fleet Intelligence Platform
## Complete Product Documentation & Technical Specification

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Market Analysis & Product Positioning](#2-market-analysis--product-positioning)
3. [Product Vision & Strategic Goals](#3-product-vision--strategic-goals)
4. [User Personas & Journey Maps](#4-user-personas--journey-maps)
5. [Comprehensive Feature Catalog](#5-comprehensive-feature-catalog)
6. [Technical Architecture](#6-technical-architecture)
7. [Data Model & Schema Design](#7-data-model--schema-design)
8. [Business Logic & Workflow Rules](#8-business-logic--workflow-rules)
9. [AI/ML Strategy & Implementation](#9-aiml-strategy--implementation)
10. [Security & Compliance Framework](#10-security--compliance-framework)
11. [Phased Implementation Roadmap](#11-phased-implementation-roadmap)
12. [Success Metrics & KPIs](#12-success-metrics--kpis)
13. [Risk Management & Mitigation](#13-risk-management--mitigation)
14. [Go-to-Market Strategy](#14-go-to-market-strategy)
15. [Appendices](#15-appendices)

---

## 1. Executive Summary

### 1.1 Product Name
**FleetIQ** — AI Logistics & Fleet Intelligence Platform

### 1.2 Vision Statement
Transform logistics operations from reactive problem-solving to proactive intelligence-driven management through automated tracking, intelligent alerts, and AI-powered decision support.

### 1.3 Problem Statement
Logistics companies struggle with:
- **Manual tracking**: 70% of shipment delays discovered after customer complaints
- **Fuel leakage**: 15-25% fuel cost variance due to theft, inefficiency, or poor route planning
- **Invoice disputes**: 30-40% of transport invoices require manual reconciliation
- **Opacity**: Limited real-time visibility into fleet location and delivery status
- **Reactive management**: Issues discovered too late for corrective action
- **Data silos**: Operations, finance, and compliance teams work from different spreadsheets

### 1.4 Solution Overview
FleetIQ is a cloud-native SaaS platform that:
- Provides **real-time shipment and fleet visibility**
- **Automates** fuel monitoring, invoice reconciliation, and variance detection
- Uses **AI/ML** to predict delays, detect anomalies, and recommend optimizations
- Offers a **conversational AI copilot** for natural-language analytics
- Scales from **small businesses to enterprise** with multi-tenant architecture
- Integrates with existing **ERP, GPS, and accounting systems**

### 1.5 Target Market Segments

| Segment | Company Size | Primary Pain Point | Price Sensitivity |
|---------|--------------|-------------------|-------------------|
| FMCG Distributors | 50-500 employees | Delivery accuracy | Medium |
| Manufacturing Logistics | 200-2000 employees | Fleet utilization | Low |
| 3PL Providers | 100-1000 employees | Client visibility | Medium |
| Transport Contractors | 20-200 employees | Fuel cost control | High |
| Warehouse Operations | 50-500 employees | Dispatch efficiency | Medium |

### 1.6 Competitive Advantage

1. **AI-First Design**: Built for intelligence, not just tracking
2. **Unified Platform**: Replaces 5-7 different tools companies currently use
3. **African Market Focus**: Designed for infrastructure realities (intermittent connectivity, diverse fuel pricing)
4. **Conversational Interface**: Non-technical users can ask questions in plain language
5. **Cost Transparency**: Full fuel and transport cost visibility with audit trails

### 1.7 Business Model

**Primary Revenue Streams:**
- **Subscription SaaS** (per company, tiered by vehicle count)
- **Premium AI Features** (add-on modules)
- **API Access** (integration tier)
- **Professional Services** (implementation, training, custom integrations)

**Pricing Tiers:**
- **Starter**: $99/month (up to 10 vehicles)
- **Professional**: $499/month (up to 50 vehicles)
- **Enterprise**: Custom pricing (50+ vehicles, dedicated support)

---

## 2. Market Analysis & Product Positioning

### 2.1 Market Size & Opportunity

**Global Logistics Software Market:**
- Current size: $14.2B (2024)
- CAGR: 12.3% through 2030
- Fleet management subset: $4.8B

**African Market Specific:**
- Growing middle class driving FMCG demand
- Infrastructure investment increasing logistics complexity
- Digital transformation lagging in traditional sectors
- High fuel costs making efficiency critical

### 2.2 Competitive Landscape

| Competitor | Strengths | Weaknesses | Our Differentiation |
|------------|-----------|------------|---------------------|
| Tookan, OnFleet | Delivery tracking | No fuel/finance modules | Full operational suite |
| Samsara, Geotab | Hardware + GPS | Expensive, complex | Software-first, affordable |
| Oracle TMS | Enterprise features | Not SMB-friendly | Accessible to all sizes |
| Local spreadsheets | Familiar, flexible | Error-prone, no automation | Smart automation + familiarity |

### 2.3 Product Positioning Statement

**For** logistics managers and fleet operators in FMCG, manufacturing, and distribution companies **who** struggle with manual tracking, fuel waste, and invoice disputes, **FleetIQ** is an AI-powered logistics intelligence platform **that** provides real-time visibility, automated cost control, and predictive insights. **Unlike** traditional fleet tracking tools or complex enterprise TMS systems, **FleetIQ** combines operational tracking, financial reconciliation, and AI decision support in one affordable, easy-to-use platform designed for African market realities.

---

## 3. Product Vision & Strategic Goals

### 3.1 3-Year Vision

**Year 1 (MVP to Product-Market Fit):**
- Launch core operational features
- Onboard 20-50 companies
- Validate pricing and feature mix
- Establish customer success playbook

**Year 2 (AI Maturity & Scale):**
- Deploy full AI insight engine
- Expand to 200+ companies
- Build integration marketplace
- Launch API partner program

**Year 3 (Market Leadership):**
- 1000+ companies across 5 countries
- Industry-specific editions (FMCG, Manufacturing, 3PL)
- Advanced predictive analytics
- Mobile-first driver experience

### 3.2 Product Principles

1. **Simplicity Over Complexity**: Every feature must reduce workload, not add it
2. **Mobile-First for Field, Desktop-First for Office**: Right interface for the context
3. **AI as Copilot, Not Autopilot**: Augment human decisions, don't replace them
4. **Data Integrity as Foundation**: No insights without trustworthy data
5. **Offline-Ready**: Critical workflows work without constant connectivity
6. **Security by Default**: Multi-tenant isolation, encryption, audit trails built-in

### 3.3 Success Criteria

**Product Success:**
- 80%+ daily active user rate for logistics managers
- 50%+ reduction in delivery variance resolution time
- 20%+ improvement in fuel cost per km
- 90%+ user satisfaction score

**Business Success:**
- $1M ARR by end of Year 2
- <5% monthly churn
- 40%+ gross margin
- Net Promoter Score >50

---

## 4. User Personas & Journey Maps

### 4.1 Primary Personas

#### Persona 1: Logistics Manager (Primary User)

**Name:** Chioma Okafor  
**Age:** 34  
**Company:** Mid-size FMCG distributor  
**Team Size:** 30 vehicles, 45 drivers  
**Tech Comfort:** Medium

**Day in the Life:**
- 6:00 AM: Reviews overnight dispatch plans
- 7:00 AM: Confirms vehicle availability and driver assignments
- 9:00 AM: Monitors active deliveries, handles customer queries
- 12:00 PM: Investigates delay alerts, reassigns shipments
- 3:00 PM: Reviews delivery variances, approves DVRs
- 5:00 PM: Prepares daily summary for management

**Pain Points:**
- Spends 40% of time on manual status updates and WhatsApp coordination
- Discovers problems too late to fix them
- Cannot prove delivery issues to customers or transporters
- Lacks visibility into fuel usage patterns
- Weekly fire-drills reconciling transport invoices

**Goals:**
- Reduce time spent on manual coordination by 60%
- Know about delays before customers complain
- Have proof for every delivery dispute
- Cut fuel costs by 15%
- Present clean operational reports to executives

**How FleetIQ Helps:**
- Real-time dashboard shows all active shipments
- AI alerts predict delays 2-4 hours early
- Mobile app captures proof-of-delivery automatically
- Fuel anomaly detection flags unusual patterns
- One-click executive summary reports

---

#### Persona 2: Transport Admin (Finance-Focused User)

**Name:** Ahmed Ibrahim  
**Age:** 41  
**Role:** Transport & Finance Coordinator  
**Company:** Manufacturing company with owned fleet  
**Responsibilities:** Invoice reconciliation, transporter payments, cost analysis

**Pain Points:**
- Manually matches 200+ invoice line items per month
- Cannot verify transporter claims without operational data
- No visibility into why fuel costs vary week-to-week
- Disputes take 3-4 weeks to resolve
- Lacks historical data to negotiate better rates

**Goals:**
- Automate invoice validation
- Reduce disputed charges by 50%
- Build transporter performance scorecards
- Prove fuel efficiency improvements to management

**How FleetIQ Helps:**
- Auto-match invoice items to shipment records
- Flag discrepancies for review before payment
- Fuel cost trending by route, vehicle, driver
- Transporter performance scoring
- Audit trail for every charge

---

#### Persona 3: Driver (Mobile User)

**Name:** Emeka Eze  
**Age:** 29  
**Experience:** 7 years commercial driving  
**Tech Comfort:** Low-Medium (smartphone user)

**Pain Points:**
- Blamed for delays outside his control
- No easy way to report issues en route
- Paperwork gets lost or damaged
- Fuel receipts disputed weeks later
- Doesn't receive clear trip instructions

**Goals:**
- Clear trip assignments with all details
- Easy way to update status and report problems
- Digital proof that he delivered correctly
- Fair evaluation based on actual performance

**How FleetIQ Helps:**
- Mobile app shows trip details, route, customer info
- One-tap status updates
- Photo capture for proof-of-delivery
- Automatic GPS logging proves his location
- Driver performance score based on data, not perception

---

#### Persona 4: Executive Stakeholder (Decision Maker)

**Name:** Dr. Folake Adeyemi  
**Age:** 52  
**Role:** Operations Director  
**Company:** Large FMCG company  
**Oversight:** 150 vehicles, 12 distribution centers

**Pain Points:**
- Cannot get operational visibility without asking for reports
- Lacks confidence in data accuracy
- Wants to invest in efficiency but needs ROI proof
- Board asks questions she cannot answer without 2-day research

**Goals:**
- Real-time operational pulse
- Trustworthy data for board presentations
- Evidence-based decision making
- Clear ROI from logistics investments

**How FleetIQ Helps:**
- Executive dashboard with key metrics
- AI-generated weekly summaries
- Conversational queries ("Which routes have highest fuel variance?")
- Trend analysis and benchmarking
- Exportable reports for board meetings

---

### 4.2 User Journey Maps

#### Journey 1: Creating and Tracking a Shipment

**Actor:** Logistics Manager

| Stage | User Action | System Response | Pain Point Addressed | Success Metric |
|-------|-------------|-----------------|---------------------|----------------|
| **Planning** | Opens dashboard, clicks "New Shipment" | Shows shipment creation form with smart defaults | Manual entry errors | <30 sec to create |
| **Assignment** | Selects customer, products, destination | Suggests available vehicles and drivers based on location, capacity | Suboptimal assignment | 90% first-choice acceptance |
| **Dispatch** | Confirms and dispatches | Notifies driver via mobile app, creates shipment record | Coordination delays | Instant notification |
| **Monitoring** | Views shipment on live dashboard | Shows real-time status, ETA, route adherence | No visibility | 100% uptime |
| **Exception** | Receives delay alert | AI predicts 45-min delay, suggests action | Reactive problem-solving | 2-hour advance warning |
| **Delivery** | Driver completes delivery | Proof-of-delivery uploaded, status auto-updated | Manual confirmation | 95% same-day closure |
| **Reporting** | Reviews daily performance | AI summarizes day's operations with insights | Time-consuming manual reports | 5-min daily review |

---

#### Journey 2: Fuel Issuance and Anomaly Detection

**Actor:** Fleet Supervisor

| Stage | User Action | System Response | Pain Point Addressed | Success Metric |
|-------|-------------|-----------------|---------------------|----------------|
| **Issuance** | Records fuel dispensed to vehicle | Logs date, quantity, price, vehicle, odometer | Manual tracking | <2 min per entry |
| **Consumption** | System tracks trip distance | Calculates fuel efficiency (km/liter) | No consumption visibility | Auto-calculated |
| **Benchmarking** | Reviews weekly fuel report | Compares vehicle efficiency to fleet average | No performance comparison | All vehicles benchmarked |
| **Anomaly** | Receives alert: "Vehicle 12 - 40% below expected efficiency" | AI flags unusual pattern with context | Theft/waste discovered late | Same-day detection |
| **Investigation** | Clicks alert, reviews trip history | Shows route, driver, recent fuel records | Tedious manual review | 1-click context |
| **Action** | Assigns vehicle for inspection, notes issue | Creates audit trail, flags for follow-up | No accountability | 100% documented |

---

#### Journey 3: Invoice Reconciliation

**Actor:** Finance Officer

| Stage | User Action | System Response | Pain Point Addressed | Success Metric |
|-------|-------------|-----------------|---------------------|----------------|
| **Receipt** | Uploads transporter invoice PDF | Extracts line items (AI OCR) | Manual data entry | 95% extraction accuracy |
| **Matching** | Clicks "Auto-Match" | Matches invoice items to shipment records | Hours of manual work | <5 min matching |
| **Variance** | Reviews flagged discrepancies | Highlights extra charges, quantity mismatches | Hidden overcharges | 100% discrepancy visibility |
| **Investigation** | Clicks discrepancy, sees shipment details | Shows DVR if exists, proof-of-delivery, route | No supporting context | 1-click evidence |
| **Resolution** | Approves correct items, disputes others | Generates dispute memo with evidence | Manual documentation | Auto-generated |
| **Payment** | Marks invoice approved | Updates payment status, logs approval | No audit trail | Complete history |

---

## 5. Comprehensive Feature Catalog

### 5.1 Core Features (MVP - Phase 1-8)

#### 5.1.1 Authentication & Access Control

**Features:**
- Multi-tenant architecture with company-level data isolation
- Role-based access control (RBAC) with 8 predefined roles
- JWT-based authentication with refresh tokens
- OAuth2 SSO support (Google Workspace, Microsoft Entra)
- Password policies (complexity, expiration, history)
- Two-factor authentication (SMS, authenticator app)
- Account lockout after failed attempts
- Password reset via email with time-limited tokens
- User invitation system with email verification
- Session management with configurable timeout
- Audit logs for all authentication events
- IP whitelisting for enterprise clients

**User Stories:**
- As a Company Admin, I can invite users with specific roles so they have appropriate access
- As a user, I can log in securely and stay logged in across devices
- As a Super Admin, I can enforce 2FA for all users in sensitive roles

---

#### 5.1.2 Company & Tenant Management

**Features:**
- Company profile with branding (logo, colors)
- Multi-location support (warehouses, distribution centers)
- Company settings and preferences
- Subscription tier management
- Usage tracking (vehicles, users, storage)
- Data export controls
- Custom fields for company-specific needs
- Timezone and locale settings
- Fiscal year and calendar configuration
- Integration credentials management

**User Stories:**
- As a Company Admin, I can configure our company settings so the platform matches our operations
- As a Super Admin, I can manage multiple companies and switch between them easily

---

#### 5.1.3 Fleet Management

**Vehicle Management:**
- Vehicle registry with full details (make, model, year, VIN, license plate)
- Vehicle categorization (truck, van, motorcycle, etc.)
- Capacity specifications (weight, volume, pallet count)
- Ownership type (owned, leased, contracted)
- Insurance and registration tracking
- Maintenance schedule and history
- Fuel tank capacity and fuel type
- GPS device assignment
- Vehicle status (active, maintenance, retired)
- Vehicle photos and documents
- Odometer tracking
- Cost per kilometer calculation

**Driver Management:**
- Driver profiles (name, contact, photo, ID)
- License details with expiration tracking
- Driver ratings and performance scores
- Shift schedules and availability
- Driver-vehicle assignment history
- Contact information and emergency contacts
- Training records and certifications
- Driver app access credentials
- Performance metrics (on-time %, safety score, fuel efficiency)
- Driver documents (license, insurance, contracts)

**User Stories:**
- As a Transport Admin, I can maintain an accurate fleet registry so I know what assets we have
- As a Logistics Manager, I can assign the right vehicle and driver to each shipment based on capacity and availability
- As a Driver, I can view my performance score and understand how it's calculated

---

#### 5.1.4 Shipment Management & Tracking

**Shipment Creation:**
- Customer details (name, contact, delivery address)
- Product/cargo details (SKUs, quantities, weight, volume)
- Pickup and delivery locations with GPS coordinates
- Scheduled pickup and delivery times
- Special instructions and handling requirements
- Priority levels (standard, urgent, critical)
- Multiple drop-off support (multi-drop shipments)
- Reference numbers (customer PO, internal job number)
- Attachments (order confirmation, packing list)
- Cost estimation
- Vehicle and driver assignment

**Shipment Tracking:**
- Real-time status updates (13-state lifecycle)
- GPS location tracking with breadcrumb trail
- ETA calculation with traffic consideration
- Route adherence monitoring
- Geofence alerts (arrived at pickup/delivery)
- Automatic status updates based on GPS
- Manual status override capability
- Timeline view of all status changes
- Proof-of-delivery capture (photo, signature, notes)
- Exception flagging and escalation
- Customer notification triggers
- Live map view with all active shipments

**Shipment States:**
1. **Draft** - Created but not finalized
2. **Scheduled** - Planned for future dispatch
3. **Assigned** - Vehicle and driver assigned
4. **Dispatched** - Released for pickup
5. **En Route to Pickup** - Traveling to load point
6. **At Pickup** - Arrived at origin
7. **Loaded** - Cargo loaded, in transit
8. **In Transit** - Traveling to destination
9. **At Delivery** - Arrived at destination
10. **Unloading** - Cargo being unloaded
11. **Delivered** - Successfully completed
12. **Delayed** - Behind schedule
13. **Exception** - Issue requiring intervention

**User Stories:**
- As a Logistics Manager, I can create shipments quickly with all necessary details
- As a Driver, I can see my assigned shipments with clear instructions
- As a Customer Service Rep, I can check shipment status and provide accurate ETAs
- As an Operations Manager, I can see all active shipments on a live map

---

#### 5.1.5 Fuel Management & Cost Control

**Fuel Issuance:**
- Fuel dispensing records (date, time, vehicle, quantity, odometer)
- Fuel station/pump identification
- Fuel price per liter
- Attendant name
- Receipt photo upload
- Fuel card tracking
- Pre-authorization vs. actual fuel
- Fuel advance tracking

**Fuel Monitoring:**
- Weekly fuel price history by region
- Fuel consumption calculation (liters per 100km)
- Expected vs. actual consumption comparison
- Fuel efficiency by vehicle, driver, route
- Fuel cost per shipment/trip
- Tank capacity vs. fill patterns
- Fuel variance alerts
- Benchmark reporting (fleet average, industry standard)
- Fuel theft detection algorithms

**Multi-Drop Fuel Tracking:**
- Fuel allocated per leg of multi-stop route
- Pro-rated fuel cost per delivery
- Route-based consumption modeling

**User Stories:**
- As a Fleet Supervisor, I can record fuel issuance accurately and quickly
- As a Finance Officer, I can see total fuel costs broken down by vehicle, route, and time period
- As a Logistics Manager, I receive alerts when fuel usage is abnormal so I can investigate immediately

---

#### 5.1.6 Delivery Variance Reports (DVR)

**Variance Types:**
- Short delivery (quantity less than expected)
- Over delivery (quantity more than expected)
- Damaged goods
- Wrong items delivered
- Late delivery (beyond SLA)
- Missed delivery window
- Wrong destination
- Customer refused delivery
- Access issues (closed, unreachable)
- Fuel variance
- Route deviation
- Unauthorized stops

**DVR Workflow:**
1. **Creation** - Driver or logistics manager creates DVR
2. **Evidence Capture** - Photos, notes, customer signature/refusal
3. **Categorization** - Variance type, severity, fault assignment
4. **Review** - Logistics manager investigates
5. **Approval/Rejection** - Decision with justification
6. **Reconciliation** - Financial adjustment if needed
7. **Closure** - Resolution notes, lessons learned

**Features:**
- DVR form with structured fields
- Multi-photo upload
- Customer acknowledgment capture
- Fault assignment (driver, transporter, customer, force majeure)
- Severity rating (minor, moderate, major, critical)
- Impact assessment (financial, reputation, safety)
- Internal comments and notes
- Approval workflow with notifications
- Resolution tracking (open, under review, resolved, closed)
- Charge adjustment linking
- Memo generation for internal/external communication
- DVR analytics dashboard

**User Stories:**
- As a Driver, I can report delivery issues immediately with photo evidence
- As a Logistics Manager, I can review all delivery variances in one place and approve resolutions
- As a Finance Officer, I can see financial impact of variances and link them to invoice adjustments

---

#### 5.1.7 Invoice & Cost Reconciliation

**Invoice Management:**
- Invoice upload (PDF, image, manual entry)
- AI-powered OCR for invoice extraction
- Line item breakdown (shipment ID, quantity, rate, amount)
- Invoice header info (number, date, transporter, payment terms)
- Multiple invoices per transporter per period
- Invoice status tracking (pending, approved, disputed, paid)
- Payment terms and due date tracking
- Payment status and history

**Auto-Matching Engine:**
- Match invoice items to shipment records
- Flag extra charges not in original quote
- Detect quantity mismatches
- Highlight rate discrepancies
- Compare against contracted rates
- Calculate expected cost vs. invoiced cost

**Reconciliation Workflow:**
1. **Upload** - Invoice received
2. **Extraction** - AI extracts line items
3. **Matching** - Auto-match to shipments
4. **Variance Detection** - Highlight discrepancies
5. **Review** - Finance officer investigates
6. **Evidence Gathering** - Link DVRs, POD, GPS data
7. **Dispute/Approve** - Decision per line item
8. **Memo Generation** - Document for transporter
9. **Payment Processing** - Update accounting
10. **Audit Trail** - Complete record

**Incentive & Extra Charge Memos:**
- Template-based memo generation
- Evidence attachment (shipment data, GPS, photos)
- Approval workflow
- PDF export with company letterhead
- Email distribution

**User Stories:**
- As a Finance Officer, I can upload invoices and have them automatically checked against our records
- As a Transport Admin, I can generate dispute memos with supporting evidence in minutes
- As an Auditor, I can see complete history of every invoice from receipt to payment

---

#### 5.1.8 Transporter Management

**Transporter Profiles:**
- Company details (name, contact, registration)
- Contract terms and rate agreements
- Payment terms
- Insurance and compliance docs
- Performance rating
- Historical performance data
- Vehicle and driver roster (for contracted fleet)

**Performance Scoring:**
- On-time delivery rate
- Variance frequency
- Invoice accuracy
- Response time
- Safety record
- Customer feedback
- Cost competitiveness

**User Stories:**
- As a Logistics Manager, I can compare transporter performance to make informed decisions
- As a Procurement Officer, I can use performance data to negotiate better rates

---

### 5.2 Analytics & Reporting Features (Phase 8)

#### 5.2.1 Operational Dashboards

**Shipment Dashboard:**
- Active shipments count
- On-time delivery rate (daily, weekly, monthly)
- Average delivery time
- Delayed shipments with reasons
- Exception rate and top exception types
- Shipment volume trends
- Geographic distribution map
- Peak delivery times heatmap

**Fleet Dashboard:**
- Fleet utilization rate
- Vehicle availability status
- Vehicles in maintenance
- Average distance per vehicle
- Fleet efficiency score
- Capacity utilization
- Most/least utilized vehicles

**Fuel Dashboard:**
- Total fuel consumption (volume, cost)
- Fuel cost per km by vehicle
- Fuel efficiency trends
- Anomaly count and investigation status
- Price variance by station/region
- Budget vs. actual fuel spend
- Top fuel-efficient vehicles/drivers

**Cost Dashboard:**
- Total transport costs
- Cost per shipment
- Cost per kilometer
- Cost breakdown (fuel, labor, vehicle, overhead)
- Budget tracking
- Cost trends over time
- Cost variance analysis

**Driver Performance Dashboard:**
- Driver rankings by key metrics
- On-time delivery percentage
- Fuel efficiency by driver
- DVR frequency
- Route adherence
- Safety incidents
- Availability and utilization

**Transporter Performance Dashboard:**
- Transporter rankings
- Delivery success rate
- Cost comparison
- Variance frequency
- Invoice accuracy
- Response time metrics

**Exceptions Dashboard:**
- Open exceptions count
- Exception aging report
- Exception types distribution
- Resolution time average
- High-priority exceptions
- Exception trends

#### 5.2.2 Reports

**Standard Reports:**
- Daily shipment summary
- Weekly operational review
- Monthly performance report
- Quarterly cost analysis
- Annual executive summary
- Fuel consumption report
- DVR summary report
- Invoice reconciliation report
- Driver performance report
- Transporter scorecard

**Custom Report Builder:**
- Drag-and-drop field selection
- Multiple data sources
- Custom filters and grouping
- Calculated fields
- Scheduled report generation
- Email distribution lists
- Format options (PDF, Excel, CSV)

**Export Capabilities:**
- PDF with company branding
- Excel with formatted tables and charts
- CSV for further analysis
- API access for BI tools

**User Stories:**
- As an Operations Director, I need weekly executive summaries so I can brief leadership
- As a Finance Officer, I need monthly cost reports for budget variance analysis
- As a Logistics Manager, I want to create custom reports for specific operational questions

---

### 5.3 AI & Intelligence Features (Phase 9-10)

#### 5.3.1 Predictive Analytics

**Delay Prediction Engine:**
- Predicts shipment delays 2-4 hours in advance
- Confidence score for each prediction
- Contributing factors identified (traffic, weather, vehicle history, driver pattern)
- Recommended actions (reassign, notify customer, adjust route)
- Historical accuracy tracking

**Fuel Anomaly Detection:**
- Statistical anomaly detection (Z-score, IQR methods)
- Pattern recognition (time-based, route-based)
- Clustering analysis for outlier identification
- Alert severity levels (yellow, orange, red)
- Automatic investigation prompts
- Anomaly resolution tracking

**Route Optimization:**
- Best route recommendations based on historical data
- Traffic pattern analysis
- Fuel-efficient route suggestions
- Multi-stop optimization
- Real-time rerouting recommendations
- Cost-time tradeoff analysis

**Demand Forecasting:**
- Shipment volume prediction by route, customer, season
- Peak period identification
- Resource planning recommendations
- Capacity planning insights

#### 5.3.2 Scoring & Recommendation Engines

**Transporter Scoring Algorithm:**
- Weighted scoring across multiple dimensions
- Automatic score recalculation after each shipment
- Trend analysis (improving, declining, stable)
- Risk flagging for underperforming transporters
- Benchmark comparison

**Driver Performance Scoring:**
- Composite score from multiple metrics
- Fair evaluation considering external factors
- Improvement tracking over time
- Coaching recommendations

**Vehicle Efficiency Scoring:**
- Performance rating by vehicle
- Maintenance impact analysis
- Replacement/retirement recommendations
- ROI calculation for fleet upgrades

#### 5.3.3 AI Copilot & Conversational Analytics

**Natural Language Query Interface:**
- Plain English question processing
- Secure data access with RBAC enforcement
- Context-aware responses
- Follow-up question support
- Query history and favorites

**Example Queries:**
- "Show me all delayed shipments this week"
- "Which transporter has the highest variance rate?"
- "What was our average fuel cost last month?"
- "Compare driver performance between Q1 and Q2"
- "Which routes are most fuel-efficient?"
- "Summarize today's exceptions"
- "Show me vehicles due for maintenance"
- "What's causing the cost increase this month?"

**AI-Generated Insights:**
- Daily operational summaries
- Weekly trend reports
- Anomaly explanations in plain language
- Recommended actions with reasoning
- Executive briefings

**User Stories:**
- As a Logistics Manager, I can ask "Why are deliveries delayed this week?" and get an AI-generated analysis
- As an Operations Director, I receive AI summaries highlighting what requires my attention
- As a Finance Officer, I can ask questions about cost drivers in natural language

---

### 5.4 Mobile Driver App Features

**Core Capabilities:**
- Login with PIN or biometric
- View assigned trips for the day
- Trip details (customer, address, products, special instructions)
- Turn-by-turn navigation integration
- One-tap status updates
- Photo capture for proof-of-delivery
- Digital signature collection
- Offline mode for poor connectivity areas
- Push notifications for new assignments
- DVR creation on-the-go
- Fuel log entry
- Vehicle inspection checklist
- Emergency contact and SOS button
- Performance score visibility

**User Stories:**
- As a Driver, I can complete my entire workflow from my phone without paperwork
- As a Driver, I can work even when internet is spotty by syncing later
- As a Driver, I can capture proof immediately so there's no dispute later

---

### 5.5 Integration & API Features (Phase 12)

**ERP Integration:**
- Bidirectional sync with SAP, Oracle, Microsoft Dynamics
- Order import from ERP to create shipments automatically
- Delivery confirmation pushed back to ERP
- Cost data export for accounting
- Master data synchronization (customers, products)

**GPS/Telematics Integration:**
- Integration with GPS devices (CalAmp, Geotab, etc.)
- Real-time location updates
- Vehicle diagnostics data (engine hours, fault codes)
- Harsh braking and speeding alerts
- Route replay

**Map & Routing Services:**
- Google Maps Platform integration
- Here Maps as alternative
- Traffic data integration
- Geocoding and reverse geocoding
- Distance matrix calculations

**Communication Channels:**
- SMS gateway for alerts
- Email service integration
- WhatsApp Business API for customer notifications
- Push notification services

**Accounting System Integration:**
- QuickBooks integration
- Xero integration
- Invoice export
- Payment reconciliation

**Webhook & API Access:**
- RESTful API for all major resources
- Webhook support for real-time events
- API documentation (OpenAPI/Swagger)
- Rate limiting and quota management
- API key management

---

## 6. Technical Architecture

### 6.1 System Architecture

**Architecture Pattern:** Microservices with API Gateway

```
┌─────────────────────────────────────────────────────────┐
│                     Load Balancer                       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│                    API Gateway                          │
│            (Authentication, Rate Limiting)              │
└──┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬───┘
   │      │      │      │      │      │      │      │
   │      │      │      │      │      │      │      │
┌──▼──┐ ┌▼──┐ ┌─▼─┐ ┌─▼─┐ ┌─▼─┐ ┌─▼─┐ ┌─▼─┐ ┌▼──┐
│Auth │ │Fleet│ │Ship│ │Fuel│ │DVR│ │Bill│ │AI │ │Notif│
│Svc  │ │Svc  │ │Svc │ │Svc │ │Svc│ │Svc │ │Svc│ │Svc  │
└─┬───┘ └─┬──┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬──┘
  │       │      │     │     │     │     │     │
  └───────┴──────┴─────┴─────┴─────┴─────┴─────┘
                      │
          ┌───────────┴───────────┐
          │                       │
    ┌─────▼─────┐         ┌──────▼──────┐
    │ PostgreSQL│         │   Redis     │
    │ (Primary) │         │ (Cache/Queue)│
    └───────────┘         └─────────────┘
          │
    ┌─────▼─────┐         ┌──────────────┐
    │PostgreSQL │         │ Object Storage│
    │ (Replica) │         │   (S3/Azure) │
    └───────────┘         └──────────────┘
```

### 6.2 Technology Stack Details

**Frontend Web:**
- **Framework**: Next.js 14+ (React 18+, App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui components
- **State Management**: Zustand or React Query
- **Charts**: Recharts or Apache ECharts
- **Maps**: Google Maps JavaScript API with React wrapper
- **Forms**: React Hook Form + Zod validation
- **Data Tables**: TanStack Table
- **Real-time**: Socket.io client

**Mobile App:**
- **Framework**: Flutter 3.x
- **Language**: Dart
- **State Management**: Riverpod or BLoC
- **Local Storage**: Hive or SQLite
- **Maps**: Google Maps Flutter plugin
- **Camera**: Camera plugin for photo capture
- **Offline Sync**: Background sync with retry logic

**Backend:**
- **Framework**: FastAPI (Python 3.11+)
- **API Documentation**: Auto-generated OpenAPI/Swagger
- **Async Processing**: Celery with Redis broker
- **Task Scheduling**: Celery Beat
- **Real-time**: Socket.io server or WebSocket
- **Validation**: Pydantic models
- **ORM**: SQLAlchemy 2.0+
- **Migrations**: Alembic
- **Testing**: Pytest, httpx

**Database:**
- **Primary**: PostgreSQL 15+
  - Multi-tenant isolation via tenant_id
  - Row-level security for extra protection
  - JSONB for flexible document storage
  - PostGIS extension for geospatial queries
  - Full-text search with pg_trgm
- **Caching**: Redis 7+
  - Session storage
  - API rate limiting
  - Real-time data cache
  - Celery broker and result backend
- **Time-series (Optional)**: TimescaleDB for GPS breadcrumbs and metrics

**File Storage:**
- **Primary**: AWS S3 / Azure Blob / GCP Cloud Storage
- **CDN**: CloudFront / Azure CDN for image delivery
- **Structure**: Tenant-isolated buckets with versioning

**AI/ML Stack:**
- **Framework**: scikit-learn for classical ML, PyTorch for deep learning
- **LLM Integration**: OpenAI API / Anthropic Claude / Azure OpenAI
- **Vector Database**: Pinecone or Qdrant for semantic search
- **Feature Store**: Feast (optional, for production ML)
- **Experiment Tracking**: MLflow or Weights & Biases
- **Model Serving**: FastAPI endpoints with caching

**Infrastructure:**
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes (production) or Docker Swarm (smaller deployments)
- **CI/CD**: GitHub Actions or GitLab CI
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana) or Loki
- **Error Tracking**: Sentry
- **APM**: New Relic or DataDog

**Cloud Platform Options:**
1. **AWS**: ECS/EKS, RDS PostgreSQL, ElastiCache Redis, S3, CloudWatch
2. **Azure**: AKS, Azure Database for PostgreSQL, Azure Cache for Redis, Blob Storage
3. **GCP**: GKE, Cloud SQL, Memorystore, Cloud Storage

### 6.3 Data Flow Patterns

**1. Shipment Creation Flow:**
```
Web UI → API Gateway → Auth Check → Shipment Service →
PostgreSQL → Event Queue → Notification Service →
Driver Mobile App (Push Notification)
```

**2. Real-time Location Update:**
```
Driver App (GPS) → API → Validation → Redis Cache →
PostgreSQL (batch write) → WebSocket → Dashboard (live update)
```

**3. AI Prediction Flow:**
```
Scheduled Job → Fetch Recent Data → AI Service →
Run Model → Store Prediction → Check Thresholds →
Generate Alert → Notification Service → User
```

**4. Invoice Processing:**
```
Upload PDF → Object Storage → OCR Service → Extract Data →
Matching Engine → Flag Discrepancies → Store Results →
Notify Finance Team
```

---

## 7. Data Model & Schema Design

### 7.1 Core Tables

#### companies
```sql
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    industry VARCHAR(100),
    logo_url TEXT,
    primary_contact_email VARCHAR(255),
    primary_contact_phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    timezone VARCHAR(50) DEFAULT 'Africa/Lagos',
    subscription_tier VARCHAR(50) DEFAULT 'starter',
    subscription_status VARCHAR(50) DEFAULT 'trial',
    trial_ends_at TIMESTAMP,
    max_vehicles INTEGER DEFAULT 10,
    max_users INTEGER DEFAULT 5,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_companies_slug ON companies(slug);
CREATE INDEX idx_companies_subscription ON companies(subscription_tier, subscription_status);
```

#### users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    avatar_url TEXT,
    role_id UUID REFERENCES roles(id),
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    two_factor_secret VARCHAR(255),
    last_login_at TIMESTAMP,
    last_login_ip INET,
    password_changed_at TIMESTAMP DEFAULT NOW(),
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_company ON users(company_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role_id);
```

#### roles & permissions
```sql
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_system_role BOOLEAN DEFAULT FALSE,
    permissions JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource VARCHAR(100) NOT NULL, -- e.g., 'shipments', 'vehicles'
    action VARCHAR(50) NOT NULL, -- e.g., 'create', 'read', 'update', 'delete'
    description TEXT
);

-- Many-to-many relationship
CREATE TABLE role_permissions (
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    permission_id UUID REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);
```

#### vehicles
```sql
CREATE TABLE vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    vehicle_number VARCHAR(50) NOT NULL,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    vin VARCHAR(50),
    make VARCHAR(100),
    model VARCHAR(100),
    year INTEGER,
    vehicle_type VARCHAR(50), -- truck, van, motorcycle, etc.
    ownership_type VARCHAR(50), -- owned, leased, contracted
    capacity_weight_kg DECIMAL(10,2),
    capacity_volume_m3 DECIMAL(10,2),
    fuel_type VARCHAR(50), -- diesel, petrol, electric, hybrid
    tank_capacity_liters DECIMAL(10,2),
    insurance_policy_number VARCHAR(100),
    insurance_expiry_date DATE,
    registration_expiry_date DATE,
    gps_device_id VARCHAR(100),
    status VARCHAR(50) DEFAULT 'active', -- active, maintenance, retired
    current_odometer_km DECIMAL(10,2) DEFAULT 0,
    last_maintenance_date DATE,
    next_maintenance_due_date DATE,
    photos JSONB DEFAULT '[]',
    documents JSONB DEFAULT '[]',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_vehicles_company ON vehicles(company_id);
CREATE INDEX idx_vehicles_license_plate ON vehicles(license_plate);
CREATE INDEX idx_vehicles_status ON vehicles(status);
```

#### drivers
```sql
CREATE TABLE drivers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    driver_code VARCHAR(50) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    license_number VARCHAR(50) UNIQUE NOT NULL,
    license_type VARCHAR(50),
    license_expiry_date DATE,
    date_of_birth DATE,
    national_id VARCHAR(50),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    emergency_contact_name VARCHAR(200),
    emergency_contact_phone VARCHAR(20),
    hire_date DATE,
    status VARCHAR(50) DEFAULT 'active', -- active, on_leave, suspended, terminated
    rating DECIMAL(3,2) DEFAULT 5.00,
    total_deliveries INTEGER DEFAULT 0,
    on_time_deliveries INTEGER DEFAULT 0,
    photo_url TEXT,
    documents JSONB DEFAULT '[]',
    training_records JSONB DEFAULT '[]',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_drivers_company ON drivers(company_id);
CREATE INDEX idx_drivers_license ON drivers(license_number);
CREATE INDEX idx_drivers_status ON drivers(status);
```

#### shipments
```sql
CREATE TABLE shipments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    shipment_number VARCHAR(50) UNIQUE NOT NULL,
    customer_reference VARCHAR(100),
    customer_name VARCHAR(255) NOT NULL,
    customer_phone VARCHAR(20),
    customer_email VARCHAR(255),
    
    -- Pickup details
    pickup_address TEXT NOT NULL,
    pickup_lat DECIMAL(10,8),
    pickup_lng DECIMAL(11,8),
    pickup_city VARCHAR(100),
    pickup_state VARCHAR(100),
    scheduled_pickup_time TIMESTAMP,
    actual_pickup_time TIMESTAMP,
    
    -- Delivery details
    delivery_address TEXT NOT NULL,
    delivery_lat DECIMAL(10,8),
    delivery_lng DECIMAL(11,8),
    delivery_city VARCHAR(100),
    delivery_state VARCHAR(100),
    scheduled_delivery_time TIMESTAMP,
    estimated_delivery_time TIMESTAMP,
    actual_delivery_time TIMESTAMP,
    
    -- Assignment
    vehicle_id UUID REFERENCES vehicles(id),
    driver_id UUID REFERENCES drivers(id),
    transporter_id UUID REFERENCES transporters(id),
    
    -- Cargo details
    cargo_description TEXT,
    cargo_items JSONB DEFAULT '[]', -- [{sku, name, quantity, weight, volume}]
    total_weight_kg DECIMAL(10,2),
    total_volume_m3 DECIMAL(10,2),
    total_value DECIMAL(12,2),
    
    -- Operational
    priority VARCHAR(50) DEFAULT 'standard', -- standard, high, urgent, critical
    status VARCHAR(50) DEFAULT 'draft',
    status_updated_at TIMESTAMP DEFAULT NOW(),
    status_updated_by UUID REFERENCES users(id),
    distance_km DECIMAL(10,2),
    planned_route JSONB,
    actual_route JSONB,
    
    -- Costs
    estimated_cost DECIMAL(12,2),
    actual_cost DECIMAL(12,2),
    fuel_cost DECIMAL(12,2),
    
    -- Tracking
    current_lat DECIMAL(10,8),
    current_lng DECIMAL(11,8),
    last_location_update TIMESTAMP,
    
    -- Flags
    is_multi_drop BOOLEAN DEFAULT FALSE,
    has_variance BOOLEAN DEFAULT FALSE,
    has_delay BOOLEAN DEFAULT FALSE,
    delay_reason TEXT,
    
    -- Documents
    special_instructions TEXT,
    proof_of_delivery_url TEXT,
    delivery_signature_url TEXT,
    delivery_photos JSONB DEFAULT '[]',
    delivery_notes TEXT,
    
    -- Metadata
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_shipments_company ON shipments(company_id);
CREATE INDEX idx_shipments_number ON shipments(shipment_number);
CREATE INDEX idx_shipments_status ON shipments(status);
CREATE INDEX idx_shipments_vehicle ON shipments(vehicle_id);
CREATE INDEX idx_shipments_driver ON shipments(driver_id);
CREATE INDEX idx_shipments_delivery_date ON shipments(scheduled_delivery_time);
CREATE INDEX idx_shipments_location ON shipments USING GIST (ll_to_earth(current_lat, current_lng));
```

### 7.2 Supporting Tables

#### shipment_status_logs
```sql
CREATE TABLE shipment_status_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shipment_id UUID NOT NULL REFERENCES shipments(id) ON DELETE CASCADE,
    from_status VARCHAR(50),
    to_status VARCHAR(50) NOT NULL,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    notes TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_status_logs_shipment ON shipment_status_logs(shipment_id, created_at DESC);
```

#### delivery_variance_reports
```sql
CREATE TABLE delivery_variance_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    shipment_id UUID NOT NULL REFERENCES shipments(id) ON DELETE CASCADE,
    dvr_number VARCHAR(50) UNIQUE NOT NULL,
    variance_type VARCHAR(50) NOT NULL, -- short, over, damaged, late, wrong_destination, etc.
    severity VARCHAR(50) DEFAULT 'moderate', -- minor, moderate, major, critical
    
    reported_quantity DECIMAL(10,2),
    expected_quantity DECIMAL(10,2),
    variance_quantity DECIMAL(10,2),
    
    description TEXT NOT NULL,
    root_cause TEXT,
    fault_assignment VARCHAR(100), -- driver, transporter, customer, warehouse, force_majeure
    
    -- Evidence
    evidence_photos JSONB DEFAULT '[]',
    customer_acknowledgment_url TEXT,
    supporting_documents JSONB DEFAULT '[]',
    
    -- Financial impact
    financial_impact DECIMAL(12,2),
    adjustment_amount DECIMAL(12,2),
    
    -- Workflow
    status VARCHAR(50) DEFAULT 'open', -- open, under_review, approved, rejected, closed
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMP,
    review_notes TEXT,
    resolution TEXT,
    resolution_date TIMESTAMP,
    
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_dvr_company ON delivery_variance_reports(company_id);
CREATE INDEX idx_dvr_shipment ON delivery_variance_reports(shipment_id);
CREATE INDEX idx_dvr_status ON delivery_variance_reports(status);
```

#### fuel_issuance_logs
```sql
CREATE TABLE fuel_issuance_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    vehicle_id UUID NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    shipment_id UUID REFERENCES shipments(id) ON DELETE SET NULL,
    driver_id UUID REFERENCES drivers(id) ON DELETE SET NULL,
    
    issuance_date TIMESTAMP NOT NULL DEFAULT NOW(),
    fuel_station VARCHAR(255),
    quantity_liters DECIMAL(10,2) NOT NULL,
    price_per_liter DECIMAL(10,2) NOT NULL,
    total_cost DECIMAL(12,2) NOT NULL,
    
    odometer_reading_km DECIMAL(10,2),
    previous_odometer_km DECIMAL(10,2),
    distance_since_last_fill DECIMAL(10,2),
    fuel_efficiency_kmpl DECIMAL(5,2),
    
    payment_method VARCHAR(50), -- cash, card, fuel_card, credit
    receipt_number VARCHAR(100),
    receipt_photo_url TEXT,
    attendant_name VARCHAR(200),
    
    is_anomaly BOOLEAN DEFAULT FALSE,
    anomaly_reason TEXT,
    anomaly_flagged_at TIMESTAMP,
    anomaly_resolved BOOLEAN DEFAULT FALSE,
    
    notes TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_fuel_logs_company ON fuel_issuance_logs(company_id);
CREATE INDEX idx_fuel_logs_vehicle ON fuel_issuance_logs(vehicle_id);
CREATE INDEX idx_fuel_logs_date ON fuel_issuance_logs(issuance_date DESC);
CREATE INDEX idx_fuel_logs_anomaly ON fuel_issuance_logs(is_anomaly) WHERE is_anomaly = TRUE;
```

#### fuel_price_history
```sql
CREATE TABLE fuel_price_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    region VARCHAR(100) NOT NULL,
    fuel_type VARCHAR(50) DEFAULT 'diesel',
    price_per_liter DECIMAL(10,2) NOT NULL,
    effective_date DATE NOT NULL,
    source VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_fuel_prices_region_date ON fuel_price_history(region, effective_date DESC);
```

#### transporters
```sql
CREATE TABLE transporters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    contact_person VARCHAR(200),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    registration_number VARCHAR(100),
    tax_id VARCHAR(100),
    
    contract_start_date DATE,
    contract_end_date DATE,
    payment_terms VARCHAR(100),
    rate_agreement JSONB DEFAULT '{}',
    
    performance_score DECIMAL(3,2) DEFAULT 5.00,
    total_shipments INTEGER DEFAULT 0,
    on_time_deliveries INTEGER DEFAULT 0,
    variance_count INTEGER DEFAULT 0,
    
    insurance_details JSONB DEFAULT '{}',
    compliance_docs JSONB DEFAULT '[]',
    
    status VARCHAR(50) DEFAULT 'active',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_transporters_company ON transporters(company_id);
```

#### invoices
```sql
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    transporter_id UUID REFERENCES transporters(id) ON DELETE SET NULL,
    invoice_number VARCHAR(100) NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE,
    period_start DATE,
    period_end DATE,
    
    subtotal DECIMAL(12,2) DEFAULT 0,
    tax_amount DECIMAL(12,2) DEFAULT 0,
    total_amount DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'NGN',
    
    status VARCHAR(50) DEFAULT 'pending', -- pending, approved, disputed, paid
    payment_date DATE,
    payment_reference VARCHAR(100),
    
    invoice_file_url TEXT,
    line_items JSONB DEFAULT '[]',
    
    auto_matched_count INTEGER DEFAULT 0,
    discrepancy_count INTEGER DEFAULT 0,
    discrepancy_total DECIMAL(12,2) DEFAULT 0,
    
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMP,
    review_notes TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    CONSTRAINT unique_company_invoice UNIQUE(company_id, invoice_number)
);

CREATE INDEX idx_invoices_company ON invoices(company_id);
CREATE INDEX idx_invoices_transporter ON invoices(transporter_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_date ON invoices(invoice_date DESC);
```

#### invoice_line_items
```sql
CREATE TABLE invoice_line_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    shipment_id UUID REFERENCES shipments(id) ON DELETE SET NULL,
    
    line_number INTEGER NOT NULL,
    description TEXT,
    shipment_reference VARCHAR(100),
    route VARCHAR(255),
    quantity DECIMAL(10,2),
    unit_price DECIMAL(12,2),
    amount DECIMAL(12,2) NOT NULL,
    
    matched_shipment_id UUID REFERENCES shipments(id),
    is_matched BOOLEAN DEFAULT FALSE,
    has_discrepancy BOOLEAN DEFAULT FALSE,
    discrepancy_type VARCHAR(100),
    discrepancy_amount DECIMAL(12,2),
    discrepancy_notes TEXT,
    
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_invoice_items_invoice ON invoice_line_items(invoice_id);
CREATE INDEX idx_invoice_items_shipment ON invoice_line_items(shipment_id);
```

---

### 7.3 AI & Analytics Tables

#### ai_predictions
```sql
CREATE TABLE ai_predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    prediction_type VARCHAR(50) NOT NULL, -- delay, fuel_anomaly, cost_overrun
    related_entity_type VARCHAR(50), -- shipment, vehicle, driver
    related_entity_id UUID,
    
    prediction_value JSONB NOT NULL,
    confidence_score DECIMAL(5,4),
    contributing_factors JSONB DEFAULT '[]',
    recommended_actions JSONB DEFAULT '[]',
    
    status VARCHAR(50) DEFAULT 'active', -- active, acknowledged, resolved, false_positive
    actual_outcome JSONB,
    was_accurate BOOLEAN,
    
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

CREATE INDEX idx_predictions_company ON ai_predictions(company_id);
CREATE INDEX idx_predictions_type ON ai_predictions(prediction_type, status);
CREATE INDEX idx_predictions_entity ON ai_predictions(related_entity_type, related_entity_id);
```

#### alerts
```sql
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(50) NOT NULL, -- info, warning, critical
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    
    related_entity_type VARCHAR(50),
    related_entity_id UUID,
    
    status VARCHAR(50) DEFAULT 'active', -- active, acknowledged, resolved, dismissed
    acknowledged_by UUID REFERENCES users(id),
    acknowledged_at TIMESTAMP,
    resolved_at TIMESTAMP,
    resolution_notes TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

CREATE INDEX idx_alerts_company ON alerts(company_id);
CREATE INDEX idx_alerts_status ON alerts(status, severity);
CREATE INDEX idx_alerts_created ON alerts(created_at DESC);
```

#### audit_logs
```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    
    action VARCHAR(100) NOT NULL, -- login, logout, create, update, delete, approve, etc.
    resource_type VARCHAR(100) NOT NULL,
    resource_id UUID,
    
    changes JSONB, -- {field: {old: value, new: value}}
    ip_address INET,
    user_agent TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_company ON audit_logs(company_id, created_at DESC);
CREATE INDEX idx_audit_user ON audit_logs(user_id, created_at DESC);
CREATE INDEX idx_audit_resource ON audit_logs(resource_type, resource_id);
```

---

## 8. Business Logic & Workflow Rules

### 8.1 Shipment Lifecycle Rules

**State Transitions:**
```
Draft → Scheduled → Assigned → Dispatched → En Route to Pickup →
At Pickup → Loaded → In Transit → At Delivery → Delivered → Closed

Exception states can occur at any point:
- Delayed (can return to In Transit)
- Exception (requires resolution before proceeding)
```

**Business Rules:**
1. A shipment cannot be dispatched without both vehicle and driver assigned
2. Status can only move forward except for exception states
3. Actual pickup time must be recorded before moving to "Loaded"
4. Proof-of-delivery (photo or signature) required to mark "Delivered"
5. Automatic status change to "Delayed" if ETA exceeded by 30 minutes
6. Automatic status change to "Exception" if no location update for 2 hours while "In Transit"
7. DVR creation automatically flags `has_variance = TRUE`
8. Closing a shipment requires resolution of all associated DVRs

### 8.2 Fuel Anomaly Detection Rules

**Anomaly Triggers:**
1. **Efficiency Drop**: Fuel efficiency drops >30% below vehicle's 30-day average
2. **Excessive Fill**: Fill amount exceeds 110% of tank capacity
3. **Frequency Anomaly**: More than 2 fills in a 24-hour period
4. **Distance Anomaly**: Distance since last fill <50km but full tank refill
5. **Cost Spike**: Price per liter >15% above regional average for that week
6. **Pattern Break**: Fill on non-working day or unusual location

**Anomaly Resolution Process:**
1. System auto-flags anomaly
2. Fleet supervisor receives alert
3. Investigation notes added
4. Resolution actions: (a) Confirmed legitimate, (b) Driver training required, (c) Vehicle maintenance needed, (d) Suspected theft - escalate
5. Anomaly marked resolved with outcome recorded

### 8.3 Invoice Matching Logic

**Auto-Matching Algorithm:**
```
FOR EACH invoice_line_item:
    1. Extract shipment_reference from line description
    2. Query shipments table for matching shipment_number OR customer_reference
    3. IF single match found:
        - Compare quantity (if applicable)
        - Compare rate against contracted rate
        - Calculate expected cost vs invoiced amount
        - IF variance < 5%: mark matched, no discrepancy
        - ELSE: mark matched but flag discrepancy
    4. IF multiple matches OR no match:
        - Mark unmatched, flag for manual review
    5. IF rate variance > contracted rate + 10%:
        - Flag as "extra_charge" discrepancy
```

**Discrepancy Types:**
- `quantity_mismatch`: Invoiced quantity ≠ delivered quantity
- `rate_variance`: Invoiced rate > agreed rate
- `extra_charge`: Charge not in original quote
- `unmatched_shipment`: Cannot link to any shipment
- `duplicate`: Same shipment charged multiple times

### 8.4 Driver Performance Scoring

**Composite Score Calculation:**
```
Performance Score = (
    on_time_delivery_rate * 0.35 +
    fuel_efficiency_percentile * 0.25 +
    variance_free_rate * 0.20 +
    route_adherence_rate * 0.10 +
    customer_feedback_score * 0.10
) * 100

WHERE:
- on_time_delivery_rate = (on-time deliveries / total deliveries)
- fuel_efficiency_percentile = (driver_efficiency / fleet_avg_efficiency)
- variance_free_rate = ((total_deliveries - DVR_count) / total_deliveries)
- route_adherence_rate = (trips_with_<10%_deviation / total_trips)
- customer_feedback_score = avg(customer_ratings) / 5.0
```

**Score Ranges:**
- 90-100: Excellent
- 75-89: Good
- 60-74: Fair
- Below 60: Needs Improvement

### 8.5 Transporter Performance Scoring

**Weighted Scorecard:**
```
Transporter Score = (
    on_time_delivery_rate * 0.30 +
    variance_rate_inverse * 0.25 +
    invoice_accuracy * 0.20 +
    response_time_score * 0.15 +
    cost_competitiveness * 0.10
) * 100

WHERE:
- variance_rate_inverse = (1 - (DVR_count / shipments_count))
- invoice_accuracy = (1 - (disputed_invoices / total_invoices))
- response_time_score = (1 - avg_hours_to_respond / 48) capped at 1.0
- cost_competitiveness = (fleet_avg_cost_per_km / transporter_cost_per_km) capped at 1.2
```

---

## 9. AI/ML Strategy & Implementation

### 9.1 AI Use Cases & Priority

**Phase 9 (Core AI):**
1. **Delay Prediction** (Priority 1)
2. **Fuel Anomaly Detection** (Priority 2)
3. **Transporter Scoring** (Priority 3)
4. **Route Optimization Suggestions** (Priority 4)

**Phase 10 (Advanced AI):**
5. **Natural Language Query Interface** (Priority 1)
6. **Automated Executive Summaries** (Priority 2)
7. **Demand Forecasting** (Priority 3)

### 9.2 Delay Prediction Model

**Model Type:** Gradient Boosting (XGBoost or LightGBM)

**Features:**
- **Shipment Features**: Distance, cargo weight, priority, time of day, day of week
- **Vehicle Features**: Age, maintenance status, recent performance
- **Driver Features**: Historical on-time rate, experience, recent performance
- **Route Features**: Historical avg delivery time, traffic patterns
- **Weather Features**: Current/forecast weather conditions
- **Time Features**: Hour of day, day of week, month, holiday indicator
- **Historical Features**: Same route avg delay, same driver avg delay

**Target Variable:** Binary (delayed: yes/no) + Continuous (delay minutes)

**Training Data:** Historical shipments (min 6 months, 1000+ records)

**Prediction Timing:** Run prediction when shipment status = "In Transit", re-run every 30 mins

**Output:**
```json
{
  "shipment_id": "uuid",
  "will_delay": true,
  "confidence": 0.87,
  "predicted_delay_minutes": 45,
  "current_eta": "2026-04-16T15:30:00Z",
  "adjusted_eta": "2026-04-16T16:15:00Z",
  "contributing_factors": [
    {"factor": "driver_avg_delay", "importance": 0.35},
    {"factor": "traffic_on_route", "importance": 0.28},
    {"factor": "vehicle_age", "importance": 0.15}
  ],
  "recommended_actions": [
    "Notify customer of potential delay",
    "Consider reassigning to faster driver if available",
    "Monitor closely for next 30 minutes"
  ]
}
```

**Model Retraining:** Weekly with last 90 days of data

### 9.3 Fuel Anomaly Detection Model

**Model Type:** Isolation Forest (unsupervised anomaly detection)

**Features:**
- Fuel efficiency (km/liter)
- Fill frequency (days since last fill)
- Fill amount (% of tank capacity)
- Price paid vs regional average
- Distance since last fill
- Time of day
- Location deviation from usual stations
- Driver behavior patterns

**Training:** Historical fuel logs (min 3 months per vehicle)

**Prediction:** Real-time on fuel log entry

**Output:**
```json
{
  "is_anomaly": true,
  "anomaly_score": 0.72,
  "severity": "high",
  "reasons": [
    "Fuel efficiency 45% below vehicle average",
    "Fill amount exceeds tank capacity by 15%",
    "Location 50km from usual fuel stations"
  ],
  "recommended_action": "Flag for immediate investigation - possible fuel theft or data entry error"
}
```

### 9.4 Natural Language Query System

**Architecture:**
```
User Question → Intent Classification → Entity Extraction →
Query Generation → SQL Execution → Result Formatting →
Natural Language Response
```

**Intent Classification:**
- Shipment queries
- Fuel queries
- Cost/financial queries
- Performance queries
- Trend analysis
- Comparison queries

**Implementation Options:**
1. **LLM-based** (Recommended): Use OpenAI GPT-4 or Anthropic Claude with function calling
2. **Hybrid**: Intent classifier (fine-tuned BERT) + LLM for response generation

**Security Guardrails:**
- SQL injection prevention (parameterized queries only)
- Row-level security (filter by company_id automatically)
- Role-based filtering (respect user permissions)
- Query timeout limits
- Result set size limits
- No DDL queries allowed

**Example Implementation (Pseudo-code):**
```python
def handle_nl_query(user_question: str, user: User):
    # Step 1: Classify intent and extract entities
    intent = classify_intent(user_question)
    entities = extract_entities(user_question)
    
    # Step 2: Generate safe SQL query
    query_template = get_query_template(intent)
    sql_query = query_template.format(
        company_id=user.company_id,
        **entities
    )
    
    # Step 3: Execute with safety checks
    validate_query_safety(sql_query)
    results = execute_query(sql_query, timeout=30)
    
    # Step 4: Format response
    if len(results) == 0:
        return "No results found for your query."
    
    # Step 5: Generate natural language summary
    summary = llm.generate(f"""
        User asked: {user_question}
        Query results: {results}
        
        Provide a concise, helpful answer in 2-3 sentences.
    """)
    
    return {
        "answer": summary,
        "data": results,
        "visualization": suggest_chart_type(results)
    }
```

---

## 10. Security & Compliance Framework

### 10.1 Security Architecture

**Defense in Depth Layers:**
1. **Network Layer**: TLS 1.3 encryption, DDoS protection, WAF
2. **Authentication Layer**: JWT with short expiry, refresh tokens, 2FA
3. **Authorization Layer**: RBAC with tenant isolation
4. **Application Layer**: Input validation, output encoding, CSRF protection
5. **Data Layer**: Encryption at rest, row-level security, audit logging
6. **Infrastructure Layer**: Security groups, private subnets, bastion hosts

### 10.2 Data Security

**Encryption:**
- **In Transit**: TLS 1.3 for all API calls
- **At Rest**: AES-256 encryption for database and object storage
- **PII Fields**: Additional field-level encryption for sensitive data (license numbers, national IDs)

**Data Classification:**
| Data Type | Sensitivity | Storage | Retention |
|-----------|-------------|---------|-----------|
| User credentials | Critical | Encrypted DB | Account lifetime |
| Financial data | High | Encrypted DB | 7 years |
| GPS locations | Medium | DB | 2 years |
| Photos/POD | Medium | Object storage | 3 years |
| Audit logs | High | Immutable store | 10 years |
| Analytics aggregates | Low | Data warehouse | 5 years |

### 10.3 Access Control

**Role-Permission Matrix:**

| Role | Shipments | Fleet | Fuel | DVR | Invoices | Reports | Users | AI |
|------|-----------|-------|------|-----|----------|---------|-------|-----|
| Super Admin | Full | Full | Full | Full | Full | Full | Full | Full |
| Company Admin | Full | Full | Full | Full | Full | Full | Manage | View |
| Transport Admin | Full | Full | Full | View | Full | View | View | View |
| Logistics Mgr | Full | View | View | Full | View | View | - | View |
| Finance Officer | View | View | View | View | Full | View | - | View |
| Driver | Assigned | - | Log | Create | - | Own | - | - |
| Auditor | Read | Read | Read | Read | Read | Full | - | Read |

### 10.4 Compliance Requirements

**NDPR (Nigeria Data Protection Regulation):**
- Data processing lawful basis documented
- User consent for data collection
- Right to access personal data
- Right to deletion (with business justification exceptions)
- Data breach notification within 72 hours

**GDPR (For UK operations):**
- All NDPR requirements plus:
- Data Protection Officer appointed
- Privacy Impact Assessments for high-risk processing
- Data portability in machine-readable format
- Stricter consent requirements

**Industry Standards:**
- ISO 27001 readiness (Information Security Management)
- SOC 2 Type II (for enterprise clients)

### 10.5 Audit & Monitoring

**Audit Log Requirements:**
- All authentication events
- Data access (who viewed what, when)
- Data modifications (what changed, by whom)
- Permission changes
- Configuration changes
- Failed access attempts
- API calls (for integration audit trail)

**Monitoring:**
- Real-time security event monitoring (SIEM)
- Anomalous access pattern detection
- Failed login threshold alerts
- Data exfiltration prevention
- API rate limiting and abuse detection

---

## 11. Phased Implementation Roadmap

### Phase 0: Foundation (Weeks 1-2)

**Deliverables:**
- ✅ Finalized product requirements document (this document)
- ✅ Technical architecture decision record
- ✅ Development environment setup
- ✅ CI/CD pipeline skeleton
- ✅ Project management setup (Jira/Linear)
- ✅ Team role assignments

**Build Prompts:**
- "Set up a complete development environment for a multi-tenant logistics SaaS platform using FastAPI, PostgreSQL, Redis, Next.js, and Flutter. Include Docker Compose for local dev, linting, formatting, and pre-commit hooks."

---

### Phase 1: Design System (Weeks 3-4)

**Deliverables:**
- Design tokens (colors, typography, spacing)
- Component library (buttons, inputs, cards, tables, charts)
- Dashboard layouts (desktop + mobile responsive)
- Navigation patterns
- Empty states and loading states
- Icon set
- Brand guidelines

**Key Screens:**
- Login/Signup flow
- Dashboard home
- Shipment list view
- Shipment detail page
- Live map view
- Fuel monitoring page
- Invoice review page
- Settings page
- Mobile driver app (5 core screens)

**Build Prompts:**
- "Design a complete UI/UX system for an enterprise logistics SaaS platform. Create a design system with tokens, component library, dashboard layouts, and key screen mockups. The design should be modern, data-dense but scannable, with clear hierarchy and excellent mobile responsiveness."

---

### Phase 2: Authentication & Tenancy (Weeks 5-7)

**Deliverables:**
- User registration and email verification
- Login with JWT auth
- Password reset flow
- Role-based access control
- Company onboarding
- User invitation system
- Session management
- 2FA (basic setup)
- Audit logging for auth events

**Build Prompts:**
- "Implement secure authentication and multi-tenant architecture for a logistics platform. Include user registration, email verification, JWT auth with refresh tokens, password reset, RBAC, company onboarding, user invitations, session management, and audit logging. Use FastAPI, PostgreSQL, Redis."

**Acceptance Tests:**
- User can register and verify email
- User can log in and receive JWT
- Password reset works end-to-end
- Company admin can invite users with roles
- Users only see their company's data
- Audit logs capture all auth events

---

### Phase 3: Core Data Model (Weeks 8-10)

**Deliverables:**
- Database schema (all tables)
- CRUD APIs for core entities (companies, users, vehicles, drivers, transporters)
- Validation rules
- Error handling
- API documentation (Swagger)
- Database migrations
- Seed data for development

**Build Prompts:**
- "Build the complete database schema and CRUD API layer for a logistics platform. Include companies, users, roles, vehicles, drivers, transporters, shipments (structure only), fuel logs (structure), and audit logs. Use PostgreSQL with proper constraints, indexes, and relationships. Implement FastAPI CRUD endpoints with validation, error handling, and OpenAPI docs."

**Acceptance Tests:**
- All CRUD operations work for core entities
- Relational constraints enforced
- Validation prevents bad data
- API docs are complete and accurate

---

### Phase 4: Shipment Management (Weeks 11-14)

**Deliverables:**
- Shipment creation form (web + mobile)
- Vehicle/driver assignment
- Status update workflows
- Shipment list with filters and search
- Shipment detail view
- Status timeline
- Proof-of-delivery capture
- Basic GPS location logging
- Live map view (simple)
- Notifications for status changes

**Build Prompts:**
- "Implement complete shipment management for a logistics platform. Include shipment creation with validation, vehicle/driver assignment, 13-state status lifecycle, status logging, proof-of-delivery capture, GPS location updates, shipment list with filters, detail view with timeline, live map, and status change notifications. Backend: FastAPI. Frontend: Next.js. Mobile: Flutter."

**Acceptance Tests:**
- Shipment can be created and assigned
- Status transitions follow lifecycle rules
- Timeline shows all status changes
- POD can be captured (photo + signature)
- Live map shows active shipments
- Notifications work

---

### Phase 5: Fuel Management (Weeks 15-17)

**Deliverables:**
- Fuel issuance form (web + mobile)
- Fuel log history
- Weekly fuel price tracking
- Fuel consumption calculation
- Fuel efficiency dashboard
- Basic anomaly detection (rule-based)
- Anomaly alerts
- Fuel cost summaries

**Build Prompts:**
- "Build fuel monitoring module for logistics platform. Include fuel issuance logging, weekly price tracking, automated fuel efficiency calculation, consumption summaries by vehicle/driver/route, rule-based anomaly detection (efficiency drops, excessive fills, frequency anomalies), alert system, and fuel dashboard. Backend: FastAPI. Frontend: Next.js with charts."

**Acceptance Tests:**
- Fuel can be logged with all details
- Efficiency is calculated correctly
- Anomalies are detected and flagged
- Alerts are sent for anomalies
- Dashboard shows fuel metrics

---

### Phase 6: DVR & Reconciliation (Weeks 18-20)

**Deliverables:**
- DVR creation form
- Photo evidence upload
- Variance categorization
- DVR workflow (create → review → resolve)
- DVR list and detail views
- Resolution tracking
- Financial impact recording
- Memo generation

**Build Prompts:**
- "Implement delivery variance report (DVR) system for logistics platform. Include DVR creation with categories, multi-photo upload, fault assignment, severity rating, approval workflow, resolution tracking, financial impact assessment, and memo generation. Support both web and mobile creation."

**Acceptance Tests:**
- DVRs can be created with evidence
- Workflow moves through states correctly
- Approvals/rejections are recorded
- Financial adjustments link to DVRs
- Memos can be generated

---

### Phase 7: Invoice Management (Weeks 21-24)

**Deliverables:**
- Invoice upload and manual entry
- AI-powered OCR for invoice extraction
- Line item parsing
- Auto-matching algorithm
- Discrepancy detection
- Invoice review interface
- Approval workflow
- Dispute memo generation
- Payment status tracking

**Build Prompts:**
- "Build invoice and transport cost automation module. Include invoice upload with OCR extraction, line item parsing, auto-matching to shipment records, discrepancy detection (quantity, rate, extra charges), review interface, approval workflow, dispute memo generation, and payment tracking. Use OCR library or API for extraction."

**Acceptance Tests:**
- Invoices can be uploaded and extracted
- Line items match automatically where possible
- Discrepancies are flagged correctly
- Approval workflow functions
- Memos can be generated

---

### Phase 8: Analytics Dashboard (Weeks 25-28)

**Deliverables:**
- Shipment KPI dashboard
- Fleet utilization dashboard
- Fuel cost dashboard
- Driver performance dashboard
- Transporter scorecard
- Exception dashboard
- Filters by date, vehicle, driver, route
- Export to PDF and Excel
- Scheduled report generation

**Build Prompts:**
- "Create comprehensive analytics and reporting module for logistics platform. Build operational dashboards showing shipment KPIs, fleet utilization, fuel costs, driver performance, transporter scores, and exceptions. Include date range filters, drill-downs, charts (line, bar, pie), and export to PDF/Excel. Use React with Recharts or ECharts. Backend generates report data."

**Acceptance Tests:**
- All dashboards display accurate data
- Filters work correctly
- Charts render properly
- Exports work in PDF and Excel
- Performance is acceptable (<3 sec load)

---

### Phase 9: AI Insight Engine (Weeks 29-34)

**Deliverables:**
- Delay prediction model (trained and deployed)
- Fuel anomaly detection model
- Transporter performance scoring
- Route optimization suggestions
- AI insights dashboard
- Prediction accuracy tracking
- Model retraining pipeline

**Build Prompts:**
- "Develop AI insight engine for logistics platform. Build delay prediction model (XGBoost), fuel anomaly detection (Isolation Forest), transporter scoring algorithm, and route optimization logic. Include model training pipelines, inference APIs, accuracy tracking, and retraining automation. Deploy using FastAPI endpoints. Store predictions in database."

**Acceptance Tests:**
- Delay predictions run automatically
- Fuel anomalies are detected accurately
- Transporter scores calculate correctly
- Recommendations are actionable
- Model performance is tracked

---

### Phase 10: AI Copilot (Weeks 35-38)

**Deliverables:**
- Natural language query interface
- Intent classification
- Entity extraction
- Safe SQL generation
- LLM integration for responses
- Chat history
- Conversational context
- Access control enforcement

**Build Prompts:**
- "Build AI copilot for logistics platform. Create natural language query interface that lets users ask questions about shipments, fuel, costs, and performance. Use LLM (OpenAI or Anthropic) with function calling to generate safe SQL queries. Enforce row-level security and RBAC. Include chat interface, history, and conversational context. Frontend: React chat component."

**Acceptance Tests:**
- Users can ask questions in plain English
- Queries return accurate results
- SQL injection is prevented
- RBAC is enforced
- Responses are helpful and concise

---

### Phase 11: Notifications (Weeks 39-40)

**Deliverables:**
- Email notification service
- SMS gateway integration
- Push notifications (mobile)
- In-app notification center
- Notification preferences
- Alert escalation rules
- Notification history

**Build Prompts:**
- "Implement comprehensive notification system for logistics platform. Support email, SMS, push notifications, and in-app alerts. Include notification preferences, alert escalation for unresolved issues, notification center UI, and history. Use Celery for async sending. Integrate with SendGrid/Twilio/FCM."

**Acceptance Tests:**
- Notifications sent via multiple channels
- Users can configure preferences
- Escalations work correctly
- Notification center displays all alerts

---

### Phase 12: Integrations (Weeks 41-44)

**Deliverables:**
- ERP sync framework
- GPS device integration
- Map services integration
- Webhook system
- Import/export tools
- API documentation for partners
- Integration marketplace (basic)

**Build Prompts:**
- "Build integration layer for logistics platform. Create framework for ERP sync (SAP, Dynamics), GPS device integration (CalAmp, Geotab), map services (Google Maps), webhooks for real-time events, and import/export tools. Provide REST API with authentication for partners. Document all endpoints in OpenAPI."

**Acceptance Tests:**
- ERP sync works bidirectionally
- GPS devices push location data
- Maps display correctly
- Webhooks fire reliably
- API docs are comprehensive

---

### Phase 13: Security Hardening (Weeks 45-46)

**Deliverables:**
- Penetration testing
- Security audit
- Encryption audit
- Backup/restore testing
- Disaster recovery plan
- Compliance documentation
- Security training materials

**Build Prompts:**
- "Perform security hardening for logistics SaaS platform. Implement comprehensive security audit, penetration testing, encryption verification, backup/restore procedures, disaster recovery plan, and compliance documentation (NDPR, GDPR). Provide security training materials for team and end-users."

**Acceptance Tests:**
- Penetration test finds no critical issues
- Backups can be restored successfully
- Disaster recovery is tested
- Compliance requirements documented

---

### Phase 14: Testing (Weeks 47-48)

**Deliverables:**
- Unit test coverage (>80%)
- Integration test suite
- End-to-end tests
- Performance/load testing
- UAT with pilot customers
- Bug triage and fixes

**Build Prompts:**
- "Create comprehensive test suite for logistics platform. Write unit tests (Pytest), integration tests, end-to-end tests (Playwright or Cypress), and load tests (Locust). Achieve >80% coverage. Run UAT with pilot customers and document findings. Fix critical and high-priority bugs."

**Acceptance Tests:**
- Test coverage meets targets
- All critical paths tested
- Performance meets SLAs
- UAT feedback addressed

---

### Phase 15: Deployment & Launch (Weeks 49-52)

**Deliverables:**
- Production infrastructure
- Database migrations
- Monitoring setup
- Log aggregation
- Backup automation
- Domain and SSL configuration
- Production deployment
- Launch communications
- Customer onboarding materials

**Build Prompts:**
- "Prepare production deployment for logistics SaaS platform. Set up Kubernetes cluster or ECS service, configure RDS PostgreSQL with replication, ElastiCache Redis, S3 storage, CloudWatch monitoring, ELK logging, automated backups, SSL certificates, and domain setup. Create deployment runbook, rollback procedures, and customer onboarding docs."

**Acceptance Tests:**
- Production environment is stable
- Monitoring and alerts work
- Backups run automatically
- Rollback procedure tested
- First customers onboarded successfully

---

## 12. Success Metrics & KPIs

### 12.1 Product Metrics

**Engagement:**
- Daily Active Users (DAU) / Weekly Active Users (WAU)
- Average session duration
- Feature adoption rates
- Mobile app usage vs web

**Performance:**
- Average response time (< 500ms for API calls)
- Dashboard load time (< 3 seconds)
- Mobile app load time (< 2 seconds)
- Uptime (target: 99.5%)

**Satisfaction:**
- Net Promoter Score (target: >50)
- Customer Satisfaction Score (target: >4.5/5)
- Feature satisfaction ratings
- Support ticket volume and resolution time

### 12.2 Business Impact Metrics

**For Customers:**
- % reduction in delivery variance resolution time (target: 50%)
- % improvement in on-time delivery rate (target: 15%)
- % reduction in fuel cost per km (target: 20%)
- % reduction in invoice dispute time (target: 60%)
- Time saved per week on manual tasks (target: 10 hours)

**For Business:**
- Monthly Recurring Revenue (MRR)
- Annual Recurring Revenue (ARR)
- Customer Acquisition Cost (CAC)
- Customer Lifetime Value (LTV)
- LTV:CAC ratio (target: >3:1)
- Monthly churn rate (target: <5%)
- Average Revenue Per User (ARPU)
- Gross margin (target: >70%)

### 12.3 AI Model Metrics

**Delay Prediction:**
- Accuracy (target: >75%)
- Precision (target: >70%)
- Recall (target: >80%)
- Lead time (target: 2-4 hours before delay)

**Fuel Anomaly Detection:**
- True positive rate (target: >85%)
- False positive rate (target: <10%)
- Detection latency (target: <5 minutes)

**Query Copilot:**
- Query success rate (target: >90%)
- Average response time (target: <3 seconds)
- User satisfaction with answers (target: >4/5)

---

## 13. Risk Management & Mitigation

### 13.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Performance issues with large datasets | Medium | High | Implement pagination, caching, database indexing, query optimization |
| Scalability bottlenecks | Medium | High | Load testing early, horizontal scaling architecture, database read replicas |
| GPS accuracy in poor coverage areas | High | Medium | Offline mode, last-known location caching, fallback to network triangulation |
| AI model inaccuracy | Medium | Medium | Continuous model monitoring, human-in-the-loop validation, confidence thresholds |
| Integration failures with external systems | Medium | Medium | Retry logic, circuit breakers, error logging, fallback modes |

### 13.2 Business Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Low initial adoption | Medium | High | Pilot program with early customers, onboarding support, training materials |
| Feature creep delaying MVP | High | High | Strict scope management, phase-based delivery, MVP focus |
| Competition from established players | Medium | Medium | Focus on underserved SMB market, superior UX, African market expertise |
| Customer churn after trial | Medium | High | Customer success program, value demonstration, quick wins |
| Pricing resistance | Medium | Medium | Flexible pricing tiers, ROI calculators, freemium tier consideration |

### 13.3 Operational Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Data breach | Low | Critical | Strong security practices, regular audits, penetration testing, insurance |
| Service outage | Medium | High | High availability architecture, disaster recovery plan, monitoring |
| Compliance violations (NDPR/GDPR) | Low | High | Legal review, DPO appointment, compliance audits, training |
| Key team member departure | Medium | Medium | Documentation, knowledge sharing, cross-training |

---

## 14. Go-to-Market Strategy

### 14.1 Target Market Segments (Priority Order)

**1. FMCG Distributors (Primary Focus)**
- Pain: Delivery accuracy, customer complaints, driver coordination
- Entry: Pilot program, 3-month trial
- Pricing: Professional tier ($499/month)

**2. Manufacturing Companies with Owned Fleets**
- Pain: Fuel cost control, fleet utilization
- Entry: Enterprise RFP process
- Pricing: Enterprise tier (custom)

**3. 3PL Providers**
- Pain: Client visibility, operational efficiency
- Entry: Industry conferences, partnerships
- Pricing: Professional tier

### 14.2 Sales & Marketing Strategy

**Pre-Launch (Months 1-3):**
- Build landing page with waitlist
- Content marketing (blog posts on logistics challenges)
- LinkedIn presence targeting logistics managers
- Industry partnerships
- Beta program recruitment (5-10 companies)

**Launch (Months 4-6):**
- Product Hunt launch
- Industry webinars
- Case studies from beta customers
- Paid advertising (Google, LinkedIn)
- Trade show presence (optional)

**Growth (Months 7-12):**
- Referral program
- Expansion to adjacent markets
- Partner channel development
- Content marketing at scale
- Customer success stories

**Sales Process:**
1. **Discovery Call** (30 min): Understand pain points, current process
2. **Demo** (45 min): Show platform tailored to their use case
3. **Pilot Proposal** (2-3 weeks trial)
4. **Implementation** (1-2 weeks setup + training)
5. **Review & Expand** (Month 2-3)

### 14.3 Pricing Strategy

**Starter Tier: $99/month**
- Up to 10 vehicles
- 5 users
- Core tracking features
- Basic reports
- Email support

**Professional Tier: $499/month**
- Up to 50 vehicles
- 20 users
- All features including AI insights
- Advanced analytics
- Priority support
- API access

**Enterprise Tier: Custom Pricing**
- 50+ vehicles
- Unlimited users
- All features + custom integrations
- Dedicated account manager
- SLA guarantees
- On-premise deployment option

**Add-Ons:**
- Additional vehicles: $5/vehicle/month
- Additional users: $10/user/month
- Advanced AI features: $200/month
- Premium integrations: $100-500/integration
- Professional services: Custom rates

---

## 15. Appendices

### Appendix A: Glossary

**DVR**: Delivery Variance Report  
**POD**: Proof of Delivery  
**ETA**: Estimated Time of Arrival  
**3PL**: Third-Party Logistics Provider  
**FMCG**: Fast-Moving Consumer Goods  
**TMS**: Transportation Management System  
**GPS**: Global Positioning System  
**OCR**: Optical Character Recognition  
**RBAC**: Role-Based Access Control  
**JWT**: JSON Web Token  
**API**: Application Programming Interface  
**SLA**: Service Level Agreement  
**KPI**: Key Performance Indicator  
**MRR**: Monthly Recurring Revenue  
**ARR**: Annual Recurring Revenue  
**LTV**: Customer Lifetime Value  
**CAC**: Customer Acquisition Cost  

### Appendix B: API Endpoint Summary

**Authentication:**
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/forgot-password` - Request password reset
- `POST /api/v1/auth/reset-password` - Reset password
- `POST /api/v1/auth/verify-email` - Verify email address

**Companies:**
- `GET /api/v1/companies` - List companies (super admin)
- `GET /api/v1/companies/{id}` - Get company details
- `POST /api/v1/companies` - Create company
- `PATCH /api/v1/companies/{id}` - Update company
- `DELETE /api/v1/companies/{id}` - Delete company

**Users:**
- `GET /api/v1/users` - List users in company
- `GET /api/v1/users/{id}` - Get user details
- `POST /api/v1/users` - Create user
- `PATCH /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user
- `POST /api/v1/users/invite` - Invite user

**Vehicles:**
- `GET /api/v1/vehicles` - List vehicles
- `GET /api/v1/vehicles/{id}` - Get vehicle details
- `POST /api/v1/vehicles` - Create vehicle
- `PATCH /api/v1/vehicles/{id}` - Update vehicle
- `DELETE /api/v1/vehicles/{id}` - Delete vehicle

**Drivers:**
- `GET /api/v1/drivers` - List drivers
- `GET /api/v1/drivers/{id}` - Get driver details
- `POST /api/v1/drivers` - Create driver
- `PATCH /api/v1/drivers/{id}` - Update driver
- `DELETE /api/v1/drivers/{id}` - Delete driver

**Shipments:**
- `GET /api/v1/shipments` - List shipments (with filters)
- `GET /api/v1/shipments/{id}` - Get shipment details
- `POST /api/v1/shipments` - Create shipment
- `PATCH /api/v1/shipments/{id}` - Update shipment
- `POST /api/v1/shipments/{id}/status` - Update shipment status
- `GET /api/v1/shipments/{id}/timeline` - Get status timeline
- `POST /api/v1/shipments/{id}/proof-of-delivery` - Upload POD
- `GET /api/v1/shipments/active` - Get all active shipments
- `GET /api/v1/shipments/map` - Get shipments for map view

**Fuel:**
- `GET /api/v1/fuel` - List fuel logs
- `GET /api/v1/fuel/{id}` - Get fuel log details
- `POST /api/v1/fuel` - Create fuel log
- `GET /api/v1/fuel/prices` - Get fuel price history
- `POST /api/v1/fuel/prices` - Record fuel price
- `GET /api/v1/fuel/anomalies` - Get fuel anomalies
- `PATCH /api/v1/fuel/{id}/resolve-anomaly` - Resolve anomaly

**DVR:**
- `GET /api/v1/dvr` - List DVRs
- `GET /api/v1/dvr/{id}` - Get DVR details
- `POST /api/v1/dvr` - Create DVR
- `PATCH /api/v1/dvr/{id}` - Update DVR
- `POST /api/v1/dvr/{id}/approve` - Approve DVR
- `POST /api/v1/dvr/{id}/reject` - Reject DVR
- `POST /api/v1/dvr/{id}/close` - Close DVR

**Invoices:**
- `GET /api/v1/invoices` - List invoices
- `GET /api/v1/invoices/{id}` - Get invoice details
- `POST /api/v1/invoices` - Create invoice
- `POST /api/v1/invoices/upload` - Upload invoice PDF
- `POST /api/v1/invoices/{id}/auto-match` - Auto-match invoice
- `PATCH /api/v1/invoices/{id}` - Update invoice
- `POST /api/v1/invoices/{id}/approve` - Approve invoice
- `POST /api/v1/invoices/{id}/dispute` - Dispute invoice

**Analytics:**
- `GET /api/v1/analytics/shipments` - Shipment KPIs
- `GET /api/v1/analytics/fleet` - Fleet metrics
- `GET /api/v1/analytics/fuel` - Fuel metrics
- `GET /api/v1/analytics/drivers` - Driver performance
- `GET /api/v1/analytics/transporters` - Transporter scores

**AI:**
- `GET /api/v1/ai/predictions` - Get active predictions
- `POST /api/v1/ai/chat` - Natural language query
- `GET /api/v1/ai/insights` - Get AI insights
- `GET /api/v1/ai/summaries` - Get executive summaries

**Notifications:**
- `GET /api/v1/notifications` - List notifications
- `PATCH /api/v1/notifications/{id}/read` - Mark as read
- `POST /api/v1/notifications/preferences` - Update preferences

### Appendix C: Sample Prompts for Claude Code

**Initial Setup Prompt:**
```
Create a production-ready FastAPI backend for a multi-tenant logistics SaaS platform.

Core requirements:
- FastAPI with async support
- PostgreSQL database with SQLAlchemy ORM
- Redis for caching and Celery task queue
- JWT authentication with role-based access control
- Multi-tenant data isolation
- Alembic for database migrations
- Pytest for testing
- Docker Compose for local development
- Pre-commit hooks for linting and formatting
- Comprehensive API documentation

Generate the project structure, configuration files, and core modules for:
1. Authentication service
2. User management
3. Company/tenant management
4. Database connection and session handling
5. Middleware for tenant isolation
6. Error handling
7. Logging configuration
8. Environment variable management
9. Docker setup

Include example models, API endpoints, and tests.
```

**Frontend Setup Prompt:**
```
Create a production-ready Next.js 14 frontend for a logistics dashboard with:

- TypeScript strict mode
- App Router
- Tailwind CSS + shadcn/ui components
- Zustand for state management
- React Query for API data fetching
- React Hook Form + Zod for forms
- Recharts for data visualization
- Google Maps integration
- Authentication flow (login, register, password reset)
- Responsive layout with sidebar navigation
- Dashboard with KPI cards and charts
- Table component with sorting, filtering, pagination
- Error boundaries and loading states
- Environment variable management

Generate:
1. Project structure
2. Configuration files (tailwind, typescript, eslint)
3. Core components (Layout, Sidebar, Header, Button, Card, Table)
4. Authentication pages and logic
5. Dashboard page with mock data
6. API client setup with axios/fetch
7. Type definitions
8. Example usage of all major patterns
```

**Database Schema Prompt:**
```
Generate complete PostgreSQL schema (using SQLAlchemy 2.0 models) for a logistics platform with these entities:

1. companies (id, name, slug, settings, subscription_tier, created_at)
2. users (id, company_id, email, password_hash, role_id, is_active, created_at)
3. roles (id, company_id, name, permissions JSONB)
4. vehicles (id, company_id, license_plate, make, model, capacity, status)
5. drivers (id, company_id, user_id, license_number, rating, status)
6. shipments (id, company_id, shipment_number, customer details, pickup/delivery addresses with lat/lng, vehicle_id, driver_id, status, timestamps)
7. shipment_status_logs (id, shipment_id, from_status, to_status, lat, lng, created_at)
8. delivery_variance_reports (id, shipment_id, dvr_number, variance_type, description, status, created_at)
9. fuel_issuance_logs (id, vehicle_id, quantity_liters, price_per_liter, odometer_reading, is_anomaly, created_at)
10. transporters (id, company_id, name, performance_score, status)
11. invoices (id, company_id, transporter_id, invoice_number, total_amount, status, created_at)
12. invoice_line_items (id, invoice_id, shipment_id, amount, is_matched, has_discrepancy)
13. audit_logs (id, company_id, user_id, action, resource_type, resource_id, changes JSONB, created_at)

Include:
- Proper relationships with foreign keys
- Indexes on frequently queried fields
- JSONB fields where appropriate
- Timestamps (created_at, updated_at)
- Proper data types
- Unique constraints
- Check constraints where applicable
- Comments documenting each field

Also generate Alembic migration files.
```

**AI Model Prompt:**
```
Create a delay prediction model for shipments using XGBoost with these requirements:

Features:
- Shipment: distance_km, cargo_weight_kg, priority, scheduled_delivery_hour, day_of_week
- Vehicle: vehicle_age_years, maintenance_overdue (bool), recent_avg_delay_minutes
- Driver: driver_total_deliveries, driver_on_time_rate, driver_avg_delay_minutes
- Route: route_historical_avg_delay, route_traffic_score
- Weather: temperature_c, is_raining (bool)
- Time: is_peak_hours (bool), is_weekend (bool), is_holiday (bool)

Target: 
- Binary classification: will_delay (yes/no)
- Regression: delay_minutes (if delayed)

Include:
1. Data preprocessing pipeline
2. Feature engineering
3. Train-test split
4. Model training with hyperparameter tuning
5. Evaluation metrics (accuracy, precision, recall, F1, RMSE)
6. Feature importance analysis
7. Model serialization (pickle or joblib)
8. Inference function that returns prediction + confidence + top contributing factors
9. API endpoint for predictions
10. Logging and monitoring

Generate complete Python code with scikit-learn and XGBoost.
```

---

## Summary & Next Steps

This enhanced documentation provides a **comprehensive blueprint** for building FleetIQ from concept to production. It includes:

✅ **Clear Product Vision** with market analysis and positioning  
✅ **Detailed User Personas** with journey maps  
✅ **Complete Feature Catalog** organized by priority  
✅ **Technical Architecture** with stack decisions  
✅ **Full Database Schema** with all relationships  
✅ **Business Logic Rules** for all workflows  
✅ **AI/ML Implementation Strategy** with model details  
✅ **Security & Compliance Framework**  
✅ **Phase-by-Phase Roadmap** with build prompts  
✅ **Success Metrics & KPIs**  
✅ **Risk Management Plan**  
✅ **Go-to-Market Strategy**  

### Immediate Next Steps:

1. **Review & Validate**: Share with stakeholders for feedback
2. **Prioritize MVP**: Confirm Phases 2-7 as MVP scope
3. **Assemble Team**: Identify developers, designer, PM
4. **Set Up Infrastructure**: Cloud account, repos, project management
5. **Start Phase 2**: Begin authentication and tenancy implementation

### Recommended Tools for Execution:

**Project Management**: Linear or Jira  
**Design**: Figma  
**Version Control**: GitHub or GitLab  
**CI/CD**: GitHub Actions  
**Communication**: Slack  
**Documentation**: Notion or Confluence  
**Testing**: Pytest, Playwright  
**Monitoring**: Sentry + DataDog  

**Estimated Timeline to MVP**: 20-24 weeks (Phases 2-7)  
**Estimated Timeline to Full Launch**: 52 weeks (All phases)  

This document serves as the **single source of truth** for product requirements, technical design, and implementation roadmap. Refer to it throughout development to maintain alignment and scope discipline.