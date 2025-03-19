import os
from aiogram import Router, F, types
from aiogram.enums import ContentType
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, CallbackQuery
from app.db.requests import get_ordernumber_orders, up_pay_ordernumber, up_pay_price
import app.keyboards as kb

# from yookassa import Configuration
#
# Configuration.account_id = os.getenv('UKASSATOKEN')
# Configuration.secret_key = os.getenv('TESTSHOP')


pay = Router()
#################################################### pay
@pay.callback_query(F.data.startswith('pay'))
async def pay_order(callback: CallbackQuery):
    ordernumber_id = callback.data.split('_')[1]
    description = ''
    builder = InlineKeyboardBuilder()
    ordernumber = await get_ordernumber_orders(ordernumber_id)
    summ = float(ordernumber.delivery_price)
    for order in ordernumber.orders:
        description = f"{order.product}. "
        summ = summ + (float(order.price) * order.quantity)
    description = description[:128]
    if ordernumber.status == 'verified':

        PRICE = [types.LabeledPrice(label=f'К оплате за заказ № {ordernumber_id}', amount=int(summ * 100))]
        await callback.message.bot.send_invoice(chat_id=callback.message.chat.id,
                                                title=f"Заказ № {ordernumber_id}",
                                                description=description,
                                                payload=ordernumber_id,
                                                provider_token=os.getenv('UKASSATOKEN'),
                                                currency=os.getenv('CURRENCY'),
                                                start_parameter=ordernumber.uuid,
                                                is_flexible=False,
                                                prices=PRICE
                                                )

@pay.message(F.successful_payment)
@pay.message(F.content_types == ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message):
    ordernumber_id =  message.successful_payment.invoice_payload
    ordernumber = await get_ordernumber_orders(ordernumber_id)
    text = (f"currency = {message.successful_payment.currency}, "
            f"total_amount = {message.successful_payment.total_amount}, "
            f"invoice_payload = {message.successful_payment.invoice_payload}, "
            f"telegram_payment_charge_id = {message.successful_payment.telegram_payment_charge_id}, "
            f"provider_payment_charge_id = {message.successful_payment.provider_payment_charge_id}, "
            f"subscription_expiration_dat = {message.successful_payment.subscription_expiration_date}, "
            f"is_recurring = {message.successful_payment.is_recurring}, "
            f"is_first_recurring = {message.successful_payment.is_first_recurring}, "
            f"shipping_option_id = {message.successful_payment.shipping_option_id}, "
            f"order_info = {message.successful_payment.order_info}"
            )
    await up_pay_ordernumber(ordernumber_id, text)
    for order in ordernumber.orders:
        await up_pay_price(order.price_id, order.quantity)
    await message.answer(f"{kb.name_menu['pay_menu']}\n"
                         f"Товар оплачен! Менеджер с Вами свяжется!", reply_markup = await kb.menu_us(kb.name_menu['main_menu'],
                                                "start"))


    # print(f"-----------------------{message.successful_payment.invoice_payload}")

# @user.pre_checkout_query_handler(F.data.startswith('pay'))
# async def pay_order(callback: CallbackQuery):