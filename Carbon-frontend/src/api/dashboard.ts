import axios from 'axios';
import type { TableData } from '@arco-design/web-vue/es/table/interface';
import {
  BJCarbonMarketRecord,
  GDCarbonMarketRecord,
  HBCarbonMarketRecord,
  TJCarbonMarketRecord,
} from '@/api/list';

// 折线图数据
export interface ContentDataRecord {
  x: Date;
  y: number;
}

export interface ContentDataRecordListRes {
  total: number;
  items: ContentDataRecord[];
}

// 饼图数据
export interface PieDataRecord {
  market: string;
  count: number;
}
export interface PieDataRecordListRes {
  total: number;
  items: PieDataRecord[];
}

// 获取湖北的日期碳价格数据
export function queryContentDataHb() {
  return axios.get<ContentDataRecordListRes[]>(
    '/api/carbon_market/content-data/hb'
  );
}

// 获取广东的日期碳价格数据
export function queryContentDataGd() {
  return axios.get<ContentDataRecordListRes[]>(
    '/api/carbon_market/content-data/gd'
  );
}

// 获取天津的日期碳价格数据
export function queryContentDataTj() {
  return axios.get<ContentDataRecordListRes[]>(
    '/api/carbon_market/content-data/tj'
  );
}

// 获取北京的日期碳价格数据
export function queryContentDataBj() {
  return axios.get<ContentDataRecordListRes[]>(
    '/api/carbon_market/content-data/bj'
  );
}

// 定义通用的 CarbonMarketRecord 类型
export type CarbonMarketRecord =
  | HBCarbonMarketRecord
  | GDCarbonMarketRecord
  | TJCarbonMarketRecord
  | BJCarbonMarketRecord;

export interface PopularRecord {
  total: number;
  items: CarbonMarketRecord[];
}

export function queryPopularList() {
  return axios.get<PopularRecord[]>('/api/carbon_market/latest');
}

export function queryAllCarbonMarketList() {
  return axios.get<PieDataRecordListRes[]>('/api/carbon_market/carbon_count');
}
