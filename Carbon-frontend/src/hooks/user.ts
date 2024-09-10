import { useRouter } from 'vue-router';
import { Message } from '@arco-design/web-vue';

import { useUserStore } from '@/store';

export default function useUser() {
  const router = useRouter();
  const userStore = useUserStore();
  const logout = async (logoutTo?: string) => {
    try {
      await userStore.logout();
      const currentRoute = router.currentRoute.value;
      Message.success('注销成功');
      await router.push({
        name: logoutTo && typeof logoutTo === 'string' ? logoutTo : 'login',
        query: {
          ...router.currentRoute.value.query,
          redirect: currentRoute.name as string,
        },
      });
    } catch (e: any) {
      Message.error('注销失败，请稍后再试');
      // eslint-disable-next-line no-console
      console.log('注销失败', e);
    }
  };
  return {
    logout,
  };
}
