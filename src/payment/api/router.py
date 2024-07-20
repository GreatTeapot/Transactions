from .payment import router as pay_router
from .accounts import router as acc_router

all_routers = [pay_router, acc_router]