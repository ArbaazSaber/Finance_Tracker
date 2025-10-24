import React, { useState, useEffect } from 'react';
import { Account, Bank } from '../types/api';
import { accountsApi, banksApi } from '../services/api';
import './Accounts.css';

const Accounts: React.FC = () => {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [banks, setBanks] = useState<Bank[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingAccount, setEditingAccount] = useState<Account | null>(null);

  const currentUserId = 1; // Demo user ID

  const [formData, setFormData] = useState({
    user_id: currentUserId,
    acc_name: '',
    bank_id: 0,
    balance: 0,
    currency: 'USD',
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [accountsRes, banksRes] = await Promise.all([
        accountsApi.getByUser(currentUserId),
        banksApi.getAll()
      ]);

      console.log('Banks response:', banksRes.data);
      console.log('Accounts response:', accountsRes.data);
      
      setAccounts(accountsRes.data);
      setBanks(Array.isArray(banksRes.data) ? banksRes.data : []);
    } catch (err: any) {
      console.error('Error loading data:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingAccount) {
        await accountsApi.update(editingAccount.acc_id!, formData);
      } else {
        await accountsApi.create(formData);
      }
      
      resetForm();
      await loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save account');
    }
  };

  const handleEdit = (account: Account) => {
    setEditingAccount(account);
    setFormData({
      user_id: account.user_id,
      acc_name: account.acc_name,
      bank_id: account.bank_id,
      balance: account.balance,
      currency: account.currency || 'USD',
    });
    setShowAddForm(true);
  };

  const handleDelete = async (accId: number) => {
    if (window.confirm('Are you sure you want to delete this account?')) {
      try {
        await accountsApi.delete(accId);
        await loadData();
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to delete account');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      user_id: currentUserId,
      acc_name: '',
      bank_id: 0,
      balance: 0,
      currency: 'USD',
    });
    setShowAddForm(false);
    setEditingAccount(null);
  };


  const getBankName = (account: Account): string => {
    // First try to use bank_name from account response (if backend provides it)
    if (account.bank_name) {
      return account.bank_name;
    }
    // Otherwise lookup from banks array
    const bank = banks.find(b => b.bank_id === account.bank_id);
    if (bank) {
      return bank.name;
    }
    // Debug log if we can't find the bank
    console.log('Bank not found for account:', account, 'banks array:', banks);
    return 'Unknown Bank';
  };

  const formatCurrency = (amount: number | undefined, currencyCode: string): string => {
    const numAmount = amount || 0;
    const locale = navigator.language || 'en-US';
    try {
      return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currencyCode,
      }).format(numAmount);
    } catch (error) {
      // Fallback to just the amount with currency code
      return `${currencyCode} ${numAmount.toFixed(2)}`;
    }
  };

  if (loading) {
    return <div className="accounts-loading">Loading accounts...</div>;
  }

  if (error) {
    return (
      <div className="accounts-error">
        <p>Error: {error}</p>
        <button onClick={loadData} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="accounts">
      <div className="accounts-header">
        <h1>Accounts</h1>
        <button 
          onClick={() => setShowAddForm(!showAddForm)}
          className="add-button"
        >
          {showAddForm ? 'Cancel' : 'Add Account'}
        </button>
      </div>

      {showAddForm && (
        <div className="account-form-container">
          <h2>{editingAccount ? 'Edit Account' : 'Add New Account'}</h2>
          <form onSubmit={handleSubmit} className="account-form">
            <div className="form-group">
              <label htmlFor="bank_id">Bank:</label>
              <select
                id="bank_id"
                value={formData.bank_id}
                onChange={(e) => setFormData({...formData, bank_id: parseInt(e.target.value)})}
                required
              >
                <option value={0}>Select a bank</option>
                {banks.length === 0 ? (
                  <option disabled>No banks available - Please add banks first</option>
                ) : (
                  banks.map(bank => (
                    <option key={bank.bank_id} value={bank.bank_id}>
                      {bank.name}
                    </option>
                  ))
                )}
              </select>
              {banks.length === 0 && (
                <small style={{color: '#e74c3c', marginTop: '5px'}}>No banks found. Please add banks using the backend API first.</small>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="acc_name">Account Name:</label>
              <input
                type="text"
                id="acc_name"
                maxLength={20}
                value={formData.acc_name}
                onChange={(e) => setFormData({...formData, acc_name: e.target.value})}
                required
                placeholder="e.g., Main Checking, Savings"
              />
            </div>

            <div className="form-group">
              <label htmlFor="balance">Balance:</label>
              <input
                type="number"
                id="balance"
                step="0.01"
                value={formData.balance}
                onChange={(e) => setFormData({...formData, balance: parseFloat(e.target.value) || 0})}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="currency">Currency:</label>
              <select
                id="currency"
                value={formData.currency}
                onChange={(e) => setFormData({...formData, currency: e.target.value})}
                required
              >
                <option value="USD">USD - US Dollar</option>
                <option value="EUR">EUR - Euro</option>
                <option value="GBP">GBP - British Pound</option>
                <option value="INR">INR - Indian Rupee</option>
                <option value="JPY">JPY - Japanese Yen</option>
                <option value="AUD">AUD - Australian Dollar</option>
                <option value="CAD">CAD - Canadian Dollar</option>
                <option value="CHF">CHF - Swiss Franc</option>
                <option value="CNY">CNY - Chinese Yuan</option>
                <option value="SEK">SEK - Swedish Krona</option>
                <option value="NZD">NZD - New Zealand Dollar</option>
              </select>
            </div>

            <div className="form-buttons">
              <button type="submit" className="submit-button">
                {editingAccount ? 'Update' : 'Add'} Account
              </button>
              <button type="button" onClick={resetForm} className="cancel-button">
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="accounts-list">
        {accounts.length === 0 ? (
          <p className="no-data">No accounts found</p>
        ) : (
          <div className="accounts-grid">
            {accounts.map((account) => (
              <div key={account.acc_id} className="account-card">
                <div className="account-header">
                  <h3>{account.acc_name}</h3>
                  <div className="account-actions">
                    <button 
                      onClick={() => handleEdit(account)}
                      className="edit-button"
                    >
                      Edit
                    </button>
                    <button 
                      onClick={() => handleDelete(account.acc_id!)}
                      className="delete-button"
                    >
                      Delete
                    </button>
                  </div>
                </div>
                
                <div className="account-details">
                  <p className="bank-name">{getBankName(account)}</p>
                  <p className="account-status">
                    Status: <span className={account.is_active ? 'status-active' : 'status-inactive'}>
                      {account.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </p>
                  <p className="account-balance">
                    {formatCurrency(account.balance, account.currency)}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Accounts;
