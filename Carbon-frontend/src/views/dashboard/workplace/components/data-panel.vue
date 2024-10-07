<template>
  <a-grid :cols="24" :row-gap="16" class="panel">
    <a-grid-item
      class="panel-col"
      :span="{ xs: 6, sm: 6, md: 6, lg: 6, xl: 6, xxl: 5 }"
    >
      <a-space>
        <a-avatar :size="54" class="col-avatar">
          <img
            alt="avatar"
            src="//p3-armor.byteimg.com/tos-cn-i-49unhts6dw/288b89194e657603ff40db39e8072640.svg~tplv-49unhts6dw-image.image"
          />
        </a-avatar>
        <a-statistic
          :title="$t('workplace.carbonMarket')"
          :value="carbonMarketCount"
          :value-from="0"
          animation
          show-group-separator
        >
          <template #suffix>
            <span class="unit">{{ $t('workplace.pecs') }}</span>
          </template>
        </a-statistic>
      </a-space>
    </a-grid-item>
    <a-grid-item
      class="panel-col"
      :span="{ xs: 18, sm: 18, md: 18, lg: 18, xl: 18, xxl: 19 }"
    >
      <a-space :size="'mini'">
        <a-link href="https://www.hbets.cn/list_51.html" icon>
          湖北碳排放权交易中心
        </a-link>
        <a-divider direction="vertical" />
        <a-link href="https://www.cnemission.com/article/hqxx/" icon>
          广州碳排放权交易中心
        </a-link>
        <a-divider direction="vertical" />
        <a-link href="https://www.chinatcx.com.cn/list/13.html?page=1" icon>
          天津排放权交易所
        </a-link>
        <a-divider direction="vertical" />
        <a-link href="https://www.bjets.com.cn/article/jyxx/?105" icon>
          北京绿色交易所
        </a-link>
      </a-space>
    </a-grid-item>
    <a-grid-item
      class="panel-col"
      :span="{ xs: 6, sm: 6, md: 6, lg: 6, xl: 6, xxl: 5 }"
    >
      <a-space>
        <a-avatar :size="54" class="col-avatar">
          <img
            alt="avatar"
            src="//p3-armor.byteimg.com/tos-cn-i-49unhts6dw/fdc66b07224cdf18843c6076c2587eb5.svg~tplv-49unhts6dw-image.image"
          />
        </a-avatar>
        <a-statistic
          :title="$t('workplace.factor')"
          :value="externalFactorsCount"
          :value-from="0"
          animation
          show-group-separator
        >
          <template #suffix>
            <span class="unit">{{ $t('workplace.pecs') }}</span>
          </template>
        </a-statistic>
      </a-space>
    </a-grid-item>
    <a-grid-item
      class="panel-col"
      :span="{ xs: 18, sm: 18, md: 18, lg: 18, xl: 18, xxl: 18 }"
      style="border-right: none"
    >
      <a-typography-text type="primary">
        能源市场指标(13)
        <a-divider direction="vertical" />
        宏观经济变量(7)
        <a-divider direction="vertical" />
        国际市场溢出效应(1)
        <a-divider direction="vertical" />
        环境指标(1)
        <a-divider direction="vertical" />
        公众情绪(1)
        <a-divider direction="vertical" />
        <a-link href="https://economicpolicyuncertaintyinchina.weebly.com/">
          政策不确定性(4)
        </a-link>
      </a-typography-text>
      <a-typography-text
        :ellipsis="{
          suffix: '',
          rows: 1,
          expandable: true,
        }"
        >Oil Price、NG Price、Coal Price、Brent、NEWC Spot、BOCE
        CC、HS300、INE、Henry Hub、NYMEX NG、ICE NG、Coal Futures、Coking
        Futures.
        <a-divider direction="vertical" />
        STOXX50、USD、DAX、FTSE100、CAC40、DJIA、S&P500.
        <a-divider direction="vertical" />EUA
        <a-divider direction="vertical" />AQI
        <a-divider direction="vertical" />BSI
        <a-divider direction="vertical" />EPU、FPU、TPU、ECPU
      </a-typography-text>
      <a-typography-text type="primary"></a-typography-text>
    </a-grid-item>
    <a-grid-item :span="24">
      <a-divider class="panel-border" />
    </a-grid-item>
  </a-grid>
</template>

<script lang="ts" setup>
  const carbonMarketCount = 4;
  const externalFactorsCount = 29;
</script>

<style lang="less" scoped>
  .arco-grid.panel {
    margin-bottom: 0;
    padding: 16px 20px 0 20px;
  }

  .panel-col {
    padding-left: 43px;
    border-right: 1px solid rgb(var(--gray-2));
  }

  .col-avatar {
    margin-right: 12px;
    background-color: var(--color-fill-2);
  }

  .up-icon {
    color: rgb(var(--red-6));
  }

  .unit {
    margin-left: 8px;
    color: rgb(var(--gray-8));
    font-size: 12px;
  }

  :deep(.panel-border) {
    margin: 4px 0 0 0;
  }
</style>
