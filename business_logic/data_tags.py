class Type:
    data_request = "data_request"
    subscription = "subscription"


class SubType:
    social_media = "social_media"
    news = "news"
    stock = "stock"


class Indicator:
    industry_average = "industry_average"
    just_price = "just_price"
    price_today = "price_today"
    price_yesterday = "price_yesterday"
    stock_variance = "stock_variance"

    news = "news"
    social_media = "social_media"


class Mood:
    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class OutgoingMessageType:
    response = "response"
    on_unknown_request = "unknown_request"
    on_exception = "exception"


class MimeTypes:
    text = "text/plain"
    ogg = "audio/ogg"
    flac = "audio/flac"
