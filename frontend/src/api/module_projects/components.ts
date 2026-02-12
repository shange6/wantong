import request from "@/utils/request";

const API_PATH = "/projects/components";

export interface ComponentsQuery {
  page_no?: number;
  page_size?: number;
  project_code?: string;
  wtcode?: string;
  code?: string;
  spec?: string;
  material?: string;
  remark?: string;
}

export interface ComponentsForm {
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

export interface ComponentsData {
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
  created_time: string;
  updated_time: string;
}

export class ComponentsAPI {
  static getList(params: ComponentsQuery) {
    return request({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  }

  static create(data: ComponentsForm) {
    return request({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  }

  static update(id: number, data: Partial<ComponentsForm>) {
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

export default ComponentsAPI;
