import request from "@/utils/request";

const API_PATH = "/projects/parts";

export interface PartsQuery {
  page_no?: number;
  page_size?: number;
  project_code?: string;
  component_wtcode?: string;
  wtcode?: string;
  code?: string;
  spec?: string;
  material?: string;
  remark?: string;
}

export interface PartsForm {
  id?: number;
  project_code: string;
  parent_code: string;
  wtcode: string;
  code: string;
  spec: string;
  count: number;
  material: string;
  unit_mass: number;
  total_mass: number;
  remark: string;
}

export interface PartsData {
  id: number;
  project_code: string;
  parent_code: string;
  wtcode: string;
  code: string;
  spec: string;
  count: number;
  material: string;
  unit_mass: number;
  total_mass: number;
  remark: string;
  children?: PartsData[];
  created_time: string;
  updated_time: string;
}

export class PartsAPI {
  static getList(params: PartsQuery) {
    return request({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  }

  static create(data: PartsForm) {
    return request({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  }

  static update(id: number, data: Partial<PartsForm>) {
    return request({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data,
    });
  }

  static delete(ids: number[]) {
    return request({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  }
}

export default PartsAPI;
