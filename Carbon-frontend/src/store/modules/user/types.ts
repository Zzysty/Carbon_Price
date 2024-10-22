export type RoleType = 'admin' | 'user';

export interface UserState {
  id?: number;
  username?: string;
  gender?: string;
  avatar?: string;
  // job?: string;
  // location?: string;
  email?: string;
  description?: string;
  // personalWebsite?: string;
  phone?: string;
  created_at?: string;
  updated_at?: string;
  user_role: RoleType;
  isLoading?: boolean;
}

export interface Token {
  access_token: string;
  token_type: string;
}
