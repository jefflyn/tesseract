# Futures Data Management System

A Minimum Viable Product (MVP) for futures data scraping, analysis, and email notification system built with Python Flask and Vue3.

## 📋 Overview

This system provides automated futures market data collection from Chinese commodity exchanges, including:
- Real-time basic futures information
- Main contract tracking and management
- Daily trading data (K-line) collection
- Scheduled automatic updates
- Email notifications for daily reports

## 🛠️ Tech Stack

### Backend
- **Language**: Python 3.8+
- **Framework**: Flask (RESTful API)
- **Data Source**: akshare (financial data interface)
- **Database**: SQLite
- **Scheduler**: schedule library
- **Email**: SMTP protocol

### Frontend
- **Framework**: Vue 3 (Composition API)
- **UI Library**: Element Plus
- **Build Tool**: Vite
- **HTTP Client**: Axios

## 📁 Project Structure

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- Node.js 16 or higher
- npm (comes with Node.js)
- Git

### Installation

#### 1. Clone or Navigate to Project

#### 2. Backend Setup

Install Python dependencies:

#### 3. Frontend Setup

Install Node.js dependencies:

Or manually:

#### 4. Configure Environment Variables

Copy the environment template and configure:


Edit `.env` file with your settings:

**Note**: For QQ邮箱, you need to enable SMTP service and get an authorization code from [QQ Mail Settings](https://mail.qq.com/cgi-bin/frame_html?c=zh_CN&r=).

### Running the Application

#### Option 1: Start All Services (Recommended)


This will start both backend and frontend simultaneously.

#### Option 2: Start Services Separately

**Terminal 1 - Backend API:**

**Terminal 2 - Frontend Dev Server:**


**Terminal 3 - Scheduler (Optional for auto-updates):**
### Access the Application

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

## 📖 User Guide

### Feature 1: Basic Futures Information

**Purpose**: Fetch and view basic information about all futures contracts.

**Steps**:
1. Open http://localhost:3000
2. Navigate to "基本信息" tab
3. Click "获取基本信息" button
4. View the fetched data in the table

**What it does**:
- Fetches all futures basic info from Sina Finance
- Stores in SQLite database
- Displays symbol, name, exchange, unit, etc.

### Feature 2: Main Contract Management

**Purpose**: Track and manage main (dominant) futures contracts.

**Steps**:
1. Navigate to "合约管理" tab
2. Click "获取主力合约" to fetch current main contracts
3. Use checkbox "仅显示选中" to filter selected contracts
4. Toggle the "已选择" checkbox to mark contracts of interest

**What it does**:
- Fetches current main contracts
- Tracks price ranges (high/low)
- Allows selection of contracts to monitor
- Stores historical context

### Feature 3: Daily Trading Data

**Purpose**: Collect and analyze daily K-line data for selected contracts.

**Steps**:
1. Navigate to "日K数据" tab
2. Enter a contract code in the search box and click "查询" to filter
3. Click "获取单个合约数据" to fetch specific contract history
4. Click "更新所有主力合约" to update all main contracts at once
5. Browse paginated results

**What it does**:
- Fetches daily OHLC (Open/High/Low/Close) data
- Stores trading volume and price changes
- Supports date range queries
- Paginated display for performance

### Feature 4: Automated Daily Updates

**Purpose**: Automatically update trading data every weekday at 16:00.

**Setup**:

**What it does**:
- Runs continuously in background
- Triggers data update at 16:00 daily
- Sends email report after update
- Logs all activities to console

### Feature 5: Email Notifications

**Purpose**: Receive daily update reports via email.

**Configuration**:
1. Set SMTP credentials in `.env`
2. Add recipient emails to `NOTIFICATION_EMAILS`
3. Trigger an update (manual or scheduled)

**Report includes**:
- Update timestamp
- List of updated contracts
- Number of records per contract
- Success/failure status

## 🔌 API Documentation

### Base URL

### Endpoints

#### Health Check
#### Basic Information

**Get all basics:**

#### Contracts

**Get contracts:**
#### Contracts

**Get contracts:**
**Fetch main contracts:**
