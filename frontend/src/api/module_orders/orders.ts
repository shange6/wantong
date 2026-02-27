import request from "@/utils/request";
import { AxiosInterceptorManager } from "axios";

const MODULE_API_PREFIX = "/orders/order";

export interface OrdersFilter {
  wtcode?: string;
  // Add other filter fields as needed
}

export interface OrdersData {
  id: number;
  wtcode: string;
  components_code: string;
  components_spec: string;
  components_count: number;
  components_material: string;
  components_unit_mass: string;
  components_totle_mass: string;
  components_remark: string;
  is_blanking: boolean;
  blanking_time?: string;
  blanking_user?: string;
  blanking_laborhour?: number;
  is_rivetweld: boolean;
  rivetweld_time?: string;
  rivetweld_user?: string;
  rivetweld_laborhour?: number;
  is_machine: boolean;
  machine_time?: string;
  machine_user?: string;
  machine_laborhour?: number;
  is_fitting: boolean;
  fitting_time?: string;
  fitting_user?: string;
  fitting_laborhour?: number;
  is_painting: boolean; 
  painting_time?: string;
  painting_user?: string;
  painting_laborhour?: number;
  created_time: string;
  updated_time: string;
  [key: string]: any;
}

export interface OrdersPageQuery extends OrdersFilter {
  page_no: number;
  page_size: number;
}

class OrdersAPI {
  static getUnCreateList(params: OrdersPageQuery) {
    // return request<any, { data: { items: OrdersData[]; total: number } }>({
    return request({
      url: `${MODULE_API_PREFIX}/uncreatelist`,
      method: "get",
      params,
    });
  }

  static getUnLaborhourList(params: OrdersPageQuery) {
    return request({
      url: `${MODULE_API_PREFIX}/unlaborhourlist`,
      method: "get",
      params,
    });
  }

  static getList(params: OrdersPageQuery) {
    return request<any, { data: { items: OrdersData[]; total: number } }>({
      url: `${MODULE_API_PREFIX}/list`,
      method: "get",
      params,
    });
  }

  static create(data: any) {
    return request({
      url: `${MODULE_API_PREFIX}/create`,
      method: "post",
      data,
    });
  }

  static update(id: number, data: any) {
    return request({
      url: `${MODULE_API_PREFIX}/update/${id}`,
      method: "put",
      data,
    });
  }

  static delete(ids: number[]) {
    return request({
      url: `${MODULE_API_PREFIX}/delete`,
      method: "delete",
      data: ids, // body for delete? check axios config or backend expectation
      // Usually delete with body needs 'data' property in config
    });
  }
}

export default OrdersAPI;
