import type { Router, LocationQueryRaw } from 'vue-router';
import NProgress from 'nprogress'; // progress bar

import { useUserStore } from '@/store';
import { isLogin } from '@/utils/auth';

/**
 * 设置用户登录信息守卫
 * 在用户访问页面之前进行权限校验和登录状态处理
 * @param router Vue Router实例
 */
export default function setupUserLoginInfoGuard(router: Router) {
  router.beforeEach(async (to, from, next) => {
    NProgress.start(); // 开始显示进度条
    const userStore = useUserStore();
    if (isLogin()) {
      if (userStore.user_role) {
        next();
      } else {
        try {
          // 尝试获取用户信息
          await userStore.info();
          next();
        } catch (error) {
          // 获取用户信息失败，则清除登录状态并重定向到登录页面
          await userStore.logout();
          next({
            name: 'login',
            query: {
              redirect: to.name,
              ...to.query,
            } as LocationQueryRaw,
          });
        }
      }
    } else {
      if (to.name === 'login' || to.name === 'register') {
        next();
        return;
      }
      // 非登录页面，重定向至登录页面
      next({
        name: 'login',
        query: {
          redirect: to.name,
          ...to.query,
        } as LocationQueryRaw,
      });
    }
  });
}
