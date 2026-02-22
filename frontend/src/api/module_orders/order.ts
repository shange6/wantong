import request from "@/utils/request";
import { AxiosInterceptorManager } from "axios";

const MODULE_API_PREFIX = "/orders/orders";

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
  blanking?: Date;
  rivetweld?: Date;
  machine?: Date;
  fitting?: Date;
  painting?: Date;
  created_time: Date;
  updated_time: Date;
  [key: string]: any;
}

export interface OrdersPageQuery extends OrdersFilter {
  page_no: number;
  page_size: number;
}

class OrdersAPI {
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
