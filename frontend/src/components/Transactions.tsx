import React, { useState, useEffect } from 'react';
import { Transaction, Account, Category } from '../types/api';
import { transactionsApi, accountsApi, tagsApi } from '../services/api';
import './Transactions.css';

const Transactions: React.FC = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingTransaction, setEditingTransaction] = useState<Transaction | null>(null);

  const currentUserId = 1; // Demo user ID

  const [formData, setFormData] = useState({
    acc_id: 0,
    description: '',
    amount: 0,
    transaction_date: new Date().toISOString().split('T')[0],
    tag_id: 0,
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [transactionsRes, accountsRes] = await Promise.all([
        transactionsApi.getByUser(currentUserId),
        accountsApi.getByUser(currentUserId)
      ]);

      
      setTransactions(transactionsRes.data.sort((a, b) => 
        new Date((b.transaction_time || b.transaction_date || '') + 'Z').getTime() - new Date((a.transaction_time || a.transaction_date || '') + 'Z').getTime()
      ));
      setAccounts(accountsRes.data);
      
      // Load universal tags (which include category information)
      try {
        const tagsRes = await tagsApi.getAll();
        // Convert tags to category-like structure for compatibility
        const categoriesFromTags = tagsRes.data.map((tag: any) => ({
          category_id: tag.tag_id,
          name: tag.tag_name,
          description: tag.category_name, // This is the broader category (Needs, Wants, Future)
          user_id: 0, // Not user-specific
          created_at: '',
          is_deleted: false
        }));
        setCategories(categoriesFromTags);
      } catch (tagsError) {
        setCategories([]);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingTransaction) {
        await transactionsApi.update(editingTransaction.transaction_id || editingTransaction.trans_id!, formData);
      } else {
        await transactionsApi.create(formData);
      }
      
      resetForm();
      await loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save transaction');
    }
  };

  const handleEdit = (transaction: Transaction) => {
    setEditingTransaction(transaction);
    setFormData({
      acc_id: transaction.acc_id,
      description: transaction.description,
      amount: typeof transaction.amount === 'string' ? parseFloat(transaction.amount) : transaction.amount,
      transaction_date: (transaction.transaction_time || transaction.transaction_date || '').split('T')[0],
      tag_id: transaction.tag_id || 0,
    });
    setShowAddForm(true);
  };

  const resetForm = () => {
    setFormData({
      acc_id: 0,
      description: '',
      amount: 0,
      transaction_date: new Date().toISOString().split('T')[0],
      tag_id: 0,
    });
    setShowAddForm(false);
    setEditingTransaction(null);
  };

  const formatCurrency = (amount: number | string): string => {
    const numAmount = typeof amount === 'string' ? parseFloat(amount) : amount;
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(numAmount);
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

  const getAccountName = (accId: number): string => {
    const account = accounts.find(acc => acc.acc_id === accId);
    if (!account) return 'Unknown Account';
    return account.acc_name || account.account_type || 'Unknown Account';
  };

  const getCategoryName = (tagId?: number): string => {
    if (!tagId) return 'Uncategorized';
    const tag = categories.find(cat => cat.category_id === tagId);
    return tag ? `${tag.name} (${tag.description})` : 'Unknown Category';
  };

  if (loading) {
    return <div className="transactions-loading">Loading transactions...</div>;
  }

  if (error) {
    return (
      <div className="transactions-error">
        <p>Error: {error}</p>
        <button onClick={loadData} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="transactions">
      <div className="transactions-header">
        <h1>Transactions</h1>
        <button 
          onClick={() => setShowAddForm(!showAddForm)}
          className="add-button"
        >
          {showAddForm ? 'Cancel' : 'Add Transaction'}
        </button>
      </div>

      {showAddForm && (
        <div className="transaction-form-container">
          <h2>{editingTransaction ? 'Edit Transaction' : 'Add New Transaction'}</h2>
          <form onSubmit={handleSubmit} className="transaction-form">
            <div className="form-group">
              <label htmlFor="acc_id">Account:</label>
              <select
                id="acc_id"
                value={formData.acc_id}
                onChange={(e) => setFormData({...formData, acc_id: parseInt(e.target.value)})}
                required
              >
                <option value={0}>Select an account</option>
                {accounts.map(account => (
                  <option key={account.acc_id} value={account.acc_id}>
                    {getAccountName(account.acc_id!)}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="description">Description:</label>
              {editingTransaction && editingTransaction.old_description && (
                <div className="original-description-info">
                  <small className="text-muted">
                    Original: {editingTransaction.old_description}
                  </small>
                </div>
              )}
              <input
                type="text"
                id="description"
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                required
                title={editingTransaction?.old_description || 'Transaction description'}
              />
            </div>

            <div className="form-group">
              <label htmlFor="amount">Amount:</label>
              <input
                type="number"
                id="amount"
                step="0.01"
                value={formData.amount}
                onChange={(e) => setFormData({...formData, amount: parseFloat(e.target.value)})}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="transaction_date">Date:</label>
              <input
                type="date"
                id="transaction_date"
                value={formData.transaction_date}
                onChange={(e) => setFormData({...formData, transaction_date: e.target.value})}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="tag_id">Tag:</label>
              <select
                id="tag_id"
                value={formData.tag_id}
                onChange={(e) => setFormData({...formData, tag_id: parseInt(e.target.value)})}
              >
                <option value={0}>Uncategorized</option>
                {categories.map(tag => (
                  <option key={tag.category_id} value={tag.category_id}>
                    {tag.name} ({tag.description})
                  </option>
                ))}
              </select>
            </div>

            <div className="form-buttons">
              <button type="submit" className="submit-button">
                {editingTransaction ? 'Update' : 'Add'} Transaction
              </button>
              <button type="button" onClick={resetForm} className="cancel-button">
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="transactions-list">
        {transactions.length === 0 ? (
          <p className="no-data">No transactions found</p>
        ) : (
          <div className="transactions-table">
            <div className="table-header">
              <span>Date</span>
              <span>Description</span>
              <span>Account</span>
              <span>Category</span>
              <span>Amount</span>
              <span>Actions</span>
            </div>
            {transactions.map((transaction) => (
              <div key={transaction.transaction_id || transaction.trans_id} className="table-row">
                <span className="transaction-date">
                  {formatDate(transaction.transaction_time || transaction.transaction_date || '')}
                </span>
                <span 
                  className="transaction-description"
                  title={transaction.old_description || transaction.description}
                >
                  {transaction.description}
                </span>
                <span className="transaction-account">
                  {getAccountName(transaction.acc_id)}
                </span>
                <span className="transaction-category">
                  {getCategoryName(transaction.tag_id)}
                </span>
                <span className={`transaction-amount ${parseFloat(transaction.amount?.toString() || '0') >= 0 ? 'income' : 'expense'}`}>
                  {formatCurrency(transaction.amount)}
                </span>
                <span className="transaction-actions">
                  <button 
                    onClick={() => handleEdit(transaction)}
                    className="edit-button"
                  >
                    Edit
                  </button>
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Transactions;