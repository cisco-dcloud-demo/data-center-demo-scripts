import sys
import os
from mcp.server.fastmcp import FastMCP
import requests
from datetime import datetime
sys.path.append(os.path.abspath("intersight-rest-api"))
from intersight_auth import IntersightAuth
import json
import httpx
from typing import Any
import asyncio

# Create an AUTH object
AUTH = IntersightAuth(
    secret_key_filename='intersight-rest-api/key/SecretKey.txt',
    api_key_id='59bc454c16267c000192f683/677e626f7564613101d4e790/684fbd8c7564613101ba65f0'
    )

BURL = "https://intersight.com/api/v1/"

async def make_intersight_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Intersight API with proper error handling."""

    def sync_request() -> dict[str, Any] | None:
        try:
            response = requests.get(url, auth=AUTH, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            return {
                "status_code": e.response.status_code,
                "error_text": e.response.text
            }
        except requests.RequestException as e:
            return {
                "status_code": 0,
                "error_text": str(e)
            }
        except Exception as e:
            return {
                "status_code": -1,
                "error_text": str(e)
            }

    return await asyncio.to_thread(sync_request)

async def get_compute_rackunits(site: str):
    """
    Use Intersight API to retrieve Cisco Compute rackunits for a specific site.
    The 'site' parameter is required and cannot be an empty string.
    Returns a JSON string of filtered rack unit information.
    """

    resource_path = "compute/RackUnits"

    url = BURL + resource_path

    response = await make_intersight_request(url)

    def site_tag_matches(tags: list, query_site: str):
        # if not tags or not site_query:
        #     return True  # No filter applied
        for tag in tags:
            if tag.get("Key") == "SITE" and query_site.lower() in tag.get("Value", "").lower():
                return True
        return False

    filtered = []
    
    if "Results" in response and isinstance(response["Results"], list):
        for item in response["Results"]:
            if site_tag_matches(item.get("Tags"), site):
                filtered.append({
                    "AccountMoid": item.get("AccountMoid"),
                    "KvmIpAddresses": item.get("KvmIpAddresses"),
                    "Management IP Address": item.get("MgmtIpAddress"),
                    "Server Name": item.get("Name"),
                    "NumCpuCores": item.get("NumCpuCores"),
                    "NumCpus": item.get("NumCpus"),
                    "Model": item.get("Model"),
                    "Alarm Summary": item.get("AlarmSummary"),
                    "AdminPowerState": item.get("AdminPowerState"),
                    "Serial": item.get("Serial"),
                    "Tags": item.get("Tags"),
                    "Moid": item.get("Moid"),
                    "PCIE Information": item.get("PciDevices"),
                    "Alert": item.get("Alerts")
                })
    else:
        if site_tag_matches(response.get("Tags"), site):
            filtered.append({
                "AccountMoid": response.get("AccountMoid"),
                "KvmIpAddresses": response.get("KvmIpAddresses"),
                "Management IP Address": response.get("MgmtIpAddress"),
                "Server Name": response.get("Name"),
                "NumCpuCores": response.get("NumCpuCores"),
                "NumCpus": response.get("NumCpus"),
                "Model": response.get("Model"),
                "Alarm Summary": response.get("AlarmSummary"),
                "AdminPowerState": response.get("AdminPowerState"),
                "Serial": response.get("Serial"),
                "Tags": response.get("Tags"),
                "Moid": response.get("Moid"),
                "PCIE Information": response.get("PciDevices"),
                "Alert": response.get("Alerts")
            })
            print('conditioni 2')

    return json.dumps(filtered)

if __name__ == "__main__":
    result = asyncio.run(get_compute_rackunits("LON"))
    # filtered = result.get("Tags")
    print(result)