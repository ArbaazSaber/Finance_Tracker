export interface User {
  user_id?: number;
  name: string;
  email: string;
  created_at?: string;
  is_deleted?: boolean;
}

export interface Account {
  acc_id?: number;
  user_id: number;
  bank_id: number;
  account_number?: string;
  account_type?: string;
  balance?: number;
  created_at?: string;
  is_deleted?: boolean;
  // Backend response includes these additional fields
  acc_name?: string;
  bank_name?: string;
  user_name?: string;
  is_active?: boolean;
}

export interface Transaction {
  trans_id?: number;
  acc_id: number;
  description: string;
  amount: number | string;
  transaction_date?: string;
  category_id?: number;
  created_at?: string;
  is_deleted?: boolean;
  // Backend response includes these additional fields
  transaction_id?: number;
  transaction_time?: string;
  old_description?: string;
  reference_id?: string;
  type?: string;
  modified_at?: string;
  tag_id?: number;
  user_id?: number;
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