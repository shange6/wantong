<template>
  <div v-loading="loading" class="components-table">
    <MiddleTable
      v-bind="$attrs"
      :data="displayData"
      :current-page="currentPage"
      :page-size="pageSize"
      @update:current-page="handlePageUpdate"
      @update:page-size="handleSizeUpdate"
    >
      <template #append-columns>
        <el-table-column type="selection" fixed min-width="30" align="center" />
        <el-table-column label="万通码" prop="wtcode" min-width="100" show-overflow-tooltip />
        <el-table-column label="代号" prop="code" min-width="120" show-overflow-tooltip />
        <el-table-column label="名称" prop="spec" min-width="120" show-overflow-tooltip />
        <el-table-column label="数量" prop="count" min-width="50" align="center" />
        <el-table-column label="材料" prop="material" min-width="120" show-overflow-tooltip align="center" />
        <el-table-column label="单重" prop="unit_mass" min-width="70" align="center" />
        <el-table-column label="总重" prop="total_mass" min-width="80" align="center" />
        <el-table-column label="备注" prop="remark" min-width="100" show-overflow-tooltip />
        <el-table-column fixed="right" label="操作" align="center" min-width="60">
          <template #default="scope">
            <el-button
              v-hasPerm="['module_orders:order:update']"
              type="primary"
              size="small"
              link
              icon="edit"
              @click="handleOpenDialog(scope.row)"
            >
              编辑
            </el-button>
          </template>
        </el-table-column>
        <slot name="operation-column"></slot>
      </template>
    </MiddleTable>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="720px"
      @close="handleCloseDialog"
    >
      <el-descriptions :column="5" border>
        <el-descriptions-item
          label="万通码"
          :span="4"
          label-class-name="item-label"
          class-name="item-content"
        >
          <el-text type="primary" bold>{{ selectedRow?.wtcode || "-" }}</el-text>
        </el-descriptions-item>
        <el-descriptions-item label="数量" label-class-name="item-label" class-name="item-content">
          <el-text type="primary" bold>{{ selectedRow?.count ?? "-" }}</el-text>
        </el-descriptions-item>
        <el-descriptions-item
          label="代号"
          :span="4"
          label-class-name="item-label"
          class-name="item-content"
        >
          <el-text type="primary" bold>{{ selectedRow?.code || "-" }}</el-text>
        </el-descriptions-item>
        <el-descriptions-item label="材料" label-class-name="item-label" class-name="item-content">
          <el-text type="primary" bold>{{ selectedRow?.material || "-" }}</el-text>
        </el-descriptions-item>
        <el-descriptions-item
          label="名称"
          :span="4"
          label-class-name="item-label"
          class-name="item-content"
        >
          <el-text type="primary" bold>{{ selectedRow?.spec || "-" }}</el-text>
        </el-descriptions-item>
        <el-descriptions-item label="单重" label-class-name="item-label" class-name="item-content">
          <el-text type="primary" bold>{{ selectedRow?.unit_mass ?? "-" }}</el-text>
        </el-descriptions-item>
        <el-descriptions-item
          label="备注"
          :span="4"
          label-class-name="item-label"
          class-name="item-content"
        >
          <el-text type="primary" bold>{{ selectedRow?.remark || "-" }}</el-text>
        </el-descriptions-item>
        <el-descriptions-item label="总重" label-class-name="item-label" class-name="item-content">
          <el-text type="primary" bold>{{ selectedRow?.total_mass ?? "-" }}</el-text>
        </el-descriptions-item>
      </el-descriptions>
      <hr />
      <hr />
      <el-form ref="formRef" :model="formData" label-width="90px">
        <el-row :gutter="24">
          <el-col :span="5">
            <el-form-item label="是否下料">
              <el-switch v-model="formData.is_blanking" />
            </el-form-item>
          </el-col>
          <el-col :span="9">
            <el-form-item label="下料时间">
              <el-date-picker
                v-model="formData.blanking_time"
                :disabled="!formData.is_blanking"
                type="date"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                placeholder="选择下料时间"
                clearable
              />
            </el-form-item>
          </el-col>
          <el-col :span="9">
            <el-form-item label="下料人员">
              <el-select
                v-model="formData.blanking_user"
                :disabled="!formData.is_blanking"
                placeholder="选择下料人员"
                filterable
                clearable
              >
                <el-option
                  v-for="item in roleUserOptions.blanking"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="5">
            <el-form-item label="是否铆焊">
              <el-switch v-model="formData.is_rivetweld" />
            </el-form-item>
          </el-col>
          <el-col :span="9">
            <el-form-item label="铆焊时间">
              <el-date-picker
                v-model="formData.rivetweld_time"
                :disabled="!formData.is_rivetweld"
                type="date"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                placeholder="选择铆焊时间"
                clearable
              />
            </el-form-item>
          </el-col>
          <el-col :span="9">
            <el-form-item label="铆焊人员">
              <el-select
                v-model="formData.rivetweld_user"
                :disabled="!formData.is_rivetweld"
                placeholder="选择铆焊人员"
                filterable
                clearable
              >
                <el-option
                  v-for="item in roleUserOptions.rivetweld"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="5">
            <el-form-item label="是否机加">
              <el-switch v-model="formData.is_machine" />
            </el-form-item>
          </el-col>
          <el-col :span="9">
            <el-form-item label="机加时间">
              <el-date-picker
                v-model="formData.machine_time"
                :disabled="!formData.is_machine"
                type="date"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                placeholder="选择机加时间"
                clearable
              />
            </el-form-item>
          </el-col>
          <el-col :span="9">
            <el-form-item label="机加人员">
              <el-select
                v-model="formData.machine_user"
                :disabled="!formData.is_machine"
                placeholder="选择机加人员"
                filterable
                clearable
              >
                <el-option
                  v-for="item in roleUserOptions.machine"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="5">
            <el-form-item label="是否装配">
              <el-switch v-model="formData.is_fitting" />
            </el-form-item>
          </el-col>
          <el-col :span="9">
            <el-form-item label="装配时间">
              <el-date-picker
                v-model="formData.fitting_time"
                :disabled="!formData.is_fitting"
                type="date"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                placeholder="选择装配时间"
                clearable
              />
            </el-form-item>
          </el-col>
          <el-col :span="9">
            <el-form-item label="装配人员">
              <el-select
                v-model="formData.fitting_user"
                :disabled="!formData.is_fitting"
                placeholder="选择装配人员"
                filterable
                clearable
              >
                <el-option
                  v-for="item in roleUserOptions.fitting"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="5">
            <el-form-item label="是否喷漆">
              <el-switch v-model="formData.is_painting" />
            </el-form-item>
          </el-col>
          <el-col :span="9">
            <el-form-item label="喷漆时间">
              <el-date-picker
                v-model="formData.painting_time"
                :disabled="!formData.is_painting"
                type="date"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                placeholder="选择喷漆时间"
                clearable
              />
            </el-form-item>
          </el-col>
          <el-col :span="9">
            <el-form-item label="喷漆人员">
              <el-select
                v-model="formData.painting_user"
                :disabled="!formData.is_painting"
                placeholder="选择喷漆人员"
                filterable
                clearable
              >
                <el-option
                  v-for="item in roleUserOptions.painting"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import MiddleTable from "@/views/module_projects/MiddleTable.vue";
