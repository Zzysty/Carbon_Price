<template>
  <a-form
    ref="formRef"
    :model="formData"
    class="form"
    :wrapper-col-props="{ span: 16 }"
  >
    <a-form-item
      field="username"
      :label="$t('userSetting.basicInfo.form.label.username')"
    >
      <a-input
        v-model="formData.username"
        :placeholder="$t('userSetting.basicInfo.placeholder.username')"
      />
    </a-form-item>
    <a-form-item field="user_role" label="权限">
      <a-radio-group v-model="formData.user_role" :size="'medium'" label="role">
        <a-radio value="user">用户</a-radio>
        <a-radio value="admin">管理员</a-radio>
      </a-radio-group>
    </a-form-item>
    <a-form-item field="gender" label="性别">
      <a-radio-group v-model="formData.gender" :size="'medium'">
        <a-radio value="male">男</a-radio>
        <a-radio value="female">女</a-radio>
      </a-radio-group>
    </a-form-item>
    <a-form-item field="phone" label="电话">
      <a-input v-model="formData.phone" placeholder="请输入电话" />
    </a-form-item>
    <a-form-item
      field="email"
      :label="$t('userSetting.basicInfo.form.label.email')"
    >
      <a-input
        v-model="formData.email"
        :placeholder="$t('userSetting.basicInfo.placeholder.email')"
      />
    </a-form-item>
    <!--    <a-form-item field="gender" label="性别">-->
    <!--      <a-select v-model="formData.gender" placeholder="请选择性别">-->
    <!--        <a-option value="male">男</a-option>-->
    <!--        <a-option value="female">女</a-option>-->
    <!--      </a-select>-->
    <!--    </a-form-item>-->
    <a-form-item
      field="profile"
      :label="$t('userSetting.basicInfo.form.label.profile')"
      :rules="[
        {
          maxLength: 200,
          message: $t('userSetting.form.error.profile.maxLength'),
        },
      ]"
      row-class="keep-margin"
    >
      <a-textarea
        v-model="formData.description"
        :placeholder="$t('userSetting.basicInfo.placeholder.profile')"
      />
    </a-form-item>
    <a-form-item>
      <a-space>
        <a-button type="primary" @click="validateAndSave">
          {{ $t('userSetting.save') }}
        </a-button>
        <a-button type="secondary" @click="reset">
          {{ $t('userSetting.reset') }}
        </a-button>
      </a-space>
    </a-form-item>
  </a-form>
</template>

<script lang="ts" setup>
  import { ref } from 'vue';
  import { FormInstance } from '@arco-design/web-vue/es/form';
  import { BasicInfoModel, updateUserInfo } from '@/api/user-center';
  import { Message } from '@arco-design/web-vue';
  import { useUserStore } from '@/store';

  const userStore = useUserStore();
  const formRef = ref<FormInstance>();
  const formData = ref<BasicInfoModel>({
    username: '',
    gender: '',
    email: '',
    phone: '',
    description: '',
    user_role: '',
  });
  const reset = async () => {
    formRef.value?.resetFields();
  };
  // 保存并更新表单数据
  const validateAndSave = async () => {
    try {
      // const res = await formRef.value?.validate();
      const res = await updateUserInfo(formData.value);

      if (res.code === 200) {
        await userStore.info();
        // 提示保存成功
        Message.success('保存成功');
        formRef.value?.resetFields();
      } else {
        // 处理错误
        Message.error(res.msg);
      }
    } catch (error) {
      // eslint-disable-next-line no-console
      console.error('表单验证失败或保存出错:', error);
    }
  };
</script>

<style scoped lang="less">
  .form {
    width: 580px;
    margin: 0 auto;
  }
</style>
