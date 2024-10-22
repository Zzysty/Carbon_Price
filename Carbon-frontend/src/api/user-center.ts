import axios from 'axios';
import { getToken } from '@/utils/auth';

export interface MyProjectRecord {
  id: number;
  name: string;
  description: string;
  peopleNumber: number;
  contributors: {
    name: string;
    email: string;
    avatar: string;
  }[];
}

export function queryMyProjectList() {
  return axios.post('/api/user/my-project/list');
}

export interface MyTeamRecord {
  id: number;
  avatar: string;
  name: string;
  peopleNumber: number;
}

export function queryMyTeamList() {
  return axios.post('/api/user/my-team/list');
}

export interface LatestActivity {
  id: number;
  title: string;
  description: string;
  avatar: string;
}

export function queryLatestActivity() {
  return axios.post<LatestActivity[]>('/api/user/latest-activity');
}

// 更新用户基本信息
export interface BasicInfoModel {
  username: string;
  gender: string;
  email: string;
  phone: string;
  description: string;
  user_role: string;
}

export function updateUserInfo(data: BasicInfoModel) {
  return axios.put<BasicInfoModel>('/api/user/update', data);
}

export interface EnterpriseCertificationModel {
  accountType: number;
  status: number;
  time: string;
  legalPerson: string;
  certificateType: string;
  authenticationNumber: string;
  enterpriseName: string;
  enterpriseCertificateType: string;
  organizationCode: string;
}

export type CertificationRecord = Array<{
  certificationType: number;
  certificationContent: string;
  status: number;
  time: string;
}>;

export interface UnitCertification {
  enterpriseInfo: EnterpriseCertificationModel;
  record: CertificationRecord;
}

export function queryCertification() {
  return axios.post<UnitCertification>('/api/user/certification');
}

export function userUploadApi(
  data: FormData,
) {
  const token = getToken();
  if (!token) {
    throw new Error('Token is not available');
  }
  return axios.post('/api/user/upload', data, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'Authorization': `Bearer ${token}`,
    },
  });
}
