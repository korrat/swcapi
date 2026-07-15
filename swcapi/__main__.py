import csv
import sys
from typing import cast

from easyverein import EasyvereinAPI
from easyverein.models.contact_details import ContactDetails
from easyverein.models.member import MemberFilter
from easyverein.models.member_custom_field import MemberCustomField

from swcapi.config import settings
from swcapi.models import CustomField, Member
from swcapi.utils import handle_token_refresh


def fetch_members() -> tuple[Member, ...]:
    # Initialize Easyverein API client
    ev_client = EasyvereinAPI(
        api_key=settings.apikey,
        api_version="v2.0",
        token_refresh_callback=handle_token_refresh,
        auto_refresh_token=True,
    )

    # FIXME: this should be changed to be opt-in for members
    filter = ev_client.member.get_all(
        query="{id}",
        search=MemberFilter(
            custom_field_name="Ich möchte NICHT auf der Alumni-Homepage gelistet werden", custom_field_value="True"
        ),
    )

    members = ev_client.member.get_all(
        query="{id,_profilePicture,membershipNumber,contactDetails{familyName,firstName},customFields{customField{id,name},value}}",
        search=MemberFilter(id__in=[cast(int, m.id) for m in filter]),
    )

    return tuple(
        Member.from_api(
            m,
            profilePicture=(
                ev_client.c.fetch_file(str(m.profilePicture))[0]
                if m.profilePicture != "https://easyverein.com/app/image/defaultUserImage.png"
                else None
            ),
        )
        for m in members
    )


def saveProfilePicture(id: int | None, data: bytes | None) -> str | None:
    if id is None or data is None:
        return None

    path = f"output/profile-pictures/{id}.png"
    with open(path, mode="wb") as f:
        f.write(data)

    return path


def main() -> None:
    print("Fetching members...")
    try:
        members = fetch_members()
    except Exception as e:
        print(f"Error fetching members: {e}", file=sys.stderr)
        sys.exit(1)

    fieldnames = (
        "id",
        "firstName",
        "familyName",
        "profilePicture",
        *set(cf for m in members for cf in m.customFields),
    )

    with open("output/members.csv", mode="w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()

        for m in members:
            writer.writerow(
                {
                    "id": m.id,
                    "firstName": m.firstName,
                    "familyName": m.familyName,
                    "profilePicture": saveProfilePicture(m.id, m.profilePicture),
                }
                | {field.name: field.value for field in m.customFields.values()}
            )


if __name__ == "__main__":
    main()
