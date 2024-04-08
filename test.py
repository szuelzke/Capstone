import phonenumbers

phone_number = "6148136876"  # Your phone number without the country code

# Parse the phone number and format it to E.164
formatted_phone_number = phonenumbers.format_number(phonenumbers.parse(phone_number, "US"), phonenumbers.PhoneNumberFormat.E164)

print(formatted_phone_number)  # Output: +16148136876