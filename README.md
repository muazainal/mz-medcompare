<h1 align="center">💊 Comparative Medicine Database</h1>

<p align="center">
  <em>A full-stack web application for searchable, comparable, and verified medicine information</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/Backend-Django-blue" alt="Backend">
  <img src="https://img.shields.io/badge/Frontend-HTML%7CCSS%7CBootstrap-orange" alt="Frontend">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-green" alt="Database">
  <img src="https://img.shields.io/badge/Payment-Stripe-purple" alt="Stripe Integration">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

<p align="center">
  <a href="#">Live Demo (Coming Soon)</a>
</p>

---

## Table of Contents
- [Purpose](#purpose)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Target Users](#target-users)
- [Scalability & Maintenance](#scalability--maintenance)
- [Deployment](#deployment)
- [Planned Updates](#planned-updates)
- [Contact](#contact)

---

## Purpose

<div align="justify">

This project is designed to solve challenges in navigating the pharmaceutical market. Users face difficulties in retrieving accurate medicine information, comparing similar products, and verifying quality reports. The **Comparative Medicine Database** provides a **centralised, user-friendly platform** where consumers, healthcare professionals, and manufacturers can search, compare, and manage medicine data securely.

</div>

---

## Features

- **Advanced Medicine Search**: Search by brand name, generic name, or active ingredient  
- **Formula-Based Comparison**: Compare all medicines containing the same formula  
- **Dynamic Filtering & Sorting**: Filter by quality ratings, sort by price  
- **Lab Report Upload & Viewing**: View PDF lab reports for quality verification  
- **Manufacturer Portal**: Secure registration, medicine submission, document upload  
- **Payment Integration (Stripe)**: Secure one-time purchases and subscription payments  
- **Responsive Design**: Optimised for desktop, tablet, and mobile  

---

## Tech Stack

- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, Bootstrap, JavaScript  
- **Database:** PostgreSQL  
- **Payment Integration:** Stripe  
- **Deployment:** Heroku  
- **Authentication:** Django Authentication System  

---

## Target Users

- Consumers seeking verified and affordable medicine options  
- Healthcare professionals looking for comparative data  
- Pharmaceutical manufacturers managing product listings  
- Charity organisations promoting transparency  

---

## Scalability & Maintenance

- **Database Scalability:** PostgreSQL handles growing records and users efficiently  
- **Modular Architecture:** Easily add new features like analytics or AI recommendations  
- **File & Media Management:** Cloud storage for lab reports and documentation  
- **User & Role Expansion:** Add new roles like auditors or pharmacists without breaking the system  
- **Maintainability:** Well-structured code and clear documentation for easy future updates  

---

## Deployment

To run locally:

```bash
git clone https://github.com/muazainal/mz-medcompare.git
cd comparative-medicine-database
# set up Python virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
