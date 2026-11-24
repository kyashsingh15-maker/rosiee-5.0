# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic


import pyrogram

from anony import config, logger


class Bot(pyrogram.Client):
    def __init__(self):
        super().__init__(
            name="anony",
            api_id=int(str(config.API_ID).strip()),
            api_hash=str(config.API_HASH).strip(),
            bot_token=str(config.BOT_TOKEN).strip(),
            in_memory=True,
            ipv6=False,
            workers=8,
            sleep_threshold=60,
            parse_mode=pyrogram.enums.ParseMode.HTML,
            max_concurrent_transmissions=7,
            link_preview_options=pyrogram.types.LinkPreviewOptions(is_disabled=True),
        )
        self.owner = config.OWNER_ID
        self.logger = config.LOGGER_ID
        self.bl_users = pyrogram.filters.user()
        self.sudoers = pyrogram.filters.user(self.owner)

    async def boot(self):
        """
        Starts the bot and performs initial setup.

        Raises:
            SystemExit: If the bot fails to access the log group or is not an administrator in the logger group.
        """
        try:
            await super().start()
        except Exception as ex:
            logger.error(f"Bot login failed: {type(ex).__name__}: {ex}")
            raise
        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(self.logger, "Bot Started")
            get = await self.get_chat_member(self.logger, self.id)
        except Exception as ex:
            raise SystemExit(f"Bot has failed to access the log group: {self.logger}\nReason: {ex}")

        if get.status != pyrogram.enums.ChatMemberStatus.ADMINISTRATOR:
            raise SystemExit("Please promote the bot as an admin in logger group.")
        logger.info(f"Bot started as @{self.username}")

    async def exit(self):
        """
        Asynchronously stops the bot.
        """
        await super().stop()
        logger.info("Bot stopped.")
        
