from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class CustomField:
    name: str
    value: any


@dataclass(frozen=True, kw_only=True)
class Member:
    id: int
    firstName: str
    familyName: str
    profilePicture: bytes | None

    customFields: dict[str, any]
