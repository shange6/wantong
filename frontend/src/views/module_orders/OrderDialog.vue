<template>
  <el-dialog
    v-model="visible"
    :title="dialogTitle"
    width="720px"
    @close="handleClose"
  >
    <el-descriptions :column="5" border>
      <el-descriptions-item
        label="万通码"
        :span="4"
        label-class-name="item-label"
        class-name="item-content"
      >
        <el-text type="primary" bold>{{ data?.wtcode || "-" }}</el-text>
      </el-descriptions-item>
      <el-descriptions-item label="数量" label-class-name="item-label" class-name="item-content">
        <el-text type="primary" bold>{{ data?.count ?? "-" }}</el-text>
      </el-descriptions-item>
      <el-descriptions-item
        label="代号"
        :span="4"
        label-class-name="item-label"
        class-name="item-content"
      >
        <el-text type="primary" bold>{{ data?.code || "-" }}</el-text>
      </el-descriptions-item>
      <el-descriptions-item label="材料" label-class-name="item-label" class-name="item-content">
        <el-text type="primary" bold>{{ data?.material || "-" }}</el-text>
      </el-descriptions-item>
      <el-descriptions-item
        label="名称"
        :span="4"
        label-class-name="item-label"
        class-name="item-content"
      >
        <el-text type="primary" bold>{{ data?.spec || "-" }}</el-text>
      </el-descriptions-item>
      <el-descriptions-item label="单重" label-class-name="item-label" class-name="item-content">
        <el-text type="primary" bold>{{ data?.unit_mass ?? "-" }}</el-text>
      </el-descriptions-item>
      <el-descriptions-item
        label="备注"
        :span="4"
        label-class-name="item-label"
        class-name="item-content"
      >
        <el-text type="primary" bold>{{ data?.remark || "-" }}</el-text>
      </el-descriptions-item>
      <el-descriptions-item label="总重" label-class-name="item-label" class-name="item-content">
        <el-text type="primary" bold>{{ data?.total_mass ?? "-" }}</el-text>
      </el-descriptions-item>
    </el-descriptions>
    <hr />
    <hr />
    <el-form ref="formRef" :model="formData" label-width="90px">
      <el-row :gutter="24">
        <!-- 下料 -->
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

        <!-- 铆焊 -->
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

        <!-- 机加 -->
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

        <!-- 装配 -->
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

        <!-- 喷漆 -->
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
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确定</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import OrdersAPI from "@/api/module_orders/order";
import RoleAPI from "@/api/module_system/role";
import { ElMessage } from "element-plus";

const props = defineProps<{
  modelValue: boolean;
  data: any | null;
  title?: string;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", val: boolean): void;
  (e: "success"): void;
}>();

const visible = ref(false);
const dialogTitle = ref("创建工单");
const formRef = ref();
const submitLoading = ref(false);

const roleUserOptions = ref<Record<string, any[]>>({
  blanking: [],
  rivetweld: [],
  machine: [],
  fitting: [],
  painting: [],
});

const initialFormData = {
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

const formData = ref({ ...initialFormData });

watch(
  () => props.modelValue,
  (val) => {
    visible.value = val;
    if (val && props.data) {
      // 合并初始数据、万通码以及可能存在的旧工单数据
      formData.value = { 
        ...initialFormData, 
        wtcode: props.data.wtcode,
        ...props.data 
      };
      dialogTitle.value = props.title || (props.data.id ? "编辑工单" : "创建工单");
      loadRoleUsers();
    }
  }
);

watch(
  () => visible.value,
  (val) => {
    emit("update:modelValue", val);
  }
);

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

function handleClose() {
  visible.value = false;
  formData.value = { ...initialFormData };
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
    emit("success");
    handleClose();
  } catch (error) {
    console.error(error);
  } finally {
    submitLoading.value = false;
  }
}
</script>

<style scoped>
:deep(.item-label) {
  width: 70px !important;
  text-align: right !important;
}
</style>
