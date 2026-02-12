import request from "@/utils/request";

const API_PATH = "/projects/datas";

const DatasAPI = {
  uploadFile(formData: FormData) {
    return request<ApiResponse<UploadInnerData>>({
      url: `${API_PATH}/upload`,
      method: "post",
      data: formData,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  saveDatas(payload: any) {
    return request({
      url: `${API_PATH}/savedatas`,
      method: "post",
      data: payload,
    });
  },
};

export default DatasAPI;

// 通用分页查询参数（项目通用，无需修改）
export interface DatasPageQuery {
  page_no?: number;
  page_size?: number;
  code?: string;
  spec?: string;
  material?: string;
  remark?: string;
}

// 表格行数据类型（和Vue表格列prop完全对应，匹配后端res.data.data.data里的字段）
export interface TableItemSchema {
  id?: number; // 前端手动添加的唯一ID（删除用）
  seq?: string;
  wtcode?: string;
  code: string;
  spec: string;
  count: string | number; // 后端返回字符串，前端可转数字
  material: string;
  unit_mass: string | number;
  total_mass: string | number;
  remark?: string;
  x?: number;
  y?: number;
}

// 上传接口的后端内层data类型（匹配res.data.data）
export interface UploadInnerData {
  文件个数: number;
  部件编号: string;
  data: TableItemSchema[]; // 这才是表格真正需要的数组数据
  info: string[];
  文件数量: number;
  项目名称: string;
  合同号: string;
  部件名称: string;
  数量: string;
  零件数量: number;
}

// 上传接口的响应类型（最终匹配axios返回的res结构）
// export type DataUploadResponse = AxiosResponse<ApiResponse<UploadInnerData>>;
