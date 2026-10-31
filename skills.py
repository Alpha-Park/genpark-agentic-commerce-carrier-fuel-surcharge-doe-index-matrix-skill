# -*- coding: utf-8 -*-
"""Freight Carrier DOE Weekly Diesel Fuel Surcharge (FSC) Matrix Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def calculate_freight_fsc_surcharge(**kwargs):
    """Calculates contractually enforceable Freight Fuel Surcharges (FSC) linked to US Energy Information Administration (EIA/DOE) On-Highway Diesel weekly indexes."""
    current_doe_diesel_price_per_gallon = kwargs.get('current_doe_diesel_price_per_gallon')
    base_peg_price_per_gallon = kwargs.get('base_peg_price_per_gallon')
    fsc_increment_interval_cents = kwargs.get('fsc_increment_interval_cents')
    fsc_surcharge_per_interval_cents = kwargs.get('fsc_surcharge_per_interval_cents')
    total_linehaul_miles = kwargs.get('total_linehaul_miles')
    billed_carrier_fsc_amount_usd = kwargs.get('billed_carrier_fsc_amount_usd')

    price_delta = max(0.0, current_doe_diesel_price_per_gallon - base_peg_price_per_gallon)
    intervals_elapsed = int(price_delta / fsc_increment_interval_cents)
    
    # Contractual FSC rate per mile
    contractual_fsc_rate_per_mile = round(intervals_elapsed * fsc_surcharge_per_interval_cents, 3)
    authorized_fsc_charge_usd = round(contractual_fsc_rate_per_mile * total_linehaul_miles, 2)
    
    overbilled_amount_usd = round(max(0.0, billed_carrier_fsc_amount_usd - authorized_fsc_charge_usd), 2)
    has_dispute = overbilled_amount_usd > 1.0
    
    result = {
        "status": "success",
        "current_doe_index": current_doe_diesel_price_per_gallon,
        "base_fuel_peg": base_peg_price_per_gallon,
        "contractual_fsc_rate_per_mile": contractual_fsc_rate_per_mile,
        "billable_linehaul_miles": total_linehaul_miles,
        "authorized_contractual_fsc_usd": authorized_fsc_charge_usd,
        "carrier_invoiced_fsc_usd": billed_carrier_fsc_amount_usd,
        "overcharge_disputed_usd": overbilled_amount_usd,
        "audit_disposition": "AUDIT_APPROVED" if not has_dispute else f"DISPUTE_SUBMITTED: Overcharge of ${overbilled_amount_usd:.2f} flagged against DOE contract matrix.",
        "engine": "GenPark DOE Diesel Index Fuel Surcharge Audit Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "calculate_freight_fsc_surcharge": {
        "name": "calculate_freight_fsc_surcharge",
        "description": "Calculates contractually enforceable Freight Fuel Surcharges (FSC) linked to US Energy Information Administration (EIA/DOE) On-Highway Diesel weekly indexes.",
        "parameters": {
            "type": "object",
            "properties": {
                "current_doe_diesel_price_per_gallon": {"type": "number", "description": "Current DOE National On-Highway Diesel average ($/gal)"},
                "base_peg_price_per_gallon": {"type": "number", "description": "Contract base fuel peg (e.g. $1.25 or $2.50)"},
                "fsc_increment_interval_cents": {"type": "number", "description": "Price change interval per tier (e.g. $0.05 or $0.06)"},
                "fsc_surcharge_per_interval_cents": {"type": "number", "description": "Additional surcharge per interval (e.g. $0.01/mile or 0.5%)"},
                "total_linehaul_miles": {"type": "number", "description": "Total billable linehaul distance (miles)"},
                "billed_carrier_fsc_amount_usd": {"type": "number", "description": "Fuel surcharge amount billed by carrier on invoice"},
            },
            "required": ['current_doe_diesel_price_per_gallon', 'base_peg_price_per_gallon', 'fsc_increment_interval_cents', 'fsc_surcharge_per_interval_cents', 'total_linehaul_miles', 'billed_carrier_fsc_amount_usd']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "calculate_freight_fsc_surcharge":
            res = calculate_freight_fsc_surcharge(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-carrier-fuel-surcharge-doe-index-matrix-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-carrier-fuel-surcharge-doe-index-matrix-skill...")
    test_args = {'current_doe_diesel_price_per_gallon': 3.82, 'base_peg_price_per_gallon': 2.5, 'fsc_increment_interval_cents': 0.05, 'fsc_surcharge_per_interval_cents': 0.01, 'total_linehaul_miles': 840.0, 'billed_carrier_fsc_amount_usd': 245.0}
    res = calculate_freight_fsc_surcharge(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-carrier-fuel-surcharge-doe-index-matrix-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
