from fastapi import APIRouter

from .client import client_router
from .products import product_router
from .supplier import supplier_router
from .images import images_router

router = APIRouter()

router.include_router(client_router)
router.include_router(product_router)
router.include_router(supplier_router)
router.include_router(images_router)
