<template>
  <a-spin :loading="loading" style="width: 100%">
    <a-card
      class="general-card"
      :header-style="{ paddingBottom: '0' }"
      :body-style="{
        padding: '20px',
      }"
    >
      <template #title>
        {{ $t('workplace.categoriesPercent') }}
      </template>
      <Chart height="300px" :option="chartOption" />
    </a-card>
  </a-spin>
</template>

<script lang="ts" setup>
  import useLoading from '@/hooks/loading';
  import useChartOption from '@/hooks/chart-option';
  import { PieDataRecord, queryAllCarbonMarketList } from '@/api/dashboard';
  import { ref } from 'vue';

  const { loading, setLoading } = useLoading();
  const pieData = ref<PieDataRecord[]>([]);
  const carbonTotal = ref<number>(0);
  const { chartOption } = useChartOption((isDark) => {
    // echarts support https://echarts.apache.org/zh/theme-builder.html
    // It's not used here
    // 定义颜色数组，为每个市场设置不同的颜色
    const colors = isDark
      ? ['#3D72F6', '#A079DC', '#6CAAF5', '#F2994A', '#56CCF2']
      : ['#249EFF', '#313CA9', '#21CCFF', '#4BC0C0', '#36A2EB'];

    return {
      legend: {
        left: 'center',
        data: pieData.value.map((item) => item.market),
        bottom: 0,
        icon: 'circle',
        itemWidth: 8,
        textStyle: {
          color: isDark ? 'rgba(255, 255, 255, 0.7)' : '#4E5969',
        },
        itemStyle: {
          borderWidth: 0,
        },
      },
      tooltip: {
        show: true,
        trigger: 'item',
      },
      graphic: {
        elements: [
          {
            type: 'text',
            left: 'center',
            top: '40%',
            style: {
              text: '数据总量',
              textAlign: 'center',
              fill: isDark ? '#ffffffb3' : '#4E5969',
              fontSize: 14,
            },
          },
          {
            type: 'text',
            left: 'center',
            top: '50%',
            style: {
              text: carbonTotal.value.toLocaleString(),
              textAlign: 'center',
              fill: isDark ? '#ffffffb3' : '#1D2129',
              fontSize: 16,
              fontWeight: 500,
            },
          },
        ],
      },
      series: [
        {
          type: 'pie',
          radius: ['50%', '70%'],
          center: ['50%', '50%'],
          label: {
            formatter: '{d}%',
            fontSize: 14,
            color: isDark ? 'rgba(255, 255, 255, 0.7)' : '#4E5969',
          },
          itemStyle: {
            borderColor: isDark ? '#232324' : '#fff',
            borderWidth: 1,
          },
          data: pieData.value.map((item, index) => ({
            value: item.count,
            name: item.market,
            itemStyle: {
              color: colors[index % colors.length], // 根据市场索引设置不同的颜色
            },
          })),
          // data: [
          //   {
          //     value: [148564],
          //     name: '纯文本',
          //     itemStyle: {
          //       color: isDark ? '#3D72F6' : '#249EFF',
          //     },
          //   },
          //   {
          //     value: [334271],
          //     name: '图文类',
          //     itemStyle: {
          //       color: isDark ? '#A079DC' : '#313CA9',
          //     },
          //   },
          //   {
          //     value: [445694],
          //     name: '视频类',
          //     itemStyle: {
          //       color: isDark ? '#6CAAF5' : '#21CCFF',
          //     },
          //   },
          // ],
        },
      ],
    };
  });

  const fetchData = async () => {
    setLoading(true);
    try {
      const { data: pData } = await queryAllCarbonMarketList();
      // eslint-disable-next-line no-console
      // console.log(data);
      if (pData) {
        // 适配后端返回的数据
        carbonTotal.value = pData.total; // 设置总数据条数
        pieData.value = pData.items; // 设置饼图数据
      }
    } catch (err) {
      // you can report use errorHandler or other
    } finally {
      setLoading(false);
    }
  };
  fetchData();
</script>

<style scoped lang="less"></style>
