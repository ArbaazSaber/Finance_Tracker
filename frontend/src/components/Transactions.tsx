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
  const [showFilters, setShowFilters] = useState(false);
  
  // Search and filter states
  const [searchQuery, setSearchQuery] = useState('');
  const [filterAccount, setFilterAccount] = useState<number>(0);
  const [filterCategory, setFilterCategory] = useState<number>(0);
  const [filterMinAmount, setFilterMinAmount] = useState<number>(0);
  const [filterMaxAmount, setFilterMaxAmount] = useState<number>(100000);
  const [sliderMax, setSliderMax] = useState<number>(100000);
  const [filterAmountType, setFilterAmountType] = useState<'all' | 'credit' | 'debit'>('all');
  const [filterStartDate, setFilterStartDate] = useState<string>('');
  const [filterEndDate, setFilterEndDate] = useState<string>('');

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

  const formatCurrency = (amount: number | string, currencyCode: string = 'USD'): string => {
    const numAmount = typeof amount === 'string' ? parseFloat(amount) : amount;
    const locale = navigator.language || 'en-US';
    try {
      return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currencyCode,
      }).format(numAmount);
    } catch (error) {
      // Fallback if currency formatting fails
      return `${currencyCode} ${numAmount.toFixed(2)}`;
    }
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
    return account.acc_name || 'Unknown Account';
  };

  const getAccountCurrency = (accId: number): string => {
    const account = accounts.find(acc => acc.acc_id === accId);
    return account?.currency || 'USD';
  };

  const getCategoryName = (tagId?: number): string => {
    if (!tagId) return 'Uncategorized';
    const tag = categories.find(cat => cat.category_id === tagId);
    return tag ? `${tag.name} (${tag.description})` : 'Unknown Category';
  };

  // Filter and search transactions
  const filteredTransactions = transactions.filter((transaction) => {
    // Search filter
    if (searchQuery && !transaction.description.toLowerCase().includes(searchQuery.toLowerCase())) {
      return false;
    }
    
    // Account filter
    if (filterAccount && transaction.acc_id !== filterAccount) {
      return false;
    }
    
    // Category filter
    if (filterCategory && transaction.tag_id !== filterCategory) {
      return false;
    }
    
    // Amount type filter (credit/debit)
    const rawAmount = typeof transaction.amount === 'string' ? parseFloat(transaction.amount) : transaction.amount;
    if (filterAmountType === 'credit' && rawAmount <= 0) {
      return false;
    }
    if (filterAmountType === 'debit' && rawAmount >= 0) {
      return false;
    }
    
    // Amount range filter (only apply if not at default values)
    const amount = Math.abs(rawAmount);
    if (filterMinAmount > 0 && amount < filterMinAmount) {
      return false;
    }
    if (filterMaxAmount < sliderMax && amount > filterMaxAmount) {
      return false;
    }
    
    // Date range filter
    const transactionDate = transaction.transaction_time || transaction.transaction_date || '';
    if (filterStartDate && transactionDate < filterStartDate) {
      return false;
    }
    if (filterEndDate && transactionDate > filterEndDate) {
      return false;
    }
    
    return true;
  });

  // Dynamic step calculation (1000 levels)
  const dynamicStep = Math.max(1, Math.floor(sliderMax / 1000));

  const handleMinAmountChange = (value: number) => {
    const newMin = Math.max(0, Math.min(value, filterMaxAmount - dynamicStep));
    setFilterMinAmount(newMin);
    // Extend slider max if needed
    if (value > sliderMax) {
      setSliderMax(Math.ceil(value / 10000) * 10000);
    }
  };

  const handleMaxAmountChange = (value: number) => {
    const newMax = Math.max(value, filterMinAmount + dynamicStep);
    setFilterMaxAmount(newMax);
    // Extend slider max if needed
    if (newMax > sliderMax) {
      setSliderMax(Math.ceil(newMax / 10000) * 10000);
    }
  };

  const resetAmountRange = () => {
    setFilterMinAmount(0);
    setFilterMaxAmount(100000);
    setSliderMax(100000);
  };

  const clearFilters = () => {
    setSearchQuery('');
    setFilterAccount(0);
    setFilterCategory(0);
    setFilterMinAmount(0);
    setFilterMaxAmount(100000);
    setSliderMax(100000);
    setFilterAmountType('all');
    setFilterStartDate('');
    setFilterEndDate('');
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

      {/* Search and Filter Section */}
      <div className="search-filter-container">
        <div className="search-bar-wrapper">
          <input
            type="text"
            placeholder="Search transactions by description..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          <button 
            onClick={() => setShowFilters(!showFilters)}
            className="filter-toggle-button"
            title="Toggle Filters"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="4" y1="6" x2="20" y2="6"></line>
              <line x1="4" y1="12" x2="20" y2="12"></line>
              <line x1="4" y1="18" x2="20" y2="18"></line>
              <circle cx="7" cy="6" r="2" fill="currentColor"></circle>
              <circle cx="17" cy="12" r="2" fill="currentColor"></circle>
              <circle cx="12" cy="18" r="2" fill="currentColor"></circle>
            </svg>
            Filters
          </button>
        </div>
        
        {showFilters && (
        <div className="filters-section filters-floating">
          <div className="filters-header">
            <h3>Filters</h3>
            <button onClick={() => setShowFilters(false)} className="close-filters-button" title="Close Filters">
              ×
            </button>
          </div>
          
          <div className="filter-category">
            <h4>Basic Filters</h4>
            <div className="filters-grid">
            <div className="filter-group">
              <label htmlFor="filter-account">Account:</label>
              <select
                id="filter-account"
                value={filterAccount}
                onChange={(e) => setFilterAccount(parseInt(e.target.value))}
              >
                <option value={0}>All Accounts</option>
                {accounts.map(account => (
                  <option key={account.acc_id} value={account.acc_id}>
                    {getAccountName(account.acc_id!)}
                  </option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="filter-category">Category:</label>
              <select
                id="filter-category"
                value={filterCategory}
                onChange={(e) => setFilterCategory(parseInt(e.target.value))}
              >
                <option value={0}>All Categories</option>
                {categories.map(category => (
                  <option key={category.category_id} value={category.category_id}>
                    {category.name} ({category.description})
                  </option>
                ))}
              </select>
            </div>

              <div className="filter-group">
                <label htmlFor="filter-amount-type">Amount Type:</label>
                <select
                  id="filter-amount-type"
                  value={filterAmountType}
                  onChange={(e) => setFilterAmountType(e.target.value as 'all' | 'credit' | 'debit')}
                >
                  <option value="all">All</option>
                  <option value="credit">Credit (Income)</option>
                  <option value="debit">Debit (Expense)</option>
                </select>
              </div>
            </div>
          </div>

          <div className="filter-category">
            <div className="filter-category-header">
              <h4>Amount Range</h4>
              <button onClick={resetAmountRange} className="reset-range-button" title="Reset Amount Range">
                Reset
              </button>
            </div>
            <div className="filters-grid">
              <div className="filter-group amount-slider-group">
              <label>Amount Range</label>
              <div className="amount-inputs">
                <div className="amount-input-wrapper">
                  <label htmlFor="min-amount-input">Min:</label>
                  <input
                    type="number"
                    id="min-amount-input"
                    min="0"
                    step={dynamicStep}
                    value={filterMinAmount}
                    onChange={(e) => handleMinAmountChange(Number(e.target.value))}
                    className="amount-number-input"
                  />
                </div>
                <div className="amount-input-wrapper">
                  <label htmlFor="max-amount-input">Max:</label>
                  <input
                    type="number"
                    id="max-amount-input"
                    min="0"
                    step={dynamicStep}
                    value={filterMaxAmount}
                    onChange={(e) => handleMaxAmountChange(Number(e.target.value))}
                    className="amount-number-input"
                  />
                </div>
              </div>
              <div className="dual-range-slider">
                <input
                  type="range"
                  min="0"
                  max={sliderMax}
                  step={dynamicStep}
                  value={filterMinAmount}
                  onChange={(e) => handleMinAmountChange(Number(e.target.value))}
                  className="range-slider range-slider-min"
                />
                <input
                  type="range"
                  min="0"
                  max={sliderMax}
                  step={dynamicStep}
                  value={filterMaxAmount}
                  onChange={(e) => handleMaxAmountChange(Number(e.target.value))}
                  className="range-slider range-slider-max"
                />
              </div>
            </div>
            </div>
          </div>

          <div className="filter-category">
            <h4>Date Range</h4>
            <div className="filters-grid">
            <div className="filter-group date-range-group">
              <label>Date Range:</label>
              <div className="date-range-inputs">
                <input
                  type="date"
                  id="filter-start-date"
                  value={filterStartDate}
                  onChange={(e) => setFilterStartDate(e.target.value)}
                  placeholder="Start Date"
                  className="date-input"
                />
                <span className="date-separator">to</span>
                <input
                  type="date"
                  id="filter-end-date"
                  value={filterEndDate}
                  onChange={(e) => setFilterEndDate(e.target.value)}
                  placeholder="End Date"
                  className="date-input"
                />
              </div>
            </div>
            </div>
          </div>

          <div className="filters-actions">
            <button onClick={clearFilters} className="clear-filters-button">
              Clear All Filters
            </button>
          </div>
        </div>
        )}
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
        ) : filteredTransactions.length === 0 ? (
          <p className="no-data">No transactions match your filters</p>
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
            {filteredTransactions.map((transaction) => (
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
                  {formatCurrency(transaction.amount, getAccountCurrency(transaction.acc_id))}
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