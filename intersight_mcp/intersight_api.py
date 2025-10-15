import sys
import os
from mcp.server.fastmcp import FastMCP
import requests
from datetime import datetime

sys.path.append(os.path.abspath("intersight-rest-api"))
from intersight_auth import IntersightAuth
import json
from typing import Any
import asyncio
from dotenv import load_dotenv
import logging

load_dotenv()

mcp = FastMCP("Intersight Agent", host="0.0.0.0")

# Create an AUTH object
AUTH = IntersightAuth(
    secret_key_filename='intersight-rest-api/key/SecretKey.txt',
    api_key_id=os.getenv("api_key_id")
)

BURL = "https://intersight.com/api/v1/"

@mcp.tool()
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


# @mcp.tool()
# async def get_compute_physicalsummaries():
#     """
#     Use Intersight API to retrieve Cisco Compute physical summaries
#     """

#     resource_path = "compute/PhysicalSummaries" 

#     # Make the GET request
#     url = BURL + resource_path

#     response = await make_intersight_request(url)

#     return response

@mcp.tool()
async def get_ntp_policies(moid="Use Intersight API to retrieve Cisco ntp policies, mention moid to filter specific moid. Empty input "" will return all available ntp policies."):
    """
    Use Intersight API to retrieve Cisco ntp policies, mention moid to filter specific moid. Empty input "" will return all available ntp policies
    """

    moid = "/" + moid if moid != "" else moid

    resource_path = "ntp/Policies" + moid

    url = BURL + resource_path

    response = await make_intersight_request(url)

    return response


