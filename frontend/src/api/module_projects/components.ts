import request from "@/utils/request";

const API_PATH = "/projects/components";

export interface ComponentsQuery {
  page_no?: number;
  page_size?: number;
  project_code?: string;
  wtcode?: string;
  code?: string;
  name?: string;
}

export interface ComponentsForm {
  id?: number;
  project_code: string;
  parent_code: string;
  wtcode: string;
  code: string;
  name: string;
  count: number;
}

export interface ComponentsData {
  id: number;
  project_code: string;
  parent_code: string;
  wtcode: string;
  code: string;
  name: string;
  count: number;
  created_time: string;
  updated_time: string;
}

class ComponentsAPI {
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
