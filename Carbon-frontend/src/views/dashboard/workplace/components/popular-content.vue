<template>
  <a-spin :loading="loading" style="width: 100%">
    <a-card
      class="general-card"
      :header-style="{ paddingBottom: '0' }"
      :body-style="{ padding: '17px 20px 21px 20px' }"
    >
      <template #title> 各市场最新成交情况</template>
      <a-space direction="vertical" :size="10" fill>
        <a-table
          :data="renderList"
          :pagination="false"
          :bordered="false"
          :scroll="{ x: '100%', y: '264px' }"
        >
          <template #columns>
            <a-table-column title="市场" data-index="market" />
            <a-table-column title="日期" data-index="date"></a-table-column>
            <a-table-column
              title="成交价格"
              data-index="price"
            ></a-table-column>
            <a-table-column title="成交量" data-index="volume"></a-table-column>
            <a-table-column
              title="成交额"
              data-index="turnover"
            ></a-table-column>
            <a-table-column
              title="日涨幅"
              data-index="price_change"
              :sortable="{
                sortDirections: ['ascend', 'descend'],
              }"
            >
              <template #cell="{ record }">
                <div class="increases-cell">
                  <span v-if="record.price_change">
                    {{ record.price_change }}%
                  </span>
                  <icon-caret-up
                    v-if="record.price_change > 0"
                    style="color: #f53f3f; font-size: 8px"
                  />
                  <icon-caret-down
                    v-if="record.price_change < 0"
                    style="color: #0ad3d3; font-size: 8px"
                  />
                </div>
              </template>
            </a-table-column>
          </template>
        </a-table>
      </a-space>
      <!--      <a-list>-->
      <!--        &lt;!&ndash; 使用 v-for 循环渲染市场数据 &ndash;&gt;-->
      <!--        <a-list-item v-for="(market, index) in marketList" :key="index">-->
      <!--          <a-row class="grid-demo" justify="space-between">-->
      <!--            <a-col :span="4">-->
      <!--              <a-typography-title :heading="4" bold-->
      <!--                >{{ market.name }}-->
      <!--              </a-typography-title>-->
      <!--            </a-col>-->
      <!--            <a-col :span="4">-->
      <!--              <a-statistic-->
      <!--                :title="market.priceTitle"-->
      <!--                :value="market.price"-->
      <!--                :precision="2"-->
      <!--                show-group-separator-->
      <!--                animation-->
      <!--              ></a-statistic>-->
      <!--            </a-col>-->
      <!--            <a-col :span="4">-->
      <!--              <a-statistic-->
      <!--                title="成交量"-->
      <!--                :value="market.volume"-->
      <!--                show-group-separator-->
      <!--                animation-->
      <!--              ></a-statistic>-->
      <!--            </a-col>-->
      <!--            <a-col :span="6">-->
      <!--              <a-statistic-->
      <!--                title="成交额"-->
      <!--                :value="market.turnover"-->
      <!--                :precision="2"-->
      <!--                show-group-separator-->
      <!--                animation-->
      <!--              ></a-statistic>-->
      <!--            </a-col>-->
      <!--            <a-col v-if="market.showChange" :span="4">-->
      <!--              <a-statistic-->
      <!--                title="涨跌幅"-->
      <!--                :value="market.changeValue * 100"-->
      <!--                :precision="2"-->
      <!--                animation-->
      <!--                :value-style="{ color: market.changeColor }"-->
      <!--              >-->
      <!--                &lt;!&ndash; 动态选择上升或下降图标 &ndash;&gt;-->
      <!--                <template #prefix>-->
      <!--                  <icon-arrow-rise v-if="market.changeValue > 0" />-->
      <!--                  <icon-arrow-fall v-else />-->
      <!--                </template>-->
      <!--                <template #suffix>%</template>-->
      <!--              </a-statistic>-->
      <!--            </a-col>-->
      <!--          </a-row>-->
      <!--        </a-list-item>-->
      <!--      </a-list>-->
    </a-card>
  </a-spin>
</template>

<script lang="ts" setup>
  import { ref } from 'vue';
  import useLoading from '@/hooks/loading';
  import { queryPopularList } from '@/api/dashboard';
  import { TableData } from '@arco-design/web-vue/es/table/interface';

  const { loading, setLoading } = useLoading();
  const renderList = ref<TableData[]>();

  const fetchData = async () => {
    try {
      setLoading(true);
      const { data } = await queryPopularList();
      // eslint-disable-next-line no-console
      console.log(data.items);
      renderList.value = data.items;
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  fetchData();
</script>

<style scoped lang="less">
  .general-card {
    min-height: 100%;
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