import OrdersAPI from "@/api/module_orders/order";
import RoleAPI from "@/api/module_system/role";

defineOptions({
  name: "OrdersTable",
  inheritAttrs: false,
});

interface Props {
  data?: any[];
  queryParams?: Record<string, any>;
  currentPage?: number;
  pageSize?: number;
}

const props = withDefaults(defineProps<Props>(), {
  queryParams: () => ({}),
  currentPage: 1,
  pageSize: 10,
});

const emit = defineEmits<{
  (e: "update:currentPage", val: number): void;
  (e: "update:pageSize", val: number): void;
  (e: "load-data", data: any[]): void;
}>();

type UnOrdersItem = {
  id?: number;
  wtcode: string;
  code?: string;
  spec?: string;
  count?: number;
  material?: string;
  unit_mass?: number;
  total_mass?: number;
  remark?: string;
};

type RoleUserOption = {
  label: string;
  value: string;
};

type OrderProcessForm = {
  wtcode: string;
  is_blanking?: boolean;
  blanking_time?: string;
  blanking_user?: string;
  is_rivetweld?: boolean;
  rivetweld_time?: string;
  rivetweld_user?: string;
  is_machine?: boolean;
  machine_time?: string;
  machine_user?: string;
  is_fitting?: boolean;
  fitting_time?: string;
  fitting_user?: string;
  is_painting?: boolean;
  painting_time?: string;
  painting_user?: string;
};

