import React, { useState, useEffect, useCallback } from 'react';
import { Account, Transaction } from '../types/api';
import { accountsApi, transactionsApi } from '../services/api';
import './Dashboard.css';

interface DashboardStats {
  totalBalance: number;
  totalAccounts: number;
  recentTransactions: number;
  monthlySpending: number;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats>({
    totalBalance: 0,
    totalAccounts: 0,
    recentTransactions: 0,
    monthlySpending: 0,
  });
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [recentTransactions, setRecentTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // For demo purposes, using user_id = 1
  const currentUserId = 1;

  const loadDashboardData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Load accounts
      const accountsResponse = await accountsApi.getByUser(currentUserId);
      const userAccounts = accountsResponse.data;
      setAccounts(userAccounts);

      // Load recent transactions
      const transactionsResponse = await transactionsApi.getByUser(currentUserId);
      const allTransactions = transactionsResponse.data;
      
      // Sort transactions by date and take the 5 most recent
      const sortedTransactions = allTransactions
        .sort((a, b) => {
          const dateA = new Date((a.transaction_time || a.transaction_date || '') + 'Z').getTime();
          const dateB = new Date((b.transaction_time || b.transaction_date || '') + 'Z').getTime();
          return dateB - dateA;
        })
        .slice(0, 5);
      setRecentTransactions(sortedTransactions);

      // Calculate stats
      // Note: Backend doesn't provide balance, so we'll calculate from transactions or set to 0
      const totalBalance = 0; // userAccounts.reduce((sum, account) => sum + (account.balance || 0), 0);
      const monthlySpending = calculateMonthlySpending(allTransactions);
      
      setStats({
        totalBalance,
        totalAccounts: userAccounts.length,
        recentTransactions: allTransactions.length,
        monthlySpending,
      });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  }, [currentUserId]);

  useEffect(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  const calculateMonthlySpending = (transactions: any[]): number => {
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    
    return transactions
      .filter(transaction => {
        const transactionDate = new Date(transaction.transaction_time + 'Z');
        return transactionDate.getMonth() === currentMonth && 
               transactionDate.getFullYear() === currentYear &&
               parseFloat(transaction.amount) < 0; // Only count expenses
      })
      .reduce((sum, transaction) => sum + Math.abs(parseFloat(transaction.amount)), 0);
  };

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const formatDate = (dateString: string): string => {
    if (!dateString) return 'N/A';
    
    // Handle ISO format dates from backend (e.g., "2024-01-08T00:00:00")
    // Since the backend sends dates without timezone info, treat them as UTC to avoid shifts
    const date = new Date(dateString + 'Z'); // Add Z to treat as UTC
    
    // Check if date is valid
    if (isNaN(date.getTime())) {
      return 'Invalid Date';
    }
    
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getDisplayName = (account: any): string => {
    return account.acc_name || 'Unknown Account';
  };

  const getAccountNumber = (account: any): string => {
    // Extract account number from acc_name if available
    const match = account.acc_name?.match(/(\d{4})/);
    return match ? `****${match[1]}` : '****0000';
  };

  if (loading) {
    return <div className="dashboard-loading">Loading dashboard...</div>;
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <p>Error: {error}</p>
        <button onClick={loadDashboardData} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <h1 className="dashboard-title">Finance Dashboard</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Balance</h3>
          <p className="stat-value">{formatCurrency(stats.totalBalance)}</p>
        </div>
        
        <div className="stat-card">
          <h3>Total Accounts</h3>
          <p className="stat-value">{stats.totalAccounts}</p>
        </div>
        
        <div className="stat-card">
          <h3>Total Transactions</h3>
          <p className="stat-value">{stats.recentTransactions}</p>
        </div>
        
        <div className="stat-card">
          <h3>Monthly Spending</h3>
          <p className="stat-value expense">{formatCurrency(stats.monthlySpending)}</p>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="accounts-section">
          <h2>Your Accounts</h2>
          {accounts.length === 0 ? (
            <p className="no-data">No accounts found</p>
          ) : (
            <div className="accounts-list">
              {accounts.map((account) => (
                <div key={account.acc_id} className="account-card">
                  <h4>{getDisplayName(account)}</h4>
                  <p className="account-number">
                    {getAccountNumber(account)}
                  </p>
                  <p className="account-balance">{account.bank_name}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="transactions-section">
          <h2>Recent Transactions</h2>
          {recentTransactions.length === 0 ? (
            <p className="no-data">No recent transactions</p>
          ) : (
            <div className="transactions-list">
              {recentTransactions.map((transaction) => (
                <div key={transaction.transaction_id} className="transaction-item">
                  <div className="transaction-details">
                    <p 
                      className="transaction-description"
                      title={transaction.old_description || transaction.description}
                    >
                      {transaction.description}
                    </p>
                    <p className="transaction-date">{formatDate(transaction.transaction_time || transaction.transaction_date || '')}</p>
                  </div>
                  <p className={`transaction-amount ${parseFloat(transaction.amount?.toString() || '0') >= 0 ? 'income' : 'expense'}`}>
                    {formatCurrency(parseFloat(transaction.amount?.toString() || '0'))}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;