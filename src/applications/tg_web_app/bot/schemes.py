from pydantic import BaseModel, Field, ConfigDict

from applications.tg_web_app.bot.enums import ParseModeEnum, TGBotCommandEnum


class TelegramUserData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    first_name: str
    last_name: str | None = None
    username: str | None = None
    photo_url: str | None = None
    auth_date: str | None = None


class TelegramAuthData(TelegramUserData):
    hash: str


# Payload WebHook
class TelegramFromData(BaseModel):
    id: int = Field(..., description="Unique identifier for the user")
    is_bot: bool = Field(..., description="True if the user is a bot")
    first_name: str = Field(..., description="User's first name")
    last_name: str | None = Field(None, description="User's last name")
    username: str | None = Field(None, description="User's username")
    language_code: str | None = Field(
        None, description="IETF language tag of the user's language"
    )
    is_premium: bool | None = Field(None, description="True if the user is premium")


class TelegramChatData(BaseModel):
    id: int = Field(..., description="Unique identifier for the chat")
    first_name: str = Field(..., description="User's or bot's first name")
    last_name: str | None = Field(None, description="User's or bot's last name")
    username: str | None = Field(None, description="User's or bot's username")
    type: str = Field(..., description="Type of chat")


class TelegramEntitiesItem(BaseModel):
    offset: int = Field(..., description="Offset in UTF-16 code units to the start of the entity")
    length: int = Field(..., description="Length of the entity in UTF-16 code units")
    type: str = Field(..., description="Type of the entity")


class TelegramMessageWebHookPayload(BaseModel):
    message_id: int = Field(..., description="Unique message identifier")
    from_: TelegramFromData = Field(..., alias="from", description="Sender")
    chat: TelegramChatData = Field(..., description="Chat the message belongs to")
    date: int = Field(..., description="Date the message was sent in Unix time")
    text: str = Field(..., description="For text messages, the actual UTF-8 text of the message")
    entities: list[TelegramEntitiesItem] | None = Field(
        None, description="For text messages, special entities like usernames, URLs, bot commands, etc."
    )


class TelegramWebHookPayload(BaseModel):
    update_id: int = Field(..., description="The update's unique identifier")
    message: TelegramMessageWebHookPayload | None = Field(
        None, description="New incoming message of any kind — text, photo, sticker, etc."
    )

    @property
    def text(self) -> str:
        return self.message.text if self.message else None

    @property
    def chat_id(self) -> int:
        return self.message.chat.id if self.message else None

    @property
    def bot_command(self) -> TGBotCommandEnum | None:
        if self.message:
            if self.message.entities[0].type == "bot_command":
                return self.message.text
        return None

    @property
    def sender_is_bot(self) -> bool:
        return self.message.from_.is_bot if self.message else False

    @property
    def tg_id(self) -> int:
        return self.message.from_.id if self.message else None


class KeyboardButtonRequestUser(BaseModel):
    request_id: int = Field(..., description="Unique identifier for the request")
    user_is_bot: bool | None = Field(None, description="Allow only bots")
    user_is_premium: bool | None = Field(None, description="Allow only premium users")


class ChatAdministratorRights(BaseModel):
    is_anonymous: bool = Field(..., description="Administrator is anonymous")
    can_manage_chat: bool = Field(..., description="Can manage chat")
    can_delete_messages: bool = Field(..., description="Can delete messages")
    can_manage_video_chats: bool = Field(..., description="Can manage video chats")
    can_restrict_members: bool = Field(..., description="Can restrict members")
    can_promote_members: bool = Field(..., description="Can promote members")
    can_change_info: bool = Field(..., description="Can change chat information")
    can_invite_users: bool = Field(..., description="Can invite new users")
    can_post_messages: bool | None = Field(
        None, description="Can post messages (for channels)"
    )
    can_edit_messages: bool | None = Field(
        None, description="Can edit messages (for channels)"
    )
    can_pin_messages: bool | None = Field(None, description="Can pin messages")
    can_manage_topics: bool | None = Field(None, description="Can manage topics")


class KeyboardButtonRequestChat(BaseModel):
    request_id: int = Field(..., description="Unique identifier for the request")
    chat_is_channel: bool = Field(..., description="Require a channel chat")
    chat_is_forum: bool | None = Field(None, description="Require a forum chat")
    chat_has_username: bool | None = Field(
        None, description="Require chat to have a username"
    )
    chat_is_created: bool | None = Field(
        None, description="Require a newly created chat"
    )
    user_administrator_rights: ChatAdministratorRights | None = Field(
        None, description="User's administrator rights in the chat"
    )
    bot_administrator_rights: ChatAdministratorRights | None = Field(
        None, description="Bot's administrator rights in the chat"
    )
    bot_is_member: bool | None = Field(
        None, description="Bot must be a member of the chat"
    )


class KeyboardButtonPollType(BaseModel):
    type: str | None = Field(
        None, description="Allowed poll type ('quiz', 'regular', or None)"
    )


class WebAppInfo(BaseModel):
    url: str = Field(..., description="URL of the Web App")


class TGUser(BaseModel):
    id: int = Field(..., description="Unique identifier for the user")
    is_bot: bool = Field(..., description="True if the user is a bot")
    first_name: str = Field(..., description="User's first name")
    last_name: str | None = Field(None, description="User's last name")
    username: str | None = Field(None, description="User's username")
    language_code: str | None = Field(
        None, description="IETF language tag of the user's language"
    )


