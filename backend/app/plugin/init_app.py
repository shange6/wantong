from collections.abc import AsyncGenerator
from typing import Any

from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter, WebSocketRateLimiter

from app.config.setting import settings
from app.core.exceptions import handle_exception
from app.core.http_limit import http_limit_callback, ws_limit_callback
from app.core.logger import log
from app.scripts.initialize import InitializeData
from app.utils.common_util import import_module, import_modules_async
from app.utils.console import console_close, console_run


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    """
    自定义 FastAPI 应用生命周期。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - AsyncGenerator[Any, Any]: 生命周期上下文生成器。
    """
    from app.api.v1.module_system.dict.service import DictDataService
    from app.api.v1.module_system.params.service import ParamsService
    from app.plugin.module_application.job.tools.ap_scheduler import SchedulerUtil
    from app.core.database import redis_connect  # 💡 导入你的这个函数
    try:
        await InitializeData().init_db()
        log.info(f"✅ {settings.DATABASE_TYPE}数据库初始化完成")
        # 1. 显式初始化 Redis 并挂载到 state
        # 即使 import_modules_async 也会调，这里手动调一次能确保万无一失
        await redis_connect(app, status=True) 
        log.info("✅ Redis 物理连接已确立并挂载到 app.state")
        await import_modules_async(
            modules=settings.EVENT_LIST, desc="全局事件", app=app, status=True
        )
        log.info("✅ 全局事件模块加载完成")
        await ParamsService().init_config_service(redis=app.state.redis)
        log.info("✅ Redis系统配置初始化完成")
        await DictDataService().init_dict_service(redis=app.state.redis)
        log.info("✅ Redis数据字典初始化完成")
        await SchedulerUtil.init_system_scheduler(redis=app.state.redis)
        log.info("✅ 定时任务调度器初始化完成")
        await FastAPILimiter.init(
            redis=app.state.redis,
            prefix=settings.REQUEST_LIMITER_REDIS_PREFIX,
            http_callback=http_limit_callback,
            ws_callback=ws_limit_callback,
        )
        log.info("✅ 请求限流器初始化完成")

        # 导入并显示最终的启动信息面板
        from app.common.enums import EnvironmentEnum

        scheduler_jobs_count = len(SchedulerUtil.get_all_jobs())
        scheduler_status = SchedulerUtil.get_job_status()
        console_run(
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
            reload=settings.ENVIRONMENT == EnvironmentEnum.DEV,
            redis_ready=True,
            scheduler_jobs=scheduler_jobs_count,
            scheduler_status=scheduler_status,
        )

    except Exception as e:
        log.error(f"❌ 应用初始化失败: {e!s}")
        raise

    yield

    try:
        await import_modules_async(
            modules=settings.EVENT_LIST, desc="全局事件", app=app, status=False
        )
        log.info("✅ 全局事件模块卸载完成")
        await SchedulerUtil.close_system_scheduler()
        log.info("✅ 定时任务调度器已关闭")
        await FastAPILimiter.close()
        log.info("✅ 请求限制器已关闭")
        console_close()

    except Exception as e:
        log.error(f"❌ 应用关闭过程中发生错误: {e!s}")


def register_middlewares(app: FastAPI) -> None:
    """
    注册全局中间件。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - None
    """
    for middleware in settings.MIDDLEWARE_LIST[::-1]:
        if not middleware:
            continue
        middleware = import_module(middleware, desc="中间件")
        app.add_middleware(middleware)


def register_exceptions(app: FastAPI) -> None:
    """
    统一注册异常处理器。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - None
    """
    handle_exception(app)


def register_routers(app: FastAPI) -> None:
    """
    注册根路由。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - None
    """
    from app.api.v1.module_common import common_router
    from app.api.v1.module_monitor import monitor_router
    from app.api.v1.module_system import system_router

    app.include_router(common_router, dependencies=[Depends(RateLimiter(times=5, seconds=10))])
    app.include_router(system_router, dependencies=[Depends(RateLimiter(times=5, seconds=10))])
    app.include_router(monitor_router, dependencies=[Depends(RateLimiter(times=5, seconds=10))])

    from app.plugin.module_application.ai.ws import WS_AI

    # 手动注册WebSocket路由，不使用速率限制器
    app.include_router(
        router=WS_AI, dependencies=[Depends(WebSocketRateLimiter(times=1, seconds=5))]
    )
    # 先将动态路由注册到应用，使用速率限制器
    from app.core.discover import get_dynamic_router

    # 获取动态路由实例
    app.include_router(
        router=get_dynamic_router(),
        dependencies=[Depends(RateLimiter(times=5, seconds=10))],
    )


def register_files(app: FastAPI) -> None:
    """
    注册静态资源挂载和文件相关配置。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - None
    """
    # 挂载静态文件目录
    if settings.STATIC_ENABLE:
        # 确保日志目录存在
        settings.STATIC_ROOT.mkdir(parents=True, exist_ok=True)
        app.mount(
            path=settings.STATIC_URL,
            app=StaticFiles(directory=settings.STATIC_ROOT),
            name=settings.STATIC_DIR,
        )


def reset_api_docs(app: FastAPI) -> None:
    """
    使用本地静态资源自定义 API 文档页面（Swagger UI 与 ReDoc）。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - None
    """

    @app.get(settings.DOCS_URL, include_in_schema=False)
    async def custom_swagger_ui_html() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=str(app.root_path) + str(app.openapi_url),
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=settings.SWAGGER_JS_URL,
            swagger_css_url=settings.SWAGGER_CSS_URL,
            swagger_favicon_url=settings.FAVICON_URL,
        )

    @app.get(str(app.swagger_ui_oauth2_redirect_url), include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get(settings.REDOC_URL, include_in_schema=False)
    async def custom_redoc_html():
        return get_redoc_html(
            openapi_url=str(app.root_path) + str(app.openapi_url),
            title=app.title + " - ReDoc",
            redoc_js_url=settings.REDOC_JS_URL,
            redoc_favicon_url=settings.FAVICON_URL,
        )
