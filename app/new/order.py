from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from sqlalchemy import null
from app.admin import product_menu
from app.cmd.paginator import get_paginat_kb
from app.db.requests import get_category_id, get_product_id, set_product_new, set_product_up
from app.filter import Admin
from aiogram.types import Message, CallbackQuery
from app.states import UpProduct
import app.keyboards as kb

neworder = Router()
neworder.message.filter(Admin())