const loading = ref(false);
const submitLoading = ref(false);
const internalData = ref<UnOrdersItem[]>([]);
const displayData = computed<UnOrdersItem[]>(() => {
  // 优先使用父组件传递的数据（支持空数组，用于显示搜索无结果）
  // 仅当 props.data 为 undefined 时，才使用内部数据
  if (props.data !== undefined) {
    return props.data;
  }
  return internalData.value;
});

/**
 * 请求 API 数据
 * @param params 查询对象
 */
const handleQuery = async (params?: Record<string, any>) => {
  loading.value = true;
  try {
    const query = {
      page_no: props.currentPage,
      page_size: props.pageSize,
      ...(props.queryParams || {}),
      ...(params || {}),
    };
    const res = await OrdersAPI.getUnOrdersList(query);
    internalData.value = res.data?.data?.items || res.data?.items || [];
    emit("load-data", internalData.value);
  } catch (error) {
    console.error("获取待办工单列表失败:", error);
    internalData.value = [];
  } finally {
    loading.value = false;
  }
};

// 事件转发逻辑
const handlePageUpdate = (val: number) => emit("update:currentPage", val);
const handleSizeUpdate = (val: number) => emit("update:pageSize", val);

// 暴露刷新方法给父组件
defineExpose({
  handleQuery,
});

const dialogVisible = ref(false);
const dialogTitle = ref("创建工单");
const formRef = ref();
const selectedRow = ref<UnOrdersItem | null>(null);
const roleUserOptions = ref<Record<string, RoleUserOption[]>>({
  blanking: [],
  rivetweld: [],
  machine: [],
  fitting: [],
  painting: [],
});

const initialFormData: OrderProcessForm = {
  wtcode: "",
  is_blanking: false,
  blanking_time: "",
  blanking_user: "",
  is_rivetweld: false,
  rivetweld_time: "",
  rivetweld_user: "",
  is_machine: false,
  machine_time: "",
  machine_user: "",
  is_fitting: false,
  fitting_time: "",
  fitting_user: "",
  is_painting: false,
  painting_time: "",
  painting_user: "",
};

const formData = ref<OrderProcessForm>({ ...initialFormData });

async function loadRoleUsers() {
  const roleNameMap: Record<string, string> = {
    blanking: "下料班长",
    rivetweld: "铆焊班长",
    machine: "机加班长",
    fitting: "装配班长",
    painting: "喷漆班长",
  };
  await Promise.all(
    Object.entries(roleNameMap).map(async ([key, roleName]) => {
      if (roleUserOptions.value[key]?.length) {
        return;
      }
      const res = await RoleAPI.listRoleUsers({ role_name: roleName });
      const list = res.data?.data || res.data || [];
      roleUserOptions.value[key] = list.map((item: { name: string }) => ({
        label: item.name,
        value: item.name,
      }));
    })
  );
}

async function handleOpenDialog(row: UnOrdersItem) {
  selectedRow.value = row;
  formData.value = { ...initialFormData, wtcode: row.wtcode };
  await loadRoleUsers();
  dialogVisible.value = true;
}

function handleCloseDialog() {
  dialogVisible.value = false;
  formData.value = { ...initialFormData };
  selectedRow.value = null;
}

async function handleSubmit() {
  if (!formData.value.wtcode) {
    ElMessage.warning("缺少万通码");
    return;
  }
  submitLoading.value = true;
  try {
    await OrdersAPI.create(formData.value);
    ElMessage.success("保存成功");
    handleCloseDialog();
    await handleQuery();
  } catch (error) {
    console.error(error);
  } finally {
    submitLoading.value = false;
  }
}

onMounted(() => {
  handleQuery();
});
</script>

<style scoped>
.components-table {
  flex: 1;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

:deep(.item-label) {
  width: 70px !important; /* 固定标签宽度 */
  text-align: right !important; /* 文字居中 */
}
</style>
