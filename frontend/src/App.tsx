import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Transactions from './components/Transactions';
import Accounts from './components/Accounts';
import './App.css';

const Navigation: React.FC = () => {
  const location = useLocation();
  
  return (
    <nav className="navigation">
      <div className="nav-brand">
        <h2>Finance Tracker</h2>
      </div>
      <div className="nav-links">
        <Link 
          to="/" 
          className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
        >
          Dashboard
        </Link>
        <Link 
          to="/transactions" 
          className={`nav-link ${location.pathname === '/transactions' ? 'active' : ''}`}
        >
          Transactions
        </Link>
        <Link 
          to="/accounts" 
          className={`nav-link ${location.pathname === '/accounts' ? 'active' : ''}`}
        >
          Accounts
        </Link>
      </div>
    </nav>
  );
};

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/transactions" element={<Transactions />} />
            <Route path="/accounts" element={<Accounts />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
