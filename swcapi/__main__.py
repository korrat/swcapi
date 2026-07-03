import sys
from pprint import pprint

from easyverein import EasyvereinAPI

from swcapi.config import settings
from swcapi.utils import handle_token_refresh


def main() -> None:
    # Initialize Easyverein API client
    ev_client = EasyvereinAPI(
        api_key=settings.apikey,
        api_version="v2.0",
        token_refresh_callback=handle_token_refresh,
        auto_refresh_token=True,
    )

    print("Fetching custom fields...")
    try:
        custom_fields = {}
        all_cfs = ev_client.custom_field.get_all()
        for cf in all_cfs:
            custom_fields[cf.id] = cf.name
    except Exception as e:
        print(f"Error fetching custom fields: {e}", file=sys.stderr)
        sys.exit(1)

    print("Fetching members...")
    try:
        members, _ = ev_client.member.get(
            query="{id,membershipNumber,contactDetails{familyName,firstName},customFields}"
        )
    except Exception as e:
        print(f"Error fetching members: {e}", file=sys.stderr)
        sys.exit(1)

    if not members:
        print("No members found.")
        return

    m = members[0]
    print(f"\nCustom fields for member {m.membershipNumber} ({m.contactDetails.firstName} {m.contactDetails.familyName}):")

    try:
        fields, _ = ev_client.member.custom_field(m.id).get()
        for cf in fields:
            # Parse custom field ID from the endpoint URL reference
            cf_id = int(str(cf.customField).split("/")[-1])
            name = custom_fields.get(cf_id, "X")
            print(f"  {name}: {cf.value}")
    except Exception as e:
        print(f"Error fetching member custom fields: {e}", file=sys.stderr)

    print("\nFetching specific custom field by ID 13081650:")
    try:
        cf = ev_client.custom_field.get_by_id(13081650)
        pprint(cf)
    except Exception as e:
        print(f"Error fetching custom field 13081650: {e}")


if __name__ == "__main__":
    main()
