<template>
  <div class="register-form-wrapper">
    <div class="register-form-title">注册</div>
    <div class="register-form-sub-title">从这里开始你的碳市场之旅</div>
    <div class="register-form-error-msg">{{ errorMessage }}</div>
    <a-form
      ref="loginForm"
      :model="userInfo"
      class="register-form"
      layout="vertical"
      @submit="handleSubmit"
    >
      <a-form-item
        field="gender"
        label=""
        :rules="[{ match: /one/, message: 'must select one' }]"
      >
        <a-radio-group v-model="userInfo.gender">
          <a-radio value="radio one">男</a-radio>
          <a-radio value="radio two">女</a-radio>
        </a-radio-group>
      </a-form-item>
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
      <a-form-item
        field="repassword"
        :rules="[{ required: true, message: '确认密码为必填项' }]"
        :validate-trigger="['change', 'blur']"
        hide-label
      >
        <a-input-password
          v-model="userInfo.password"
          placeholder="请再次输入密码"
          allow-clear
        >
          <template #prefix>
            <icon-lock />
          </template>
        </a-input-password>
      </a-form-item>
      {{ userInfo }}
      <a-space :size="16" direction="vertical">
        <div class="register-form-password-actions">
          <!--          <a-checkbox-->
          <!--            checked="rememberPassword"-->
          <!--            :model-value="loginConfig.rememberPassword"-->
          <!--            @change="setRememberPassword as any"-->
          <!--          >-->
          <!--            {{ $t('register.form.rememberPassword') }}-->
          <!--          </a-checkbox>-->
          <!--          <a-link>{{ $t('register.form.forgetPassword') }}</a-link>-->
        </div>
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
  </div>
</template>

<script lang="ts" setup>
  import { ref, reactive } from 'vue';
  import { useRouter } from 'vue-router';
  import { Message } from '@arco-design/web-vue';
  import { ValidatedError } from '@arco-design/web-vue/es/form/interface';
  import { useI18n } from 'vue-i18n';
  import { useStorage } from '@vueuse/core';
  import { useUserStore } from '@/store';
  import useLoading from '@/hooks/loading';
  import { LoginData, RegisterData } from '@/api/user';

  const router = useRouter();
  const { t } = useI18n();
  const errorMessage = ref('');
  const { loading, setLoading } = useLoading();
  const userStore = useUserStore();

  const registerConfig = useStorage('register-config', {
    // rememberPassword: true,
    username: '',
    password: '',
    gender: '',
    email: '',
    user_role: '',
  });
  const userInfo = reactive({
    username: registerConfig.value.username,
    password: registerConfig.value.password,
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
        // const { rememberPassword } = registerConfig.value;
        const { username, password } = values;
        // 实际生产环境需要进行加密存储。
        // The actual production environment requires encrypted storage.
        // registerConfig.value.username = rememberPassword ? username : '';
        // registerConfig.value.password = rememberPassword ? password : '';
      } catch (err) {
        errorMessage.value = (err as Error).message;
      } finally {
        setLoading(false);
      }
    }
  };
  // const setRememberPassword = (value: boolean) => {
  //   registerConfig.value.rememberPassword = value;
  // };
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
