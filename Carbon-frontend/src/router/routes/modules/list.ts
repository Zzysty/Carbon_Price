import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const LIST: AppRouteRecordRaw = {
  path: '/list',
  name: 'list',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.list',
    requiresAuth: true,
    icon: 'icon-list',
    order: 2,
  },
  children: [
    {
      path: 'search-table-hb', // The midline path complies with SEO specifications
      name: 'SearchTableHB',
      component: () => import('@/views/list/search-table/index.vue'),
      meta: {
        locale: 'menu.list.Hubei',
        requiresAuth: true,
        roles: ['*'],
      },
    },
    {
      path: 'search-table-gd', // The midline path complies with SEO specifications
      name: 'SearchTableGD',
      component: () => import('@/views/list/search-table/guangdong.vue'),
      meta: {
        locale: 'menu.list.Guangdong',
        requiresAuth: true,
        roles: ['*'],
      },
    },
    {
      path: 'search-table-tj', // The midline path complies with SEO specifications
      name: 'SearchTableTJ',
      component: () => import('@/views/list/search-table/tianjin.vue'),
      meta: {
        locale: 'menu.list.Tianjin',
        requiresAuth: true,
        roles: ['*'],
      },
    },
    {
      path: 'search-table-bj', // The midline path complies with SEO specifications
      name: 'SearchTableBJ',
      component: () => import('@/views/list/search-table/beijing.vue'),
      meta: {
        locale: 'menu.list.Beijing',
        requiresAuth: true,
        roles: ['*'],
      },
    },
    {
      path: 'search-table-other', // The midline path complies with SEO specifications
      name: 'SearchTableOther',
      component: () => import('@/views/list/search-table/factors.vue'),
      meta: {
        locale: 'menu.list.Factors',
        requiresAuth: true,
        roles: ['*'],
      },
    }
    // {
    //   path: 'card',
    //   name: 'Card',
    //   component: () => import('@/views/list/card/index.vue'),
    //   meta: {
    //     locale: 'menu.list.cardList',
    //     requiresAuth: true,
    //     roles: ['*'],
    //   },
    // },
  ],
};

export default LIST;