@mcp.tool(description="Retrieve detailed Cisco Compute rack unit information from Intersight API using site as input which looks like rtp, sng, lon, etc., covering physical attributes and health status. Empty site input "" will return all available compute rackunit information.")
async def get_compute_rackunits_by_site(site: str):
    """
    Retrieve Cisco Compute rack units for a specific site using the Intersight API. Empty input "" will return all available compute rackunit information

    Args:
        site: The site identifier string used to filter rack units.
        Empty site input "" will return all available compute rackunit information

    Returns:
        A list of dictionaries, each containing details for a rack unit:
           - AccountMoid: Unique account identifier
           - KvmIpAddresses: List of KVM IP addresses
           - Management IP Address: Primary management IP address
           - Server Name: Name of the server
           - NumCpuCores: Number of CPU cores
           - NumCpus: Number of CPUs
           - Model: Server model
           - Alarm Summary: Summary of alarms for the server
           - AdminPowerState: Administrative power state
           - Serial: Serial number
           - Tags: List of tags associated with the server
           - Moid: Unique identifier for the server object
           - PCIE Information: List of PCIe device details
           - Alert: List of active alerts
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
                    # "KvmIpAddresses": item.get("KvmIpAddresses"),
                    "Management IP Address": item.get("MgmtIpAddress"),
                    "Server Name": item.get("Name"),
                    "NumCpuCores": item.get("NumCpuCores"),
                    "NumCpus": item.get("NumCpus"),
                    "Model": item.get("Model"),
                    "Alarm Summary": item.get("AlarmSummary"),
                    # "AdminPowerState": item.get("AdminPowerState"),
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
                # "KvmIpAddresses": response.get("KvmIpAddresses"),
                "Management IP Address": response.get("MgmtIpAddress"),
                "Server Name": response.get("Name"),
                "NumCpuCores": response.get("NumCpuCores"),
                "NumCpus": response.get("NumCpus"),
                "Model": response.get("Model"),
                "Alarm Summary": response.get("AlarmSummary"),
                # "AdminPowerState": response.get("AdminPowerState"),
                "Serial": response.get("Serial"),
                "Tags": response.get("Tags"),
                "Moid": response.get("Moid"),
                "PCIE Information": response.get("PciDevices"),
                "Alert": response.get("Alerts")
            })

    return json.dumps(filtered[:10])
    # return response
    
@mcp.tool(description="Retrieve detailed Cisco Compute rack unit information from Intersight API using server name as argument. An example of server name is sng-ai1-srv2 or rtp-ai2-srv6, covering physical attributes and health status. Empty input "" will return all available compute rackunit infoermation")
async def get_compute_rackunit_by_server_name(server_name: str):
    """
    Retrieve Cisco Compute rack unit details for a specific server name using the Intersight API. Empty input "" will return all available compute rackunit infoermation

    Args:
        server_name: The name of the server to retrieve details for.
        Empty server_name input "" will return all available compute rackunit information

    Returns:
        A JSON string representing a dictionary with details for the matched rack unit,
        or an empty JSON object ({}) if no server with the given name is found.
        The dictionary contains:
           - AccountMoid: Unique account identifier
           - Management IP Address: Primary management IP address
           - Server Name: Name of the server
           - NumCpuCores: Number of CPU cores
           - NumCpus: Number of CPUs
           - Model: Server model
           - Alarm Summary: Summary of alarms for the server
           - Serial: Serial number
           - Tags: List of tags associated with the server
           - Moid: Unique identifier for the server object
           - Alert: List of active alerts
    """

    resource_path = "compute/RackUnits"
    url = BURL + resource_path

    response = await make_intersight_request(url)

    def server_name_matches(tags: str, server_name: str):
        if server_name.lower() in tags.lower():
            return True
        else:
            return False

    filtered = []

    if "Results" in response and isinstance(response["Results"], list):
        for item in response["Results"]:
            if server_name_matches(item.get("Name"),server_name):
                filtered.append({
                    "AccountMoid": item.get("AccountMoid"),
                    # "KvmIpAddresses": item.get("KvmIpAddresses"),
                    "Management IP Address": item.get("MgmtIpAddress"),
                    "Server Name": item.get("Name"),
                    "NumCpuCores": item.get("NumCpuCores"),
                    "NumCpus": item.get("NumCpus"),
                    "Model": item.get("Model"),
                    "Alarm Summary": item.get("AlarmSummary"),
                    # "AdminPowerState": item.get("AdminPowerState"),
                    "Serial": item.get("Serial"),
                    "Tags": item.get("Tags"),
                    "Moid": item.get("Moid"),
                    "PCIE Information": item.get("PciDevices"),
                    "Alert": item.get("Alerts")
                })
    elif server_name_matches(item.get("Name"),server_name): # Handle case where response might be a single object directly
        filtered.append({
            "AccountMoid": item.get("AccountMoid"),
            # "KvmIpAddresses": item.get("KvmIpAddresses"),
            "Management IP Address": item.get("MgmtIpAddress"),
            "Server Name": item.get("Name"),
            "NumCpuCores": item.get("NumCpuCores"),
            "NumCpus": item.get("NumCpus"),
            "Model": item.get("Model"),
            "Alarm Summary": item.get("AlarmSummary"),
            # "AdminPowerState": item.get("AdminPowerState"),
            "Serial": item.get("Serial"),
            "Tags": item.get("Tags"),
            "Moid": item.get("Moid"),
            "PCIE Information": item.get("PciDevices"),
            "Alert": item.get("Alerts")
        })

    return json.dumps(filtered[:10])

@mcp.tool(description="Retrieve PCI device information for a specified compute rack unit from Intersight API using moid which is alphanumeric string as argument. An example of moid is 6745b8bd61767533017a5f2b. Empty input "" will return all available pci devices")
async def get_pci_devices(moid: str = ""):
    """Retrieve PCI device information for a specified compute rack unit using the Intersight API. Empty input "" will return all available pci devices

    Args:
        moid: The unique identifier (Moid) of the compute rack unit. If not provided, defaults to an empty string.
        Empty moid input "" will return all available pci devices

    Returns:
        A list of dictionaries, each containing PCI device details for the specified rack unit:
    """

    moid = "/" + moid if moid != "" else moid

    resource_path = "pci/Devices" + moid

    url = BURL + resource_path

    response = await make_intersight_request(url)

    filtered = []

    if "Results" in response and isinstance(response["Results"], list):
        # When response contains "Results" list
        for item in response["Results"][:10]:
            compute_rack_unit = item.get("ComputeRackUnit")
            if compute_rack_unit and "link" in compute_rack_unit:
                link = compute_rack_unit["link"]
                server_info = await make_intersight_request(link)
                server_name = server_info.get("Name")

            filtered.append({
                "AccountMoid": item.get("AccountMoid"),
                "PCIE Moid": item.get("Moid"),
                "PCIE Model": item.get("Model"),
                # "Compute Rack Unit Link": link
                "Server Name": server_name
            })
    else:
        # When response does not have "Results", treat the whole response as a single item
        compute_rack_unit = response.get("ComputeRackUnit")
        if compute_rack_unit and "link" in compute_rack_unit:
            link = compute_rack_unit["link"]
            server_info = await make_intersight_request(link)
            server_name = server_info.get("Name")

        filtered.append({
            "AccountMoid": response.get("AccountMoid"),
            "PCIE Moid": response.get("Moid"),
            "PCIE Model": response.get("Model"),
            "Compute Rack Unit": server_name
        })

    return json.dumps(filtered[:10])


if __name__ == "__main__":
    # Initialize and run the server
    # asyncio.run(
    #     mcp.run(transport='stdio')
    # )
    asyncio.run(
        mcp.run(transport='streamable-http')
    )