class MessageEntity(BaseModel):
    type: str = Field(
        ..., description="Type of the entity (e.g., 'mention', 'hashtag')"
    )
    offset: int = Field(
        ..., description="Offset in UTF-16 code units to the start of the entity"
    )
    length: int = Field(..., description="Length of the entity in UTF-16 code units")
    url: str | None = Field(
        None, description="URL that will be opened after user taps on the text"
    )
    user: TGUser | None = Field(None, description="User mentioned in the text")
    language: str | None = Field(
        None, description="Programming language of the entity text"
    )
    custom_emoji_id: str | None = Field(
        None, description="Unique identifier for a custom emoji"
    )


class KeyboardButton(BaseModel):
    text: str = Field(..., description="Text of the button")
    request_user: KeyboardButtonRequestUser | None = Field(
        None, description="User request button"
    )
    request_chat: KeyboardButtonRequestChat | None = Field(
        None, description="Chat request button"
    )
    request_contact: bool | None = Field(
        None, description="Send user's contact when pressed"
    )
    request_location: bool | None = Field(
        None, description="Send user's location when pressed"
    )
    request_poll: KeyboardButtonPollType | None = Field(
        None, description="Send a poll when pressed"
    )
    web_app: WebAppInfo | None = Field(
        None, description="Launch a Web App when pressed"
    )


class ReplyKeyboardMarkup(BaseModel):
    keyboard: list[list[KeyboardButton]] = Field(
        ..., description="Array of button rows"
    )
    is_persistent: bool | None = Field(None, description="Keep the keyboard on screen")
    resize_keyboard: bool | None = Field(
        None, description="Resize the keyboard vertically for optimal fit"
    )
    one_time_keyboard: bool | None = Field(
        None, description="Hide the keyboard after it's used"
    )
    input_field_placeholder: str | None = Field(
        None, description="Placeholder to be shown in the input field"
    )
    selective: bool | None = Field(
        None, description="Show the keyboard to specific users only"
    )


class LoginUrl(BaseModel):
    url: str = Field(
        ...,
        description="An HTTPS URL to be opened with user authorization data added to the query string",
    )
    forward_text: str | None = Field(
        None, description="New text of the button in forwarded messages"
    )
    bot_username: str | None = Field(None, description="Username of a bot")
    request_write_access: bool | None = Field(
        None,
        description="Pass True to request permission for your bot to send messages",
    )


class CallbackGame(BaseModel):
    user_id: int = Field(..., description="Unique identifier for the target chat")
    score: int = Field(..., description="New score in the game")
    force: bool | None = Field(
        None,
        description="Pass True to update the score even if it's lower than the current score",
    )
    disable_edit_message: bool | None = Field(
        None, description="Pass True if the high score is allowed to decrease"
    )
    chat_id: int | None = Field(
        None, description="Unique identifier for the target chat"
    )
    message_id: int | None = Field(None, description="Identifier of the sent message")
    inline_message_id: str | None = Field(
        None, description="Identifier of the inline message"
    )


class InlineKeyboardButton(BaseModel):
    text: str = Field(..., description="Label text on the button")
    url: str | None = Field(
        None, description="HTTP URL to be opened when button is pressed"
    )
    callback_data: str | None = Field(
        None,
        description="Data to be sent in a callback query to the bot when button is pressed",
    )
    web_app: WebAppInfo | None = Field(
        None,
        description="Description of the Web App to be launched when the button is pressed",
    )
    login_url: LoginUrl | None = Field(
        None, description="An HTTPS URL used to automatically authorize the user"
    )
    switch_inline_query: str | None = Field(
        None,
        description="If set, pressing the button will prompt the user to select one of their chats",
    )
    switch_inline_query_current_chat: str | None = Field(
        None,
        description="If set, pressing the button will insert the bot's username and the specified inline query in the current chat's input field",
    )
    callback_game: CallbackGame | None = Field(
        None,
        description="Description of the game that will be launched when the user presses the button",
    )
    pay: bool | None = Field(None, description="Specify True to send a Pay button")


class InlineKeyboardMarkup(BaseModel):
    inline_keyboard: list[list[InlineKeyboardButton]] = Field(
        ..., description="Array of button rows"
    )


class ReplyKeyboardRemove(BaseModel):
    remove_keyboard: bool = Field(
        default=True, description="Requests clients to remove the custom keyboard"
    )
    selective: bool | None = Field(
        None,
        description="Use this parameter if you want to remove the keyboard for specific users only",
    )


class ForceReply(BaseModel):
    force_reply: bool = Field(default=True, description="Forces a reply from the user")
    input_field_placeholder: str | None = Field(
        None, description="Placeholder to be shown in the input field"
    )
    selective: bool | None = Field(
        None,
        description="Use this parameter if you want to force reply from specific users only",
    )

class LinkPreviewOptions(BaseModel):
    url: str | None = Field(None, description="URL of the link to be previewed")
    prefer_small_media: bool | None = Field(
        None, description="Prefer small media file links"
    )
    prefer_large_media: bool | None = Field(
        None, description="Prefer large media file links"
    )
    show_above_text: bool | None = Field(
        None, description="Show the link preview above the message text"
    )

class SendMessagePayload(BaseModel):
    chat_id: int | str = Field(
        ...,
        description="Unique identifier for the target chat or username of the target channel",
    )
    text: str = Field(..., description="Text of the message to be sent")
    parse_mode: str | None = Field(
        None, description="Mode for parsing entities in the message text use ParseModeEnum"
    )

    link_preview_options: LinkPreviewOptions | None = Field(
        None, description="Disable link previews for links in this message"
    )

    disable_notification: bool | None = Field(
        None, description="Sends the message silently"
    )
    protect_content: bool = Field(
        True,
        description="Protects the contents of the sent message from forwarding and saving",
    )

    reply_markup: (
            ReplyKeyboardMarkup
            | InlineKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
    ) = Field(None, description="Additional interface options")
