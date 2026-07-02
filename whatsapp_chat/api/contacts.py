import frappe




@frappe.whitelist()
def create(contact_name, mobile_no, email):
    """Create contact."""
    frappe.get_doc({
        "doctype": "WhatsApp Contact",
        "contact_name": contact_name,
        "mobile_no": mobile_no,
        "email": email
    }).save()
    return "email"




@frappe.whitelist()
def get(email):
    """Get all contacts assigned to email, enriched with WhatsApp Profiles display name."""
    contacts = frappe.db.get_all(
        "WhatsApp Contact",
        filters={"email": ["in", [email, ""]]},
        fields=["*"],
    )

    # Enrich each contact with a display_name from WhatsApp Profiles.
    # WhatsApp Profiles stores a human-readable title (e.g. "Ravi - 917842272227")
    # that is set automatically from the sender's profile name on each incoming message.
    # Falling back to contact_name (which is the raw phone number) keeps backward compatibility.
    for contact in contacts:
        profile_title = frappe.db.get_value(
            "WhatsApp Profiles",
            {"number": contact.get("mobile_no")},
            "title",
        )
        contact["display_name"] = profile_title or contact.get("contact_name") or contact.get("mobile_no")

    return contacts
