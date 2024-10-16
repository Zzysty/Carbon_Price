export type RoleType = 'admin' | 'user';

export interface UserState {
  id?: number;
  username?: string;
  gender?: string;
  avatar?: string;
  // job?: string;
  // location?: string;
  email?: string;
  // introduction?: string;
  // personalWebsite?: string;
  // phone?: string;
  // registrationDate?: string;
  user_role: RoleType;
}

export interface Token {
  access_token: string;
  token_type: string;
}
