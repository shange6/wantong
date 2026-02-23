<template>
  <div class="app-container">
    <!-- 搜索表单 -->
    <!-- 数据表格 -->
    <el-table v-loading="loading" :data="tableData" border style="width: 100%" align="center">
      <!-- <el-table-column prop="id" label="ID" width="80" /> -->
      <!-- <el-table-column prop="wtcode" label="万通码" min-width="130" fixed="left"/> -->
      <el-table-column prop="components_code" label="代码" min-width="130" fixed="left" />
      <el-table-column
        prop="components_spec"
        label="名称"
        min-width="130"
        align="center"
        fixed="left"
      />
      <el-table-column prop="components_count" label="数量" min-width="60" align="center" />
      <el-table-column prop="components_material" label="材料" min-width="130" align="center" />
      <el-table-column prop="components_unit_mass" label="单重" min-width="60" align="center" />
      <el-table-column prop="components_totle_mass" label="总重" min-width="70" align="center" />
      <el-table-column prop="components_remark" label="备注" min-width="100" align="center" />

      <el-table-column prop="blanking" label="下料" width="130" align="center" />
      <el-table-column prop="rivetweld" label="铆焊" width="130" align="center" />
      <el-table-column prop="machine" label="机加" width="130" align="center" />
      <el-table-column prop="fitting" label="装配" width="130" align="center" />
      <el-table-column prop="painting" label="喷漆" width="130" align="center" />
      <!-- <el-table-column prop="created_at" label="创建时间" width="130" align="center" /> -->
    </el-table>

    <!-- 分页 -->
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import OrdersAPI, { OrdersData, OrdersPageQuery } from "@/api/module_orders/order";

defineOptions({
  name: "Order",
});

const loading = ref(false);
const total = ref(0);
const tableData = ref<OrdersData[]>([]);

const queryParams = reactive<OrdersPageQuery>({
  page_no: 1,
  page_size: 10,
  wtcode: undefined,
});

async function handleQuery() {
  if (loading.value) {
    return;
  }
  loading.value = true;
  try {
    const res = await OrdersAPI.getList(queryParams);
    tableData.value = res.data.items;
    total.value = res.data.total;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

function handleReset() {
  queryParams.wtcode = undefined;
  queryParams.page_no = 1;
  handleQuery();
}

onMounted(() => {
  handleQuery();
});
</script>

<style scoped>
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
