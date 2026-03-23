from fastapi import Request


def flash(request: Request, message: str, category: str = "") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append({"message": message, "category": category})


def get_flashed_messages(request: Request) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = request.session.pop("_messages", [])
    return messages
