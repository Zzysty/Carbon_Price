<template>
  <a-spin style="width: 100%" :loading="isLoading as boolean" :size="32">
    <a-card class="user-info" :bordered="false">
      <a-space :size="54">
        <a-upload
          :custom-request="customRequest"
          list-type="picture-card"
          :file-list="fileList"
          :show-upload-button="true"
          :show-file-list="false"
          @change="uploadChange"
        >
          <template #upload-button>
            <a-avatar :size="100" class="info-avatar">
              <template #trigger-icon>
                <icon-camera />
              </template>
              <img v-if="fileList.length" :src="fileList[0].url" alt="" />
            </a-avatar>
          </template>
        </a-upload>
        <!--        {{ fileList[0] }}-->
        <a-descriptions :data="renderData" :column="2">
          <template #label="{ label }">{{ $t(label) }} :</template>
          <!--        <template #value="{ value, data }">-->
          <!--          <a-tag-->
          <!--            v-if="data.label === 'userSetting.label.certification'"-->
          <!--            color="green"-->
          <!--            size="small"-->
          <!--          >-->
          <!--            已认证-->
          <!--          </a-tag>-->
          <!--          <span v-else>{{ value }}</span>-->
          <!--        </template>-->
        </a-descriptions>
      </a-space>
    </a-card>
  </a-spin>
</template>

<script lang="ts" setup>
  import { computed, ref } from 'vue';
  import type {
    FileItem,
    RequestOption,
  } from '@arco-design/web-vue/es/upload/interfaces';
  import { useUserStore } from '@/store';
  import { userUploadApi } from '@/api/user-center';
  import type { DescData } from '@arco-design/web-vue/es/descriptions/interface';
  import dayjs from 'dayjs';
  import { Message } from '@arco-design/web-vue';

  const userStore = useUserStore();

  const userInfo = computed(() => userStore.userInfo);
  const isLoading = computed(() => userStore.isLoading);
  const BACKEND_URL = import.meta.env.VITE_API_BASE_URL;

  const file = {
    uid: '',
    name: '',
    url: `${BACKEND_URL}/${userInfo.value.avatar}`,
  };

  // 格式化日期时间
  const formatDate = (date?: string | Date) => {
    return dayjs(date || '').isValid()
      ? dayjs(date).format('YYYY-MM-DD HH:mm:ss')
      : '';
  };
  // 性别转换函数
  const formatGender = (gender: string | undefined) => {
    // eslint-disable-next-line no-nested-ternary
    return gender === 'male' ? '男' : gender === 'female' ? '女' : '未知'; // 默认值为 '未知'
  };
  // 动态渲染数据列表
  const renderData = computed(
    () =>
      [
        {
          label: 'userSetting.label.name',
          value: userInfo.value.username,
        },
        {
          label: 'userSetting.label.gender',
          value: formatGender(userInfo.value.gender),
        },
        {
          label: 'userSetting.label.phone',
          value: userInfo.value.phone,
        },
        {
          label: 'userSetting.label.email',
          value: userInfo.value.email,
        },
        {
          label: 'userSetting.label.registrationDate',
          value: formatDate(userInfo.value.created_at),
        },
        {
          label: 'userSetting.label.description',
          value: userInfo.value.description,
        },
      ] as DescData[]
  );

  const fileList = ref<FileItem[]>([file]);
  // 获取图片的 URL
  const getImageUrl = (fileItem: FileItem) => {
    if (
      fileItem.status === 'done' &&
      fileItem.response &&
      fileItem.response.code === 200
    ) {
      // 文件上传完成并成功，拼接后端 URL
      return `${BACKEND_URL}${fileItem.response.data}`;
    }
    if (fileItem.status === 'uploading' || fileItem.status === 'init') {
      // 文件上传中或初始化阶段，使用 blob URL
      return file.url;
    }
    // 其他情况（例如错误），返回空字符串或一个默认 URL
    return file.url;
  };
  const uploadChange = (fileItemList: FileItem[], fileItem: FileItem) => {
    // 更新 fileList 以展示新的 URL
    fileList.value = [
      {
        ...fileItem,
        url: getImageUrl(fileItem),
      },
    ];
  };
  const customRequest = (options: RequestOption) => {
    // docs: https://axios-http.com/docs/cancellation
    const controller = new AbortController();

    (async function requestWrap() {
      const { onProgress, onError, onSuccess, fileItem } = options;
      onProgress(20);
      const formData = new FormData();
      formData.append('file', fileItem.file as Blob);
      // const onUploadProgress = (event: ProgressEvent) => {
      //   let percent;
      //   if (event.total > 0) {
      //     percent = (event.loaded / event.total) * 100;
      //   }
      //   onProgress(parseInt(String(percent), 10), event);
      // };

      try {
        // https://github.com/axios/axios/issues/1630
        // https://github.com/nuysoft/Mock/issues/127

        const res = await userUploadApi(formData);
        if (res.code === 200) {
          fileList.value = [
            {
              uid: fileItem.uid,
              name: fileItem.name,
              url: res.data,
            },
          ];
          Message.success('上传成功');
        }
        onSuccess(res);
      } catch (error) {
        Message.error('上传失败');
        onError(error);
      }
    })();
    return {
      abort() {
        controller.abort();
      },
    };
  };
</script>

<style scoped lang="less">
  .arco-card {
    padding: 14px 0 4px 4px;
    border-radius: 4px;
  }

  :deep(.arco-avatar-trigger-icon-button) {
    width: 32px;
    height: 32px;
    line-height: 32px;
    background-color: #e8f3ff;

    .arco-icon-camera {
      margin-top: 8px;
      color: rgb(var(--arcoblue-6));
      font-size: 14px;
    }
  }
</style>
