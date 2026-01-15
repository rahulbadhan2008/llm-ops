from fastapi import APIRouter
from app.utils.cost_control import CostController

router = APIRouter()

@router.get("/")
async def get_costs():
    controller = CostController()
    spending = controller.get_current_spending()
    return {"current_spending_usd": spending or 0.0}
