import request from "@/utils/request";

const API_PATH = "/projects/project";

export interface ProjectQuery {
  page_no?: number;
  page_size?: number;
  code?: string;
  name?: string;
  no?: string;
}

export interface ProjectForm {
  id?: number;
  code: string;
  name: string;
  no: string;
}

export interface ProjectData {
  id: number;
  code: string;
  name: string;
  no: string;
  created_time: string;
  updated_time: string;
}

class ProjectAPI {
  static getList(params: ProjectQuery) {
    return request({
      url: `${API_PATH}/list`, 
      method: "get",
      params,
    });
  }

  static create(data: ProjectForm) {
    return request({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  }

  static update(id: number, data: Partial<ProjectForm>) {
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

export default ProjectAPI;
