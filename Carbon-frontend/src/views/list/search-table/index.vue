<template>
  <div class="container">
    <Breadcrumb :items="['menu.list', 'menu.list.Hubei']" />
    <a-card class="general-card" :title="$t('menu.list.Hubei')">
      <a-row>
        <a-col :flex="1">
          <a-form
            :model="formModel"
            :label-col-props="{ span: 6 }"
            :wrapper-col-props="{ span: 14 }"
            label-align="left"
          >
            <a-row :gutter="18">
              <!--              <a-col :span="6">-->
              <!--                <a-form-item-->
              <!--                  field="number"-->
              <!--                  :label="$t('searchTable.form.number')"-->
              <!--                >-->
              <!--                  <a-input-->
              <!--                    v-model="formModel.number"-->
              <!--                    :placeholder="$t('searchTable.form.number.placeholder')"-->
              <!--                  />-->
              <!--                </a-form-item>-->
              <!--              </a-col>-->
              <a-col :span="8">
                <a-form-item field="createdTime" label="日期范围">
                  <a-range-picker
                    v-model="formModel.dateRange"
                    style="width: 100%"
                  />
                </a-form-item>
              </a-col>
              <!--              <a-col :span="6">-->
              <!--                <a-form-item field="product" label="产品">-->
              <!--                  <a-select-->
              <!--                    v-model="formModel.product"-->
              <!--                    :options="productOptions"-->
              <!--                    placeholder="请选择产品"-->
              <!--                  />-->
              <!--                </a-form-item>-->
              <!--              </a-col>-->
            </a-row>
          </a-form>
        </a-col>
        <!--        <a-divider style="height: 84px" direction="vertical" />-->
        <!--        <a-col :flex="'86px'" style="text-align: right"></a-col>-->
      </a-row>

      <a-divider style="margin-top: 0" />

      <a-row style="margin-bottom: 16px">
        <a-col :span="12">
          <a-space :size="'small'">
            <a-button type="primary" @click="search">
              <template #icon>
                <icon-search />
              </template>
              查询
            </a-button>
            <a-button @click="reset">
              <template #icon>
                <icon-refresh />
              </template>
              重置
            </a-button>

            <a-divider direction="vertical" />

            <a-upload :custom-request="handleUpload" :show-file-list="false" />
            <a-button>
              <template #icon>
                <icon-download />
              </template>
              导出
            </a-button>
          </a-space>
        </a-col>
        <a-col
          :span="12"
          style="display: flex; align-items: center; justify-content: end"
        >
          <a-tooltip :content="$t('searchTable.actions.columnSetting')">
            <a-popover
              trigger="click"
              position="bl"
              @popup-visible-change="popupVisibleChange"
            >
              <div class="action-icon">
                <icon-settings size="18" />
              </div>
              <template #content>
                <div id="tableSetting">
                  <div
                    v-for="(item, index) in showColumns"
                    :key="item.dataIndex"
                    class="setting"
                  >
                    <div style="margin-right: 4px; cursor: move">
                      <icon-drag-arrow />
                    </div>
                    <div>
                      <a-checkbox
                        v-model="item.checked"
                        @change="
                          handleChange($event, item as TableColumnData, index)
                        "
                      >
                      </a-checkbox>
                    </div>
                    <div class="title">
                      {{ item.title === '#' ? '序列号' : item.title }}
                    </div>
                  </div>
                </div>
              </template>
            </a-popover>
          </a-tooltip>
          <a-dropdown @select="handleSelectDensity">
            <a-tooltip :content="$t('searchTable.actions.density')">
              <div class="action-icon">
                <icon-line-height size="18" />
              </div>
            </a-tooltip>
            <template #content>
              <a-doption
                v-for="item in densityList"
                :key="item.value"
                :value="item.value"
                :class="{ active: item.value === size }"
              >
                <span>{{ item.name }}</span>
              </a-doption>
            </template>
          </a-dropdown>
          <a-tooltip :content="$t('searchTable.actions.refresh')">
            <div class="action-icon" @click="search">
              <icon-refresh size="18" />
            </div>
          </a-tooltip>
        </a-col>
      </a-row>
      <a-table
        row-key="id"
        :loading="loading"
        :pagination="pagination as PaginationProps"
        :columns="(cloneColumns as TableColumnData[])"
        :data="renderData"
        :bordered="false"
        :size="size"
        column-resizable
      >
        <!--        <template #index="{ rowIndex }">-->
        <!--          {{ rowIndex + 1 + (pagination.current - 1) * pagination.pageSize }}-->
        <!--        </template>-->
        <template #contentType="{ record }">
          <a-space>
            <a-avatar
              v-if="record.contentType === 'img'"
              :size="16"
              shape="square"
            >
              <img
                alt="avatar"
                src="//p3-armor.byteimg.com/tos-cn-i-49unhts6dw/581b17753093199839f2e327e726b157.svg~tplv-49unhts6dw-image.image"
              />
            </a-avatar>
            <a-avatar
              v-else-if="record.contentType === 'horizontalVideo'"
              :size="16"
              shape="square"
            >
              <img
                alt="avatar"
                src="//p3-armor.byteimg.com/tos-cn-i-49unhts6dw/77721e365eb2ab786c889682cbc721c1.svg~tplv-49unhts6dw-image.image"
              />
            </a-avatar>
            <a-avatar v-else :size="16" shape="square">
              <img
                alt="avatar"
                src="//p3-armor.byteimg.com/tos-cn-i-49unhts6dw/ea8b09190046da0ea7e070d83c5d1731.svg~tplv-49unhts6dw-image.image"
              />
            </a-avatar>
            {{ $t(`searchTable.form.contentType.${record.contentType}`) }}
          </a-space>
        </template>
        <template #filterType="{ record }">
          {{ $t(`searchTable.form.filterType.${record.filterType}`) }}
        </template>
        <template #status="{ record }">
          <span v-if="record.status === 'offline'" class="circle"></span>
          <span v-else class="circle pass"></span>
          {{ $t(`searchTable.form.status.${record.status}`) }}
        </template>
        <template #operations>
          <a-button v-permission="['admin']" type="text" size="small">
            {{ $t('searchTable.columns.operations.view') }}
          </a-button>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script lang="ts" setup>
  import { computed, nextTick, ref, watch } from 'vue';
  import { useI18n } from 'vue-i18n';
  import useLoading from '@/hooks/loading';
  import {
    CarbonMarketParams,
    GDCarbonMarketRecord,
    HBCarbonMarketRecord,
    queryGuangdongList,
    queryHubeiList,
    uploadHubeiFile,
  } from '@/api/list';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import cloneDeep from 'lodash/cloneDeep';
  import Sortable from 'sortablejs';
  import { Notification, PaginationProps } from '@arco-design/web-vue';

  type SizeProps = 'mini' | 'small' | 'medium' | 'large';
  type Column = TableColumnData & {
    checked?: true;
  };

  const generateFormModel = () => {
    return {
      dateRange: [], // 日期范围
    };
  };
  const { loading, setLoading } = useLoading(true);
  const { t } = useI18n();
  const renderData = ref<HBCarbonMarketRecord[]>([]);
  const formModel = ref(generateFormModel());
  const cloneColumns = ref<Column[]>([]);
  const showColumns = ref<Column[]>([]);

  const size = ref<SizeProps>('small');
  const errorMessage = ref('');

  // const basePagination: Pagination = {
  //   current: 1,
  //   pageSize: 20,
  // };
  // const pagination = reactive({
  //   ...basePagination,
  // });
  const pagination = {
    'show-page-size': true,
    'show-total': true,
  };
  const densityList = computed(() => [
    {
      name: '迷你',
      value: 'mini',
    },
    {
      name: '偏小',
      value: 'small',
    },
    {
      name: '中等',
      value: 'medium',
    },
    {
      name: '偏大',
      value: 'large',
    },
  ]);

  // 辅助函数，根据值筛选涨跌幅
  function filterByPriceChange(value: string, priceChange: number) {
    if (value === 'positive') {
      return priceChange > 0; // 正：大于0
    }
    if (value === 'negative') {
      return priceChange < 0; // 负：小于0
    }
    return true; // 默认返回所有数据
  }

  const columns = computed<TableColumnData[]>(() => [
    {
      title: 'id',
      dataIndex: 'id',
      ellipsis: true,
      tooltip: true,
    },
    {
      title: '产品',
      dataIndex: 'product',
      filterable: {
        filters: [
          {
            text: 'HBEA',
            value: 'HBEA',
          },
          {
            text: 'HBEA2022',
            value: 'HBEA2022',
          },
        ],
        filter: (value, row) => row.product.includes(value),
      },
    },
    {
      title: '日期',
      dataIndex: 'date',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '最新',
      dataIndex: 'latest_price',
    },
    {
      title: '涨跌幅',
      dataIndex: 'price_change',
      filterable: {
        filters: [
          {
            text: '正', // 涨跌幅大于 0
            value: 'positive',
          },
          {
            text: '负', // 涨跌幅小于 0
            value: 'negative',
          },
        ],
        filter: (value, record) => {
          // 处理值为数组的情况
          if (Array.isArray(value)) {
            return value.some((v) =>
              filterByPriceChange(v, record.price_change)
            );
          }
          return filterByPriceChange(value, record.price_change);
        },
      },
    },
    {
      title: '最高',
      dataIndex: 'highest_price',
    },
    {
      title: '最低',
      dataIndex: 'lowest_price',
    },
    {
      title: '成交量',
      dataIndex: 'volume',
    },
    {
      title: '成交额',
      dataIndex: 'turnover',
    },
    {
      title: '昨收盘价',
      dataIndex: 'previous_close_price',
    },
    // {
    //   title: '操作',
    //   dataIndex: 'operations',
    //   slotName: 'operations',
    // },
  ]);
  // const productOptions = computed<SelectOptionData[]>(() => [
  //   {
  //     label: 'HBEA',
  //     value: 'HBEA',
  //   },
  //   {
  //     label: 'HBEA2022',
  //     value: 'HBEA2022',
  //   },
  // ]);
  // 缓存键
  const CACHE_KEY = 'hb_carbon_market_data';
  // 提交查询请求
  const fetchData = async (params: CarbonMarketParams) => {
    setLoading(true);
    try {
      // 检查是否存在缓存的数据
      const cachedData = localStorage.getItem(CACHE_KEY);
      if (cachedData && params.dateRange.length < 2) {
        Notification.info({
          id: 'cache',
          title: 'Info',
          content: '正在加载缓存数据',
          duration: 1000,
        });
        const parsedData = JSON.parse(cachedData);
        // 短暂延时以便用户看到加载提示
        // eslint-disable-next-line no-promise-executor-return
        // await new Promise((resolve) => setTimeout(resolve, 2000));
        // 如果缓存存在，可以根据需求决定是否直接返回，或者进行进一步处理
        renderData.value = parsedData.items;
        setLoading(false);
        return;
      }

      Notification.info({
        id: 'request',
        title: 'Info',
        content: '正在请求最新数据',
      });
      // 无缓存发送请求
      const { data } = await queryHubeiList(params);

      // 将返回数据缓存到 localStorage
      localStorage.setItem(CACHE_KEY, JSON.stringify(data));

      renderData.value = data.items;
      Notification.success({
        id: 'request',
        title: 'Success',
        content: '查询成功',
      });
    } catch (err) {
      errorMessage.value = (err as Error).message;
      Notification.error({
        id: 'request',
        title: 'Error',
        content: errorMessage.value,
      });
    } finally {
      setLoading(false);
    }
  };

  const search = () => {
    fetchData({
      // ...basePagination,
      ...formModel.value,
    } as unknown as CarbonMarketParams);
  };
  // const onPageChange = (current: number) => {
  //   fetchData({ ...basePagination, current });
  // };

  fetchData({
    // ...basePagination,
    ...formModel.value,
  } as unknown as CarbonMarketParams);

  const reset = () => {
    // 清空表单
    formModel.value = generateFormModel();
    // 清楚查询缓存
    localStorage.removeItem(CACHE_KEY);
    Notification.warning({
      title: '注意',
      content: '已重置查询条件及缓存',
    });
  };

  const handleSelectDensity = (
    val: string | number | Record<string, any> | undefined,
    e: Event
  ) => {
    size.value = val as SizeProps;
  };

  const handleChange = (
    checked: boolean | (string | boolean | number)[],
    column: Column,
    index: number
  ) => {
    if (!checked) {
      cloneColumns.value = showColumns.value.filter(
        (item) => item.dataIndex !== column.dataIndex
      );
    } else {
      cloneColumns.value.splice(index, 0, column);
    }
  };

  const exchangeArray = <T extends Array<any>>(
    array: T,
    beforeIdx: number,
    newIdx: number,
    isDeep = false
  ): T => {
    const newArray = isDeep ? cloneDeep(array) : array;
    if (beforeIdx > -1 && newIdx > -1) {
      // 先替换后面的，然后拿到替换的结果替换前面的
      newArray.splice(
        beforeIdx,
        1,
        newArray.splice(newIdx, 1, newArray[beforeIdx]).pop()
      );
    }
    return newArray;
  };

  const popupVisibleChange = (val: boolean) => {
    if (val) {
      nextTick(() => {
        const el = document.getElementById('tableSetting') as HTMLElement;
        const sortable = new Sortable(el, {
          onEnd(e: any) {
            const { oldIndex, newIndex } = e;
            exchangeArray(cloneColumns.value, oldIndex, newIndex);
            exchangeArray(showColumns.value, oldIndex, newIndex);
          },
        });
      });
    }
  };

  watch(
    () => columns.value,
    (val) => {
      cloneColumns.value = cloneDeep(val);
      cloneColumns.value.forEach((item, index) => {
        item.checked = true;
      });
      showColumns.value = cloneDeep(cloneColumns.value);
    },
    { deep: true, immediate: true }
  );

  // 上传文件的自定义请求处理逻辑
  const handleUpload = async (option: any) => {
    setLoading(true);
    try {
      const { fileItem } = option;
      Notification.success({
        id: 'upload',
        title: 'Success',
        content: '文件上传成功',
      });
      // 调用封装的 API 函数进行文件上传
      const res = await uploadHubeiFile(fileItem);
      // eslint-disable-next-line no-console
      // console.log(res);
      if (res.code === 200) {
        if (res.data) {
          Notification.success({
            id: 'upload',
            title: 'Success',
            content: `更新${res.data.file_size}条数据`,
          });
        } else {
          Notification.warning({
            id: 'upload',
            title: 'Warning',
            content: '无数据更新',
          });
        }
      }
    } catch (err) {
      errorMessage.value = (err as Error).message;
      Notification.error({
        id: 'upload',
        title: 'Error',
        content: errorMessage.value,
        duration: 5000,
      });
    }
    setLoading(false);
  };
</script>

<script lang="ts">
  export default {
    name: 'SearchTable',
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px 20px;
  }

  :deep(.arco-table-th) {
    &:last-child {
      .arco-table-th-item-title {
        margin-left: 16px;
      }
    }
  }

  .action-icon {
    margin-left: 12px;
    cursor: pointer;
  }

  .active {
    color: #0960bd;
    background-color: #e3f4fc;
  }

  .setting {
    display: flex;
    align-items: center;
    width: 150px;

    .title {
      margin-left: 12px;
      cursor: pointer;
    }
  }
</style>
