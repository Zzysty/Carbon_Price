import axios from 'axios';
import qs from 'query-string';
import type { RouteRecordNormalized } from 'vue-router';
import { Token, UserState } from '@/store/modules/user/types';

export interface LoginData {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  password: string;
  email: string;
  user_role: string;
  gender: string;
}

export interface LoginRes {
  code: number;
  msg: string;
  data: Token;
}

export interface RegisterRes {
  code: number;
  msg: string;
  data: null;
}

export function register(data: RegisterData) {
  // 注册
  return axios.post<RegisterRes>('/api/user/register', data);
}

// @ts-ignore
export function login(data: LoginData) {
  // 登录
  return axios.post<LoginRes>('/api/user/login', qs.stringify(data), {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
}

// @ts-ignore
export function logout() {
  // 注销
  return axios.post<LoginRes>('/api/user/logout');
}

// @ts-ignore
export function getUserInfo() {
  // 获取当前用户信息
  return axios.get<UserState>('/api/user/me');
}

// @ts-ignore
export function getMenuList() {
  return axios.post<RouteRecordNormalized[]>('/api/user/menu');
}
