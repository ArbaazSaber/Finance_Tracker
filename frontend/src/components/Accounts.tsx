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
    bank_id: 0,
    account_number: '',
    account_type: '',
    balance: 0,
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

      setAccounts(accountsRes.data);
      setBanks(banksRes.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load data');
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
      bank_id: account.bank_id,
      account_number: account.account_number || '',
      account_type: account.account_type || '',
      balance: account.balance || 0,
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
      bank_id: 0,
      account_number: '',
      account_type: '',
      balance: 0,
    });
    setShowAddForm(false);
    setEditingAccount(null);
  };


  const getBankName = (bankId: number): string => {
    const bank = banks.find(b => b.bank_id === bankId);
    return bank ? bank.name : 'Unknown Bank';
  };

  const getAccountDisplayName = (account: Account): string => {
    return account.acc_name || account.account_type || 'Account';
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
                {banks.map(bank => (
                  <option key={bank.bank_id} value={bank.bank_id}>
                    {bank.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="account_number">Account Number:</label>
              <input
                type="text"
                id="account_number"
                value={formData.account_number}
                onChange={(e) => setFormData({...formData, account_number: e.target.value})}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="balance">Initial Balance:</label>
              <input
                type="number"
                id="balance"
                step="0.01"
                value={formData.balance}
                onChange={(e) => setFormData({...formData, balance: parseFloat(e.target.value)})}
              />
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
                  <h3>{getAccountDisplayName(account)}</h3>
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
                  <p className="bank-name">{account.bank_name || getBankName(account.bank_id)}</p>
                  <p className="account-balance">
                    Status: {account.is_active ? 'Active' : 'Inactive'}
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