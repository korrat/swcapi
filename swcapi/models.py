from pydantic_core import Url
from easyverein.models.custom_field import CustomField
from easyverein.models.member_custom_field import MemberCustomField
from easyverein.models.contact_details import ContactDetails
import easyverein.models
from dataclasses import dataclass
from typing import Any, Self


@dataclass(frozen=True, kw_only=True)
class Member:
    id: int | None
    firstName: str | None
    familyName: str | None
    profilePicture: bytes | None

    customFields: dict[str, Any]

    @classmethod
    def from_api(
        cls,
        member: easyverein.models.Member,
        profilePicture: bytes | None,
    ) -> Self:
        if member.membershipNumber is None:
            raise ValueError("id must be defined")
        id = int(member.membershipNumber)

        if not isinstance(member.contactDetails, ContactDetails):
            raise ValueError("contact details must be set")
        contact = member.contactDetails

        if contact.firstName is None:
            raise ValueError("firstName must be defined")
        firstName = contact.firstName

        if contact.familyName is None:
            raise ValueError("familyName must be defined")
        familyName = contact.familyName

        customFields = extract_custom_fields(member.customFields)

        return cls(
            id=id,
            firstName=firstName,
            familyName=familyName,
            profilePicture=profilePicture,
            customFields=customFields,
        )


def extract_custom_fields(cfs: list[int | Url | None] | list[MemberCustomField] | None) -> dict[str, Any]:
    if cfs is None:
        raise ValueError("customFieldsList must be set")

    def extract_custom_field(cf: int | MemberCustomField | Url | None) -> tuple[str, Any]:
        if not isinstance(cf, MemberCustomField):
            raise ValueError("expected expanded form of customFields list")

        if not isinstance(cf.customField, CustomField):
            raise ValueError("expected expanded form of `customField` object")

        if cf.customField.name is None:
            raise ValueError("customField.name must be set")

        return (cf.customField.name, cf.value)

    return dict(map(extract_custom_field, cfs))
