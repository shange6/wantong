<template>
  <el-dialog
    v-model="visible"
    :title="dialogTitle"
    width="720px"
    @close="handleClose"
  >
    <ComponentsInfoDialog :data="data" />
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
          <el-form-item label="下料工时">
            <el-input-number
              v-model="formData.blanking_laborhour"
              :disabled="!formData.is_blanking"
              placeholder="输入工时"
              :min="0"
              :precision="0"
              class="w-full"
            />
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
          <el-form-item label="铆焊工时">
            <el-input-number
              v-model="formData.rivetweld_laborhour"
              :disabled="!formData.is_rivetweld"
              placeholder="输入工时"
              :min="0"
              :precision="0"
              class="w-full"
            />
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
          <el-form-item label="机加工时">
            <el-input-number
              v-model="formData.machine_laborhour"
              :disabled="!formData.is_machine"
              placeholder="输入工时"
              :min="0"
              :precision="0"
              class="w-full"
            />
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
          <el-form-item label="装配工时">
            <el-input-number
              v-model="formData.fitting_laborhour"
              :disabled="!formData.is_fitting"
              placeholder="输入工时"
              :min="0"
              :precision="0"
              class="w-full"
            />
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
          <el-form-item label="喷漆工时">
            <el-input-number
              v-model="formData.painting_laborhour"
              :disabled="!formData.is_painting"
              placeholder="输入工时"
              :min="0"
              :precision="0"
              class="w-full"
            />
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
import ComponentsInfoDialog from "./ComponentsInfoDialog.vue";
import OrdersAPI from "@/api/module_orders/orders";
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
const dialogTitle = ref("填写工时");
const formRef = ref();
const submitLoading = ref(false);

const initialFormData = {
  wtcode: "",
  is_blanking: false,
  blanking_time: "",
  blanking_laborhour: 0,
  is_rivetweld: false,
  rivetweld_time: "",
  rivetweld_laborhour: 0,
  is_machine: false,
  machine_time: "",
  machine_laborhour: 0,
  is_fitting: false,
  fitting_time: "",
  fitting_laborhour: 0,
  is_painting: false,
  painting_time: "",
  painting_laborhour: 0,
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
      dialogTitle.value = props.title || (props.data.id ? "编辑工时" : "填写工时");
    }
  }
);

watch(
  () => visible.value,
  (val) => {
    emit("update:modelValue", val);
  }
);

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
    if (props.data?.id) {
      await OrdersAPI.update(props.data.id, formData.value);
    } else {
      await OrdersAPI.create(formData.value);
    }
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
