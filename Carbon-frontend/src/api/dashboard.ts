import axios from 'axios';
import type { TableData } from '@arco-design/web-vue/es/table/interface';

export interface ContentDataRecord {
  x: Date;
  y: number;
}

export interface ContentDataRecordListRes {
  total: number;
  items: ContentDataRecord[];
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

export interface PopularRecord {
  key: number;
  clickNumber: string;
  title: string;
  increases: number;
}

export function queryPopularList(params: { type: string }) {
  return axios.get<PopularRecord[]>('/api/popular/list', { params });
}
