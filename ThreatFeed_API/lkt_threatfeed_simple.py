import sys

def create_csv_content(domain):
    """Create CSV content as a string with the domain to be added."""
    csv_content = f"domain,action\n{domain},add\n"
    return csv_content

def create_curl_command(csv_content, feed_id, bearer_token):
    """Create a curl command to upload the CSV content using /dev/stdin."""
    # Escape the CSV content to ensure it's correctly interpreted in the shell
    escaped_csv_content = csv_content.replace('"', '\\"').replace("'", "\\'").replace("`", "\\`").replace("$", "\\$")

    curl_command = (
        f'curl --location "https://api.lookout.com/mgmt/threat-feeds/api/v1/threat-feeds/{feed_id}/elements?uploadType=INCREMENTAL" '
        f'--header "Accept: text/csv" '
        f'--header "Authorization: Bearer {bearer_token}" '
        f'--form "file=@/dev/stdin" <<< $'
        f"'{escaped_csv_content}'"
    )
    return curl_command

def main():
    if len(sys.argv) != 4 or not sys.argv[1].startswith('--add-domain=') or not sys.argv[2].startswith('--bearer-token=') or not sys.argv[3].startswith('--feed-id='):
        print("Usage: python lkt_threatfeed_simple.py --add-domain=<domain> --bearer-token=<token> --feed-id=<feed_id>")
        return

    domain = sys.argv[1].split('=')[1]
    bearer_token = sys.argv[2].split('=')[1]
    feed_id = sys.argv[3].split('=')[1]

    # Create CSV content with the domain
    csv_content = create_csv_content(domain)

    # Create the curl command
    curl_command = create_curl_command(csv_content, feed_id, bearer_token)

    # Print the curl command as the result
    print(curl_command)

if __name__ == '__main__':
    main()
