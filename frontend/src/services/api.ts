import axios from 'axios';
import { 
  User, Account, Transaction, Category, Bank, Tag, 
  BulkTransactionRequest, BulkTransactionResponse 
} from '../types/api';

const API_BASE_URL = process.env.REACT_APP_API_URL

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Users API
export const usersApi = {
  getAll: () => api.get<User[]>('/users/'),
  getById: (userId: number) => api.get<User>(`/users/${userId}`),
  create: (user: Omit<User, 'user_id'>) => api.post<number>('/users', user),
  update: (userId: number, user: Partial<User>) => api.put(`/users/${userId}`, user),
  delete: (userId: number) => api.delete(`/users/${userId}`),
};

// Accounts API
export const accountsApi = {
  getById: (accId: number) => api.get<Account>(`/accounts/${accId}`),
  getByUser: (userId: number) => api.get<Account[]>(`/accounts/user/${userId}`),
  create: (account: Omit<Account, 'acc_id'>) => api.post<{acc_id: number}>('/accounts', account),
  update: (accId: number, account: Partial<Account>) => api.put<Account>(`/accounts/${accId}`, account),
  delete: (accId: number) => api.delete(`/accounts/${accId}`),
};

// Transactions API
export const transactionsApi = {
  getById: (transId: number) => api.get<Transaction>(`/transactions/${transId}`),
  getByUser: (userId: number) => api.get<Transaction[]>(`/transactions/user/${userId}`),
  getByAccount: (accId: number) => api.get<Transaction[]>(`/transactions/account/${accId}`),
  create: (transaction: Omit<Transaction, 'trans_id'>) => api.post<number>('/transactions', transaction),
  update: (transId: number, transaction: Partial<Transaction>) => api.put(`/transactions/${transId}`, transaction),
  bulkCreate: (request: BulkTransactionRequest) => api.post<BulkTransactionResponse>('/transactions/bulk', request),
};

// Categories API
export const categoriesApi = {
  getAll: () => api.get<Category[]>('/categories/'),
  getById: (categoryId: number) => api.get<Category>(`/categories/${categoryId}`),
  getByUser: (userId: number) => api.get<Category[]>(`/categories/user/${userId}`),
  create: (category: Omit<Category, 'category_id'>) => api.post<number>('/categories', category),
  update: (categoryId: number, category: Partial<Category>) => api.put(`/categories/${categoryId}`, category),
  delete: (categoryId: number) => api.delete(`/categories/${categoryId}`),
};

// Banks API
export const banksApi = {
  getAll: () => api.get<Bank[]>('/banks/'),
  getById: (bankId: number) => api.get<Bank>(`/banks/${bankId}`),
  create: (bank: Omit<Bank, 'bank_id'>) => api.post<number>('/banks', bank),
  update: (bankId: number, bank: Partial<Bank>) => api.put(`/banks/${bankId}`, bank),
  delete: (bankId: number) => api.delete(`/banks/${bankId}`),
};

// Tags API
export const tagsApi = {
  getAll: () => api.get<Tag[]>('/tags/'),
  getById: (tagId: number) => api.get<Tag>(`/tags/${tagId}`),
  getByUser: (userId: number) => api.get<Tag[]>(`/tags/user/${userId}`),
  create: (tag: Omit<Tag, 'tag_id'>) => api.post<number>('/tags', tag),
  update: (tagId: number, tag: Partial<Tag>) => api.put(`/tags/${tagId}`, tag),
  delete: (tagId: number) => api.delete(`/tags/${tagId}`),
};

export default api;