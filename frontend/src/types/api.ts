export interface User {
  user_id?: number;
  name: string;
  email: string;
  created_at?: string;
  is_deleted?: boolean;
}

export interface Account {
  acc_id?: number;
  acc_name: string;
  user_id: number;
  user_name?: string;
  bank_id: number;
  bank_name?: string;
  is_active?: boolean;
  balance: number;
  currency: string;
  created_at?: string;
}

export interface Transaction {
  trans_id?: number;
  transaction_id?: number;
  acc_id: number;
  description: string;
  amount: number;
  transaction_date?: string;
  transaction_time?: string;
  old_description?: string;
  tag_id?: number;
  category_id?: number;
  created_at?: string;
  is_deleted?: boolean;
  currency?: string;
}

export interface Category {
  category_id?: number;
  user_id: number;
  name: string;
  description?: string;
  created_at?: string;
  is_deleted?: boolean;
}

export interface Bank {
  bank_id?: number;
  name: string;
  code?: string;
  created_at?: string;
  is_deleted?: boolean;
}

export interface Tag {
  tag_id?: number;
  user_id: number;
  name: string;
  color?: string;
  created_at?: string;
  is_deleted?: boolean;
}

export interface BulkTransactionRequest {
  transactions: Transaction[];
}

export interface BulkTransactionResponse {
  success_count: number;
  failure_count: number;
  total_count: number;
  errors?: string[];
}