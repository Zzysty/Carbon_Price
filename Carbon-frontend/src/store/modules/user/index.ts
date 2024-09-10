import { defineStore } from 'pinia';
import {
  login as userLogin,
  logout as userLogout,
  register as userRegister,
  getUserInfo,
  LoginData,
  RegisterData,
} from "@/api/user";
import { setToken, clearToken } from '@/utils/auth';
import { removeRouteListener } from '@/utils/route-listener';
import { UserState } from './types';
import useAppStore from '../app';

const useUserStore = defineStore('user', {
  state: (): UserState => ({
    id: undefined,
    name: undefined,
    avatar: undefined,
    job: undefined,
    location: undefined,
    email: undefined,
    introduction: undefined,
    personalWebsite: undefined,
    phone: undefined,
    registrationDate: undefined,
    role: '',
  }),

  getters: {
    userInfo(state: UserState): UserState {
      return { ...state };
    },
  },

  actions: {
    switchRoles() {
      return new Promise((resolve) => {
        this.role = this.role === 'user' ? 'admin' : 'user';
        resolve(this.role);
      });
    },
    // Set user's information
    setInfo(partial: Partial<UserState>) {
      this.$patch(partial);
    },

    // Reset user's information 重置用户信息
    resetInfo() {
      this.$reset();
    },

    // Get user's information 获取当前用户信息
    async info() {
      const res = await getUserInfo();
      // eslint-disable-next-line no-console
      console.log('test', res.data);
      this.setInfo(res.data);
    },

    // Register 注册表单
    async register(registerForm: RegisterData) {
      // eslint-disable-next-line no-useless-catch
      try {
        const res = await userRegister(registerForm);
        // eslint-disable-next-line no-console
        console.log('test', res.data);
      } catch (err) {
        throw err;
      }
    },

    // Login 登录表单
    async login(loginForm: LoginData) {
      try {
        const res = await userLogin(loginForm);
        // eslint-disable-next-line no-console
        // console.log('test', res.data);
        setToken(res.data.access_token);
      } catch (err) {
        // eslint-disable-next-line no-console
        // console.log('test', err);
        clearToken();
        throw err;
      }
    },
    // 注销后的回调操作
    logoutCallBack() {
      const appStore = useAppStore();
      // 重置信息
      this.resetInfo();
      // 清楚令牌
      clearToken();
      removeRouteListener();
      appStore.clearServerMenu();
    },
    // Logout 注销
    async logout() {
      try {
        await userLogout();
      } finally {
        this.logoutCallBack();
      }
    },
  },
});

export default useUserStore;
