export interface User {
  id: string;
  email: string;
  name: string;
  token: string;
}

export interface Transaction {
  id?: string;
  user_id?: string;
  type: 'income' | 'expense';
  amount: number;
  category: string;
  description?: string;
  date: string;
  created_at?: string;
}

export interface Budget {
  id?: string;
  user_id?: string;
  category: string;
  limit: number;
  spent: number;
  period: string;
  created_at?: string;
}

export interface Goal {
  id?: string;
  user_id?: string;
  name: string;
  target_amount: number;
  current_amount: number;
  deadline: string;
  created_at?: string;
}

export interface Stats {
  total_income: number;
  total_expenses: number;
  balance: number;
  category_expenses: { [key: string]: number };
  recent_income: number;
  recent_expenses: number;
  transaction_count: number;
}