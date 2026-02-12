import request from "@/utils/request";
import type { AxiosResponse } from "axios";

// 通用分页查询参数（项目通用，无需修改）
export interface DataPageQuery {
  page_no?: number;
  page_size?: number;
  code?: string;
  spec?: string;
  material?: string;
  remark?: string;
}

// 通用API响应体（后端标准封装，匹配你的res.data结构）
export interface ApiResponse<T = any> {
  code: number;
  msg: string;
  data: T;
  status_code: number;
  success: boolean;
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
export type DataUploadResponse = AxiosResponse<ApiResponse<UploadInnerData>>;

const API_PATH = "/orders/data";

export const DataAPI = {
  /**
   * 上传文件
   * @param formData 文件数据
   */
  uploadFile(formData: FormData): Promise<DataUploadResponse> {
    return request({
      url: `${API_PATH}/upload`,
      method: "post",
      data: formData,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  // --- 解析上传文件结果保存到数据库接口 ---
  /**
   * 保存前端数据到数据库
   * @param payload 前端数据
   */
  saveData(payload: any): Promise<ApiResponse> {
    return request({
      url: `${API_PATH}/savedata`,
      method: "post",
      data: payload,
    });
  },
};

export default DataAPI;
