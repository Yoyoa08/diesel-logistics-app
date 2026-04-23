# ⛽ Philip's Online Diesel Supply - Logistics MVP

A custom-built logistics and order management system designed for a diesel supply business in Abuja, Nigeria. This application automates the transition from manual WhatsApp-based ordering to a structured, real-time dashboard.

## 🚀 Key Features
- **Client Portal:** Real-time price calculation, secure order placement, and order tracking.
- **Admin Dashboard:** A centralized monitor for workers to track pending orders and mark deliveries.
- **Automated Workflows:** Unique Order ID generation and validation logic to prevent delivery errors.
- **Responsive UI:** Optimized for both mobile (drivers) and desktop (office) use.

## 🛠️ Tech Stack
- **Frontend/Backend:** [Streamlit](https://streamlit.io/) (Python)
- **Data Persistence:** CSV (Scalable to SQL/Supabase)
- **Deployment:** GitHub & Streamlit Community Cloud

## 📋 How It Works
1. **Ordering:** Customers enter the required volume (Litres); the app calculates the total price based on current market rates.
2. **Verification:** Customers receive a unique 5-digit Order ID to track their request.
3. **Logistics:** Admins access the `/view=admin` route to manage orders and update statuses upon delivery.

## 🚧 Status
- [x] Phase 1: MVP Core Logic
- [x] Phase 2: Live Price Calculation & UI Polish
- [ ] Phase 3: Migration to Cloud Database (Supabase)