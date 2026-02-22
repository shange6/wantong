import request from "@/utils/request";

const API_PATH = "/projects/projects";

export interface ProjectsQuery {
  code?: string;
  name?: string;
  no?: string;
}

export interface ProjectsForm {
  id?: number;
  code: string;
  name: string;
  no: string;
}

export interface ProjectsData {
  id: number;
  code: string;
  name: string;
  no: string;
  created_time: string;
  updated_time: string;
}

class ProjectsAPI {
  static getList(params: ProjectsQuery) {
    return request({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  }

  static create(data: ProjectsForm) {
    return request({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  }

  static update(id: number, data: Partial<ProjectsForm>) {
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

export default ProjectsAPI;
