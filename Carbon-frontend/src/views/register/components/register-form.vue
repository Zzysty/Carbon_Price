<template>
  <div class="register-form-wrapper">
    <a-space direction="vertical" size="mini" :style="{ width: '300px' }">
      <div class="register-form-title">注册</div>
      <div class="register-form-sub-title">从这里开始你的碳市场之旅</div>
      <div class="register-form-error-msg">{{ errorMessage }}</div>
      <a-form
        ref="RegisterForm"
        :model="userInfo"
        class="register-form"
        layout="vertical"
        @submit="handleSubmit"
      >
        <!--账号-->
        <a-form-item
          field="username"
          :rules="[{ required: true, message: '账号为必填项' }]"
          :validate-trigger="['change', 'blur']"
          hide-label
        >
          <a-input v-model="userInfo.username" placeholder="请输入账号">
            <template #prefix>
              <icon-user />
            </template>
          </a-input>
        </a-form-item>
        <!--密码-->
        <a-form-item
          field="password"
          :rules="[{ required: true, message: '密码为必填项' }]"
          :validate-trigger="['change', 'blur']"
          hide-label
        >
          <a-input-password
            v-model="userInfo.password"
            placeholder="请输入密码"
            allow-clear
          >
            <template #prefix>
              <icon-lock />
            </template>
          </a-input-password>
        </a-form-item>
        <!--确认密码-->
        <!--        <a-form-item-->
        <!--          field="repassword"-->
        <!--          :rules="[{ required: true, message: '确认密码为必填项' }]"-->
        <!--          :validate-trigger="['change', 'blur']"-->
        <!--          hide-label-->
        <!--        >-->
        <!--          <a-input-password-->
        <!--            v-model="userInfo.password"-->
        <!--            placeholder="请再次输入密码"-->
        <!--            allow-clear-->
        <!--          >-->
        <!--            <template #prefix>-->
        <!--              <icon-lock />-->
        <!--            </template>-->
        <!--          </a-input-password>-->
        <!--        </a-form-item>-->
        <!--邮箱-->
        <a-form-item
          field="email"
          :rules="[{ required: false, message: '邮箱为选填项' }]"
          :validate-trigger="['change', 'blur']"
          hide-label
        >
          <a-input v-model="userInfo.email" placeholder="请输入邮箱（选填）">
            <template #prefix>
              <icon-email />
            </template>
          </a-input>
        </a-form-item>
        <a-space :size="16">
          <!--角色-->
          <a-form-item field="user_role">
            <a-radio-group
              v-model="userInfo.user_role"
              type="button"
              :size="'medium'"
              label="role"
            >
              <a-radio value="user">用户</a-radio>
              <a-radio value="admin">管理员</a-radio>
            </a-radio-group>
          </a-form-item>
          <!--性别-->
          <a-form-item field="gender">
            <a-radio-group
              v-model="userInfo.gender"
              type="button"
              :size="'medium'"
              default-checked="male"
            >
              <a-radio value="male">男</a-radio>
              <a-radio value="female">女</a-radio>
            </a-radio-group>
          </a-form-item>
        </a-space>
        <a-space :size="16" direction="vertical">
          <a-button type="primary" html-type="submit" long :loading="loading">
            注册
          </a-button>
          <a-button
            type="text"
            long
            class="register-form-register-btn"
            @click="$router.push({ name: 'login' })"
          >
            已有账号，请登录
          </a-button>
        </a-space>
      </a-form>
    </a-space>
  </div>
</template>

<script lang="ts" setup>
  import { ref, reactive } from 'vue';
  import { useRouter } from 'vue-router';
  import { Message } from '@arco-design/web-vue';
  import { ValidatedError } from '@arco-design/web-vue/es/form/interface';
  import { useStorage } from '@vueuse/core';
  import { useUserStore } from '@/store';
  import useLoading from '@/hooks/loading';
  import { RegisterData } from '@/api/user';

  const router = useRouter();
  const errorMessage = ref('');
  const { loading, setLoading } = useLoading();
  const userStore = useUserStore();

  const registerConfig = useStorage('register-config', {
    username: '',
    password: '',
    gender: '',
    email: '',
    user_role: '',
  });
  const userInfo = reactive({
    username: registerConfig.value.username,
    password: registerConfig.value.password,
    email: registerConfig.value.email,
    gender: registerConfig.value.gender || 'male',
    user_role: registerConfig.value.user_role || 'user',
  });

  const handleSubmit = async ({
    errors,
    values,
  }: {
    errors: Record<string, ValidatedError> | undefined;
    values: Record<string, any>;
  }) => {
    if (loading.value) return;
    if (!errors) {
      setLoading(true);
      try {
        await userStore.register(values as RegisterData);

        const { redirect, ...othersQuery } = router.currentRoute.value.query;
        await router.push({
          name: (redirect as string) || 'login',
          query: {
            ...othersQuery,
          },
        });
        Message.success('注册成功');
      } catch (err) {
        errorMessage.value = (err as Error).message;
        Message.error('注册失败');
      } finally {
        setLoading(false);
      }
    }
  };
</script>

<style lang="less" scoped>
  .register-form {
    &-wrapper {
      width: 320px;
    }

    &-title {
      color: var(--color-text-1);
      font-weight: 500;
      font-size: 24px;
      line-height: 32px;
    }

    &-sub-title {
      color: var(--color-text-3);
      font-size: 16px;
      line-height: 24px;
    }

    &-error-msg {
      height: 32px;
      color: rgb(var(--red-6));
      line-height: 32px;
    }

    &-password-actions {
      display: flex;
      justify-content: space-between;
    }

    &-register-btn {
      color: var(--color-text-3) !important;
    }
  }
</style>
