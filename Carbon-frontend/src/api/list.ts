import axios from 'axios';
import qs from 'query-string';
import type { DescData } from '@arco-design/web-vue/es/descriptions/interface';

export interface HBCarbonMarketRecord {
  id: string;
  product: string;
  date: Date;
  latest_price: number;
  price_change: number;
  highest_price: number;
  lowest_price: number;
  volume: number;
  turnover: number;
  previous_close_price: number;
}

export interface HBCarbonMarketParams {
  current: number;
  pageSize: number;
  dateRange?: [string, string];
}

export interface HBCarbonMarketListRes {
  list: HBCarbonMarketRecord[];
  total: number;
}

export function queryHubeiList(params: HBCarbonMarketParams) {
  return axios.post<HBCarbonMarketListRes>('/api/carbon_market/hb', params);
}

export interface ServiceRecord {
  id: number;
  title: string;
  description: string;
  name?: string;
  actionType?: string;
  icon?: string;
  data?: DescData[];
  enable?: boolean;
  expires?: boolean;
}

export function queryInspectionList() {
  return axios.get('/api/list/quality-inspection');
}

export function queryTheServiceList() {
  return axios.get('/api/list/the-service');
}

export function queryRulesPresetList() {
  return axios.get('/api/list/rules-preset');
}
