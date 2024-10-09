<template>
  <a-spin :loading="loading" style="width: 100%">
    <a-card
      class="general-card"
      :header-style="{ paddingBottom: '0' }"
      :body-style="{ padding: '17px 20px 21px 20px' }"
    >
      <template #title> 各市场最新成交情况</template>
      <!--      <template #extra>-->
      <!--        <a-link>{{ $t('workplace.viewMore') }}</a-link>-->
      <!--      </template>-->
      <a-list>
        <!-- 使用 v-for 循环渲染市场数据 -->
        <a-list-item v-for="(market, index) in marketList" :key="index">
          <a-row class="grid-demo" justify="space-between">
            <a-col :span="4">
              <a-typography-title :heading="4" bold>{{ market.name }}</a-typography-title>
            </a-col>
            <a-col :span="4">
              <a-statistic
                :title="market.priceTitle"
                :value="market.price"
                :precision="2"
                show-group-separator
                animation
              ></a-statistic>
            </a-col>
            <a-col :span="4">
              <a-statistic
                title="成交量"
                :value="market.volume"
                show-group-separator
                animation
              ></a-statistic>
            </a-col>
            <a-col :span="6">
              <a-statistic
                title="成交额"
                :value="market.turnover"
                :precision="2"
                show-group-separator
                animation
              ></a-statistic>
            </a-col>
            <a-col v-if="market.showChange" :span="4">
              <a-statistic
                title="涨跌幅"
                :value="market.changeValue * 100"
                :precision="2"
                animation
                :value-style="{ color: market.changeColor }"
              >
                <!-- 动态选择上升或下降图标 -->
                <template #prefix>
                  <icon-arrow-rise v-if="market.changeValue > 0" />
                  <icon-arrow-fall v-else />
                </template>
                <template #suffix>%</template>
              </a-statistic>
            </a-col>
          </a-row>
        </a-list-item>
      </a-list>
    </a-card>
  </a-spin>
</template>

<script lang="ts" setup>
  import { computed, ref } from 'vue';
  import useLoading from '@/hooks/loading';
  // eslint-disable-next-line import/namespace
  import { queryPopularList } from '@/api/dashboard';
  import type { TableData } from '@arco-design/web-vue/es/table/interface';

  // 获取当前日期 YY-MM-DD
  // const date = new Date();
  // const currentDate = `${date.getFullYear()}年${
  //   date.getMonth() + 1
  // }月${date.getDate()}日`;

  const { loading, setLoading } = useLoading();
  // 市场数据列表
  const marketList = ref([
    {
      name: '湖北',
      priceTitle: '收盘价',
      price: 0,
      volume: 0,
      turnover: 0,
      changeValue: 0,
      changeColor: '',
      showChange: true,
    },
    {
      name: '广东',
      priceTitle: '收盘价',
      price: 0,
      volume: 0,
      turnover: 0,
      changeValue: 0,
      changeColor: '',
      showChange: true,
    },
    {
      name: '天津',
      priceTitle: '成交均价',
      price: 0,
      volume: 0,
      turnover: 0,
      showChange: false,
    },
    {
      name: '北京',
      priceTitle: '成交均价',
      price: 0,
      volume: 0,
      turnover: 0,
      showChange: false,
    },
  ]);

  // 更新 marketList 数据
  const updateMarketData = (data) => {
    marketList.value[0] = {
      ...marketList.value[0],
      price: data.items[0].latest_price,
      volume: data.items[0].volume,
      turnover: data.items[0].turnover,
      changeValue: data.items[0].price_change,
      changeColor: data.items[0].price_change > 0 ? '#0fbf60' : '#FF3333',
    };
    marketList.value[1] = {
      ...marketList.value[1],
      price: data.items[1].closing_price,
      volume: data.items[1].volume,
      turnover: data.items[1].turnover,
      changeValue: data.items[1].price_change_percentage,
      changeColor: data.items[1].price_change_percentage > 0 ? '#0fbf60' : '#FF3333',
    };
    marketList.value[2] = {
      ...marketList.value[2],
      price: data.items[2].average_price_auction,
      volume: data.items[2].volume_auction,
      turnover: data.items[2].turnover_auction,
    };
    marketList.value[3] = {
      ...marketList.value[3],
      price: data.items[3].average_price,
      volume: data.items[3].volume,
      turnover: data.items[3].turnover,
    };
  };
  const fetchData = async () => {
    try {
      setLoading(true);
      const { data } = await queryPopularList();
      updateMarketData(data);
    } catch (err) {
      // eslint-disable-next-line no-console
      console.log(err);
    } finally {
      setLoading(false);
    }
  };
  fetchData();
</script>

<style scoped lang="less">
  .general-card {
    min-height: 395px;
  }

  :deep(.arco-table-tr) {
    height: 44px;

    .arco-typography {
      margin-bottom: 0;
    }
  }

  .increases-cell {
    display: flex;
    align-items: center;

    span {
      margin-right: 4px;
    }
  }
</style>
