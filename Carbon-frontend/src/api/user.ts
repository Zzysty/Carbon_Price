import axios from 'axios';
import type { RouteRecordNormalized } from 'vue-router';
import { Token, UserState } from "@/store/modules/user/types";

export interface LoginData {
  username: string;
  password: string;
}

export interface LoginRes {
  code: number;
  msg: string;
  data: Token;
}
export function login(data: LoginData) {
  return axios.post<LoginRes>('/api/user/login', data, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
}

export function logout() {
  return axios.post<LoginRes>('/api/user/logout');
}

export function getUserInfo() {
  return axios.get<UserState>('/api/user/me');
}

export function getMenuList() {
  return axios.post<RouteRecordNormalized[]>('/api/user/menu');
}
