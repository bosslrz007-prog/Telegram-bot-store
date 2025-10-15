import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# -----------------------------
# Product Data
# -----------------------------
PRODUCT = {
    "name": "WP ACC",
    "price": 20,
    "stock": 60,
    "status": "Available"
}

ADMIN_ID = int(os.getenv("ADMIN_ID", "6017879905"))

# -----------------------------
# /start Command
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Buy Now", callback_data='buy')],
        [InlineKeyboardButton("📦 Check Stock", callback_data='stock')],
        [InlineKeyboardButton("⚙️ Status", callback_data='status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        f"👋 *Welcome to Digital Store!*\n\n"
        f"🛍️ *Product:* {PRODUCT['name']}\n"
        f"💰 *Price:* ₹{PRODUCT['price']}\n"
        f"📦 *Stock:* {PRODUCT['stock']}\n"
        f"⚙️ *Status:* {PRODUCT['status']}"
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

# -----------------------------
# Button Handler
# -----------------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "stock":
        await query.edit_message_text(f"📦 Stock left: {PRODUCT['stock']}")
    elif query.data == "status":
        await query.edit_message_text(f"⚙️ Current Status: {PRODUCT['status']}")
    elif query.data == "buy":
        if PRODUCT["status"].lower() != "available":
            await query.edit_message_text("❌ Product is currently unavailable.")
            return
        if PRODUCT["stock"] > 0:
            PRODUCT["stock"] -= 1
            await query.edit_message_text("✅ *Order placed successfully!*", parse_mode="Markdown")
        else:
            PRODUCT["status"] = "Out of Stock"
            await query.edit_message_text("❌ Out of stock now!")

# -----------------------------
# Admin Commands
# -----------------------------
async def add_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 Not authorized.")
        return
    try:
        amount = int(context.args[0])
        PRODUCT["stock"] += amount
        await update.message.reply_text(f"✅ Added {amount}. New stock: {PRODUCT['stock']}")
    except:
        await update.message.reply_text("⚠️ Usage: /addstock <number>")

async def set_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 Not authorized.")
        return
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /setstatus <Available/Out>")
        return
    new_status = context.args[0].capitalize()
    if new_status not in ["Available", "Out"]:
        await update.message.reply_text("⚠️ Must be 'Available' or 'Out'")
        return
    PRODUCT["status"] = new_status
    await update.message.reply_text(f"✅ Status updated to: {new_status}")

# -----------------------------
# Main
# -----------------------------
def main():
    TOKEN = os.getenv("BOT_TOKEN")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("addstock", add_stock))
    app.add_handler(CommandHandler("setstatus", set_status))
    app.run_polling()

if __name__ == "__main__":
    main()