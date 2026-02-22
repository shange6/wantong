from sqlalchemy import select, func
from sqlalchemy.orm import selectinload  # 已补充导入
from .model import OrdersModel
from app.plugin.module_projects.components.model import ComponentsModel
from .schema import OrdersFilter, OrdersCreate, OrdersUpdate, OrdersOut
from app.core.database import async_db_session
from app.core.exceptions import CustomException
from datetime import datetime

class OrdersService:
    @classmethod
    async def get_orders_list_service(cls, page_no: int, page_size: int, search: OrdersFilter):
        """
        分页查询订单列表（关联组件表）
        :param page_no: 页码
        :param page_size: 每页条数（0则返回全部）
        :param search: 过滤条件
        :return: 分页结果
        """
        async with async_db_session() as session:
            # 构建查询语句，预加载关联的组件数据
            stmt = select(OrdersModel).options(
                selectinload(OrdersModel.component)  # 替换为selectinload，对齐常用ORM写法
            )
            
            # 过滤条件（可根据实际需求扩展）
            if search.wtcode:
                stmt = stmt.where(OrdersModel.wtcode.ilike(f"%{search.wtcode}%"))
            
            # 计算总条数
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = (await session.execute(count_stmt)).scalar() or 0
            
            # 分页处理（page_size为0返回全部）
            if page_size > 0:
                stmt = stmt.offset((page_no - 1) * page_size).limit(page_size)
            
            # 排序（按创建时间降序）
            stmt = stmt.order_by(OrdersModel.created_time.desc())
            
            # 执行查询
            result = await session.execute(stmt)
            items = result.scalars().all()
            
            # 格式化数据：关联组件字段 + 时间格式化
            data_list = []
            for order in items:
                # 基础订单数据（通过Pydantic序列化）
                order_dict = OrdersOut.model_validate(order).model_dump()
                
                # 关联组件数据（兼容组件为空的情况）
                component_data = order.component or ComponentsModel()
                component_dict = {
                    "components_code": component_data.code or "",
                    "components_spec": component_data.spec or "",
                    "components_count": component_data.count or 0,
                    "components_material": component_data.material or "",
                    "components_unit_mass": component_data.unit_mass or 0.0,
                    "components_totle_mass": component_data.total_mass or 0.0,
                    "components_remark": component_data.remark or "",
                }
                
                # 时间字段格式化（转为YYYY-MM-DD HH:mm:ss）
                def format_datetime(dt: datetime | None) -> str:
                    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""
                
                time_fields = ["blanking", "rivetweld", "machine", "fitting", "painting", "created_time"]
                for field in time_fields:
                    if order_dict.get(field):
                        order_dict[field] = format_datetime(order_dict[field])
                
                # 合并订单+组件数据
                order_dict.update(component_dict)
                data_list.append(order_dict)
            
            return {
                "items": data_list,
                "total": total,
                "page_no": page_no,
                "page_size": page_size
            }

    @classmethod
    async def create_orders_service(cls, data: OrdersCreate):
        """
        创建订单
        :param data: 订单创建数据
        :return: 创建后的订单对象
        """
        async with async_db_session() as session:
            async with session.begin():
                # 检查万通码重复
                stmt = select(OrdersModel).where(OrdersModel.wtcode == data.wtcode)
                existing = (await session.execute(stmt)).scalars().first()
                if existing:
                    raise CustomException(msg=f"万通编码 {data.wtcode} 已存在")
                
                # 验证关联的组件是否存在
                component_stmt = select(ComponentsModel).where(ComponentsModel.wtcode == data.wtcode)
                component = (await session.execute(component_stmt)).scalars().first()
                if not component:
                    raise CustomException(msg=f"关联的组件（万通码：{data.wtcode}）不存在")
                
                # 创建订单
                order = OrdersModel(**data.model_dump(exclude_unset=True))
                session.add(order)
            
            return order

    @classmethod
    async def update_orders_service(cls, id: int, data: OrdersUpdate):
        """
        更新订单
        :param id: 订单ID
        :param data: 订单更新数据
        :return: 更新后的订单对象
        """
        async with async_db_session() as session:
            async with session.begin():
                # 查询订单是否存在
                stmt = select(OrdersModel).where(OrdersModel.id == id)
                order = (await session.execute(stmt)).scalars().first()
                if not order:
                    raise CustomException(msg="订单不存在")
                
                # 若修改万通码，检查重复 + 验证组件
                if data.wtcode and data.wtcode != order.wtcode:
                    # 检查万通码重复
                    existing = (await session.execute(select(OrdersModel).where(OrdersModel.wtcode == data.wtcode))).scalars().first()
                    if existing:
                        raise CustomException(msg=f"万通编码 {data.wtcode} 已存在")
                    
                    # 验证新万通码对应的组件是否存在
                    component = (await session.execute(select(ComponentsModel).where(ComponentsModel.wtcode == data.wtcode))).scalars().first()
                    if not component:
                        raise CustomException(msg=f"关联的组件（万通码：{data.wtcode}）不存在")
                
                # 更新字段
                for key, value in data.model_dump(exclude_unset=True).items():
                    setattr(order, key, value)
            
            return order

    @classmethod
    async def delete_orders_service(cls, ids: list[int]):
        """
        批量删除订单
        :param ids: 订单ID列表
        :return: None
        """
        async with async_db_session() as session:
            async with session.begin():
                # 查询要删除的订单
                stmt = select(OrdersModel).where(OrdersModel.id.in_(ids))
                orders = (await session.execute(stmt)).scalars().all()
                if not orders:
                    raise CustomException(msg="订单不存在")
                
                # 执行删除
                for order in orders:
                    await session.delete(order)