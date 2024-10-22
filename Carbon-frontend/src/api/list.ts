import axios from 'axios';
import type { DescData } from '@arco-design/web-vue/es/descriptions/interface';
import { Notification } from '@arco-design/web-vue';

// 外部因素
export interface OtherFactorsRecord {
  id: string;
  date: Date;
  gas_price: number;
  coal_price: number;
  oil_price: number;
  hs300: number;
  aql_sh: number;
  aql_gd: number;
  aql_hb: number;
  si: number;
  eua_price: number;
}

// 湖北碳市场数据类型
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

// 广东碳市场数据类型
export interface GDCarbonMarketRecord {
  id: string;
  date: Date;
  product: string;
  opening_price: number;
  closing_price: number;
  highest_price: number;
  lowest_price: number;
  price_change: number;
  price_change_percentage: number;
  volume: number;
  turnover: number;
}

// 天津碳市场数据类型
export interface TJCarbonMarketRecord {
  id: string;
  date: Date;
  product: string;
  volume_auction: number;
  volume_daily_summary: number;
  turnover_auction: number;
  turnover_daily_summary: number;
  average_price_auction: number;
}

// 北京碳市场数据类型
export interface BJCarbonMarketRecord {
  id: string;
  date: Date;
  volume: number;
  average_price: number;
  turnover: number;
}

export interface OtherFactorsListRes {
  items: OtherFactorsRecord[];
  total: number;
}

export interface HBCarbonMarketListRes {
  items: HBCarbonMarketRecord[];
  total: number;
}

export interface GDCarbonMarketListRes {
  items: GDCarbonMarketRecord[];
  total: number;
}

export interface TJCarbonMarketListRes {
  items: TJCarbonMarketRecord[];
  total: number;
}

export interface BJCarbonMarketListRes {
  items: BJCarbonMarketRecord[];
  total: number;
}

export interface CarbonMarketParams {
  dateRange?: [string, string] | any;
}

// 请求其他因素数据
export function queryOtherFactorsList(params: CarbonMarketParams) {
  return axios.post<OtherFactorsListRes>('/api/carbon_market/factors', params);
}

// 请求湖北碳市场数据
export function queryHubeiList(params: CarbonMarketParams) {
  return axios.post<HBCarbonMarketListRes>('/api/carbon_market/hb', params);
}

// 请求湖北碳市场数据
export function queryGuangdongList(params: CarbonMarketParams) {
  return axios.post<GDCarbonMarketListRes>('/api/carbon_market/gd', params);
}

// 请求湖北碳市场数据
export function queryTianjinList(params: CarbonMarketParams) {
  return axios.post<TJCarbonMarketListRes>('/api/carbon_market/tj', params);
}

// 请求湖北碳市场数据
export function queryBeijingList(params: CarbonMarketParams) {
  return axios.post<BJCarbonMarketListRes>('/api/carbon_market/bj', params);
}

// 上传外部因素excel
export function uploadOtherFactors(fileItem: any) {
  const formData = new FormData();
  formData.append('file', fileItem.file);
  return axios.post('/api/carbon_market/upload/factors', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
}

// 上传湖北碳市场数据excel
export function uploadHubeiFile(fileItem: any) {
  const formData = new FormData();
  formData.append('file', fileItem.file);
  return axios.post('/api/carbon_market/upload/hb', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
}

// 上传广东碳市场数据excel
export function uploadGuangdongFile(fileItem: any) {
  const formData = new FormData();
  formData.append('file', fileItem.file);
  return axios.post('/api/carbon_market/upload/gd', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
}

// 上传天津碳市场数据excel
export function uploadTianjinFile(fileItem: any) {
  const formData = new FormData();
  formData.append('file', fileItem.file);
  return axios.post('/api/carbon_market/upload/tj', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
}

// 上传北京碳市场数据excel
export function uploadBeijingFile(fileItem: any) {
  const formData = new FormData();
  formData.append('file', fileItem.file);
  return axios.post('/api/carbon_market/upload/bj', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
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
